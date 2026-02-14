import re



# Оставляем только цифры
def clean_phone(phone: str) -> str:
    return re.sub(r'\D', '', phone)


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
