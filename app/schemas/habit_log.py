from datetime import date
from typing import Optional
from pydantic import BaseModel


class HabitLogCreate(BaseModel):
    """Schema para crear un nuevo registro de hábito"""
    habit_id: int
    date: date
    status: bool  # True = cumplido, False = no cumplido
    notes: Optional[str] = None


class HabitLogUpdate(BaseModel):
    """Schema para actualizar un registro de hábito"""
    status: Optional[bool] = None
    notes: Optional[str] = None


class HabitLogResponse(BaseModel):
    """Schema de respuesta para un registro de hábito"""
    id: int
    habit_id: int
    date: date
    status: bool
    notes: Optional[str]

    class Config:
        from_attributes = True
