from datetime import datetime

from fastapi import Depends, APIRouter

from assessment_app.models.constants import StockSymbols
from assessment_app.service.auth_service import get_current_user
from assessment_app.utils.utils import compute_cagr, datetime_to_str

router = APIRouter()


@router.get("/analysis/estimate_returns/stock", response_model=float)
async def get_stock_analysis(stock_symbol: str, start_ts: datetime, end_ts: datetime, current_user_id: str = Depends(get_current_user)) -> float:
    """
    Estimate returns for given stock based on stock prices between the given timestamps.
    Use compute_cagr method
    Example:
        200% CAGR would mean your returned value would be 200 for the duration
        5% CAGR would mean your returned value would be 5 for the duration
    """
    pass


@router.get("/analysis/estimate_returns/portfolio")
async def estimate_portfolio_returns(start_ts: datetime, end_ts: datetime, current_user_id: str = Depends(get_current_user)):
    """
    Estimate returns for the current portfolio based on stock prices between the given timestamps.
    Use compute_cagr method.
    Example:
        100% CAGR would mean your returned value would be 2.0 for the duration
        5% CAGR would mean your returned value would be 1.05 for the duration
    """

    pass
