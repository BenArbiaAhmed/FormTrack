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
from typing import Annotated

workout_router = APIRouter()


class ExerciseName(str, Enum):
    squat = 'squat'
    pushup = 'pushup'
    tricep_dip = 'tricep_dip'


class ExcerciceCreate(BaseModel):
    name: ExerciseName
    duration: int
    repetitions: int
    partial_reps: int

class WorkoutCreate(BaseModel):
    started_at: datetime
    duration: int
    exercises: list[ExcerciceCreate]

class ExerciseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: ExerciseName
    duration: int
    repetitions: int
    partial_reps: int

class WorkoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    duration: int
    started_at: datetime
    exercises: list[ExerciseResponse]
    
    
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
    
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    
    return new_workout 
    
            