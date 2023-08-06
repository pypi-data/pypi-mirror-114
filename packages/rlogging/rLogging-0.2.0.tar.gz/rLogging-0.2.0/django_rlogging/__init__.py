""" Интеграция rlogging в django

Настройки settings.py

RLOGGING_SETUP - Каллбек функция пользовательской настройки логгеров, которая будет вызвана при инициализации компонента.

"""

import django

# alpha release
__version__ = '0.2.0'

if django.VERSION < (3, 2):
    default_app_config = 'django_rlogging.RLoggingAppConfig'