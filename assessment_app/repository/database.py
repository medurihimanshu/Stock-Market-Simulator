from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@127.0.0.1:5432/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
