""" Модуль управления по средством коммандной строки """

from cleo import Application
from cleo import Command as BaseCommand
from rlogging.service import celery

class StartServiceCommand(BaseCommand):
    """ Команда запуска сервиса rlogging

        start
    """

    def __init__(self):
        super().__init__()

    def do_handle(self):
        celery.start_celery()


class StopServiceCommand(BaseCommand):
    """ Команда остановки сервиса rlogging

        stop
    """

    def do_handle(self):
        celery.stop_celery()


def start_cli():
    """ Запуск cli """

    application = Application(name='rlogging service', version=1)
    application.add_commands(StartServiceCommand(), StopServiceCommand())

    application.run()
