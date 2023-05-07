import aiosqlite
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from financial.models import FinancialData, Statistics, FinancialDataResponse, StatisticsResponse


BASE_URL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = os.path.join(BASE_URL, "financial_data.db")
app = FastAPI()


@app.get("/api/financial_data", response_model=FinancialDataResponse)
async def get_financial_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    symbol: Optional[str] = None,
    page: int = 1,
    limit: int = 5,
):
    # check whether symbol exists in database
    if symbol:
        async with aiosqlite.connect(DATABASE_URL) as db:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM financial_data WHERE symbol = ?", (symbol,)
            )
            symbol_count = await cursor.fetchone()
            if symbol_count[0] == 0:
                raise HTTPException(status_code=404, detail="Symbol not found in the database")

    where_clause = ""
    params = []
    async with aiosqlite.connect(DATABASE_URL) as db:
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

        return {
            "data": [
                FinancialData(
                    symbol=item[1],
                    date=item[2],
                    open_price=item[3],
                    close_price=item[4],
                    volume=item[5],
                )
                for item in items
            ],
            "pagination": {
                "count": len(items),
                "page": page,
                "limit": limit,
                "pages": (len(items) + limit - 1) // limit,
            },
            "info": {"error": ""},
        }


@app.get("/api/statistics", response_model=StatisticsResponse)
async def get_statistics(start_date: str, end_date: str, symbol: str):
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM financial_data WHERE symbol = ?", (symbol,))
        symbol_count = await cursor.fetchone()
        if symbol_count[0] == 0:
            raise HTTPException(status_code=404, detail="Symbol not found in the database")

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

        return {
            "data": Statistics(
                start_date=start_date,
                end_date=end_date,
                symbol=symbol,
                average_daily_open_price=statistics[0],
                average_daily_close_price=statistics[1],
                average_daily_volume=statistics[2],
            ),
            "info": {"error": ""},
        }
