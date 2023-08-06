import rlogging

from django.apps.config import AppConfig
from django.conf import settings


class RLoggingAppConfig(AppConfig):
    """ Конфигурация django приложения для подключения к django """

    name = 'django_rlogging'
    verbose_name = 'rlogging for django'

    def ready(self):

        setupCallback = getattr(settings, 'RLOGGING_SETUP', None)

        if setupCallback is not None:
            setupCallback()

        rlogging.start_loggers()
