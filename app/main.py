import asyncio
import os
import uuid

from dotenv import load_dotenv
from pprint import pprint
from fastapi import FastAPI, Request

from app.services.helpers import (
    find_contacts_by_phone, find_duplicate, get_contact_notes, 
    link_lead_to_contact, transfer_notes, update_original_contact
)
from app.services.utils import clean_phone, extract_phone_final
from app.core.logger import logger

load_dotenv()

SUBDOMAIN = os.getenv('AMOCRM_SUBDOMAIN')


app = FastAPI(title='amoCRM')


@app.get('/')
async def test(request: Request):
    return {'status': 'ok'}


@app.post('/webhook')
async def test_request(request: Request):
    request_id = str(uuid.uuid4())[:8]
    
    with logger.contextualize(request_id=request_id):
        try:
            logger.info('Webhook received')
            form_data = await request.form()
            data = dict(form_data)

            logger.info('Webhook data parsed')
            
            original_phone = await extract_phone_final(data)

            if not original_phone:
                logger.warning('Phone not found in webhook')
                return {'text': 'phone nt found'}
            
            logger.info(f'Phone extracted: {original_phone}')

            original_phone = clean_phone(original_phone)
            found_contacts = await find_contacts_by_phone(original_phone, SUBDOMAIN)

            logger.info(f'Contacts found: {len(found_contacts)}')
            
            # Если у контакта есть сделки
            lead_id = 0
            if found_contacts[-1].get('_embedded').get('leads'):
                lead_id = found_contacts[-1].get('_embedded').get('leads')[0].get('id')

            if len(found_contacts) > 1:
                logger.info('Duplicate detected')
                original, duplicate = await find_duplicate(found_contacts)

                logger.info(
                    f'Original ID={original.get('id')} | Duplicate ID={duplicate.get('id')}'
                )

                # После того как поняли что есть оригинал, ждём 2 секунды
                await asyncio.sleep(2)

                logger.info('Starting merge process')
                # Обновляем поля у оригинала
                await update_original_contact(original, duplicate, SUBDOMAIN)
                logger.info('Merge completed')

                # Привязываем сделки из дубликата к оригиналу
                await link_lead_to_contact(lead_id, original.get('id'))

                # Переносим примечания
                notes = await get_contact_notes(duplicate.get('id'), SUBDOMAIN)
                await transfer_notes(notes, original.get('id'), SUBDOMAIN)

            
            logger.info('Webhook processing finished')
            return {'status': 'ok'}

        except Exception as e:
            params = f'Phone: {original_phone}, lead_id: {lead_id}'
            logger.error(f'Ошибка при обработке вебхука. Параметры: {params}. Ошибка: {e}')
            raise
