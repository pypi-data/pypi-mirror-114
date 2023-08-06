from __future__ import annotations
import asyncio
from asyncio import subprocess
from collections import deque
from typing import NamedTuple, Protocol, TYPE_CHECKING
from enum import Enum
from os import pipe, close, EX_OK, environ
from signal import strsignal
from json import loads
from logging import getLogger
from urwid import (
    MetaSignals,
    emit_signal,
    Text,
    ProgressBar,
    LineBox,
    DEFAULT,
    LIGHT_BLUE,
    LIGHT_GREEN,
    LIGHT_RED,
    YELLOW,
)

from .translate_text import translate_text_for_urwid

if TYPE_CHECKING:
    from .ui import Screen

RECORD_SEPERATOR = '\u001E'
RECORD_SEPERATOR_BYTES = RECORD_SEPERATOR.encode('utf-8')


log = getLogger(__name__)


class StdoutLine(Text):
    pass


class StderrLine(Text):
    pass


class InfoLine(Text):
    def __init__(self, text):
        super().__init__(('info-line', text))


class ErrorLine(Text):
    def __init__(self, text):
        super().__init__(('error-line', text))


class SuccessLine(Text):
    def __init__(self, text):
        super().__init__(('success-line', text))


async def read_seperator(reader):
    while not reader.at_eof():
        try:
            record = await reader.readuntil(RECORD_SEPERATOR_BYTES)
            command_str = record.decode('utf-8').strip(RECORD_SEPERATOR)
            yield loads(command_str)
        except asyncio.IncompleteReadError:
            return


class ProcessState(NamedTuple):
    name: str
    icon: str
    color: str

    @property
    def complete_color(self):
        return f'complete-{self.name}'

    @property
    def bold_color(self):
        return f'bold-{self.name}'

    @property
    def bold_complete_color(self):
        return f'bold-complete-{self.name}'


class ProcessStates(Enum):
    stopped = ProcessState('stopped', '\u26d2', DEFAULT)  # ⛒
    running = ProcessState('running', '\u2699', LIGHT_BLUE)  # ⚙
    success = ProcessState('success', '\uf058', LIGHT_GREEN)  # 
    error = ProcessState('error', '\u26d4', LIGHT_RED)  # ⛔
    waring = ProcessState('waring', '\u26a0', YELLOW)  # ⚠


class ProcessProgress(ProgressBar):
    def __init__(self, display):
        self.__display = display
        super().__init__(
            display.state.name,
            display.state.value.complete_color,
            current=0,
        )

    def get_text(self):
        return self.__display.text


class Execution(Protocol):
    name: str

    async def restart(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    async def start(self) -> None:
        pass


class Signals(Enum):
    line = 'line'
    select = 'select'


class ProcessDisplay(LineBox, metaclass=MetaSignals):
    process: Execution
    lines: deque
    progress_bar: ProcessProgress
    name: str
    signals = ['select', 'line']

    def __init__(self, name, selected, process, state=ProcessStates.stopped):
        self.__state = state
        self.__progress = 0
        self.__selected = selected
        self.progress_bar = ProcessProgress(self)
        self.name = name
        self.process = process
        self.lines = deque(maxlen=10_000)
        self.update_text()
        super().__init__(self.progress_bar)

    def update_text(self):
        state_char = self.state.value.name[0]
        new_text = f'({state_char}) {self.name}'
        self.text = new_text
        self.update_color()
        self.progress_bar._invalidate()
        self._invalidate()

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, new_progress):
        self.__progress = new_progress
        self.progress_bar.set_completion(new_progress)
        self.update_text()

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, new_state):
        if not isinstance(new_state, ProcessStates):
            new_state = ProcessStates(new_state)

        self.__state = new_state
        self.update_text()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name
        self.update_text()

    def update_color(self):
        if self.selected:
            self.progress_bar.normal = self.state.value.bold_color
            self.progress_bar.complete = self.state.value.bold_complete_color
        else:
            self.progress_bar.normal = self.state.value.name
            self.progress_bar.complete = self.state.value.complete_color

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, new_selected):
        self.__selected = new_selected
        self.update_text()

    def mouse_event(self, *args):
        emit_signal(self, Signals.select.value, self)

    def add_line(self, line: Text):
        if self.selected:
            emit_signal(self, Signals.line.value, self, line)

        self.lines.append(line)


class Process:
    def __init__(self, cmd, *args, name, cwd=None, env=None, **kwargs):
        kwargs = tuple(
            f'--{key.replace("_", "-")}={value}'
            for key, value in kwargs.items()
            if not isinstance(value, bool)
        ) + tuple(
            f'--{key.replace("_", "-")}'
            for key, value in kwargs.items()
            if isinstance(value, bool)
            if value
        )

        if env is None:
            env = {}

        self.cmd = cmd
        self.cwd = cwd
        self.env = env
        self.args = tuple(args) + kwargs
        self.process_exec = None
        self.display = ProcessDisplay(
            name,
            selected=False,
            process=self,
        )

        super().__init__()

    @property
    def selected(self):
        return self.display.selected

    @selected.setter
    def selected(self, new_selected):
        self.display.selected = new_selected

    @property
    def name(self):
        return self.display.name

    @property
    def state(self):
        return self.display.state

    @state.setter
    def state(self,  new_state):
        if not isinstance(new_state, ProcessStates):
            new_state = getattr(ProcessStates, new_state)

        self.display.state = new_state

    @property
    def progress(self):
        return self.display.progress

    @progress.setter
    def progress(self, new_progress):
        self.display.progress = new_progress

    async def start(self, restarting=False):
        loop = asyncio.get_running_loop()
        read_fd, write_fd = pipe()

        self.read_file = open(read_fd)
        ipc_reader = asyncio.StreamReader()
        reader_protocol = asyncio.StreamReaderProtocol(ipc_reader)
        await loop.connect_read_pipe(
            lambda: reader_protocol,
            self.read_file,
        )

        self.process_exec = await asyncio.create_subprocess_exec(
            self.cmd,
            *self.args,
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            pass_fds=(write_fd,),
            env=environ | {'IPC_FD': str(write_fd)} | self.env,
        )

        self.state = ProcessStates.running
        if restarting:
            line = InfoLine('Process restarted')
        else:
            line = InfoLine('Process started')

        self.display.add_line(line)

        self.ipc_task = asyncio.create_task(
            self.process_ipc_commands(ipc_reader),
            name=f'IPC Task: {self.name}',
        )

        stdout = self.process_exec.stdout
        stderr = self.process_exec.stderr

        self.stdout_task = asyncio.create_task(
            self.process_lines(stdout, StdoutLine),
            name=f'Stdout Task: {self.name}',
        )

        self.stderr_task = asyncio.create_task(
            self.process_lines(stderr, StderrLine),
            name=f'Stderr Task: {self.name}',
        )

        self.exit_task = asyncio.create_task(
            self.handle_exit(),
            name=f'Exit Task: {self.name}',
        )

        close(write_fd)
        write_fd = None

    async def process_ipc_commands(self, reader):
        async for command_record in read_seperator(reader):
            if 'progress' in command_record:
                self.progress = command_record['progress']

            if 'state' in command_record:
                self.state = command_record['state']

    async def process_lines(self, reader, Line):
        async for line in reader:
            line = line.decode('utf-8')
            line = line.rstrip('\n\r')
            line_widget = Line(translate_text_for_urwid(line))
            self.display.add_line(line_widget)

    async def stop(self):
        if self.active:
            self.ipc_task.cancel('Process closing')
            self.stdout_task.cancel('Process closing')
            self.stderr_task.cancel('Process closing')
            self.process_exec.terminate()
            await self.process_exec.wait()
            self.read_file.close()

    async def handle_exit(self):
        return_code = await self.process_exec.wait()
        exit_reason = f'Process exited with code {return_code}.'
        if return_code < 0:
            self.state = ProcessStates.stopped
            signal_name = strsignal(abs(return_code))
            exit_reason = f'Process exited due to {signal_name}.'
            line_widget = InfoLine
        elif return_code != EX_OK:
            self.state = ProcessStates.error
            line_widget = ErrorLine
        else:
            self.state = ProcessStates.success
            line_widget = SuccessLine

        line = line_widget(exit_reason)
        self.display.add_line(line)

    @property
    def active(self):
        if self.process_exec is None:
            return False

        return self.process_exec.returncode is None

    @property
    def lines(self) -> deque:
        return self.display.lines

    async def restart(self):
        await self.stop()
        await self.start(restarting=True)

    def attach(self, screen: Screen):
        log.info('Attaching display to screen')
        screen.attach(self.display)

    def detach(self, screen: Screen):
        screen.detach(self.display)
