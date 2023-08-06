""" Настройки Celery

https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html

"""

from celery import Celery

app = Celery('rlogging')
app.conf.update(
    broker_url='redis://localhost:6379/0',
    # broker_url='redis://:password@hostname:port/db_number',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True,
)

def start_celery():
    pass


def stop_celery():
    pass


def register_record_handler():
    pass