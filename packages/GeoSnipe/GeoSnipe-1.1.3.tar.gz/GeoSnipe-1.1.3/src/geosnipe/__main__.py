import os
import sys

from fire import Fire

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from geosnipe.sniper import Sniper


def main():
    Fire(Sniper)


if __name__ == "__main__":
    main()
