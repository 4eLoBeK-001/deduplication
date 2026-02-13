import asyncio
import httpx
import json
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv('AMOCRM_CLIENT_ID')
CLIENT_SECRET = os.getenv('AMOCRM_CLIENT_SECRET')
SUBDOMAIN = os.getenv('AMOCRM_SUBDOMAIN')
REDIRECT_URL = os.getenv('AMOCRM_REDIRECT_URL')


AUTH_CODE = 'def502003f24bfc87aec358a878ecb00d82b681b08c33ccc7edab227c796a274e2d72025dfdead763bd77b3d27b5507ed643f6ea68652e2abe29b59332440aa61c3807f846236e9e498a7f28c9e414b38cdfc59f3a4a4dc8792625b897005a4b8bf204fd614cc0e8ab7f3fc249509c4e978e1e4c50cccd8d75df030f388c871c5f3086f6b61a1776e49e488c6aa039886532bccf9bfbaafacbaefc54b79cf0f46bb4b66b023edc3c8093e8e8fd28b4db22227183bb1b883e5cc78c3da87768b0abb75ed4c0321d8a322a8e39bd98c8e33c551a9481e36cf116c52aa9f95403c80e54312e793c0099f3e23c22464b641f22730902846e68d758db02c23416715544be6267ed16c7b8009737ae5e37204165c6f76c7d0e654695458618d02734b67a5e05cdfc936d8b355e946fc406c4cae28f801d04de7215cbd54b2383efce4bd9a15ab0b2944ffd2f554928426fbe74e4df82798124093a7c398e4e5abe39358aacc1f86ca02c8628c5a4377d45fabd5aae6a4707f52520d2ac855964a1d494a08c6a08eca4d67481b63b98c83d2509b923444a4934137c7b7aa70953edb444dbd1ec5a4433f02b5d248c74a5be312fb4263a874933430c0115ec00725741a813672d87c18ce065a1086001b0ee0206b7e999cf4c358e793427493fb851c9967740e8'

async def get_auth_token():
    url = f'https://{SUBDOMAIN}.amocrm.ru/oauth2/access_token'

    context = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'subdomain': SUBDOMAIN,
        'redirect_uri': REDIRECT_URL,
        'code': AUTH_CODE,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=context)

        if response.status_code == 200:
            data = response.json()
            with open('token.json', 'w') as f:
                json.dump(data, f)
                print('ok')
        else:
            print('Ошибка', response.status_code)
            print(response.text)

# asyncio.run(get_auth_token())


# Заного получаю acces_tokken
async def resresh_amo_token(refresh_token):
    url = f'https://{SUBDOMAIN}.amocrm.ru/oauth2/access_token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        # 'subdomain': SUBDOMAIN,
        'redirect_uri': REDIRECT_URL,
        'refresh_token': refresh_token,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=params)

        if response.status_code == 200:
            token = response.json()
            print(token)
            with open('token.json', 'w') as f:
                json.dump(token, f)
                print('ok')
            return token
        
        print(response.status_code, response.text)
        return response.status_code, response.text
    
asyncio.run(resresh_amo_token('def50200626f24f8eff9a65bbf1c8f0477e4f31c2530ce9821fab804dbee63a1eb4b55baf03ecdb01d3341727a3803cf0d2f479c25d6a70aeacbd74ba9eff90c510d5b8db64079c211abec528360f450997ce8e35f9803673b635ab36bca98b11ac4e761edb42a339963ff6dc3b07bb790e6b50e84ef3de36ceb1ca7cd5340a3910f59064df610de2e132869163f87a6e26d33645826e5ffc52f883c7a68695cc44a9eaf686b8f3cd93e973a429fcf8a768691bb04001c55bb95023d35623554667b139e99942832b366adc2e39876d584f6b8d5f8c4ddcc1ee7aa8fdde2a26211b06c9af8c7a7cc68c34a4ce692ffb65e1b12efef4525bf2efa251bc9c8373b5475e76a6394157cc7f01c700f8820258b609abc6653dc7b225f852964648eb6343cf30162b5121174b6e44ca0d6ad2645376a18226357d47df48ec3b641f98e419303e83ceb7971b6cc9d8c29c7dc3fe2a632e21bb3967f8bdaa9e2dc7b8fc8c4c547eacbe1afd15eca8b31a718fe1ed35aaed6458882dde627310d3e4e39588fe0428be91870bb332006ac5cf92e9d64891723368689551326aae71d33ca9cb127d6519f4f77110827b62646212b47965f3ccb09fb2bf59aba2d84227f70c8da6d8f4785014553b2a66ebac7748311f279751a3ea8033d5df53fe586c4ce3f1b61a890f4152b107329fba6e556'))


async def check_token():
    subdomain = 'kostantinef'
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjlmZjM3NTM2Zjg1NmNlYmFjN2ZjYmZiYjdkZWJhOGU4OTAxNTEyNmYwMDhjZDIzMzk4NjBlZDM0NWJiYjkyNjJkMTRjY2RlOWU0MjAxMTc5In0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiI5ZmYzNzUzNmY4NTZjZWJhYzdmY2JmYmI3ZGViYThlODkwMTUxMjZmMDA4Y2QyMzM5ODYwZWQzNDViYmI5MjYyZDE0Y2NkZTllNDIwMTE3OSIsImlhdCI6MTc3MDc1NDQ0MiwibmJmIjoxNzcwNzU0NDQyLCJleHAiOjE3NzA4NDA4NDIsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiNzU2ODA3NzEtYWJlMy00YTI1LTg1ODctMjY0NTg1OWFmMmFlIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.HVN4OAoeA12OrN0Dr6gnrqKciODFhmAN7Svm0uDKGaePMvNMKlePWCPZyMH6X2P1RHgmJjktj0kBhJa2oxp3c9a3PlpXCZw_1RdAAHQjE_HJAAvj_D7alR_OuUtQYWA94m2m_96PXXcbob0IAANHJHuYW5vI3m1YMjAz6or344byk11QPZm2VI98ONYjOQ-8hb8ayJFDe03xyp_yhxhwcp2NlwuA_K1qsnfw9l1m3GHcZbrYA-MOUtqi_IeTSSjrH3RYoV6vsbLZP4eVekAbM2nsswU-gKozeouALGXdJGmnx73LAuor6fmc_ixws9y8sQ4wrnHX4Ur3E14kZ6oG3A' 
    
    url = f'https://{subdomain}.amocrm.ru/api/v4/account' # Базовый запрос информации об аккаунте
    headers = {
        'Authorization': f'Bearer {token.strip()}',
        'User-Agent': 'amoCRM-oAuth-client/1.0'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print(f'Статус: {response.status_code}')
        print(f'Ответ: {response.text}')

# asyncio.run(check_token())
