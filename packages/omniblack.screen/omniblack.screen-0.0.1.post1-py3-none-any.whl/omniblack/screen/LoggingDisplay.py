from __future__ import annotations
from logging import Handler, LogRecord
from urwid import Text
from typing import TYPE_CHECKING
from .translate_text import translate_text_for_urwid

if TYPE_CHECKING:
    from .ui import ProcessDisplay


class DisplayHandler(Handler):
    def __init__(self, message_cls: Text, display: ProcessDisplay):
        super().__init__()
        self.display = display
        self.message_cls = message_cls

    def emit(self, record: LogRecord):
        try:
            msg = self.format(record)
            line = self.message_cls(translate_text_for_urwid(msg))
            self.display.add_line(line)
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)
