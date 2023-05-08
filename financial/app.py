from fastapi import FastAPI, Request
from financial.models import FinancialDataResponse, StatisticsResponse
from financial.services import (
    validate_symbol_in_database,
    rate_limiter,
    validate_page_limit_inputs,
    validate_date_symbol_inputs,
    get_financial_data,
    get_statistics,
    get_pagination_data,
)
from typing import Optional


app = FastAPI()


@app.get("/api/financial_data", response_model=FinancialDataResponse)
async def get_financial_data_endpoint(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    symbol: Optional[str] = None,
    page: Optional[str] = "1",
    limit: Optional[str] = "5",
    request: Request = None,
):
    # validate and raise Exceptions
    await rate_limiter(request)
    validate_date_symbol_inputs(start_date, end_date, symbol)
    page, limit = validate_page_limit_inputs(page, limit)  # page, limit should be ints now
    await validate_symbol_in_database(symbol)

    # retrieve records
    items = await get_financial_data(start_date, end_date, symbol, page, limit)
    pagination_data = get_pagination_data(items, page, limit)

    return {
        "data": items,
        "pagination": pagination_data,
        "info": {"error": ""},
    }


@app.get("/api/statistics", response_model=StatisticsResponse)
async def get_statistics_endpoint(
    start_date: str, end_date: str, symbol: str, request: Request = None
):
    # validate and raise Exceptions
    await rate_limiter(request)
    validate_date_symbol_inputs(start_date, end_date, symbol)
    await validate_symbol_in_database(symbol)

    # retrieve records
    statistics = await get_statistics(start_date, end_date, symbol)

    return {
        "data": statistics,
        "info": {"error": ""},
    }
