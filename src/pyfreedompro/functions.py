import aiohttp
import asyncio
import async_timeout

FREEDOMPRO_URL = "https://api.freedompro.eu/api/freedompro/accessories"

async def get_list(apikey, httpsession):
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
    }
    try:
        with async_timeout.timeout(10000):
            resp = await httpsession.get(FREEDOMPRO_URL, headers=headers, ssl=False)
            status = resp.status

            if status == 200:
                devices = await resp.json()
                return {"state": True, "devices": devices}

            if status == 401:
                return {"state": False, "code": -201}

            return {"state": False, "code": -200}
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return {"state": False, "code": -200}

async def get_states(apikey, httpsession):
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
    }
    try:
        with async_timeout.timeout(10000):
            resp = await httpsession.get(f"{FREEDOMPRO_URL}/state", headers=headers, ssl=False)
            status = resp.status
            if status == 200:
                data = await resp.json()
                return data
            return []
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return []


async def put_state(apikey, uid, payload, httpsession):
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
    }
    try:
        with async_timeout.timeout(10000):
            resp = await httpsession.put(
                f"{FREEDOMPRO_URL}/{uid}/state", data=payload, headers=headers, ssl=False
            )
            status = resp.status
            if status == 200:
                data = await resp.json()
                if "state" in data:
                    return data["state"]
            return {}
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return {}
