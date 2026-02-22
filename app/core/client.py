import json
import os
from dotenv import load_dotenv
import httpx
from app.services.utils import clean_phone
from app.core.logger import logger
from app.core.redis_config import redis_client

load_dotenv()

CLIENT_ID = os.getenv('AMOCRM_CLIENT_ID')
CLIENT_SECRET = os.getenv('AMOCRM_CLIENT_SECRET')
SUBDOMAIN = os.getenv('AMOCRM_SUBDOMAIN')
REDIRECT_URL = os.getenv('AMOCRM_REDIRECT_URL')


class AmoCRMClient:
    def __init__(self, subdomain: str):
        self.subdomain = subdomain
        self.base_url = f'https://{subdomain}.amocrm.ru/api/v4'
        self.token_key = 'amocrm_auth_data'
        self.access_token = None
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        await self._load_token()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    

    async def _load_token(self):
        data = await redis_client.get(self.token_key)
        if data:
            token_dict = json.loads(data)
            self.access_token = token_dict.get('access_token')
        else:
            logger.error('Токен отсутствует в Redis. Нужно провести пероаичную авторизацию')
    
    async def _refresh_token(self):
        data = await redis_client.get(self.token_key)
        if not data:
            return False

        token_data = json.loads(data)
        refresh_token = token_data.get('refresh_token')

        url = f'https://{self.subdomain}.amocrm.ru/oauth2/access_token'
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'redirect_uri': REDIRECT_URL,
            'refresh_token': refresh_token,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=params)
            if response.status_code == 200:
                data = response.json()
                await redis_client.set(self.token_key, json.dumps(data))
                self.access_token = data.get('access_token')
                logger.info('Токен обновлён в Redis')
                return True

            logger.error(f'Ошибка обновления токена: {response.status_code} | {response.text}')
            return False
    
    async def exchange_code_to_token(self, auth_code: str):
        url = f'https://{self.subdomain}.amocrm.ru/oauth2/access_token'
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': REDIRECT_URL,
        }
        respose = await self.client.post(url, json=payload)
        if respose.status_code == 200:
            data = respose.json()
            await redis_client.set(self.token_key, json.dumps(data))
            self.access_token = data.get('access_token')
            logger.info('Первичная авторизация успешна')
            return True

        logger.error(f'Ошибка: {respose.status_code} - {respose.text}')    
        return False


    async def _request(self, method, endpoint, **kwargs):
        if not self.access_token:
            await self._load_token()

        url = f'{self.base_url}/{endpoint.lstrip('/')}'

        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f'Bearer {self.access_token}'
        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'

        response = await self.client.request(method, url, headers=headers, **kwargs)

        if response.status_code == 401:
            logger.warning('Token expired')
            if await self._refresh_token():
                headers['Authorization'] = f'Bearer {self.access_token}'
                response = await self.client.request(method, url, headers=headers, **kwargs)
        
        return response


    def _headers(self, json_type: bool = False):
        headers = {'Authorization': f'Bearer {self.token}'}
        if json_type:
            headers['Content-Type'] = 'application/json'
        return headers
    
    async def get_contacts(self, query: str):
        params = {
            'query': query,
            'with': 'leads'
        }

        try:
            response = await self._request('GET', 'contacts', params=params)

            if response.status_code == 200:
                return response.json().get('_embedded', {}).get('contacts', [])
            return []
        except httpx.HTTPStatusError as e:
            logger.error(f'Ошибка API amoCRM: {e.response.status_code} при поиске {query}')
            return []
        except Exception as e:
            logger.error(f'Неожиданная ошибка при поиске контактов: {e}')
            return []

    # Поиск контакта по телефону
    async def find_contacts_by_phone(self, phone: str):
        return await self.get_contacts(clean_phone(phone))

    # Поиск контакта по его айди
    async def find_contact_by_id(self, contact_id: str):
        params = {'with': 'leads'}
        response = await self._request('GET', f'contacts/{contact_id}', params=params)
        if response.status_code == 200:
            return [response.json()]
        return []
    
    async def find_contact_by_tg_nick(self, tg_nick: str):
        params = {
            'limit': 250,
            'with': 'leads'
        }

        response = await self._request('GET', 'contacts', params=params)

        if response.status_code != 200:
            logger.error(f'Ошибка не р: {response.status_code} - {response.text}')
            return []

        contacts = response.json().get('_embedded', {}).get('contacts', [])

        filtered = []

        for contact in contacts:
            fields = contact.get('custom_fields_values') or []
            for field in fields:
                if field.get('field_id') == 2400145:
                    for value in field.get('values', []):
                        if value.get('value') == tg_nick:
                            filtered.append(contact)
        return filtered

    # Стираются все custom_fields
    async def delete_contact(self, contact_id: str):
        payload = {
            'name': '',
            'custom_fields_values': [
            ]
        }

        contact = await self.find_contact_by_id(contact_id)

        # Все поля кастомные поля опустошаются у этого контакта
        for i in contact[0].get('custom_fields_values'):
            i.get('values')[0]['value'] = ''
            payload.get('custom_fields_values').append(i)

        response = await self._request('PATCH', f'contacts/{contact_id}', json=payload)

        if response.status_code == 200:
            return 'Дубль обработан'
        return f'Ошибка: {response.status_code} - {response.text}'

        
    async def update_original_contact(self, original_id: int, duplicate_id: int):
        # Здесь будут отсутствующие поля у оригинала, но существующие у дубликата
        payload = {
            'custom_fields_values': [
            ]
        }
        
        original_contact = await self.find_contact_by_id(str(original_id))
        duplicate_contact = await self.find_contact_by_id(str(duplicate_id))

        if not original_contact:
            logger.error(f'Original contact {original_id} not found')
            return

        if not duplicate_contact:
            logger.error(f'Duplicate contact {duplicate_id} not found')
            return

        # Существующие поля дупликата и оригинала 
        existings_duplicate_fields = duplicate_contact[0].get('custom_fields_values') or []
        existings_original_fields = original_contact[0].get('custom_fields_values') or []

        # Названия существующих полей
        existings_duplicate_field_names = {field_code.get('field_code') for field_code in existings_duplicate_fields}
        existings_original_field_names = {field_code.get('field_code') for field_code in existings_original_fields}

        # Отсутствующие поля у оригинала
        missing_field_names = existings_duplicate_field_names - existings_original_field_names

        if missing_field_names:

            # Заполняются отсутствующие поля у оригинала
            for i in existings_duplicate_fields:
                if i.get('field_code') in missing_field_names:
                    payload.get('custom_fields_values').append(i)

        response = await self._request('PATCH', f'contacts/{original_id}', json=payload)

        if response.status_code == 200:
            await self.delete_contact(str(duplicate_id))
            return response.json(), response.text
        return response.status_code, response.text


    # Для того чтобы привязать сделку к контакту нужно: айди сделки и айди контакта
    async def link_lead_to_contact(self, lead_id: int, contact_id: int):
        if lead_id == 0:
            return False

        payload = [
            {
                'to_entity_id': int(contact_id),
                'to_entity_type': 'contacts',
                'metadata': {
                    'is_main': True
                }
            }
        ]

        response = await self._request('POST', f'leads/{lead_id}/link', json=payload)
        
        # Логируем ответ, чтобы увидеть ошибку от amo, если она есть
        if response.status_code not in (200, 201, 204):
            logger.error(f'Link error: {response.status_code} - {response.text}')
            return False
        return True
    
    
    # Получаем все примечания/заметки контакта. Нужно: айди контакта
    async def get_contact_notes(self, contact_id: int):
        response = await self._request('GET', f'contacts/{contact_id}/notes')

        if response.status_code == 200:
            return response.json().get('_embedded', {}).get('notes', [])
        return []

    
    # Переносит примечания из старого контакта в новый. Для этого надо
    # передать: список примечаний старого контакта и айди контакта в который надо перенести
    async def transfer_notes(self, notes_list, original_contact_id):
        if not notes_list:
            return False

        
        payload = [
            {
                'note_type': note.get('note_type', 'common'),
                'params': note.get('params', {
                    'text': note.get('params', {}).get('text')
                })
            }
            for note in notes_list
        ]

        if payload:
            await self._request('POST', f'contacts/{original_contact_id}/notes', json=payload)
            return True
        return False

