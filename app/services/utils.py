import re

from app.core.logger import logger


# Оставляем только цифры
def clean_phone(phone: str) -> str:
    return re.sub(r'\D', '', phone)


async def extract_phone_final(data: dict):
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


async def extract_tg_nick_final(data: dict):
    prefix = None
    field_id = None

    for key, value in data.items():
        if '[name]' in key:
            val_str = str(value).lower()
            if "tg" in val_str or "telegram" in val_str or "телеграм" in val_str:
                prefix = key.replace('[name]', '')
                
                field_id = data.get(f"{prefix}[id]")
                break

    if not prefix:
        return None, None

    value_key = f"{prefix}[values][0][value]"
    tg_nick = data.get(value_key)

    return tg_nick, field_id


# Передаём список контактов. 
# Возвращает оригинал и самый новый контакт
async def find_duplicate(contacts: list):
    if not contacts:
        logger.warning('Попытка найти дубликаты в пустом списке')
        return None, None

    try:
        lst = []
        for contact in contacts:
            lst.append(
                {'id': contact.get('id'), 'created_at': contact.get('created_at')}
            )
            
        original = min(lst, key=lambda x: x['id'])
        duplicate = max(lst, key=lambda x: x['id'])
        return original, duplicate
    except KeyError as e:
        logger.error(f'Ошибка ключа: {e}')
        return None, None
