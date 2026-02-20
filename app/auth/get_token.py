import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

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
    
asyncio.run(resresh_amo_token('def50200f602fb854843e202f9e529889d432da4f35b70bb34851300f1afe3ef07dfbea985c0cf4f359894e9e8c2876f638bdcca1b386066822e5214a05977c537d69e35ab9857287a25a0ba505f6abef5452208523c001e312aa406bd65cc6d27d21f1157b6e859e45beac4b05ef53b285ecddeaf5630f652eaa4f6a50db01483890b2ccedc7f60670c9a3c3d3be38b0e19e01c68744d475e9e064c10c6085f1e1eea6454dfc54f960f3b108a1617bc98eb1116fdd6bc0413f5d5f61069a1f6b82654d1d80f5d3ee48a0199317460f5ceae26bba72ec2726292db55f2f2a194acae1f73b9d7f802de66e385310672784a0266621246b98e6f5390f90943cf6d4f33a6f3d180c5325ea4ba89ddfd230bc9fc2b31dbf304f98e8ba1bd8efa53a489593c20c4823b8123034f87b096530906761d70f798c0b759daf44ed48418984d694ead78a4bf31acf6c69d1970d39193389c98e94d75c20a19abcc685b6202cd076e6f17a184214a124e74f039e89734aef154fbc0be01309d4dd5f50ead4cdf0f2a225e70b613d56e28dded82733aae5d79777130884a56b16c6b6b162eb96daeb16e70ba9c3fd572129aca316866792a055979b5c6abd1e0ee0cbc47df24f3120c03a91bc506bc7a4f1ebcdc50c9e1d2eb1b2785b49ec94bba3384f17b40ff14d55dfca9c36fab1adc4cdcbc'))


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
