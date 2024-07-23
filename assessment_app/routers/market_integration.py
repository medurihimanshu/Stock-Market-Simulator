import csv
from datetime import datetime
from tarfile import NUL
from typing import List, Optional
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Uuid, and_
from assessment_app.models.constants import TradeType
from assessment_app.models.models import TickData, TickDataResponse, Trade
from assessment_app.repository.database import HoldingDB, PortfolioDB, StockDataDB, get_db
from assessment_app.service.auth_service import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/market/data/tick", response_model=TickData)
async def get_market_data_tick(stock_symbol: str, 
                               current_ts: datetime, 
                               current_user_id: str = Depends(get_current_user), 
                               db: Session = Depends(get_db)) -> TickData:
    """
    Get data for stocks for a given datetime from `data` folder.
    Please note consider price value in TickData to be average of open and close price column value for the timestamp from the data file.
    """
    file_path = os.path.join(os.getcwd(), 'assessment_app', 'data', f'{stock_symbol}.csv')
    insert_stock_data_from_csv(db, file_path, stock_symbol)
    tick_data = get_stock_data_from_db(db, stock_symbol, current_ts)
    
    if tick_data is None:
        raise HTTPException(status_code=404, detail="Datrountersa for the given timestamp not found")

    return tick_data



@router.post("/market/data/range", response_model=TickDataResponse)
async def get_market_data_range(stock_symbol: str, 
                                from_ts: datetime, 
                                to_ts: datetime, 
                                current_user_id: str = Depends(get_current_user), 
                                db: Session = Depends(get_db)) -> TickDataResponse:
    """
    Get data for stocks for a given datetime from `data` folder.
    Please note consider price value in TickData to be average of open and close price column value for the timestamp from the data file.
    [UPDATE] - Updating response as List of TickData
    """
    # 1. Insert csv data into postgres DB for once
    file_path = os.path.join(os.getcwd(), 'assessment_app', 'data', f'{stock_symbol}.csv')
    insert_stock_data_from_csv(db, file_path, stock_symbol)

    # 2. Query for all the stock data
    stock_data = db.query(StockDataDB).filter(
        StockDataDB.stock_symbol == stock_symbol,
        and_(StockDataDB.date >= from_ts.date(), StockDataDB.date <= to_ts.date())
    ).all()
    
    if not stock_data:
        raise HTTPException(status_code=404, detail="No data found for the specified range.")

    # 3. Prepare the list of TickData
    tick_data_list = [
        TickData(
            stock_symbol=stock_symbol,
            timestamp=datetime.combine(data.date, datetime.min.time()),  # Set time to midnight
            price=(data.open + data.close) / 2
        )
        for data in stock_data
    ]
    
    return TickDataResponse(data=tick_data_list)


@router.post("/market/trade", response_model=Trade)
async def trade_stock(trade: Trade, 
                      current_user_id: str = Depends(get_current_user), 
                      db: Session = Depends(get_db)) -> Trade:
    """
    Only if trade.price is within Open and Close price of that stock on the execution timestamp, then trade should be successful.
    Trade.price must be average of Open and Close price of that stock on the execution timestamp.
    Also, update the portfolio and trade history with the trade details and adjust cash and networth appropriately.
    On every trade, current_ts of portfolio also becomes today.
    One cannot place trade in date (Trade.execution_ts) older than portfolio.current_ts
    """
    # 1. Insert csv data into postgres DB for once
    file_path = os.path.join(os.getcwd(), 'assessment_app', 'data', f'{trade.symbol}.csv')
    insert_stock_data_from_csv(db, file_path, trade.symbol)

    # 2. Fetch stock data
    stock_data = db.query(StockDataDB).filter(
        StockDataDB.stock_symbol == trade.symbol,
        StockDataDB.date == trade.execution_ts.date()
    ).first()
    if not stock_data:
        raise HTTPException(status_code=404, detail="Stock data not found for the specified date.")
    
    # 3. Validate the trade price
    if not (stock_data.open <= trade.price <= stock_data.close or stock_data.open >= trade.price >= stock_data.close) :
        raise HTTPException(status_code=400, detail="Trade price must be within the open and close price range.")
    
    # 4. Fetch and update the portfolio
    portfolio = get_portfolio(db, current_user_id)
    holding = get_holding(db, trade.symbol, portfolio.id)

    update_portfolio(db, portfolio, trade, holding)

    return Trade(
        quantity=trade.quantity,
        execution_ts=trade.execution_ts,
        type=trade.type,
        price=trade.price,
        symbol=trade.symbol
    )

def insert_stock_data_from_csv(db: Session, file_path: str, stock_symbol: str):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
            if stock_data_exists(db, stock_symbol, date):
                print(f"Data for stock symbol '{stock_symbol}' on date '{date}' already exists in the database. Skipping the persistence in DB.")
                break
            stock_data = StockDataDB(
                id=str(uuid.uuid4()),
                stock_symbol=stock_symbol,
                date=date,
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                adj_close=float(row['Adj Close']),
                volume=int(row['Volume'])
            )
            db.merge(stock_data)
        db.commit()

def get_stock_data_from_db(db: Session, stock_symbol: str, current_ts: datetime) -> Optional[TickData]:
    stock_data = db.query(StockDataDB).filter(StockDataDB.stock_symbol == stock_symbol, StockDataDB.date == current_ts.date()).first()
    
    if stock_data:
        avg_price = (stock_data.open + stock_data.close) / 2
        return TickData(
            stock_symbol=stock_symbol,
            timestamp=current_ts,
            price=avg_price
        )
    return None

def stock_data_exists(db: Session, stock_symbol: str, date: datetime.date) -> bool:
    return db.query(StockDataDB).filter(
        StockDataDB.stock_symbol == stock_symbol,
        StockDataDB.date == date
    ).first() is not None


def get_portfolio(db: Session, user_id: str):
    portfolio = db.query(PortfolioDB).filter(PortfolioDB.user_id == user_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found.")
    return portfolio

def get_holding(db: Session, symbol: str, portfolio_id: str):
    return db.query(HoldingDB).filter(HoldingDB.symbol == symbol, PortfolioDB.id == portfolio_id).first()

def update_portfolio(db: Session, portfolio: PortfolioDB, trade: Trade, holding: HoldingDB):
    """
    Update the portfolio based on the trade details.
    """
    if trade.execution_ts.date() < portfolio.current_ts.date():
        raise HTTPException(status_code=400, detail="Trade execution date cannot be older than portfolio current timestamp.")

    # 1. Update the portfolio's current timestamp
    portfolio.current_ts = datetime.now()

    # 2. Calculate the total trade value
    total_trade_value = trade.quantity * trade.price

    # 3. Adjust the cash remaining in the portfolio
    if trade.type == TradeType.BUY:
        portfolio.cash_remaining -= total_trade_value
    elif trade.type == TradeType.SELL:
        portfolio.cash_remaining += total_trade_value
    else:
        raise HTTPException(status_code=400, detail="Invalid trade type.")

    # 4. Update holdings
    if trade.type == TradeType.BUY:
        if not holding :
            holding.price = trade.quantity
        else:
            holding.price += trade.quantity
    elif trade.type == TradeType.SELL:
        if not holding:
            raise HTTPException(status_code=400, detail="Stock not found in portfolio.")
        else:
            if holding.quantity < trade.quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock quantity for sale.")
            holding.price -= trade.quantity

    db.add(holding)
    db.commit()

    db.add(portfolio)
    db.commit()