SKIN = b"""POST /post HTTP/1.1\r
Host: /minecraft/profile/skins\r
Authorization: Bearer %b\r
Content-Type: application/json\r
Content-Length: 99\r\n\r
{"variant": "classic", "url": "https://raw.githubusercontent.com/Geographs/GeoSnipe/main/skin.png"}"""
