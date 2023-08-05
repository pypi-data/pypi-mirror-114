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
