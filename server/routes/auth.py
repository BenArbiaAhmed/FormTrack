from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from dotenv import load_dotenv
from server.utils.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from server.models.user_model import User
from server.models.workout_model import Workout
from server.models.exercise_model import Exercise
import os

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7



class Token(BaseModel):
    access_token: str
    token_type: str

class Response(BaseModel):
    username: str
    token: Token


class TokenData(BaseModel):
    username: str | None = None


class UserAccount(BaseModel):
    username: str


class UserInDB(UserAccount):
    hashed_password: str


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

auth_router = APIRouter()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(username: str, db: Session):
    stmt = select(User).where(User.username == username)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user:
        return UserInDB(
            username=user.username,
            hashed_password=user.password,
        )
    return None

    


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db=db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserAccount, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@auth_router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)
) -> Response:
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"username": user.username, "token":Token(access_token=access_token, token_type="bearer")}

@auth_router.post("/signup")
async def signup_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(), ], db: Session = Depends(get_db)
) -> Response:
    if not(form_data.username and form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing credentials"
        )
    user = get_user(form_data.username, db)
    if(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in use, Choose another one !",
        )
    user = User(
        username=form_data.username,
        password=get_password_hash(form_data.password)
    )
    db.add(user)
    db.commit()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"username": user.username, "token":Token(access_token=access_token, token_type="bearer")}




@auth_router.get("/checkAuth", response_model=UserAccount)
async def checkAuth(
    current_user: Annotated[UserAccount, Depends(get_current_active_user)],
):
    return current_user


@auth_router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserAccount, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]