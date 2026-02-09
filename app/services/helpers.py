import asyncio
from pprint import pprint
import re
import httpx


def clean_phone(phone: str) -> str:
    return re.sub(r'\D', '', phone)


async def find_contact_by_phone(phone: str, subdomain: str):
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImFmODQ3ZTk5MjQzMzBmMTg4NDk0Y2E2YmRmMzc3MmQ1YmRhODI1ZjUxZDQ5YzczODNmYTNjYTg2ZGYwMjhiODQ5MTUzZWRhZDMzM2Q2NGEzIn0.eyJhdWQiOiIxYTMwYTA4ZS04MzhjLTRiYWItYTczYy0wMTkyNTIxOTI3YWEiLCJqdGkiOiJhZjg0N2U5OTI0MzMwZjE4ODQ5NGNhNmJkZjM3NzJkNWJkYTgyNWY1MWQ0OWM3MzgzZmEzY2E4NmRmMDI4Yjg0OTE1M2VkYWQzMzNkNjRhMyIsImlhdCI6MTc3MDY0NzI4NiwibmJmIjoxNzcwNjQ3Mjg2LCJleHAiOjE3NzA3MzM2ODYsInN1YiI6IjEzNDg2MDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyODk0NDkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiZDllZjc5YzUtMDgyZC00NjI2LTliOGYtMzA2ZTAwMzJhNTQ2IiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.LLwMkNMagNofruW7Hfo43xJqyTyBttENONgXSkJ1i1pCPI1m4SXSkx71f3Oj6RckAOju9fyffGH0OpDgK_97CgG6Kc1wmmQlPvjBPcqxQKqvLCN_X23SYBhPJzfx_uBCaqUBJaHVpPiUWSk8-HY5ES67UnXxdvPb1ct3rKoLJbYm4L0tYgDm5ksuJKmlzEL1q85attJ3hHSQWAQTYVmPtIMjw6dHoPJheyG-4lAPTa-AAJOyuzOGCXy4wFF0HFK5xNS4VJV3zP_gqaqiNTmJI2WS9uCleM9U7VCcqtXmKOLc026o7e2J0seZoOneMy_YCoqVxidIcRBatBjdESWaAw'
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'query': f'{phone}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

            
        if response.status_code == 200:
            contacts = response.json().get("_embedded", {}).get("contacts", [])
            return contacts
        return []
    
    
# asyncio.run(all_contacts('kostantinef'))