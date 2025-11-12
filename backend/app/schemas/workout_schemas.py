from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime
from typing import List

class ExerciseName(str, Enum):
    squat = 'squat'
    pushup = 'pushup'
    tricep_dip = 'tricep_dip'

class ExcerciseCreate(BaseModel):
    name: ExerciseName
    duration: int
    repetitions: int
    partial_reps: int

class WorkoutCreate(BaseModel):
    started_at: datetime
    duration: int
    exercises: List[ExcerciseCreate]

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
    exercises: List[ExerciseResponse]
    calories_burned: int