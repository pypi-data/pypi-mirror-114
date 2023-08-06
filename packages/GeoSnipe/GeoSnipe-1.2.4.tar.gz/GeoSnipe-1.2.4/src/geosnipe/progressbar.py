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

from os import get_terminal_size


class ProgressBar(object):
    def __init__(self, total: int, symbols: tuple[str, str] = ("█", "░")) -> None:
        self.total = total
        self.symbols = symbols
        self.width = get_terminal_size().columns

        self.progress = 0
        print()
        self.print_progress_bar()

    def print_progress_bar(self):
        percentage = int(self.progress / self.total * 100)
        bar = self.symbols[0] * percentage + self.symbols[1] * (100 - percentage)
        msg = f"{percentage}% - [{bar}]"
        spaces = int((self.width - len(msg)) / 2)

        print(f"{' ' * spaces}{msg}", end="\r" if percentage != 100 else None)

        if percentage == 100:
            print()

    def update(self):
        if self.progress < self.total:
            self.progress += 1
            self.print_progress_bar()
