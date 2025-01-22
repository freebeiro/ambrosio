import logging
from core.interfaces import ILogger

# Concrete implementation of ILogger following Dependency Inversion Principle
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
        """Log error message with exception context if available"""
        if hasattr(message, 'exc_info') and message.exc_info:
            self.logger.exception(message)
        else:
            self.logger.error(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

# Application-wide logger instance adhering to Interface Segregation Principle
logger: ILogger = ProductionLogger()
