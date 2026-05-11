from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.db import SessionLocal
from app.schemas.habit_log import HabitLogCreate, HabitLogUpdate, HabitLogResponse
from app.services import habit_log_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/", response_model=List[HabitLogResponse])
def get_logs(db: Session = Depends(get_db)):
    return habit_log_service.get_all_logs(db)

@router.get("/habit/{habit_id}", response_model=List[HabitLogResponse])
def get_logs_by_habit(habit_id: int, db: Session = Depends(get_db)):
    return habit_log_service.get_logs_by_habit(habit_id, db)

@router.post("/", response_model=HabitLogResponse, status_code=201)
def create_log(log_data: HabitLogCreate, db: Session = Depends(get_db)):
    return habit_log_service.create_log(log_data, db)

@router.put("/habit/{habit_id}/{log_date}", response_model=HabitLogResponse)
def update_log(habit_id: int, log_date: date, log_data: HabitLogUpdate, db: Session = Depends(get_db)):
    return habit_log_service.update_log(habit_id, log_date, log_data, db)

@router.delete("/habit/{habit_id}/{log_date}", status_code=204)
def delete_log(habit_id: int, log_date: date, db: Session = Depends(get_db)):
    habit_log_service.delete_log(habit_id, log_date, db)