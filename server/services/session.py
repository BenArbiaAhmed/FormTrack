import cv2
from typing import Dict
import threading
from exercise import ExerciseTemplate

class WorkoutSession:
    def __init__(self, exercise: ExerciseTemplate):
        self.exercise = exercise
        self.active = True 
        self.lock = threading.Lock()
    
    def stop(self):
        with self.lock:
            self.active = False

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, WorkoutSession] = {}
        self._lock = threading.Lock()
    
    def create_session(self, session_id: str, exercise) -> WorkoutSession:
        with self._lock:
            session = WorkoutSession(exercise)
            self.sessions[session_id] = session
            return session
    
    def get_session(self, session_id: str):
        return self.sessions.get(session_id)
    
    def end_session(self, session_id: str):
        with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.stop()
                del self.sessions[session_id]