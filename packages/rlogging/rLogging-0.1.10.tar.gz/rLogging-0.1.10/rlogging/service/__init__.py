""" Модуль реализации демона.

Демон запускается и выключается через консоль.
К демону обращается хендлер DaemonProcessHandler, после чего он передает лог в принтеры.


Для использования функционала демона, нужна библиотека `zmq`.


"""

from rlogging.service import handlers

from rlogging.service.celery import app as celery_app

__all__ = ('celery_app',)