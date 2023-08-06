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

SKIN = b"""POST /minecraft/profile/skins HTTP/1.1\r
Host: api.minecraftservices.com\r
Authorization: Bearer %b\r
Content-Type: application/json\r
Content-Length: 99\r\n\r
{"variant": "classic", "url": "https://raw.githubusercontent.com/Geographs/GeoSnipe/main/skin.png"}"""

MOJANG = b"""PUT /minecraft/profile/name/%b HTTP/1.1\r
Host: api.minecraftservices.com\r
Authorization: Bearer %b\r
Content-Type: application/json\r\n\r\n"""

MICROSOFT = b"""POST /minecraft/profile HTTP/1.1\r
Host: api.minecraftservices.com\r
Authorization: Bearer %b\r
Content-Type: application/json
Content-Length: %b\r\n\r\n%b"""

PAYLOAD = b"""POST /authenticate HTTP/1.1\r
Host: authserver.mojang.com\r
Accept: application/json\r
Content-Type: application/json\r
Content-Length: %b\r
User-Agent: %b\r\n\r\n%b"""

USER_AGENT = b"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 " \
             b"Safari/537.36"
