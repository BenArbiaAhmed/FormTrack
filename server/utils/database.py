from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

class DatabaseEngine:
    _instance = None
    _engine = None
    _SessionLocal = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseEngine, cls).__new__(cls)
            cls._engine = create_engine("sqlite:///server/data/mydatabase.db", echo=True)
            cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)
        return cls._instance
    
    @property
    def engine(self):
        return self._engine
    
    @property
    def SessionLocal(self):
        return self._SessionLocal

# Initialize singleton
db_engine = DatabaseEngine()

# Dependency function for FastAPI
def get_db() -> Generator[Session, None, None]:
    db = db_engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()