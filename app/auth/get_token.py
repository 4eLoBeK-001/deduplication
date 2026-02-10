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
    
# asyncio.run(resresh_amo_token('def50200b41c3881b94932531df744da33feb5af5d9e69240d264edc54683eb2ffffc46422377dd16db0dfdd0500e3918ab8ddd80af6dc19a00514e39abee0d3d3a5f78972deb86351e34af4f7ed7f5104997e19a63d4e51ff7f39cd777e1e7ee54407a38c4a060e04bac41f115f217a368cd14c35a8c7e8962f726994d9c6999e1b9d6bbcf21da1a4586642969a94f9c8727271013e5c68a8d0e97c8de3cf6884774efde95b01c25ba8aa72f88b4f71c6120c91066c9cb4a74a4f6e617ed514e281f07986d647c0a9e4ec923f3449354923714f3b6da750c0d769a97c5a020f8193af6faf4cd7ab4d0c5a37f07f4b618f7c178e2be94783e7d847a76a4b165fd51c62d05d797f084beaab04983e8bd5c4e7d8a7fdd635de1a9cb13164f0a38c14576b38d37665bad6ab31499b380a9c312a3720a7077e85f75010a366d04bbc2e915de60a24bdb6086ed7ff1e6a901ca9a287a2615c4367e338bea5275bbe21c395546797b37335129162842cb2f18c91c6cd47a04fa215479d93ec9914d5d8d348f8ece817d20b3939f47066553d9ddfae7837c8253e90917b98076e556097341f2a27f9321e579c0e2aa66ac33829fbbed3200a6f142194bdb98d222beef0dd238e77d067ecd6f5528c374a7e59177d6dac5220623c02626c30e4b43efd36a8f6ca58b55554bdd24511976666'))


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

asyncio.run(check_token())
