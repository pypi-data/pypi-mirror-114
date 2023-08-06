import os
import typing as _T

from rlogging.handlers import BaseHandler
from rlogging.records import Record, StopSystemRecord


class CeleryHandler(BaseHandler):
    """ Хендлер работающий на основе celery.

    Приходящие сообщения от передает в очередь celery,
    воркер которой потом все сохраняет

    """

    def send(self, record: Record):
        if record.pidId == os.getpid():
            self.loggingSetupCallback.delay(
                record.dump()
            )

        elif not isinstance(record, StopSystemRecord):
            self.printersPool.print(record)
