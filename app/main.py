from pprint import pprint
from fastapi import FastAPI, Request
import httpx

from app.services.helpers import (
    extract_phone_final, find_contacts_by_phone, clean_phone, 
    find_duplicate, get_contact_notes, link_lead_to_contact, 
    transfer_notes, update_original_contact
)


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

    original_phone = clean_phone(original_phone)
    contact = await find_contacts_by_phone(original_phone, 'kostantinef')
    
    # Если у контакта есть сделки
    lead_id = 0
    if contact[-1].get('_embedded').get('leads'):
        lead_id = contact[-1].get('_embedded').get('leads')[0].get('id')

    if len(contact) > 1:
        original, duplicate = await find_duplicate(contact)
        await update_original_contact(original, duplicate, 'kostantinef')
        await link_lead_to_contact(lead_id, original.get('id'))
        notes = await get_contact_notes(duplicate.get('id'), 'kostantinef')
        await transfer_notes(notes, original.get('id'), 'kostantinef')
        return {'Успешно': 'Супер!'}
    
    return {"status": "ok"}
