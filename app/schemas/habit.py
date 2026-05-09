from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: str = "daily"


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None


class HabitResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    frequency: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True