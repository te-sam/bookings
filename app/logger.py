from datetime import datetime
import logging  # встроенная библиотека
from pythonjsonlogger import jsonlogger

from app.config import settings

logger = logging.getLogger()

logHandler = logging.StreamHandler()  # устанавливаем hanler - то, куда будет писаться лог

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s')

logHandler.setFormatter(formatter)  # прикрепляем к handler наш formatter
logger.addHandler(logHandler)  # прикрепляем к logger наш handler
logger.setLevel(settings.LOG_LEVEL)  # устанавливаем уровень логирования