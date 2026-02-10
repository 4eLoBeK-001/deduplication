import asyncio
from pprint import pprint
import re
import httpx


def clean_phone(phone: str) -> str:
    return re.sub(r'\D', '', phone)


    

async def find_contacts_by_phone(phone: str, subdomain: str):
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjlmZjM3NTM2Zjg1NmNlYmFjN2ZjYmZiYjdkZWJhOGU4OTAxNTEyNmYwMDhjZDIzMzk4NjBlZDM0NWJiYjkyNjJkMTRjY2RlOWU0MjAxMTc5In0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiI5ZmYzNzUzNmY4NTZjZWJhYzdmY2JmYmI3ZGViYThlODkwMTUxMjZmMDA4Y2QyMzM5ODYwZWQzNDViYmI5MjYyZDE0Y2NkZTllNDIwMTE3OSIsImlhdCI6MTc3MDc1NDQ0MiwibmJmIjoxNzcwNzU0NDQyLCJleHAiOjE3NzA4NDA4NDIsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiNzU2ODA3NzEtYWJlMy00YTI1LTg1ODctMjY0NTg1OWFmMmFlIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.HVN4OAoeA12OrN0Dr6gnrqKciODFhmAN7Svm0uDKGaePMvNMKlePWCPZyMH6X2P1RHgmJjktj0kBhJa2oxp3c9a3PlpXCZw_1RdAAHQjE_HJAAvj_D7alR_OuUtQYWA94m2m_96PXXcbob0IAANHJHuYW5vI3m1YMjAz6or344byk11QPZm2VI98ONYjOQ-8hb8ayJFDe03xyp_yhxhwcp2NlwuA_K1qsnfw9l1m3GHcZbrYA-MOUtqi_IeTSSjrH3RYoV6vsbLZP4eVekAbM2nsswU-gKozeouALGXdJGmnx73LAuor6fmc_ixws9y8sQ4wrnHX4Ur3E14kZ6oG3A'
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts'
    headers = {'Authorization': f'Bearer {access_token}'}
    phone = clean_phone(phone)
    params = {'query': f'{phone}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

            
        if response.status_code == 200:
            contacts = response.json().get("_embedded", {}).get("contacts", [])
            return contacts
        return response.status_code, response.text


async def find_contact_by_id(contact_id: str, subdomain: str):
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjlmZjM3NTM2Zjg1NmNlYmFjN2ZjYmZiYjdkZWJhOGU4OTAxNTEyNmYwMDhjZDIzMzk4NjBlZDM0NWJiYjkyNjJkMTRjY2RlOWU0MjAxMTc5In0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiI5ZmYzNzUzNmY4NTZjZWJhYzdmY2JmYmI3ZGViYThlODkwMTUxMjZmMDA4Y2QyMzM5ODYwZWQzNDViYmI5MjYyZDE0Y2NkZTllNDIwMTE3OSIsImlhdCI6MTc3MDc1NDQ0MiwibmJmIjoxNzcwNzU0NDQyLCJleHAiOjE3NzA4NDA4NDIsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiNzU2ODA3NzEtYWJlMy00YTI1LTg1ODctMjY0NTg1OWFmMmFlIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.HVN4OAoeA12OrN0Dr6gnrqKciODFhmAN7Svm0uDKGaePMvNMKlePWCPZyMH6X2P1RHgmJjktj0kBhJa2oxp3c9a3PlpXCZw_1RdAAHQjE_HJAAvj_D7alR_OuUtQYWA94m2m_96PXXcbob0IAANHJHuYW5vI3m1YMjAz6or344byk11QPZm2VI98ONYjOQ-8hb8ayJFDe03xyp_yhxhwcp2NlwuA_K1qsnfw9l1m3GHcZbrYA-MOUtqi_IeTSSjrH3RYoV6vsbLZP4eVekAbM2nsswU-gKozeouALGXdJGmnx73LAuor6fmc_ixws9y8sQ4wrnHX4Ur3E14kZ6oG3A'
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
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjlmZjM3NTM2Zjg1NmNlYmFjN2ZjYmZiYjdkZWJhOGU4OTAxNTEyNmYwMDhjZDIzMzk4NjBlZDM0NWJiYjkyNjJkMTRjY2RlOWU0MjAxMTc5In0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiI5ZmYzNzUzNmY4NTZjZWJhYzdmY2JmYmI3ZGViYThlODkwMTUxMjZmMDA4Y2QyMzM5ODYwZWQzNDViYmI5MjYyZDE0Y2NkZTllNDIwMTE3OSIsImlhdCI6MTc3MDc1NDQ0MiwibmJmIjoxNzcwNzU0NDQyLCJleHAiOjE3NzA4NDA4NDIsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiNzU2ODA3NzEtYWJlMy00YTI1LTg1ODctMjY0NTg1OWFmMmFlIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.HVN4OAoeA12OrN0Dr6gnrqKciODFhmAN7Svm0uDKGaePMvNMKlePWCPZyMH6X2P1RHgmJjktj0kBhJa2oxp3c9a3PlpXCZw_1RdAAHQjE_HJAAvj_D7alR_OuUtQYWA94m2m_96PXXcbob0IAANHJHuYW5vI3m1YMjAz6or344byk11QPZm2VI98ONYjOQ-8hb8ayJFDe03xyp_yhxhwcp2NlwuA_K1qsnfw9l1m3GHcZbrYA-MOUtqi_IeTSSjrH3RYoV6vsbLZP4eVekAbM2nsswU-gKozeouALGXdJGmnx73LAuor6fmc_ixws9y8sQ4wrnHX4Ur3E14kZ6oG3A'
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

