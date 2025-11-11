from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from main import generate_frames
from server.routes.auth import auth_router
from server.routes.workouts import workout_router
from server.schemas.workout_schemas import ExerciseName
from services.session import SessionManager
import json
from main import generate_rep_counts
from fastapi import FastAPI, HTTPException, Depends
from exercises.squat import Squat
from exercises.pushup import Pushup
from exercises.tricep_dips import TricepDips

app = FastAPI()
app.include_router(auth_router)
app.include_router(workout_router)

session_manager = SessionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

def get_exercise_instance(exercise_name: str):
    """Factory function to create exercise instances"""
    exercises = {
        "squat": Squat(),
        "pushup": Pushup(),
        "tricep_dip": TricepDips()
    }
    return exercises.get(exercise_name)

def get_session_manager():
    return session_manager


@app.post("/start-session/{session_id}/{exercise_name}")
def start_session(session_id: str, exercise_name: str):
    """Initialize a workout session"""
    exercise = get_exercise_instance(exercise_name)
    if not exercise:
        raise HTTPException(status_code=400, detail="Invalid exercise name")
    
    if session_manager.get_session(session_id):
        raise HTTPException(status_code=409, detail="Session already exists")
    
    session = session_manager.create_session(session_id, exercise)
    return {
        "status": "started",
        "session_id": session_id,
        "exercise": exercise_name
    }

@app.get("/video/{session_id}/{exercise_name}")
def video_feed(session_id: str, exercise_name: str, sm: SessionManager = Depends(get_session_manager)):
    session = sm.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404, 
            detail="Session not found. Please call /start-session first."
        )
    return StreamingResponse(
        generate_frames(exercise_name, session_id, sm),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/rep-count/{session_id}")
async def rep_count_stream(session_id: str, sm: SessionManager = Depends(get_session_manager)):
    """Stream rep counts for a session"""

    session = sm.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404, 
            detail="Session not found. Please call /start-session first."
        )

    async def event_generator():
        async for counts in generate_rep_counts(session_id, sm):
            yield f"data: {json.dumps(counts)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.post("/end-session/{session_id}")
def end_session(session_id: str, sm: SessionManager = Depends(get_session_manager)):
    """End a workout session"""
    session = sm.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    final_counts = session.exercise.get_rep_counts()
    
    session_manager.end_session(session_id)
    
    return {
        "status": "ended",
        "final_counts": final_counts
    }