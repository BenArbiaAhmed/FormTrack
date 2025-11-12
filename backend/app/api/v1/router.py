from fastapi import APIRouter
from app.api.v1.endpoints import workout_router, session_router
from app.api.v1.endpoints import auth_router

api_router = APIRouter()

api_router.include_router(auth_router.auth_router, prefix="/auth")
api_router.include_router(workout_router.workout_router, prefix="/workout")
api_router.include_router(session_router.session_router, prefix="/session")