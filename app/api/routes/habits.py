from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import SessionLocal
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    return db.query(Habit).filter(Habit.is_active == True).all()


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    return habit


@router.post("/", response_model=HabitResponse, status_code=201)
def create_habit(habit_data: HabitCreate, db: Session = Depends(get_db)):
    habit = Habit(**habit_data.model_dump())
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit_data: HabitUpdate, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    for field, value in habit_data.model_dump(exclude_unset=True).items():
        setattr(habit, field, value)
    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}", status_code=204)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    habit.is_active = False
    db.commit()