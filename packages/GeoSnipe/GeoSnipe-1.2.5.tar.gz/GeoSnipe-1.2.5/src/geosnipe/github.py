import re
import asyncio


class GitHub(object):
    @staticmethod
    async def latest_download():
        try:
            reader, writer = await asyncio.open_connection("api.github.com", 443, ssl=True)
            writer.write(b"""GET /repos/Geographs/GeoSnipe/releases/latest HTTP/1.1\r\nHost: api.github.com\r
User-Agent: GeoSnipe\r\n\r\n""")
            await writer.drain()
            data = b""

            while True:
                data += await reader.read(1024)
                reader.feed_eof()
                if reader.at_eof():
                    break

            text = str(data, "utf-8")
            tag = re.findall("\"tag_name\":\"(.*?)\"", text)[0]
            return f"https://github.com/Geographs/GeoSnipe/releases/download/{tag}/geosnipe.exe"
        except IndexError:
            return None
        except ConnectionError:
            return None
