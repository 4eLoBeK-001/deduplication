import asyncio
import os
import uuid

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from pprint import pprint
from fastapi import BackgroundTasks, FastAPI, Request

from app.core.client import AmoCRMClient
from app.core.redis_config import check_redis_connection, get_cache, set_cache
from app.services.helpers import find_duplicate
from app.services.utils import clean_phone, extract_phone_final, extract_tg_nick_final
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


async def process_contact_merge(original_phone: str | None, tg_nick: str | None, data: dict):
    leads = None
    # Данные нового контакта.
    new_contact_id = data.get('contacts[add][0][id]')

    lock_id = original_phone if original_phone else f'tg_{tg_nick}'
    redis_lock = f'lock:contact:{lock_id}'

    cache_key_phone = f'contact:phone:{original_phone}' if original_phone else None
    cache_key_tg = f'contact:tg:{tg_nick}' if tg_nick else None
    
    # Блок 1: Блокировка
    is_locked = await redis_client.set(redis_lock, 'processing', ex=60, nx=True)

    if not is_locked: 
        logger.warning(f'Игнор номера {original_phone}, т.к. он уже обрабатывается')
        return
    
    try:
        original_id = None
        leads = None

        logger.info('Webhook data parsed')
        
        async with AmoCRMClient(SUBDOMAIN) as amo:
            logger.info(f'Cache phone key: {cache_key_phone}')
            logger.info(f'Cache tg key: {cache_key_tg}')

            if cache_key_phone:
                original_id = await get_cache(cache_key_phone)
                logger.info(f'Original from phone cache: {original_id}')

            if not original_id and cache_key_tg:
                original_id = await get_cache(cache_key_tg)
            
            # Блок 2: кэширование 
            # Если айди контакта нет в кэше 
            if not original_id:
                logger.info('block 2')
                found_contacts = []

                # Поиск по номеру телефона если есть
                if original_phone:
                    found_contacts = await amo.find_contacts_by_phone(original_phone)
                    logger.info(f'Contacts by phone found: {len(found_contacts)}')

                # Если не нашлось по телефону то искать по нику
                if not found_contacts and tg_nick:
                    await asyncio.sleep(2)
                    found_contacts = await amo.find_contact_by_tg_nick(tg_nick)

                if not found_contacts:
                    logger.info('Contact not found')
                    return 


                if len(found_contacts) > 1:
                    logger.info('Duplicate detected')
                    original, _ = await find_duplicate(found_contacts)
                    logger.info(
                        f'Original ID={original.get('id')} | Duplicate ID={new_contact_id}'
                    )
                    original_id = original.get('id')
                else:
                    original_id = found_contacts[0].get('id')

                if cache_key_phone:
                    await set_cache(cache_key_phone, str(original_id))
                if cache_key_tg:
                    await set_cache(cache_key_tg, str(original_id))

            # Блок 3: Если новый контакт - не сам оригинал
            if str(new_contact_id) != str(original_id):
                logger.info('block 3')
                original_contact = await amo.find_contact_by_id(str(original_id))

                if not original_contact:
                    logger.warning(f'Original contact {original_id} not found. Clearing cache.')
                    
                    if cache_key_phone:
                        await redis_client.delete(cache_key_phone)
                    if cache_key_tg:
                        await redis_client.delete(cache_key_tg)

                    return
                # После того как поняли что есть оригинал, ждём 2 секунды
                await asyncio.sleep(2)

                full_duplicate = await amo.find_contact_by_id(new_contact_id)

                # Если у контакта есть сделки
                leads = full_duplicate[0].get('_embedded', {}).get('leads', [])
                if leads:
                    for lead in leads:
                        logger.info(lead)
                        await amo.link_lead_to_contact(lead['id'], original_id)

                logger.info('Starting merge process')
                # Обновляем поля у оригинала
                await amo.update_original_contact(original_id, new_contact_id)

                # Переносим примечания
                notes = await amo.get_contact_notes(new_contact_id)
                await amo.transfer_notes(notes, original_id)

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

        original_phone = None
        tg_nick = None

        original_phone = await extract_phone_final(data)

        if not original_phone:
            logger.warning('Phone not found in webhook')
            
            tg_nick = await extract_tg_nick_final(data)
            if not tg_nick:
                logger.warning('tg nick not found in webhook')
                return {'status': '404', 'text': 'tg nick and phone not found'}
        
        logger.info(f'Phone extracted: {original_phone}') if original_phone else None
        
        background_task.add_task(process_contact_merge, original_phone, tg_nick, data)

        return {'status': 'ok'}
    