import asyncio
import httpx
import json
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("AMOCRM_CLIENT_ID")
CLIENT_SECRET = os.getenv("AMOCRM_CLIENT_SECRET")
SUBDOMAIN = os.getenv("AMOCRM_SUBDOMAIN")
REDIRECT_URL = os.getenv("AMOCRM_REDIRECT_URL")


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

asyncio.run(get_auth_token())
