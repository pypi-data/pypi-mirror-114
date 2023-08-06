from rlogging.service.celery import app

from rlogging.printers import PrintersPool



@app.task
def send_record(loggerName: str, recordString: str):
    """ Обработка объекта лога в воркере celery

    Args:
        loggerName (str): Имя логгера
        recordString (str): Строковое представление объекта лога

    """

    printerPool = PrintersPool.load(printersPoolString)

    record = Record.load(stringRecord)

    logger = rlogging.get_logger(record.loggerName)

    if not logger._started:
        logging_setup()

    logger.send_record(record)