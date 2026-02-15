from loguru import logger
import sys


logger.remove()

fmt = '{time:HH:mm:ss} | {level} | {extra[request_id]} | {message}\n'
default_fmt = '{time:HH:mm:ss} | {level} | {message}\n'

logger.add(
    sys.stdout, 
    format=lambda record: fmt if 'request_id' in record['extra'] else default_fmt, 
    level='INFO'
)

logger.add(
    'logs/main.log',
    level='INFO', 
    format=lambda record: fmt if 'request_id' in record['extra'] else default_fmt, 
    rotation='50 MB', 
    compression='zip'
)

logger.add(
    'logs/full_tracebacks.log',
    level='ERROR',
    backtrace=True,  # Показывает путь ошибки
    diagnose=True,   # Показывает значения переменных в момент падения
    rotation='10 MB',
    compression='zip'
)
