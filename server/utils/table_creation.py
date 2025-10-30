from sqlalchemy import create_engine
from server.models.base_model import Base
from server.models.user_model import User
from server.models.workout_model import Workout
from server.models.exercise_model import Exercise
import os

def create_tables():
    os.makedirs('server/data', exist_ok=True)
    
    engine = create_engine("sqlite:///server/data/mydatabase.db", echo=True)
    
    # Base.metadata.drop_all(engine)
    
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()