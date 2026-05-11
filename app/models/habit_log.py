from datetime import datetime

from app.db import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Text


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)