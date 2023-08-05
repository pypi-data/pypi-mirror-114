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
