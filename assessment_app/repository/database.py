import uuid
from sqlalchemy import Date, UniqueConstraint, Uuid, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class PortfolioDB(Base):
    __tablename__ = "portfolios"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    strategy_id = Column(String, default="0")
    cash_remaining = Column(Float, default=1000000.0)
    current_ts = Column(DateTime, default=datetime.now)

class HoldingDB(Base):
    __tablename__ = "holdings"
    id = Column(String, primary_key=True, index=True)
    portfolio_id = Column(String, ForeignKey('portfolios.id'))
    symbol = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    portfolio = relationship("PortfolioDB", back_populates="holdings")

PortfolioDB.holdings = relationship("HoldingDB", back_populates="portfolio")

class StockDataDB(Base):
    __tablename__ = 'stock_data'
    id = Column(String, primary_key=True, index=True)
    stock_symbol = Column(String, index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Integer)
    
    __table_args__ = (UniqueConstraint('stock_symbol', 'date', name='_stock_date_uc'),)
    
Base.metadata.create_all(bind=engine)


def get_db():
    """
    Make sure this is singleton
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
