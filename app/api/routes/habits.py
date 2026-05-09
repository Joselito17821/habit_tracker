from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import SessionLocal
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse
from app.services import habit_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    return habit_service.get_all_habits(db)


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    return habit_service.get_habit_by_id(habit_id, db)


@router.post("/", response_model=HabitResponse, status_code=201)
def create_habit(habit_data: HabitCreate, db: Session = Depends(get_db)):
    return habit_service.create_habit(habit_data, db)


@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit_data: HabitUpdate, db: Session = Depends(get_db)):
    return habit_service.update_habit(habit_id, habit_data, db)


@router.delete("/{habit_id}", status_code=204)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit_service.delete_habit(habit_id, db)