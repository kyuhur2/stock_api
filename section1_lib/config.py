import os
from dotenv import load_dotenv


class Configuration:
    def __init__(
        self,
        alpha_vantage_api_key: str,
        database_url: str,
        number_of_days: int,
        log_path: str,
        url_template: str,
    ):
        self.alpha_vantage_api_key = alpha_vantage_api_key
        self.database_url = database_url
        self.number_of_days = number_of_days
        self.log_path = log_path
        self.url_template = url_template


def load_configuration():
    load_dotenv()
    alpha_vantage_api_key: str = os.getenv("ALPHA_VANTAGE_API_KEY")
    database_url: str = (
        os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") else "sqlite:///./financial_data.db"
    )
    number_of_days: int = int(os.getenv("NUMBER_OF_DAYS")) if os.getenv("NUMBER_OF_DAYS") else 14
    log_path: str = os.getenv("LOG_PATH") if os.getenv("LOG_PATH") else "./logs/logs.log"
    url_template: str = (
        "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED"
        + "&symbol={symbol}&apikey={api_key}&outputsize={outputsize}"
    )

    return Configuration(
        alpha_vantage_api_key, database_url, number_of_days, log_path, url_template
    )
