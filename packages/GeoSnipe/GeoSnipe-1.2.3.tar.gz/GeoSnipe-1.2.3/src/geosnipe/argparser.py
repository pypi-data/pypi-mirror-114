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

import argparse


main_parser = argparse.ArgumentParser()
service_subparsers = main_parser.add_subparsers(title="GeoSnipe Commands", dest="service_command")


def create_offset_parser() -> None:
    offset_parser = argparse.ArgumentParser(add_help=False)
    offset_parser.add_argument(
        "--tests", "-t", type=int, help="Amount of times you want to test | DEFAULT: 5", default=5
    )
    service_subparsers.add_parser("offset", help="Find your offset", parents=[offset_parser])


def create_sniper_parser() -> None:
    snipe_parser = argparse.ArgumentParser(add_help=False)
    snipe_parser.add_argument("username", metavar="username", type=str, help="Username you want to snipe")
    snipe_parser.add_argument("drop_time", metavar="drop_time", type=float, help="What time the username drops")
    snipe_parser.add_argument("offset", metavar="offset", type=float, help="The offset of the snipe")
    snipe_parser.add_argument(
        "--bearer", "-b", type=str, help="The bearer token of the account | DEFAULT: None", default=None
    )
    snipe_parser.add_argument(
        "--combo", "-c", type=str, help="The EMAIL:PASSWORD of the account | DEFAULT: None", default=None
    )
    snipe_parser.add_argument(
        "--auth", "-a", type=str,
        help="Authentication you want to use (mojang or microsoft) | DEFAULT: mojang", default="mojang"
    )
    service_subparsers.add_parser("snipe", help="Snipe a username", parents=[snipe_parser])


def create_sshoffset_parser() -> None:
    sshoffset_parser = argparse.ArgumentParser(add_help=False)
    sshoffset_parser.add_argument("vps", metavar="vps", type=str, help="The VPS you want to use")
    sshoffset_parser.add_argument(
        "--tests", "-b", type=str, help="Amount of times you want to test | DEFAULT: None", default=None
    )
    service_subparsers.add_parser("sshoffset", help="Find offset on VPS", parents=[sshoffset_parser])


def create_sshsniper_parser() -> None:
    sshsnipe_parser = argparse.ArgumentParser(add_help=False)
    sshsnipe_parser.add_argument("vps", metavar="vps", type=str, help="The VPS you want to use")
    sshsnipe_parser.add_argument("username", metavar="username", type=str, help="Username you want to snipe")
    sshsnipe_parser.add_argument("drop_time", metavar="drop_time", type=float, help="What time the username drops")
    sshsnipe_parser.add_argument("offset", metavar="offset", type=float, help="The offset of the snipe")
    sshsnipe_parser.add_argument(
        "--bearer", "-b", type=str, help="The bearer token of the account | DEFAULT: None", default=None
    )
    sshsnipe_parser.add_argument(
        "--combo", "-c", type=str, help="The EMAIL:PASSWORD of the account | DEFAULT: None", default=None
    )
    sshsnipe_parser.add_argument(
        "--auth", "-a", type=str,
        help="Authentication you want to use (mojang or microsoft) | DEFAULT: mojang", default="mojang"
    )
    service_subparsers.add_parser("sshsnipe", help="Snipe a username on a VPS", parents=[sshsnipe_parser])


def create_sshinstall_parser() -> None:
    sshinstall_parser = argparse.ArgumentParser(add_help=False)
    sshinstall_parser.add_argument("vps", metavar="vps", type=str, help="The VPS you want to use")
    service_subparsers.add_parser("sshinstall", help="Install GeoSnipe on a VPS", parents=[sshinstall_parser])


def create_version_parser() -> None:
    version_parser = argparse.ArgumentParser(add_help=False)
    service_subparsers.add_parser("version", help="Check the version of GeoSnipe", parents=[version_parser])


def parse_args() -> argparse.Namespace:
    create_offset_parser()
    create_sniper_parser()
    create_sshoffset_parser()
    create_sshsniper_parser()
    create_sshinstall_parser()
    create_version_parser()
    return main_parser.parse_args()
