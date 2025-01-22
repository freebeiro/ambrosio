import logging
from core.interfaces import ILogger

class ProductionLogger(ILogger):
    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def __init__(self):
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )
        self.logger = logging.getLogger("ambrosio")

    def error(self, message: str) -> None:
        self.logger.error(message)

    def info(self, message: str) -> None:
        self.logger.info(message)
