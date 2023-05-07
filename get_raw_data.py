import asyncio
import os
from section1.config import load_configuration
from section1.database import SQLiteDatabaseOperations, initialize_database, store_stock_data
from section1.data_provider import AlphaVantageProvider
from section1.logger import create_logger


if __name__ == "__main__":
    # init paths, config, database, data_provider
    db_path = os.path.join(os.path.dirname(__file__), "financial_data.db")
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    config = load_configuration()
    sqlite_database_operations = SQLiteDatabaseOperations(db_path)
    stock_data_provider = AlphaVantageProvider(
        config.alpha_vantage_api_key, config.url_template, config.number_of_days
    )
    logger = create_logger(config.log_path)

    # run database ops
    asyncio.run(initialize_database(sqlite_database_operations, schema_path))

    # get and store stock data
    symbols = ["IBM", "AAPL"]
    for symbol in symbols:
        records = stock_data_provider.get_stock_data(symbol)
        asyncio.run(store_stock_data(sqlite_database_operations, records))
