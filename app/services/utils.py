import re



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
    TG_FIELD_ID = "2400145"
    tg_index = None

    for key, value in data.items():
        if '[id]' in key and value == TG_FIELD_ID:
            tg_index = key.split('[id]')[0]
            break

    if not tg_index:
        return None

    for key, value in data.items():
        if tg_index in key and '[value]' in key:
            return value

    return None

