from pprint import pprint
from fastapi import FastAPI, Request


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
    

    pprint(data) 
    
    return {"status": "ok"}
