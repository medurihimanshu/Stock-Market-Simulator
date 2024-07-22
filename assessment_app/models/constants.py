from enum import Enum

JWT_TOKEN = "jwt_token"
DAYS_IN_YEAR = 365.25


class TradeType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class Env(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


class StockSymbols(str, Enum):
    HDFCBANK: str = "HDFCBANK"
    ICICIBANK: str = "ICICIBANK"
    RELIANCE: str = "RELIANCE"
    TATAMOTORS: str = "TATAMOTORS"
