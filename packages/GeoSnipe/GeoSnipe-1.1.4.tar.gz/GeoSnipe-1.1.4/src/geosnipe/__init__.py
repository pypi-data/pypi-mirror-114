import logging


__version__ = "v1.1.4"


class ColoredFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(
            self, f"[\u001b[36mGeoSnipe\u001b[0m] [%(levelname)s] %(message)s"
        )

        self.colors = {
            "WARNING": "\u001b[33m",
            "INFO": "\u001b[34;1m",
            "CRITICAL": "\u001b[31;1m",
            "ERROR": "\u001b[31m"
        }

    def format(self, record):
        record.levelname = self.colors[record.levelname] + record.levelname + "\u001b[0m"
        return logging.Formatter.format(self, record)


logger = logging.getLogger("main")
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)
