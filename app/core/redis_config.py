import redis.asyncio as redis
import os
from app.core.logger import logger
from dotenv import load_dotenv

load_dotenv()


REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')


redis_client = redis.from_url(
    f'redis://{REDIS_HOST}:{REDIS_PORT}/0', 
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


async def set_cache(key: str, value: str, expire: int = 86400): # 24 часа
    try:
        await redis_client.set(key, value, ex=expire)
    except Exception as e:
        logger.error(f'Ошибка при записи в кэш: {e}')



async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        logger.error(f'Ошибка при получении кэша: {e}')
        return None
