import redis.asyncio as redis
import os
from app.core.logger import logger
from dotenv import load_dotenv

load_dotenv()


REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


redis_client = redis.from_url(
    f'redis://{REDIS_HOST}:{REDIS_PORT}', 
    decode_responses=True
)

async def check_redis_connection():
    try:
        await redis_client.ping()
        logger.info('Редис подключён')
        return True
    except Exception as e:
        logger.error(f'Ошибка подключения к редису: {e}')
        return False
