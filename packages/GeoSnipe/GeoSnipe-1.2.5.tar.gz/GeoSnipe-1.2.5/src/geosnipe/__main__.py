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

import os
import sys
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from geosnipe import logger as logging
from geosnipe.argparser import parse_args
from geosnipe.functions import offset, snipe, sshoffset, sshsnipe, get_version, sshinstall


def initialize():
    os.system("")
    asyncio.set_event_loop(asyncio.ProactorEventLoop())


def main():
    initialize()

    loop = asyncio.get_event_loop()
    args = parse_args()

    if args.service_command is None:
        logging.error("No command selected. Use `geosnipe --help` for a list of commands.")
    elif args.service_command == "offset":
        loop.run_until_complete(offset(args.tests))
    elif args.service_command == "snipe":
        loop.run_until_complete(snipe(args.username, args.drop_time, args.offset, args.bearer, args.combo, args.auth))
    elif args.service_command == "sshoffset":
        loop.run_until_complete(sshoffset(args.vps, args.tests))
    elif args.service_command == "sshsnipe":
        loop.run_until_complete(
            sshsnipe(args.vps, args.username, args.drop_time, args.offset, args.bearer, args.combo, args.auth)
        )
    elif args.service_command == "sshinstall":
        loop.run_until_complete(sshinstall(args.vps))
    elif args.service_command == "version":
        loop.run_until_complete(get_version())


if __name__ == "__main__":
    main()
