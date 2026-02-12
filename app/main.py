from pprint import pprint
from fastapi import FastAPI, Request
import httpx

from app.services.helpers import delete_contact, find_contact_by_id, find_contacts_by_phone, clean_phone, find_duplicate, get_contact_notes, link_lead_to_contact, update_original_contact


app = FastAPI(title='amoCRM')


@app.get('/')
async def test(request: Request):
    return {"status": "ok"}



@app.post('/webhook')
async def test_request(request: Request):

    form_data = await request.form()
    
    data = dict(form_data)

    contact_id = data.get('contacts[add][0][id]')
    phone = data.get('contacts[add][0][custom_fields][0][values][0][value]')
    print(contact_id)
    print(phone)

    phone = clean_phone(phone)
    contact = await find_contacts_by_phone(phone, 'kostantinef')

    if len(contact) > 1:
        original = await find_duplicate(contact)
        print(original)
    

    pprint(data) 
    
    return {"status": "ok"}


@app.get('/contacts')
async def all_contants_endpoint():
    result = await find_contact_by_id('81676058', 'kostantinef')
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


