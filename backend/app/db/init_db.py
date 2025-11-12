from sqlalchemy import create_engine
from app.models.base_model import Base
from app.models.exercise_model import Exercise
from app.models.user_model import User
from app.models.workout_model import Workout
import os

def create_tables():
    os.makedirs('data/db', exist_ok=True)
    
    engine = create_engine("sqlite:///data/db/mydatabase.db", echo=True)
    
    
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()