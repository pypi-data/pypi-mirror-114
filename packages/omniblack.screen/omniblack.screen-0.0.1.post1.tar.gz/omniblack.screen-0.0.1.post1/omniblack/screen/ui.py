import asyncio
from asyncio import events, tasks
from typing import NoReturn, Any, NamedTuple
from sys import exit
from os import EX_OK, environ
from logging import getLogger, DEBUG, basicConfig
from pathlib import Path
from signal import SIGINT

import urwid
from urwid import (
    connect_signal,
    BLACK,
    DARK_GRAY,
    DARK_BLUE,
    LIGHT_RED,
    LIGHT_GREEN,
    ListWalker,
    SimpleListWalker,
    LineBox,
    ListBox
)
from urwid.signals import disconnect_signal_by_key
from anyio import create_task_group

from .MonitoredDeque import MonitoredDeque
from .IdDict import IdDict
from .Process import ProcessStates, ProcessDisplay, Signals

log = getLogger(__name__)

root_logger = getLogger()

log_file = Path(environ['SRC'])/'ui_output'
try:
    log_file.unlink()
except FileNotFoundError:
    pass

basicConfig(level=DEBUG, filename=log_file)


class SimpleLinesWalker(MonitoredDeque, ListWalker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus = self.last_index
        self.anchored = True

    @property
    def last_index(self):
        return max(len(self) - 1, 0)

    def _get_contents(self):
        """
        Return self.
        Provides compatibility with old SimpleListWalker class.
        """
        return self

    contents = property(_get_contents)

    def _modified(self):
        if self.focus >= len(self):
            self.focus = self.last_index

        if self.anchored:
            self.focus = self.last_index
        super()._modified()

    def set_modified_callback(self, callback):
        """
        This function inherited from MonitoredList is not
        implemented in SimpleListWalker.
        Use connect_signal(list_walker, "modified", ...) instead.
        """
        raise NotImplementedError('Use connect_signal('
                                  'list_walker, "modified", ...) instead.')

    def set_focus(self, position):
        """Set focus position."""
        try:
            if position < 0 or position >= len(self):
                raise ValueError
        except (TypeError, ValueError):
            raise IndexError(f'No widget at position {position}')

        if position == self.last_index:
            self.anchored = True
        else:
            self.anchored = False

        self.focus = position
        self._modified()

    def next_position(self, position):
        """
        Return position after start_from.
        """
        if len(self) - 1 <= position:
            raise IndexError
        return position + 1

    def prev_position(self, position):
        """
        Return position before start_from.
        """
        if position <= 0:
            raise IndexError
        return position - 1

    def positions(self, reverse=False):
        """
        Optional method for returning an iterable of positions.
        """
        if reverse:
            return reversed(range(len(self)))
        return range(len(self))


def create_palette():
    for state in ProcessStates:
        # normal color
        yield (state.value.name, state.value.color, BLACK)
        # Progress bar completion
        yield (state.value.complete_color, state.value.color, DARK_GRAY)
        # Normal selected
        yield (state.value.bold_color, f'{state.value.color},bold', BLACK)
        # Progress bar completion selected
        yield (
            state.value.bold_complete_color,
            f'{state.value.color},bold',
            DARK_GRAY
        )


other_palette = (
    ('info-line', DARK_BLUE, BLACK),
    ('error-line', LIGHT_RED, BLACK),
    ('success-line', LIGHT_GREEN, BLACK),
)

palette = tuple(create_palette()) + other_palette


class Subscription(NamedTuple):
    line: str
    select: str


class Screen:
    def __init__(self):
        self.selected_display = None
        self.current_lines = SimpleLinesWalker(maxlen=10_000)
        self.text_list = urwid.ListBox(self.current_lines)
        self.process_list = SimpleListWalker([])
        self.process_display = ListBox(self.process_list)
        self.__subs = IdDict()

        self.columns = urwid.Columns((
            ('weight', 1, LineBox(self.process_display, title='Processes')),
            ('weight', 4, LineBox(self.text_list, title='Output')),
        ))

    def select(self, new_selected):
        if self.selected_display is not None:
            self.selected_display.selected = False
        self.selected_display = new_selected
        self.selected_display.selected = True
        self.current_lines.clear()
        self.current_lines.extend(self.selected_display.lines)

    def new_line(self, display, line):
        if display is self.selected_display:
            self.current_lines.append(line)

    async def shutdown(self):
        async with create_task_group() as tg:
            for process_display in self.process_list:
                tg.start_soon(
                    process_display.process.stop,
                    name=f'Stopping task: {process_display.name}',
                )

    exit_keys = {'q', 'Q'}

    def check_exit(self, key):
        if key in self.exit_keys:
            exit(EX_OK)

        elif key == 'r':
            asyncio.create_task(
                self.selected_display.process.restart(),
                name=f'Restarting task: {self.selected_display.name}',
            )
        elif key == 's':
            asyncio.create_task(
                self.selected_display.process.stop(),
                name=f'Stopping task: {self.selected_display.name}',
            )

    def attach(self, display: ProcessDisplay):
        if not self.process_list:
            self.select(display)
        self.process_list.append(display)
        line_sub = connect_signal(display, Signals.line.value, self.new_line)
        select_sub = connect_signal(display, Signals.select.value, self.select)
        self.__subs[display] = Subscription(line_sub, select_sub)

    def detach(self, display: ProcessDisplay):
        sub = self.__subs[display]
        disconnect_signal_by_key(display, Signals.line.value, sub.line)
        disconnect_signal_by_key(display, Signals.select.value, sub.select)
        self.process_list.remove(display)
        del self.__subs[display]

    def run(self, main: callable, *args: Any, **kwargs: Any) -> NoReturn:
        loop = events.new_event_loop()
        loop.set_debug(True)

        async_loop = urwid.AsyncioEventLoop(loop=loop)
        urwid_loop = urwid.MainLoop(
            self.columns,
            palette=palette,
            event_loop=async_loop,
            unhandled_input=self.check_exit,
        )

        try:
            log.info('Starting event loop')
            events.set_event_loop(loop)
            urwid_loop.start()
            loop.add_signal_handler(SIGINT, exit, EX_OK)
            loop.run_until_complete(
                main(*args, **kwargs)
            )
            loop.run_forever()
        finally:
            loop.run_until_complete(self.shutdown())
            try:
                _cancel_all_tasks(loop)
                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.run_until_complete(loop.shutdown_default_executor())
            finally:
                urwid_loop.stop()
                events.set_event_loop(None)
                loop.close()


def _cancel_all_tasks(loop):
    to_cancel = tasks.all_tasks(loop)
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(tasks.gather(*to_cancel, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler({
                'message': 'unhandled exception during asyncio.run() shutdown',
                'exception': task.exception(),
                'task': task,
            })
