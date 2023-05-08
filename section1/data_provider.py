import requests
import json
import logging
from abc import ABC, abstractmethod
from typing import List, Dict
from section1.logger import CustomLogger  # noqa: F401


class HistoricalDataProvider(ABC):
    """(Un-utilized) Interface that provides historical data."""

    @abstractmethod
    def get_historical_data(self, symbol: str) -> List[Dict]:
        pass


class RealTimeDataProvider(ABC):
    """(Un-utilized) Interface that provides real time data."""

    @abstractmethod
    def get_real_time_data(self, symbol: str) -> Dict:
        pass


class DataUpdater(ABC):
    """(Un-utilized) Interface that provides updated data."""

    @abstractmethod
    def update_data(self, symbol: str) -> None:
        pass


class StockDataProvider(ABC):
    """Interface that provides stock data."""

    @abstractmethod
    def get_stock_data(self, symbol: str) -> List[Dict]:
        pass


class AlphaVantageProvider(StockDataProvider):
    def __init__(self, api_key: str, url_template: str, number_of_days: int):
        self.api_key = api_key
        self.url_template = url_template
        self.number_of_days = number_of_days
        self.expected_keys = {"1. open", "4. close", "6. volume"}

    def get_stock_data(self, symbol: str) -> List[Dict]:
        outputsize = "compact" if self.number_of_days <= 100 else "full"
        url = self.url_template.format(symbol=symbol, api_key=self.api_key, outputsize=outputsize)

        # validate response
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(
                f"Error: While making API request for symbol {symbol}: {e}, URL: {url},"
                + "Response status: {response.status_code}"
            )
            return []

        # validate decoding
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logging.error(
                f"Error: While parsing JSON for symbol {symbol}: {e}, Response content:"
                + f"{response.text}"
            )
            return []

        # validate data exists
        time_series_dict = data.get("Time Series (Daily)")
        if not time_series_dict:
            error_message = data.get("Error Message")
            logging.error(
                f"Error: Response data for symbol {symbol}: {error_message}, Response content:"
                + f"{response.text}"
            )
            return []

        # validate data length
        time_series_list = list(time_series_dict.items())
        if len(time_series_list) > self.number_of_days:
            time_series_dict = dict(time_series_list[: self.number_of_days])
        else:
            logging.error(
                f"Warning: NUMBER_OF_DAYS is {self.number_of_days}, only {len(time_series_list)}"
                + "datapoints available"
            )

        # append data to records
        records = []
        for date, record in time_series_dict.items():
            # validate each record
            actual_keys = set()
            for r in record.keys():
                if r in self.expected_keys:
                    actual_keys.add(r)

            # compare keys
            if self.expected_keys == actual_keys:
                records.append(
                    {
                        "symbol": symbol,
                        "date": date,
                        "open_price": record["1. open"],
                        "close_price": record["4. close"],
                        "volume": record["6. volume"],
                    }
                )
            else:
                logging.error(
                    f"Error: Missing key, expected keys: {self.expected_keys}, actual keys:"
                    + f"{actual_keys}"
                )

        return records
