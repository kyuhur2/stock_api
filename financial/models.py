from typing import List
from pydantic import BaseModel


class PaginationInfo(BaseModel):
    count: int
    page: int
    limit: int
    pages: int


class FinancialData(BaseModel):
    symbol: str
    date: str
    open_price: float
    close_price: float
    volume: int


class Statistics(BaseModel):
    start_date: str
    end_date: str
    symbol: str
    average_daily_open_price: float
    average_daily_close_price: float
    average_daily_volume: float


class FinancialDataResponse(BaseModel):
    data: List[FinancialData]
    pagination: PaginationInfo
    info: dict


class StatisticsResponse(BaseModel):
    data: dict
    info: dict
