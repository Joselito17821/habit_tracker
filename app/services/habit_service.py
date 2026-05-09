from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate


def get_all_habits(db: Session):
    return db.query(Habit).filter(Habit.is_active == True).all()


def get_habit_by_id(habit_id: int, db: Session):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    return habit


def create_habit(habit_data: HabitCreate, db: Session):
    habit = Habit(**habit_data.model_dump())
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


def update_habit(habit_id: int, habit_data: HabitUpdate, db: Session):
    habit = get_habit_by_id(habit_id, db)
    for field, value in habit_data.model_dump(exclude_unset=True).items():
        setattr(habit, field, value)
    db.commit()
    db.refresh(habit)
    return habit


def delete_habit(habit_id: int, db: Session):
    habit = get_habit_by_id(habit_id, db)
    habit.is_active = False
    db.commit()
    