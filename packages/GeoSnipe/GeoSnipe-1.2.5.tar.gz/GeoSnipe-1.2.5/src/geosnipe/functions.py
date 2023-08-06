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

import asyncio
from time import time
from random import choice
from typing import Optional
from string import ascii_letters

from paramiko.ssh_exception import SSHException

from geosnipe.ssh import Client
from geosnipe.github import GitHub
from geosnipe.auth.mojang import Mojang
from geosnipe.progressbar import ProgressBar
from geosnipe.auth.microsoft import Microsoft
from geosnipe import logger as logging, __version__
from geosnipe.constants import SKIN, MOJANG, MICROSOFT


async def check_arguments(username: str, drop_time: int,
                          offset: int, bearer: Optional[str] = None,
                          combo: Optional[str] = None, auth: str = "mojang") -> Optional[str]:
    if bearer is None and combo is None:
        return "Must have either the `bearer` or `combo` argument."
    elif auth.lower() not in ("mojang", "microsoft"):
        return "The argument `auth` must be mojang or microsoft."
    elif drop_time - (offset / 1000) < time():
        return "Username has already dropped."
    elif combo is not None:
        if combo.count(":") != 1:
            return "Combo is not valid."
    elif len(username) < 3:
        return "This username is too short."


async def login(email: str, password: str, auth: str) -> Optional[str]:
    if auth == "microsoft":
        return await Microsoft.login(email, password)
    else:
        return await Mojang.login(email, password)


async def send_request(reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
                       data: bytes, delay: float) -> tuple[str, float]:
    await asyncio.sleep(delay)
    writer.write(data)
    await writer.drain()
    return str((await reader.read(12)), "utf-8")[9:12], time()


async def change_skin(access_token: str) -> str:
    reader, writer = await asyncio.open_connection("api.minecraftservices.com", 443, ssl=True)
    writer.write(SKIN % bytes(access_token, "utf-8"))
    await writer.drain()
    return str((await reader.read(12)), "utf-8")[9:12]


async def create_payload(username: str, bearer: str, auth: str = "mojang") -> bytes:
    if auth == "microsoft":
        content = "{\"profileName\": \"%s\"}" % username
        return MICROSOFT % (bytes(bearer, "utf-8"), bytes(str(len(content)), "utf-8"), bytes(content, "utf-8"))
    else:
        return MOJANG % (bytes(username, "utf-8"), bytes(bearer, "utf-8"))


async def snipe(username: str, drop_time: int,
                offset: int, bearer: Optional[str] = None,
                combo: Optional[str] = None, auth: str = "mojang") -> Optional[tuple]:
    args_check = await check_arguments(username, drop_time, offset, bearer, combo, auth)

    if args_check is not None:
        logging.error(args_check)
        return None

    if bearer is None:
        logging.info(f"Authenticating using `{auth}`.")

        spl = combo.split(":")
        bearer = await login(spl[0], spl[1], auth)

        if bearer is None:
            logging.info(f"Failed to authenticate using `{auth}`.")
            return None

    payload = await create_payload(username, bearer, auth)
    del spl, auth, combo

    logging.info(f"Sniping `{username}` at {drop_time - offset / 1000}.")

    await asyncio.sleep(drop_time - time() - 3)

    try:
        logging.info("Opening connections...")
        connections = await asyncio.gather(
            *[asyncio.open_connection("api.minecraftservices.com", 443, ssl=True) for _ in range(3)]
        )
    except ConnectionError:
        logging.error("Failed to open connections.")
        return

    await asyncio.sleep(drop_time - time() - offset / 1000)

    try:
        results = await asyncio.gather(
            *[send_request(connections[i][0], connections[i][1], payload, 0.001 * i) for i in range(len(connections))]
        )
    except ConnectionError:
        logging.error("Failed to change username.")
        return

    try:
        for conn in connections:
            conn[1].close()
    except ConnectionError:
        logging.error("Failed to close socket.")

    for result in results:
        logging.info(f"Received {result[0]} at {result[1]}")

        if result[0] == "200":
            logging.info("Changing skin...")

            try:
                await change_skin(bearer)
            except ConnectionError:
                logging.error("Failed to change skin.")

    return results


async def offset(tests: int = 5) -> Optional[float]:
    if tests < 1:
        logging.error("The argument `tests` cannot be less than or equal to 0.")
        return None

    data = bytes(
        f"PUT /minecraft/profile/name/{''.join([choice(ascii_letters) for _ in range(5)])} HTTP/1.1\r\n"
        f"Host: api.minecraftservices.com\r\n"
        f"Content-Type: application/json\r\n"
        f"Authorization: Bearer {''.join([choice(ascii_letters) for _ in range(250)])}\r\n\r\n",
        "utf-8"
    )
    times = []

    logging.info("Finding offset...")

    progress_bar = ProgressBar(tests)

    try:
        for _ in range(tests):
            conn = await asyncio.open_connection("api.minecraftservices.com", 443, ssl=True)
            start = time()
            conn[1].write(data)
            await conn[1].drain()
            await conn[0].read(12)
            end = time()
            times.append(end - start)
            progress_bar.update()
    except ConnectionError:
        logging.error("Failed to find offset.")
        return

    logging.info(f"Your offset is {round(sum(times) / 10 * 1000, 2)} ms.")


async def get_version():
    logging.info(f"You are using GeoSnipe {__version__}")


async def sshsnipe(vps: str, username: str, drop_time: int,
                    offset: int, bearer: Optional[str] = None,
                    combo: Optional[str] = None, auth: str = "mojang") -> None:
    args_check = await check_arguments(username, drop_time, offset, bearer, combo, auth)

    if args_check is not None:
        logging.error(args_check)
        return None

    if not vps.count(":") == 2:
        logging.error("Invalid VPS format.")
    elif not vps.count("@") == 1:
        logging.error("Invalid VPS format.")

    client = Client()
    spl = vps.replace("@", ":").split(":")

    try:
        logging.info("Connecting to VPS...")
        client.connect(spl[2], int(spl[3]), spl[0], spl[1])
    except SSHException:
        logging.info("Error logging into VPS.")

    cmd = [f"wine geosnipe snipe {username} {drop_time} {offset}"]

    if bearer is not None:
        cmd.append(f"--bearer={bearer}")
    elif combo is not None:
        cmd.append(f"--combo={combo}")
        cmd.append(f"--auth={auth}")

    try:
        logging.info("Executing command...\n")
        stdin, stdout, stderr = client.exec_command(" ".join(cmd), get_pty=True)
    except SSHException:
        logging.info("Error executing command. Make sure GeoSnipe is installed on the VPS.")
        return None

    try:
        while True:
            line = stdout.readline()
            print(line[:len(line) - 2])

            if stdout.channel.exit_status_ready():
                line = stdout.readline()
                print(line[:len(line) - 2])
                break
            else:
                await asyncio.sleep(0.05)
    except SSHException:
        logging.info("Error executing command.")
        return None

    client.close()


async def sshoffset(vps: str, tests: int = 5) -> None:
    if tests < 1:
        logging.error("The argument `tests` cannot be less than or equal to 0.")
        return None

    if not vps.count(":") == 2:
        logging.error("Invalid VPS format.")
    elif not vps.count("@") == 1:
        logging.error("Invalid VPS format.")

    client = Client()
    spl = vps.replace("@", ":").split(":")

    try:
        logging.info("Connecting to VPS...")
        client.connect(spl[2], int(spl[3]), spl[0], spl[1])
    except SSHException:
        logging.info("Error logging into VPS.")

    try:
        logging.info("Executing command...\n")
        stdin, stdout, stderr = client.exec_command(f"wine geosnipe offset --tests={tests}", get_pty=True)
    except SSHException:
        logging.info("Error executing command. Make sure GeoSnipe is installed on the VPS.")
        return None

    try:
        while True:
            line = stdout.readline()
            print(line[:len(line) - 2])

            if stdout.channel.exit_status_ready():
                line = stdout.readline()
                print(line[:len(line) - 2])
                break
            else:
                await asyncio.sleep(0.05)
    except SSHException:
        logging.info("Error executing command.")
        return None

    client.close()


async def sshinstall(vps: str) -> None:
    if not vps.count(":") == 2:
        logging.error("Invalid VPS format.")
    elif not vps.count("@") == 1:
        logging.error("Invalid VPS format.")

    client = Client()
    spl = vps.replace("@", ":").split(":")

    logging.info("Finding latest download...")
    link = await GitHub.latest_download()

    if link is None:
        logging.error("Could not find latest download.")
        return

    logging.info("Found latest download.")

    try:
        logging.info("Connecting to VPS...")
        client.connect(spl[2], int(spl[3]), spl[0], spl[1])
    except SSHException:
        logging.info("Error logging into VPS.")

    commands = (
        "rm -f geosnipe.exe", "sudo dpkg --add-architecture i386",
        "sudo apt update", "sudo apt install -f wine64",
        "sudo apt install -f wine32", f"wget {link}"
    )

    for command in commands:
        try:
            logging.info(f"Executing command `{command}`...\n")
            stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        except SSHException:
            logging.info("Error executing command. Make sure user has admin permissions.")
            return None

        try:
            while True:
                line = stdout.readline()
                print(line[:len(line) - 2])

                if stdout.channel.exit_status_ready():
                    line = stdout.readline()
                    print(line[:len(line) - 2])
                    break
                else:
                    await asyncio.sleep(0.05)
        except SSHException:
            logging.info("Error executing command.")
            return None
