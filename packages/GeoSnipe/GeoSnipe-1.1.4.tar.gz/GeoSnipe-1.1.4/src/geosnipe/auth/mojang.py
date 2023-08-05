from uuid import uuid4
from json import JSONDecodeError

from aiohttp import ClientSession


class Mojang(object):
    @staticmethod
    async def login(email: str, password: str):
        payload = {
            "agent": {
                "name": "Minecraft",
                "version": 1
            },
            "username": email,
            "password": password,
            "clientToken": str(uuid4()),
            "requestUser": True
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.164 Safari/537.36 "
        }
        try:
            async with ClientSession() as session:
                response = await session.post(
                    "https://authserver.mojang.com/authenticate", json=payload, headers=headers
                )
                return (await response.json())["accessToken"]
        except KeyError:
            return None
        except ConnectionError:
            return None
        except JSONDecodeError:
            return None
