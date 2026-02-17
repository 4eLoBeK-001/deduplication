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
    
asyncio.run(resresh_amo_token('def50200cc25f532fec0f562fb5a47da6bf1f7d5289f01a18f5c3666c62a4a349acd5889a1b53a351f83f3c58688209b095de00d2b7233b8fd327d312eaf05a90c83ce3b016d194432ec4d2e5e0322ae233cbf49e5fe04dc0c506a00a1d92afbe0a8002ae66cd58a3c88c1e7ff36edb353aa9f81b586618988534a5ff7d3e820cb86d682d7878b6732f7074d2088f04eea5edd7c942e65823d6754e6f80d6363b5994df5cc18eb17c26fc84e48cc2138d01768b60e18b5198d1482aa396f3af07abd4511d0ce4be708b75e9ab6fe6d9cbc879c10785197bf24f66aae037dd3df8b367a7e24b8abbb23a4cc6c00d542c854fbdc133e7d028311d67be960fe1f8b923fea113d339c61381b647bb9671b850552020c018cfab7906e213102588c97865fe725e80cb81f728733a0f0a28a394caf32cca8422622f174c0f5a0756285d32ce5b8c29211710c638ab8dce23d0f940ca4bc62b626f39a9433da6981bdc981699db114f1b063d3f3750aef985cd2f2dad8c0899678d091ee151a7c682729e458e8ceb861c8f05807cca664dfd7036eb81155a0a55c8653246cb71a3c679351bc13c450775e9d7dc7d2a8c1c324e303887fe33ade8fa23b7002c78bb099b7f68f13e92e2170a409bf70d83c1ad697527df4056e9d2fdc9d2862d4a914984d17914157aa6eefa7b7dc93d9b05f'))


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
