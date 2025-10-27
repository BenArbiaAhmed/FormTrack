from fastapi import APIRouter, FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends
from server.utils.database import get_db
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str


auth_router = APIRouter(prefix="/auth", tags=["authentication"])

@auth_router.post("/signup/")
def signup(user: User, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"id": new_user.id, "username": new_user.username}