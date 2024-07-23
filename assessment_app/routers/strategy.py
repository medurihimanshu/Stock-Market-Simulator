from datetime import datetime
import random
from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from assessment_app.models import schema
from assessment_app.models.models import Holding, Portfolio, PortfolioRequest, Strategy
from assessment_app.repository.database import HoldingDB, PortfolioDB, get_db
from assessment_app.service.auth_service import get_current_user
from sqlalchemy.orm import Session

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
async def create_portfolio(portfolio_request: PortfolioRequest, 
                           override_existing_portfolio : bool = True, 
                           current_user_id: str = Depends(get_current_user), 
                           db: Session = Depends(get_db)) -> Portfolio:
    """
    Create a new portfolio and initialise with funds with empty holdings.
    """
    # 1. Check and override existing portfolio
    existing_portfolio = db.query(PortfolioDB).filter(PortfolioDB.user_id == current_user_id).first()
    if existing_portfolio and not override_existing_portfolio:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A portfolio already exists for this user")

    # 2. New portfolio creation
    portfolio_id = str(uuid.uuid4())
    portfolio = PortfolioDB(
        id=portfolio_id,
        user_id=portfolio_request.user_id,
        strategy_id=portfolio_request.strategy_id,
        cash_remaining=1000000.0,  # Set initial cash
        current_ts=datetime.utcnow()  # Set the current timestamp
    )
    db.add(portfolio)
    db.commit()

    # 3. Add holdings
    for holding in portfolio_request.holdings:
        db_holding = HoldingDB(
            id=str(uuid.uuid4()),
            portfolio_id=portfolio_id,
            symbol=holding.symbol,
            price=holding.price,
            quantity=holding.quantity
        )
        db.add(db_holding)
    db.commit()

    return Portfolio(
        id=portfolio.id,
        user_id=portfolio.user_id,
        strategy_id=portfolio.strategy_id,
        holdings=portfolio_request.holdings,
        cash_remaining=portfolio.cash_remaining,
        current_ts=portfolio.current_ts
    )


@router.get("/portfolio/{portfolio_id}", response_model=Portfolio)
async def get_portfolio_by_id(portfolio_id: str, 
                              current_ts: datetime, 
                              current_user_id: str = Depends(get_current_user), 
                              db: Session = Depends(get_db)) -> Portfolio:
    """
    Get specified portfolio for the current user.
    """
    # 1. Fetch the portfolio from the database
    portfolio = db.query(PortfolioDB).filter(PortfolioDB.id == portfolio_id).first()
    
    # 2. Ensure the portfolio exists and belongs to the current user
    validationCheck(portfolio, current_user_id)
    
    # 3. Fetch the holdings associated with the portfolio
    holdings = db.query(HoldingDB).filter(HoldingDB.portfolio_id == portfolio_id).all()
    
    # 4. Convert holdings to the required response model
    holdings_response = [Holding(symbol=holding.symbol, price=holding.price, quantity=holding.quantity) for holding in holdings]

    # 5. Return the portfolio details along with its holdings
    return Portfolio(
        id=portfolio.id,
        user_id=portfolio.user_id,
        strategy_id=portfolio.strategy_id,
        holdings=holdings_response,
        cash_remaining=portfolio.cash_remaining,
        current_ts=portfolio.current_ts
    )


@router.delete("/portfolio/{portfolio_id}", response_model=Portfolio)
async def delete_portfolio(portfolio_id: str, 
                           current_user_id: str = Depends(get_current_user), 
                           db: Session = Depends(get_db)) -> Portfolio:
    """
    Delete the specified portfolio for the current user.
    """
    # 1. Fetch the portfolio from the database
    portfolio = db.query(PortfolioDB).filter(PortfolioDB.id == portfolio_id).first()
    
    # 2. Ensure the portfolio exists and belongs to the current user
    validationCheck(portfolio, current_user_id)
    
    # 3. Fetch the holdings associated with the portfolio
    holdings = db.query(HoldingDB).filter(HoldingDB.portfolio_id == portfolio_id).all()
    
    # Store the holdings for the response model
    holdings_response = [Holding(symbol=holding.symbol, price=holding.price, quantity=holding.quantity) for holding in holdings]

    # Delete holdings
    for holding in holdings:
        db.delete(holding)
    
    # Delete portfolio
    db.delete(portfolio)
    
    db.commit()

    # Return the deleted portfolio details
    return Portfolio(
        id=portfolio.id,
        user_id=portfolio.user_id,
        strategy_id=portfolio.strategy_id,
        holdings=holdings_response,
        cash_remaining=portfolio.cash_remaining,
        current_ts=portfolio.current_ts
    )


@router.get("/portfolio-net-worth", response_model=float)
async def get_net_worth(portfolio_id: str, 
                        current_user_id: str = Depends(get_current_user), 
                        db: Session = Depends(get_db)) -> float:
    """
    Get net-worth from portfolio (holdings value and cash) at current_ts field in portfolio.
    """
    
    # 1. Fetch the portfolio from the database
    portfolio = db.query(PortfolioDB).filter(PortfolioDB.id == portfolio_id).first()
    
    # 2. Ensure the portfolio exists and belongs to the current user
    validationCheck(portfolio, current_user_id)
    
    # 3. Fetch the holdings associated with the portfolio
    holdings = db.query(HoldingDB).filter(HoldingDB.portfolio_id == portfolio_id).all()
    
    # 4. Calculate the total value of the holdings
    holdings_value = sum(holding.price * holding.quantity for holding in holdings)
    
    # 5. Calculate the net worth
    net_worth = portfolio.cash_remaining + holdings_value
    
    return net_worth


def validationCheck(portfolio : PortfolioDB, current_user_id : str) :
    if portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if portfolio.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="User does not have access to this portfolio")
