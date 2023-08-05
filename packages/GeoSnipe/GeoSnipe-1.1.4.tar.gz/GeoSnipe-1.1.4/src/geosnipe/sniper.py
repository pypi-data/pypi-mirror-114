from typing import Optional

from geosnipe.functions import snipe, check_offset, get_version, ssh_snipe, ssh_offset


class Sniper(object):
    @staticmethod
    async def snipe(username: str, drop_time: int,
                    offset: int, bearer: Optional[str] = None,
                    combo: Optional[str] = None, auth: str = "mojang") -> Optional[tuple]:
        return await snipe(username, drop_time, offset, bearer, combo, auth)

    @staticmethod
    async def offset(tests: int = 5) -> Optional[float]:
        return await check_offset(tests)

    @staticmethod
    async def sshsnipe(vps: str, username: str, drop_time: int,
                       offset: int, bearer: Optional[str] = None,
                       combo: Optional[str] = None, auth: str = "mojang") -> None:
        await ssh_snipe(vps, username, drop_time, offset, bearer, combo, auth)

    @staticmethod
    async def sshoffset(vps: str, tests: int = 5) -> None:
        await ssh_offset(vps, tests)

    @staticmethod
    async def version() -> None:
        await get_version()
