import asyncio
import os
import httpx

from dotenv import load_dotenv
from pprint import pprint
from fastapi import FastAPI, Request

from app.services.helpers import (
    extract_phone_final, find_contacts_by_phone, clean_phone, 
    find_duplicate, get_contact_notes, link_lead_to_contact, 
    transfer_notes, update_original_contact
)

load_dotenv()

SUBDOMAIN = os.getenv("AMOCRM_SUBDOMAIN")


app = FastAPI(title='amoCRM')


@app.get('/')
async def test(request: Request):
    return {"status": "ok"}


@app.post('/webhook')
async def test_request(request: Request):

    form_data = await request.form()
    
    data = dict(form_data)
    
    contact_id = data.get('contacts[add][0][id]')
    original_phone = await extract_phone_final(data)
    
    if not original_phone:
        return {'text': 'phone nt found'}

    original_phone = clean_phone(original_phone)
    found_contacts = await find_contacts_by_phone(original_phone, SUBDOMAIN)
    
    # Если у контакта есть сделки
    lead_id = 0
    if found_contacts[-1].get('_embedded').get('leads'):
        lead_id = found_contacts[-1].get('_embedded').get('leads')[0].get('id')

    if len(found_contacts) > 1:
        original, duplicate = await find_duplicate(found_contacts)

        await asyncio.sleep(2)
        await update_original_contact(original, duplicate, SUBDOMAIN)
        await link_lead_to_contact(lead_id, original.get('id'))
        notes = await get_contact_notes(duplicate.get('id'), SUBDOMAIN)
        await transfer_notes(notes, original.get('id'), SUBDOMAIN)
        return {'Успешно': 'Супер!'}
    
    return {"status": "ok"}
