from pprint import pprint
from fastapi import FastAPI, Request
import httpx

from app.services.helpers import delete_contact, extract_phone_final, find_contact_by_id, find_contacts_by_phone, clean_phone, find_duplicate, get_contact_notes, link_lead_to_contact, transfer_notes, update_original_contact


app = FastAPI(title='amoCRM')


@app.get('/')
async def test(request: Request):
    return {"status": "ok"}



@app.post('/webhook')
async def test_request(request: Request):

    form_data = await request.form()
    
    data = dict(form_data)
    pprint(data)
    
    contact_id = data.get('contacts[add][0][id]')
    original_phone = await extract_phone_final(data)

    print(contact_id)
    print(original_phone)

    original_phone = clean_phone(original_phone)
    contact = await find_contacts_by_phone(original_phone, 'kostantinef')
    pprint(contact)
    
    # Если у контакта есть сделки
    lead_id = 0
    if contact[-1].get('_embedded').get('leads'):
        lead_id = contact[-1].get('_embedded').get('leads')[0].get('id')

    if len(contact) > 1:
        print('----------- ВЕТКА С ДУБЛИКАТОМ -----------')
        original, duplicate = await find_duplicate(contact)
        print('------------ АЙДИ ДУБЛИКАТА И ОРИГИНАЛА ------------')
        print(duplicate.get('id'), original.get('id'))
        await update_original_contact(original, duplicate, 'kostantinef')
        await link_lead_to_contact(lead_id, original.get('id'))
        notes = await get_contact_notes(duplicate.get('id'), 'kostantinef')
        await transfer_notes(notes, original.get('id'), 'kostantinef')
        print({'Успешно': 'Супер!'})
        return {'Успешно': 'Супер!'}
    
    return {"status": "ok"}


@app.get('/contacts')
async def all_contants_endpoint():
    result = await find_contact_by_id('81830990', 'kostantinef')
    if result[0].get('_embedded').get('leads'):
        is_leads = result[0].get('_embedded').get('leads')[0].get('id')
        print(is_leads)
    # original, duplucate = await find_duplicate(result)

    return {
        'all_contacts': result,
        # 'original': original,
        # 'duplucate': duplucate
    }


@app.delete('/contacts')
async def delete_contact_endpoint():
    deleted = await delete_contact(subdomain='kostantinef', contact_id='81700552')
    return deleted


@app.get('/GETcontacts')
async def allL_contants_endpoint():
    original_contact = await update_original_contact(subdomain='kostantinef')

    return   original_contact
    

@app.get('/link-lead')
async def link_lead_endpoint(lead_id: int=60446104, new_contact_id: int=81676058):
    success = await link_lead_to_contact(lead_id, new_contact_id, 'kostantinef')
    return {'status': 'Linked' if success else 'Failed'}



@app.get('/notes')
async def contact_notes(contact_id: int=81676058):
    success = await get_contact_notes(contact_id, 'kostantinef')
    return {'status': success if success else 'Failed'}


@app.get('/notessss')
async def transfer_notes_endpoint(contact_id: int=81676058):
    note = await get_contact_notes(81700552, 'kostantinef')

    success = await transfer_notes(note, contact_id, 'kostantinef')
    return {'status': success if success else 'Failed'}

# 81700552