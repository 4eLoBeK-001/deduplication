from pprint import pprint
from fastapi import FastAPI, Request

from app.services.helpers import delete_contact, find_contacts_by_phone, clean_phone, find_duplicate


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
        lst = []
        for i in contact:
            lst.append(
                {i.get('id'): i.get('created_at')}
            )
        print(lst)
    

    pprint(data) 
    
    return {"status": "ok"}


@app.get('/contacts')
async def all_contants_endpoint():
    result = await find_contacts_by_phone('71231231212', 'kostantinef')
    original = await find_duplicate(result)

    return {
        'all_contacts': result,
        'original': original
    }


@app.delete('/contacts')
async def delete_contact_endpoint():
    deleted = await delete_contact(subdomain='kostantinef', contact_id='81675848')
    return deleted
