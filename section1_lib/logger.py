import os
import logging


class CustomLogger:
    def __init__(self, log_file_path: str):
        if not os.path.exists(os.path.dirname(log_file_path)):
            os.makedirs(os.path.dirname(log_file_path))

        logging.basicConfig(
            filename=log_file_path,
            level=logging.DEBUG,  # Set the lowest level you want to log
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def log(self, level: int, message: str) -> None:
        logging.log(level, message)

    def error(self, message: str) -> None:
        self.log(logging.ERROR, message)

    def warning(self, message: str) -> None:
        self.log(logging.WARNING, message)

    def info(self, message: str) -> None:
        self.log(logging.INFO, message)

    def debug(self, message: str) -> None:
        self.log(logging.DEBUG, message)


def create_logger(log_file_path: str) -> CustomLogger:
    return CustomLogger(log_file_path)
