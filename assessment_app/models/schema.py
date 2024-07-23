from assessment_app.repository.database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)

    





