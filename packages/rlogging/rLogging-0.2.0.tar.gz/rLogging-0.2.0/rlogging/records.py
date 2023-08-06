""" Модуль описания Логов.

"""

from __future__ import annotations

import inspect
import json
import os
import threading
import time
import typing as _T


class BaseRecord(object):
    """ Базовый объект лога """

    collect_context_info: bool = True

    __slots__ = (
        'loggerName', 'loggingLevel', 'message',
        'loggingLevelLabel', 'loggingLevelLabelCenter',
        'time', 'timestamp', 'pidId', 'threadId',
        'fromModule', 'fromFile', 'fromFileLine', 'fromObject',
        'kwargs'
    )

    loggerName: str
    loggingLevel: int
    message: str

    loggingLevelLabel: str
    loggingLevelLabelCenter: str

    time: str
    timestamp: float
    pidId: int
    threadId: int

    fromModule: str
    fromFile: str
    fromFileLine: str
    fromObject: str
    kwargs: dict[str, _T.Any]

    def __init__(self):
        """ Получение данных о состянии приложения на момент вызова лога """
        pass

    @classmethod
    def create_log(cls, loggerName: str, loggingLevel: int, message: str, **kwargs):
        """ Получение данных о состянии приложения на момент вызова лога """

        record = cls()
        record.set_params(loggerName, loggingLevel, message, kwargs)
        return record

    def set_params(self, loggerName: str, loggingLevel: int, message: str, kwargs):
        self.loggerName = loggerName
        self.loggingLevel = loggingLevel
        self.message = message

        self.__get_main_info()

        if self.collect_context_info:
            self.__get_info_call_function()

        self.kwargs = kwargs

    def __get_main_info(self):
        self.timestamp = time.time()
        self.pidId = os.getpid()
        self.threadId = threading.get_ident()

    def __get_info_call_function(self):
        """ Получение информации о функции вызвавшей лог """

        stack = inspect.stack()[4]
        module = inspect.getmodule(stack.frame)

        self.fromModule = module.__name__
        self.fromFile = stack.filename
        self.fromFileLine = stack.lineno

        self.fromObject = stack.function

        # Если у функции есть атрибут self / cls значит она метод класса.
        if 'self' in stack.frame.f_locals:
            self.fromObject = '{0}.{1}'.format(
                stack.frame.f_locals.get('self').__class__.__name__,
                stack.function
            )

        elif 'cls' in stack.frame.f_locals:
            self.fromObject = '{0}.{1}'.format(
                stack.frame.f_locals.get('cls').__name__,
                stack.function
            )


class DumpRecord(BaseRecord):
    """ Настройка над базовым классом BaseRecord,
    которое позволяет представлять лог в виде строки с сихранением всех полей

    """

    def dump(self) -> str:
        dumpData = {}

        dumpData['collect_context_info'] = self.collect_context_info

        for field in self.__slots__:
            dumpData[field] = getattr(self, field, None)

        return json.dumps(dumpData)

    @classmethod
    def load(cls, dumpedStrign: str):
        record = cls()
        dumpData = json.loads(dumpedStrign)

        for field, value in dumpData.items():
            setattr(record, field, value)

        return record


class Record(DumpRecord):
    """ Объект лога """


class StopSystemRecord(Record):
    """ Объект, сигнализирующий о необходимости остановить систему логирования """

    collect_context_info = False

    def __init__(self):
        super().__init__()
        self.set_params('system', 100, 'stop system record', {})
