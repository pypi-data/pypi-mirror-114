import re
import asyncio

from geosnipe.constants import USER_AGENT


class GitHub(object):
    @staticmethod
    async def latest_download():
        try:
            reader, writer = await asyncio.open_connection("api.github.com", 443, ssl=True)
            writer.write(b"""GET /repos/Geographs/GeoSnipe/releases/latest HTTP/1.1\r\nHost: api.github.com\r
User-Agent: %b\r\n\r\n""" % USER_AGENT)
            await writer.drain()

            return re.findall("\"browser_download_url\": \"(.*?)\"", str((await reader.read(1024)), "utf-8"))[0]
        except IndexError:
            return None
        except ConnectionError:
            return None
