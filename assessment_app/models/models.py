import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel

from assessment_app.models.constants import TradeType


# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str
    first_name: str
    last_name: str


class RegisterUserRequest(User):
    password: str


class Stock(BaseModel):
    symbol: str


class StockPrice(Stock):
    price: float


class Trade(StockPrice):
    type: str = TradeType.BUY.value
    quantity: int
    execution_ts: datetime


class Holding(StockPrice):
    quantity: int


class Strategy(BaseModel):
    id: str
    name: str


class PortfolioRequest(BaseModel):
    user_id: str
    strategy_id: str = "0"
    holdings: List[Holding]


class Portfolio(PortfolioRequest):
    id: str = str(uuid.uuid4())
    cash_remaining: float = 1000000.0
    current_ts: datetime = "2024-07-18T00:00:00Z"


class TickData(BaseModel):
    stock_symbol: str
    timestamp: datetime
    price: float

class TickDataResponse(BaseModel):
    data: List[TickData]


class TradeHistory(BaseModel):
    portfolio_id: str
    trades: List[Trade]


class BacktestRequest(BaseModel):
    strategy_id: str
    portfolio_id: str
    start_date: datetime
    end_date: datetime
    initial_capital: float

# class Trade(BaseModel):
#     date: datetime
#     asset: str
#     action: str = TradeType.BUY.value
#     quantity: int
#     price: float


class BacktestResponse(BaseModel):
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    trades: List[Trade]
    profit_loss: float
    annualized_return: float
