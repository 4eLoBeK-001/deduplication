from pprint import pprint
from fastapi import FastAPI, Request

from app.services.helpers import find_contact_by_phone, clean_phone


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
    contact = await find_contact_by_phone(phone, 'kostantinef')

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
    result = await find_contact_by_phone('71231231212', 'kostantinef')
    lst = []
    for i in result:
        lst.append(
            {'id': i.get('id'), 'created_at': i.get('created_at')}
        )
        
    original = min(lst, key=lambda x: x['id'])


    return result