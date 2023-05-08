import aiosqlite
import re
import os
import time
import datetime
from typing import Optional, List, Tuple
from financial.models import PaginationData, FinancialData, Statistics
from fastapi import HTTPException, Request


BASE_URL = os.path.join(os.path.dirname(__file__), "..")
DATABASE_URL = os.path.join(BASE_URL, "financial_data.db")
RATE_LIMIT_REQUESTS = 120
RATE_LIMIT_TIME = 60


def validate_date_symbol_inputs(start_date: str, end_date: str, symbol: str) -> None:
    # check start_date, end_date format
    try:
        if start_date:
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD format.")

    # check symbol length is not longer than 5, assuming no options
    # https://www.quora.com/Whats-the-shortest-and-the-longest-that-a-companys-ticker-can-be-on-a-stock-market-exchange
    if symbol and len(symbol) > 5:
        raise HTTPException(
            status_code=400, detail="Invalid symbol. Maximum length is 10 characters."
        )


def validate_page_limit_inputs(page: str, limit: str) -> Tuple[int, int]:
    # check page and limit are integers and convert
    if not re.match(r"^(-?\d+)$", page):
        raise HTTPException(status_code=422, detail="Page must be an integer")

    if not re.match(r"^(-?\d+)$", limit):
        raise HTTPException(status_code=422, detail="Limit must be an integer")

    page = int(page)
    limit = int(limit)

    # check page and limit are positive values
    if page <= 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Page and limit must be greater than 0.")

    return page, limit


async def validate_symbol_in_database(symbol: str) -> bool:
    if symbol:
        async with aiosqlite.connect(DATABASE_URL) as db:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM financial_data WHERE symbol = ?", (symbol,)
            )
            symbol_count = await cursor.fetchone()
            if symbol_count[0] == 0:
                raise HTTPException(status_code=404, detail="Symbol not found in database.")


async def rate_limiter(request: Request):
    if not hasattr(request.app.state, "request_count"):
        request.app.state.request_count = 0
        request.app.state.start_time = time.time()

    request.app.state.request_count += 1
    time_passed = time.time() - request.app.state.start_time

    if time_passed > RATE_LIMIT_TIME:
        request.app.state.request_count = 1
        request.app.state.start_time = time.time()

    if request.app.state.request_count > RATE_LIMIT_REQUESTS:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    return request


async def get_financial_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    symbol: Optional[str] = None,
    page: int = 1,
    limit: int = 5,
) -> List[FinancialData]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        where_clause = ""
        params = []

        if start_date:
            where_clause += f"WHERE date >= '{start_date}'"
            params.append(start_date)

        if end_date:
            where_clause += " AND " if where_clause else "WHERE "
            where_clause += f"date <= '{end_date}'"
            params.append(end_date)

        if symbol:
            where_clause += " AND " if where_clause else "WHERE "
            where_clause += f"symbol = '{symbol}'"
            params.append(symbol)

        query = f"SELECT * FROM financial_data {where_clause} ORDER BY date DESC"

        async def paginate(query, params, page, limit):
            offset = (page - 1) * limit
            pagination_query = f"{query} LIMIT {limit} OFFSET {offset};"
            params += (limit, offset)
            return pagination_query, params

        paginated_query, params = await paginate(query, params, page, limit)
        cursor = await db.execute(paginated_query)
        items = await cursor.fetchall()

        return [
            FinancialData(
                symbol=item[1],
                date=item[2],
                open_price=item[3],
                close_price=item[4],
                volume=item[5],
            )
            for item in items
        ]


async def get_statistics(start_date: str, end_date: str, symbol: str) -> Statistics:
    async with aiosqlite.connect(DATABASE_URL) as db:
        query = f"""
        SELECT
            AVG(open_price),
            AVG(close_price),
            AVG(volume)
        FROM
            financial_data
        WHERE
            symbol = '{symbol}'
            AND date >= '{start_date}'
            AND date <= '{end_date}'
        """
        result = await db.execute(query)
        statistics = await result.fetchone()

        return Statistics(
            start_date=start_date,
            end_date=end_date,
            symbol=symbol,
            average_daily_open_price=statistics[0],
            average_daily_close_price=statistics[1],
            average_daily_volume=statistics[2],
        )


def get_pagination_data(items: List[FinancialData], page: int, limit: int):
    return PaginationData(
        count=len(items), page=page, limit=limit, pages=(len(items) + limit - 1) // limit
    )
