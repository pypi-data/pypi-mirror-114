# MIT License
#
# Copyright (c) 2021 Geographs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import asyncio
import traceback
from uuid import uuid4
from json import JSONDecodeError, dumps

from geosnipe.constants import PAYLOAD, USER_AGENT


class Mojang(object):
    @staticmethod
    async def login(email: str, password: str):
        data = dumps({
            "agent": {
                "name": "Minecraft",
                "version": 1
            },
            "username": email,
            "password": password,
            "clientToken": str(uuid4()),
            "requestUser": True
        })

        payload = PAYLOAD % (bytes(str(len(data)), "utf-8"), USER_AGENT, bytes(data, "utf-8"))

        try:
            reader, writer = await asyncio.open_connection("authserver.mojang.com", 443, ssl=True)
            writer.write(payload)
            await writer.drain()
            text = str(await reader.read(1024), "utf-8")
            writer.close()
            return re.findall("\"accessToken\":\"(.*?)\",", text)[0]
        except KeyError:
            traceback.print_exc()
            return None
        except ConnectionError:
            traceback.print_exc()
            return None
        except JSONDecodeError:
            traceback.print_exc()
            return None
        except IndexError:
            traceback.print_exc()
            return None
