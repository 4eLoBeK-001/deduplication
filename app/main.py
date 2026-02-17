import asyncio
import os
import uuid

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from pprint import pprint
from fastapi import BackgroundTasks, FastAPI, Request

from app.core.client import AmoCRMClient
from app.core.redis_config import check_redis_connection
from app.services.helpers import find_duplicate
from app.services.utils import clean_phone, extract_phone_final
from app.core.logger import logger
from app.core.redis_config import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    connected = await check_redis_connection()
    if not connected:
        print('Редис не доступен')
    yield


load_dotenv()

SUBDOMAIN = os.getenv('AMOCRM_SUBDOMAIN')


app = FastAPI(title='amoCRM', lifespan=lifespan)


@app.get('/')
async def test(request: Request):
    return {'status': 'ok'}


async def process_contact_merge(original_phone: str, data: dict):
    redis_lock = f'lock:contact:{original_phone}'

    is_locked = await redis_client.set(redis_lock, 'processing', ex=60, nx=True)

    if not is_locked: 
        logger.warning(f'Игнор номера {original_phone}, т.к. он уже обрабатывается')
        return
    
    try:
        logger.info('Webhook data parsed')
        
        async with AmoCRMClient(SUBDOMAIN) as amo:
            found_contacts = await amo.find_contacts_by_phone(original_phone)
            logger.info(f'Contacts found: {len(found_contacts)}')


            if len(found_contacts) > 1:
                logger.info('Duplicate detected')
                original, duplicate = await find_duplicate(found_contacts)
                logger.info(
                    f'Original ID={original.get('id')} | Duplicate ID={duplicate.get('id')}'
                )

                # После того как поняли что есть оригинал, ждём 2 секунды
                await asyncio.sleep(2)

                full_duplicate = await amo.find_contact_by_id(duplicate['id'])
                # Если у контакта есть сделки
                leads = full_duplicate[0].get('_embedded').get('leads') or []
                if leads:
                    for lead in leads:
                        await amo.link_lead_to_contact(lead['id'], original.get('id'))

                logger.info('Starting merge process')
                # Обновляем поля у оригинала
                await amo.update_original_contact(original['id'], duplicate['id'])

                # Переносим примечания
                notes = await amo.get_contact_notes(duplicate.get('id'))
                await amo.transfer_notes(notes, original.get('id'))

                logger.info('Merge completed')
            else:
                logger.info(f'No duolicated for {original_phone}')

        logger.info('Webhook processing finished')

    except Exception as e:
        params = f'Phone: {original_phone}, leads: {leads}'
        logger.exception(f'Ошибка при обработке вебхука. Параметры: {params}. Ошибка: {e}')
    finally:
        await redis_client.delete(redis_lock)
        logger.info(f'Замок для {original_phone} удалён')




@app.post('/webhook')
async def test_request(request: Request, background_task: BackgroundTasks):
    request_id = str(uuid.uuid4())[:8]
    
    with logger.contextualize(request_id=request_id):
        logger.info('Webhook received')
        form_data = await request.form()
        data = dict(form_data)

        original_phone = await extract_phone_final(data)

        if not original_phone:
            logger.warning('Phone not found in webhook')
            return {'text': 'phone nt found'}
        
        logger.info(f'Phone extracted: {original_phone}')

        background_task.add(process_contact_merge, original_phone, data)

        return {'status': 'ok'}
    