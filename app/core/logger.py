from loguru import logger
import sys


logger.remove()


logger.add(sys.stdout, format="{time:HH:mm:ss} | {level} | {message}", level="INFO")

logger.add(
    "logs/short_errors.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | Ошибка в {function}:{line} | Сообщение: {message}",
    level="ERROR",
    filter=lambda record: record["level"].name == "ERROR", # Только ошибки
    rotation="10 MB",
    compression="zip"
)

logger.add(
    "logs/full_tracebacks.log",
    level="ERROR",
    backtrace=True,  # Показывает путь ошибки
    diagnose=True,   # Показывает значения переменных в момент падения
    rotation="10 MB",
    compression="zip"
)
