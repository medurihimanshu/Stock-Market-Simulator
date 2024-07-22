from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends

from assessment_app.models.models import Portfolio, PortfolioRequest, Strategy
from assessment_app.service.auth_service import get_current_user

router = APIRouter()


@router.get("/strategies", response_model=List[Strategy])
async def get_strategies(current_user_id: str = Depends(get_current_user)) -> List[Strategy]:
    """
    Get all strategies available. You do not need to implement this.
    """
    return [
        Strategy(
            id="0",
            name="default"
        )
    ]


@router.post("/portfolio", response_model=Portfolio)
async def create_portfolio(portfolio_request: PortfolioRequest, current_user_id: str = Depends(get_current_user)) -> Portfolio:
    """
    Create a new portfolio and initialise with funds with empty holdings.
    """
    pass


@router.get("/portfolio/{portfolio_id}", response_model=Portfolio)
async def get_portfolio_by_id(portfolio_id: str, current_ts: datetime, current_user_id: str = Depends(get_current_user)) -> Portfolio:
    """
    Get specified portfolio for the current user.
    """
    pass


@router.delete("/portfolio/{portfolio_id}", response_model=Portfolio)
async def delete_portfolio(portfolio_id: str, current_user_id: str = Depends(get_current_user)) -> Portfolio:
    """
    Delete the specified portfolio for the current user.
    """
    pass


@router.get("/portfolio-net-worth", response_model=float)
async def get_net_worth(portfolio_id: str, current_user_id: str = Depends(get_current_user)) -> float:
    """
    Get net-worth from portfolio (holdings value and cash) at current_ts field in portfolio.
    """
    pass
