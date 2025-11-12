from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.services.session import SessionManager
from app.exercises.pushup import Pushup
from app.exercises.squat import Squat
from app.exercises.tricep_dips import TricepDips
from app.services.engine import generate_frames, generate_rep_counts
import json

session_manager = SessionManager()

session_router = APIRouter()

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


@session_router.post("/start-session/{session_id}/{exercise_name}")
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

@session_router.get("/video/{session_id}/{exercise_name}")
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


@session_router.get("/rep-count/{session_id}")
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

@session_router.post("/end-session/{session_id}")
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

