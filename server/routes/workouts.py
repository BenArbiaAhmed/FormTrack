from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime
from server.models.workout_model import Workout
from server.models.exercise_model import Exercise
from fastapi import Depends
from server.utils.database import get_db
from sqlalchemy.orm import Session
from server.routes.auth import get_current_active_user, UserAccount
from typing import Annotated, List
from sqlalchemy import select
from server.schemas.workout_schemas import WorkoutCreate, ExerciseResponse, WorkoutResponse, ExcerciceCreate
from server.utils.workout_utils import calculate_calories_burned

workout_router = APIRouter()

    
    
@workout_router.post("/workout/new", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def save_new_workout(workout: WorkoutCreate,
    current_user: Annotated[UserAccount, Depends(get_current_active_user)],
    db: Session = Depends(get_db)):
    if(current_user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No valid JWT token found")
    new_workout = Workout(
        duration=workout.duration,
        started_at=workout.started_at,
        user_id = current_user.id
    )
    
    for exercise in workout.exercises:
        new_exercise = Exercise(
            name=exercise.name,
            duration=exercise.duration,
            repetitions=exercise.repetitions,
            partial_reps=exercise.partial_reps
        )
        new_workout.exercises.append(new_exercise)
    new_workout.calories_burned = calculate_calories_burned(workout)
    
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    
    return new_workout 

@workout_router.delete("/workout/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    id: int,
    current_user: Annotated[UserAccount, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    stmt = select(Workout).where(Workout.id == id)
    result = db.execute(stmt)
    workout = result.scalar_one_or_none()
    
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Workout not found."
        )
    
    if workout.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You don't have permission to delete this workout."
        )
    
    db.delete(workout)
    db.commit()


@workout_router.get("/workout", status_code=status.HTTP_200_OK, response_model=List[WorkoutResponse])
async def fetch_workouts(
    current_user: Annotated[UserAccount, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    stmt = select(Workout).where(Workout.user_id == current_user.id)
    result = db.execute(stmt)
    workouts = result.scalars().all()
    return workouts
    
