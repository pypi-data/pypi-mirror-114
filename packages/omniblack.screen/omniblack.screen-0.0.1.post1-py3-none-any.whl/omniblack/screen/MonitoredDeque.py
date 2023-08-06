from collections import deque
from functools import wraps


class Monitor:
    def __init_subclass__(cls, **kwargs):
        if hasattr(cls, 'mutating_methods'):
            mutating_methods = cls.mutating_methods
            del cls.mutating_methods
            for method_name in mutating_methods:
                func = getattr(cls, method_name)
                call_modified_wrapper = cls.__create_monitor_method(func)

                setattr(cls, method_name, call_modified_wrapper)

        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        self.__callbacks = []
        super().__init__(*args, **kwargs)

    def watch(self, callback):
        self.__callbacks.append(callback)

    def _modified(self):
        for cb in self.__callbacks:
            cb(self)
        super()._modified()

    @classmethod
    def __create_monitor_method(cls, func):
        @wraps(func)
        def call_modified_wrapper(self, *args, **kwargs):
            return_val = func(self, *args, **kwargs)
            self._modified()
            return return_val

        return call_modified_wrapper


class MonitoredDeque(Monitor, deque):
    mutating_methods = (
        '__delitem__',
        '__iadd__',
        '__imul__',
        '__setitem__',
        'append',
        'appendleft',
        'extend',
        'extendleft',
        'insert',
        'pop',
        'popleft',
        'remove',
        'reverse',
        'rotate',
    )

