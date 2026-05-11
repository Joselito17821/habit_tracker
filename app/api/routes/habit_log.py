from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

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


@router.put("/{log_id}", response_model=HabitLogResponse)
def update_log(log_id: int, log_data: HabitLogUpdate, db: Session = Depends(get_db)):
    return habit_log_service.update_log(log_id, log_data, db)


@router.delete("/{log_id}", status_code=204)
def delete_log(log_id: int, db: Session = Depends(get_db)):
    habit_log_service.delete_log(log_id, db)