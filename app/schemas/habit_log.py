from datetime import date
from typing import Optional
from pydantic import BaseModel


class HabitLogCreate(BaseModel):
    habit_id: int
    date: date
    status: bool  # True = cumplido, False = no cumplido
    notes: Optional[str] = None


class HabitLogUpdate(BaseModel):
    status: Optional[bool] = None
    notes: Optional[str] = None


class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    date: date
    status: bool
    notes: Optional[str]

    class Config:
        from_attributes = True
