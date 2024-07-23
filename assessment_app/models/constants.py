from enum import Enum

JWT_TOKEN = "jwt_token"
DAYS_IN_YEAR = 365.25
REDIS_HOST = 'REDIS_HOST'
REDIS_PORT = 'REDIS_PORT'
PASSWORD = 'hash_password'
EMAIL = 'email'
SECRET_KEY = "TESTING"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
