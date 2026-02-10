import asyncio
from pprint import pprint
import re
import httpx


def clean_phone(phone: str) -> str:
    return re.sub(r'\D', '', phone)


    

async def find_contacts_by_phone(phone: str, subdomain: str):
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjJhNzVlODdlODM3YWJiYjMxZGU1N2VhZjZkNmQyZmIyNDIyNjdmMDFmNTFlZDAxM2EwN2YxMDBlNDdiYTNlNzA5NmY0MTgwYTBjMDEyN2ZiIn0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiIyYTc1ZTg3ZTgzN2FiYmIzMWRlNTdlYWY2ZDZkMmZiMjQyMjY3ZjAxZjUxZWQwMTNhMDdmMTAwZTQ3YmEzZTcwOTZmNDE4MGEwYzAxMjdmYiIsImlhdCI6MTc3MDc1MzYwNSwibmJmIjoxNzcwNzUzNjA1LCJleHAiOjE3NzA4NDAwMDUsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiYzMyM2MwOGMtZjJlMy00NTU5LThlMmMtYWI5YjkwMTFlYmVlIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.dOZ-A1DjGvoMkRG8ULR3LcmzTamX84Iof_vCYneYVn0yFcjlwhcbQXd9zEzRvYTfN9PigLHnvXe8GLxTFDg6PgIdIMIWx05osDDAZQ12wHVOm1KJu2tx5hyY73u8UnD_e5QZ28qL64tO0-NmjwiC1iJpPlzvLqoAzmxJoNWvetzwdc1v3Yjss5nI6QMqtQS2ao22dJbJL-zlhzKI7C7MbD_e5QZ28qL64tO0-NmjwiC1iJpPlzvLqoAzmxJoNWvetzwdc1v3Yjss5nI6QMqtQS2ao22dJbJL-zlhzKI7C7MbLgoQpJp3o0ugwTiQvDHUx-mrYjTX2Y3UurDR1nTiS-ylZgAMxlfF2wpW0V4_A1Y3AJ0sJkZV2SrPyoo8XJTLBkpaYtmYl7FFcfzMniABxp5iRpMiRoiWoXrkLW9CSm8Yg'
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts'
    headers = {'Authorization': f'Bearer {access_token}'}
    phone = clean_phone(phone)
    params = {'query': f'{phone}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

            
        if response.status_code == 200:
            contacts = response.json().get("_embedded", {}).get("contacts", [])
            return contacts
        return []


async def find_contact_by_id(contact_id: str, subdomain: str):
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjJhNzVlODdlODM3YWJiYjMxZGU1N2VhZjZkNmQyZmIyNDIyNjdmMDFmNTFlZDAxM2EwN2YxMDBlNDdiYTNlNzA5NmY0MTgwYTBjMDEyN2ZiIn0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiIyYTc1ZTg3ZTgzN2FiYmIzMWRlNTdlYWY2ZDZkMmZiMjQyMjY3ZjAxZjUxZWQwMTNhMDdmMTAwZTQ3YmEzZTcwOTZmNDE4MGEwYzAxMjdmYiIsImlhdCI6MTc3MDc1MzYwNSwibmJmIjoxNzcwNzUzNjA1LCJleHAiOjE3NzA4NDAwMDUsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiYzMyM2MwOGMtZjJlMy00NTU5LThlMmMtYWI5YjkwMTFlYmVlIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.dOZ-A1DjGvoMkRG8ULR3LcmzTamX84Iof_vCYneYVn0yFcjlwhcbQXd9zEzRvYTfN9PigLHnvXe8GLxTFDg6PgIdIMIWx05osDDAZQ12wHVOm1KJu2tx5hyY73u8UnD_e5QZ28qL64tO0-NmjwiC1iJpPlzvLqoAzmxJoNWvetzwdc1v3Yjss5nI6QMqtQS2ao22dJbJL-zlhzKI7C7MbD_e5QZ28qL64tO0-NmjwiC1iJpPlzvLqoAzmxJoNWvetzwdc1v3Yjss5nI6QMqtQS2ao22dJbJL-zlhzKI7C7MbLgoQpJp3o0ugwTiQvDHUx-mrYjTX2Y3UurDR1nTiS-ylZgAMxlfF2wpW0V4_A1Y3AJ0sJkZV2SrPyoo8XJTLBkpaYtmYl7FFcfzMniABxp5iRpMiRoiWoXrkLW9CSm8Yg'
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'query': f'{contact_id}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

            
        if response.status_code == 200:
            contacts = response.json().get("_embedded", {}).get("contacts", [])
            return contacts
        return []


async def find_duplicate(contacts: list):
    if not contacts:
        return None

    lst = []
    for contact in contacts:
        lst.append(
            {'id': contact.get('id'), 'created_at': contact.get('created_at')}
        )
        
    original = min(lst, key=lambda x: x['id'])
    duplicate = max(lst, key=lambda x: x['id'])
    # print(original, duplicate)
    return original, duplicate


async def delete_contact(subdomain: str, contact_id: str):
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjJhNzVlODdlODM3YWJiYjMxZGU1N2VhZjZkNmQyZmIyNDIyNjdmMDFmNTFlZDAxM2EwN2YxMDBlNDdiYTNlNzA5NmY0MTgwYTBjMDEyN2ZiIn0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiIyYTc1ZTg3ZTgzN2FiYmIzMWRlNTdlYWY2ZDZkMmZiMjQyMjY3ZjAxZjUxZWQwMTNhMDdmMTAwZTQ3YmEzZTcwOTZmNDE4MGEwYzAxMjdmYiIsImlhdCI6MTc3MDc1MzYwNSwibmJmIjoxNzcwNzUzNjA1LCJleHAiOjE3NzA4NDAwMDUsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiYzMyM2MwOGMtZjJlMy00NTU5LThlMmMtYWI5YjkwMTFlYmVlIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.dOZ-A1DjGvoMkRG8ULR3LcmzTamX84Iof_vCYneYVn0yFcjlwhcbQXd9zEzRvYTfN9PigLHnvXe8GLxTFDg6PgIdIMIWx05osDDAZQ12wHVOm1KJu2tx5hyY73u8UnD_e5QZ28qL64tO0-NmjwiC1iJpPlzvLqoAzmxJoNWvetzwdc1v3Yjss5nI6QMqtQS2ao22dJbJL-zlhzKI7C7MbD_e5QZ28qL64tO0-NmjwiC1iJpPlzvLqoAzmxJoNWvetzwdc1v3Yjss5nI6QMqtQS2ao22dJbJL-zlhzKI7C7MbLgoQpJp3o0ugwTiQvDHUx-mrYjTX2Y3UurDR1nTiS-ylZgAMxlfF2wpW0V4_A1Y3AJ0sJkZV2SrPyoo8XJTLBkpaYtmYl7FFcfzMniABxp5iRpMiRoiWoXrkLW9CSm8Yg'
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts/{contact_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Вместо удаления я просто делаем контакт пустым, 
    # потому что amoCRM болкирует delete запросы.
    payload = {
        "name": "",
        "custom_fields_values": [
            {
                "field_code": "PHONE",
                "values": [
                    {
                        "value": f"" 
                    }
                ] 
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return "Дубль обработан"
        return f"Ошибка: {response.status_code} - {response.text}"


async def update_original_contact():
    result = await find_contacts_by_phone('71231231212', 'kostantinef')
    print(result)
    original, duplucate = await find_duplicate(result)

    original_contact = await find_contact_by_id(original['id'], 'kostantinef')
    duplucate_contact = await find_contact_by_id(duplucate['id'], 'kostantinef')

    # Существующие поля дупликата 
    existings_duplicate_fields = duplucate_contact[0].get('custom_fields_values')

    

    # return original_contact, duplucate_contact
    return {
        'Существующие поля дупликата': duplucate_contact[0].get('custom_fields_values')
    }
    
    return {
        'idD': duplucate_contact[0].get('custom_fields_values')[0].get('values')[0].get('value'),
        'field_codeD': duplucate_contact[0].get('custom_fields_values')[0].get('field_code'),
        'idO': original_contact[0].get('custom_fields_values')[0].get('values')[0].get('value'),
        'field_codeO': original_contact[0].get('custom_fields_values')[0].get('field_code'),
    }
    duplicate_pyload = {
        'name': ...,
        "custom_fields_values": [
            {
                "field_code": "PHONE",
                "values": [
                    {
                        "value": f"" 
                    }
                ] 
            }
        ]
    }




# asyncio.run(all_contacts('kostantinef')) 
# 4545454545

