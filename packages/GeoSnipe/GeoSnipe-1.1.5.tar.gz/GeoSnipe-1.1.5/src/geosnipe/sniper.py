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
