from loguru import logger
import sys


logger.remove()


logger.add(
    sys.stdout,
    level='INFO',
    format='{time:HH:mm:ss} | {level} | {message}',
)
