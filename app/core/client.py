import httpx
from app.services.utils import clean_phone
from app.core.logger import logger


ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjY5ZDBjMzg1ZWQ0ZDRkYmEyYzkxODk2MDQwZGU1NzU5YzE0OGZiNzA3NWMzYWQ0NjEzZmVmYTgxNWUwNmMxOTFhMTc1ZTk4MjQyODJkNGMzIn0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiI2OWQwYzM4NWVkNGQ0ZGJhMmM5MTg5NjA0MGRlNTc1OWMxNDhmYjcwNzVjM2FkNDYxM2ZlZmE4MTVlMDZjMTkxYTE3NWU5ODI0MjgyZDRjMyIsImlhdCI6MTc3MTMyNTQxMiwibmJmIjoxNzcxMzI1NDEyLCJleHAiOjE3NzE0MTE4MTIsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiNjllNTQ2ZGUtODNmOS00ZWVhLWEwNDgtNWU5MWQ2MzdlMTZiIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.QU15f9bKLhBS6akkNGDsABBYkyl_QrIH6-1JicfFCYebfOL9kkdSN03NNX01hMWTydVJpvdsVkRbSzfbOCv787yBxD-6zqSE-qjextWLpm1JqpYDB4ycFy-9MkkX4weYkum8KxCj63cw2BeJXBqUaUpsoA-ovigxByIrgTvrABdUjLFDMuPp40oGWTsXnukhuTx2YhkK2szgyekpmR0K_e4ftrHJFXDBalIPZFJrsMgFGXk7KlMK_TbW8jhMnO5ieKTx57H10tFpxEGTtg6AXiyu6R_KPZw-NGJY0Qn6zdb2zNUL4KPFvIMtB5jFZlGflEBl7d62f-5uD9ngTEyedQ'

class AmoCRMClient:
    def __init__(self, subdomain: str, token: str = ACCESS_TOKEN):
        self.subdomain = subdomain
        self.base_url = f'https://{subdomain}.amocrm.ru/api/v4'
        self.token = token
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()


    def _headers(self, json_type: bool = False):
        headers = {'Authorization': f'Bearer {self.token}'}
        if json_type:
            headers['Content-Type'] = 'application/json'
        return headers
    
    async def get_contacts(self, query: str):
        url = f'{self.base_url}/contacts'
        params = {
            'query': query,
            'with': 'leads'
        }

        try:
            response = await self.client.get(url, headers=self._headers(), params=params)

            if response.status_code == 200:
                return response.json().get("_embedded", {}).get("contacts", [])
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
        return await self.get_contacts(contact_id)
    
    # Стираются все custom_fields
    async def delete_contact(self, contact_id: str):
        payload = {
            'name': '',
            'custom_fields_values': [
            ]
        }
        url = f'{self.base_url}/contacts/{contact_id}'
        headers = self._headers(True)

        contact = await self.find_contact_by_id(contact_id)

        # Все поля кастомные поля опустошаются у этого контакта
        for i in contact[0].get('custom_fields_values'):
            i.get('values')[0]['value'] = ''
            payload.get('custom_fields_values').append(i)

        response = await self.client.patch(url, headers=headers, json=payload)

        if response.status_code == 200:
            return 'Дубль обработан'
        return f'Ошибка: {response.status_code} - {response.text}'

        
    async def update_original_contact(self, original_id: int, duplicate_id: int):
        # Здесь будут отсутствующие поля у оригинала, но существующие у дубликата
        payload = {
            "custom_fields_values": [
            ]
        }
        url = f'{self.base_url}/contacts/{original_id}'
        headers = self._headers(True)
        
        original_contact = await self.find_contact_by_id(str(original_id))
        duplicate_contact = await self.find_contact_by_id(str(duplicate_id))

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

        response = await self.client.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            await self.delete_contact(str(duplicate_id))
            return response.json(), response.text
        return response.status_code, response.text


    # Для того чтобы привязать сделку к контакту нужно: айди сделки и айди контакта
    async def link_lead_to_contact(self, lead_id: int, contact_id: int):
        if lead_id == 0:
            return False
        
        url = f'{self.base_url}/leads/{lead_id}/link'
        headers = self._headers(True)
        payload = [
            {
                'to_entity_id': contact_id,
                'to_entity_type': 'contacts',
                'metadata': {'is_main': True}
            }
        ]

        response = await self.client.post(url, headers=headers, json=payload)
        if response.status_code in (200, 201, 204):
            return True
        return False
    
    
    # Получаем все примечания/заметки контакта. Нужно: айди контакта
    async def get_contact_notes(self, contact_id: int):
        url = f'{self.base_url}/contacts/{contact_id}/notes'
        headers = self._headers(True)
        response = await self.client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('_embedded', {}).get('notes', [])
        return []

    
    # Переносит примечания из старого контакта в новый. Для этого надо
    # передать: список примечаний старого контакта и айди контакта в который надо перенести
    async def transfer_notes(self, notes_list, original_contact_id):
        if not notes_list:
            return False
        
        url = f'{self.base_url}/contacts/{original_contact_id}/notes'
        headers = self._headers(True)
        
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
            await self.client.post(url, headers=headers, json=payload)
            return True
        return False

