import asyncio
from pprint import pprint
import re
import httpx

access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImJmMmE4MjEzMDVkZGJkMzc2NmRiYmFiNTQwNzRiMWRmY2NkNDFiN2FlZmRmMmVmZWJjNjk2NzNhNzNkOTY3ZjM1NTE2MTBmMDI2MjI0YzVkIn0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiJiZjJhODIxMzA1ZGRiZDM3NjZkYmJhYjU0MDc0YjFkZmNjZDQxYjdhZWZkZjJlZmViYzY5NjczYTczZDk2N2YzNTUxNjEwZjAyNjIyNGM1ZCIsImlhdCI6MTc3MDkwMTExNiwibmJmIjoxNzcwOTAxMTE2LCJleHAiOjE3NzA5ODc1MTYsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiYTczNWNiMzAtM2I2My00MWUxLTgyZTMtNzM4YTg2NzZmNWMxIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.DMtHs2awhf6LEuM3X4qigcdvuBsFe-nFlDaFQdjLD_6fgYnMbJHExCpRBFOowR4ceQxKMGtfr6mEyGy9zxLxDnKi0yhMg_HrHo7o7KVpJ-QgIV1NnndQIZJRAmnd_9wJWJVfuL-NP0cOvaXTfKF-NOBDKFBidpx3TqCHThfOwU3FFH9YoH_B2IjaAog4oyQ5VRCCP2Qfn7UuZQRLNDATv4t7YL92mjSdzo-XRBD-9r6dMYSn8UK0sgcVjz92nc2F_YyhETsDW326B7FvaH5wB_a6h1TmfK8Sgt7EGYg2hM0XLyiKnoEv2h85WHpmWRcw3iC_IqjYhUU8Lgyb6t05VA'

def clean_phone(phone: str) -> str:
    return re.sub(r'\D', '', phone)

async def find_contacts_by_phone(phone: str, subdomain: str):
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts'
    headers = {'Authorization': f'Bearer {access_token}'}
    phone = clean_phone(phone)
    params = {
        'query': f'{phone}',
        'with': 'leads',
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

            
        if response.status_code == 200:
            contacts = response.json().get("_embedded", {}).get("contacts", [])
            return contacts
        return response.status_code, response.text


async def find_contact_by_id(contact_id: str, subdomain: str):
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'query': f'{contact_id}',
        'with': 'leads',
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

            
        if response.status_code == 200:
            contacts = response.json().get("_embedded", {}).get("contacts", [])
            return contacts
        return []


# Передаём список контактов. 
# Возвращает оригинал и самый новый контакт
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
    return original, duplicate


# Стираются все custom_fields_values
async def delete_contact(subdomain: str, contact_id: str):
    payload = {
            'name': '',
            'custom_fields_values': [
            ]
        }
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts/{contact_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    contact = await find_contact_by_id(contact_id, subdomain)

    for i in contact[0].get('custom_fields_values'):
        i['values'][0]['value'] = ''
        payload.get('custom_fields_values').append(i)

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return 'Дубль обработан'
        return f'Ошибка: {response.status_code} - {response.text}'


async def update_original_contact(original, duplicate, subdomain: str):

    original_contact = await find_contact_by_id(original['id'], subdomain)
    duplicate_contact = await find_contact_by_id(duplicate['id'], subdomain)

    # Существующие поля дупликата и оригинала 
    existings_duplicate_fields = duplicate_contact[0].get('custom_fields_values')
    existings_original_fields = original_contact[0].get('custom_fields_values')

    # Названия существующих полей
    existings_duplicate_field_names = {field_code.get('field_code') for field_code in existings_duplicate_fields}
    existings_original_field_names = {field_code.get('field_code') for field_code in existings_original_fields}

    # Отсутствующие поля у оригинала
    missing_field_names = existings_duplicate_field_names - existings_original_field_names


    url = f'https://kostantinef.amocrm.ru/api/v4/contacts/{original_contact[0].get('id')}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Здесь будут отсутствующие поля у оригинала, но существующие у дубликата
    payload = {
            "custom_fields_values": [
            ]
        }
    # Заполняются отсутствующие поля у оригинала
    for i in existings_duplicate_fields:
        if i.get('field_code') in missing_field_names:
            payload.get('custom_fields_values').append(i)
            missing_field_names.remove(i.get('field_code')) # пОСЛЕ КОММИТА УДАЛИТЬ ЭТУ СТРоку

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            await delete_contact(subdomain, str(duplicate['id']))
            return response.json(), response.text
        return response.status_code, response.text


# Для того чтобы привязать сделку к контакту нужно: айди сделки и айди контакта
async def link_lead_to_contact(lead_id: int, contact_id: int, subdomain: str='kostantinef'):
    if lead_id == 0:
        return
    
    url = f'https://{subdomain}.amocrm.ru/api/v4/leads/{lead_id}/link'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = [
        {
            'to_entity_id': contact_id,
            'to_entity_type': 'contacts',
            'metadata': {
                'is_main': True
            }
        }
    ]

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        
        if response.status_code in (200, 201, 204):
            return True
        return False


# Получаем все примечания/заметки контакта. Нужно: айди контакта
async def get_contact_notes(contact_id: int, subdomain: str):
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts/{contact_id}/notes'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('_embedded', {}).get('notes', [])
        return []


# Переносит примечания из старого контакта в новый. Для этого надо
# передать: список примечаний старого контакта и айди контакта в который надо перенести
async def transfer_notes(notes_list, original_contact_id, subdomain):
    if not notes_list:
        return
        
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts/{original_contact_id}/notes'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    payload = []
    for note in notes_list:
        payload.append({
            'note_type': note.get('note_type', 'common'),
            'params': note.get('params', {
                'text': note.get('params', {}).get('text')
            })
        })

    if payload:
        async with httpx.AsyncClient() as client:
            await client.post(url, headers=headers, json=payload)
            return True


async def extract_phone_final(data):
    phone_index = None
    
    # Ищет под каким номером в списке custom_fields лежит телефон
    for key, value in data.items():
        if '[code]' in key and value == 'PHONE':
            phone_index = key.split('[code]')[0]
            break
    
    if not phone_index:
        return None

    # Ищет значение 'value', которое принадлежит этому индексу.
    for key, value in data.items():
        if phone_index in key and '[value]' in key:
            return value

    return None
