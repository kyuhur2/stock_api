import os
import aiosqlite
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DatabaseOperations(ABC):
    @abstractmethod
    async def execute(self, query: str, params: Dict[str, Any]) -> int:
        pass


class SQLiteDatabaseOperations(DatabaseOperations):
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def execute(self, query: str, params: Dict[str, Any]) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(query, params)
            await db.commit()
            return cursor.rowcount


async def initialize_database(
    database_operations: DatabaseOperations, schema_path: os.path
) -> None:
    with open(schema_path, "r") as schema_file:
        schema_sql = schema_file.read()
    await database_operations.execute(schema_sql, {})


async def store_stock_data(
    database_operations: DatabaseOperations, records: List[Dict[str, Any]]
) -> None:
    query = """
        INSERT OR IGNORE INTO financial_data (symbol, date, open_price, close_price, volume)
        VALUES (:symbol, :date, :open_price, :close_price, :volume)
    """
    for record in records:
        rowcount = await database_operations.execute(query, record)
        print(f"Inserted {rowcount} row(s) for {record['symbol']} on {record['date']}")
