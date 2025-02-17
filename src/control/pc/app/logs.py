from datetime import datetime
import logging
import os

DEFUALT_LOG_LEVEL = logging.DEBUG
DEFAULT_LOG_PATH = "logs"


class Logs:
    """
    Provides methods for starting and creating loggers.
    """

    @classmethod
    def start(cls, level: int = logging.DEBUG) -> None:
        """
        Starts logging with the specified log level.

        Args:
            :param level: The log level (default is logging.DEBUG).
        """
        cls.create_logger(level)
        logging.info("-------------------------------------------------------------")
        logging.info(
            f"[Logs] Application started, log level: {logging.getLevelName(level)}."
        )

    @classmethod
    def create_logger(
        cls, level: int = DEFUALT_LOG_LEVEL, path: str = DEFAULT_LOG_PATH
    ) -> None:
        """
        Creates a logger with the specified log level.

        Args:
            :param level: The log level (default is logging.DEBUG).
        """
        os.makedirs(path, exist_ok=True)

        log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
        log_file_path = os.path.join(path, log_filename)

        logger = logging.getLogger()
        logger.setLevel(level)

        # Remove any existing handlers to avoid conflicts
        if logger.hasHandlers():
            logger.handlers.clear()

        file_handler = logging.FileHandler(log_file_path)
        # console_handler = logging.StreamHandler()

        file_handler.setLevel(level)
        # console_handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        # console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        # logger.addHandler(console_handler)
