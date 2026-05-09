from datetime import datetime

from app.db import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    frequency = Column(String(20), nullable=False, default="daily")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)