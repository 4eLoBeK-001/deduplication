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
    
asyncio.run(resresh_amo_token('def50200628b85b2fea7318900b35bf8ed07d8044cdce89c17e7b2e2965a52e00f6e7e40a0614f71f5c069a1ecb244b814156fe79281d15f02476ccd9ad31dd515c11e87c8a648d1522aad5f5834300425dcfea0cc957941a63c9d2bcabe7265922dbe79d78989ed790e5f48bea5a21cbf1a5570638a1d32fee898c5c4b5f6334c7eb2ddd2948240f0b331e0baf702010dc443ee6589f0926d733c2e8eec21dc99cea3b6735c6e05682378581e2172d720d6bf7a9c956d3d198255d2287408ad8361ff3265003425e168c1198cfa902b9a3149000ee1920708f30201de782cd324b8ab07eb21a62de1059d70b146955402ca8cc4ba865f324ab4140b6cc10e938fa71aa0277cdce9ab59703110289662fcffeb0cdc98c10f7032b11846ce37f79b1c0b39f3982cafb6cc249de506a7ce13b2c839c42ab9e0f59af5cf7bb2f1e90b788cbad4311b7ca10c01b52436ae063144aa5c72064efe6277092706086d937fbfb025fcdb22ffeb204aafac271170685f5788e43862aa1092cd91086417cc27c271690b29ced3efe21e7531a2efecb8f11d88a818473339712821aa8f2d7db7e5a9193bc4f1a0a570d653d783bceb3f41a201833c2fc1bbad86002567feaa6b4af681db00300ccf92ce755fe352a5ddb95c448207f54d89b52c9dc289c476a0278f5ae9558f4193b7fb3794e9'))


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
