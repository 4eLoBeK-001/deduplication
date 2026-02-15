import httpx
from app.services.utils import clean_phone
from app.core.logger import logger


ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjI5NGI5YzQ5YjgzYTZlOGMyODA2NDU5ZDZlYjFmMDJhYjdhNzRiNmFiZjZkZDQ4OTA2MDdiODQ5MDUwZWVjMDcyMmFhMTBkNWRlNjBiNjRjIn0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiIyOTRiOWM0OWI4M2E2ZThjMjgwNjQ1OWQ2ZWIxZjAyYWI3YTc0YjZhYmY2ZGQ0ODkwNjA3Yjg0OTA1MGVlYzA3MjJhYTEwZDVkZTYwYjY0YyIsImlhdCI6MTc3MTA3NzA5NiwibmJmIjoxNzcxMDc3MDk2LCJleHAiOjE3NzExNjM0OTYsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiZWVmMDYxODktMDE5OC00NGMxLWE4NTAtNGQ4YWViYjNkM2VjIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.V8qHkj4VQv0PMCOTYDeSfp7OLzh6qrDVCPrCEzSGBRf-r6IUHpSrmfe2pTIyu_4KBvdcHwl5bpgC0QCOQ7kQUOgu-Zcpf7P4HXoF71Iu4DuO1bZTRfmcf6zzP4-N8XiJHSOf1cs5Erp4U3GBCVJ0aXLaWBvxfgNpZ2Cc1m3kJNzYFfjGAlYd1SnKUzKMXe0c0sZmH36GTG1UEHgJPjZLPLZdBRU3Bhu_8x5NbCPwISx_3X0xTjcPsU4quuWDV8yObIzx_4sJ6KhMPgg2LB03t1__cY8Hj7YL4sSm4EAMmXggj5v3obXMAddp8kHGQFsO_lSQm-PIKin_YlzlsXEiBQ'

class AmoCRMClient:
    def __init__(self, subdomain: str, token: str = ACCESS_TOKEN):
        self.subdomain = subdomain
        self.base_url = f'https://{subdomain}.amocrm.ru/api/v4'
        self.token = token
        self.client = httpx.AsyncClient()

    def _headers(self, json_type: bool = False):
        headers = {'Authorization': f'Bearer {self.token}'}
        if json_type:
            headers['Content-Type'] = 'application/json'
        return headers
