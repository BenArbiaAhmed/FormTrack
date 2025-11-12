import cv2
from app.services.pose_detector import PoseDetector
from app.utils.landmarks_utils import get_landmarks_dict, calculate_joint_angle
from app.exercises.squat import Squat
from app.exercises.pushup import Pushup
from app.exercises.tricep_dips import TricepDips
from app.exercises.base import RepType
from app.utils.audio_feedback import play_go_lower_sound, play_feedback_sound
import time
from typing import Generator
from app.services.squat_logic import process_squat
from app.services.pushup_logic import process_pushup
from app.services.tricep_dips_logic import process_tricep_dips
from typing import Dict
from app.services.session import SessionManager
import asyncio


pushup = Pushup()
tricep_dips = TricepDips()

last_audio_time = 0
audio_cooldown = 4
show_go_lower_message = False
message_start_time = 0


def generate_frames(exercise_name, session_id, session_manager: SessionManager)-> Generator[bytes, None, None]:
    global last_audio_time, show_go_lower_message, message_start_time, frame_count
    session = session_manager.get_session(session_id)
    if not session:
        print(f"Session {session_id} not found")
        return
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    
    frame_count = 0
    my_pose_detector = PoseDetector('models/pose_landmarker_full.task')
    try:
        while session.active:
            ret, frame = cap.read()
            
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            landmarks_dict = {} 

            timestamp_ms = int(frame_count * 1000 / fps)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_with_landmarks, landmarks = my_pose_detector.detect_landmarks(
                data=rgb_frame, 
                timestamp_ms=timestamp_ms
            )
            if landmarks.pose_world_landmarks:
                pose_world_landmarks = landmarks.pose_world_landmarks[0]
                landmarks_dict = get_landmarks_dict(pose_world_landmarks)
            feedback=""
            with session.lock:
                if exercise_name == "squat":
                    session.exercise, feedback = process_squat(landmarks_dict, session.exercise)
                elif exercise_name == 'pushup':
                    session.exercise, feedback = process_pushup(landmarks_dict, session.exercise)
                elif exercise_name == 'tricep_dip':
                    session.exercise, feedback = process_tricep_dips(landmarks_dict, session.exercise)


            if feedback :
                cv2.putText(image_with_landmarks, f'{feedback}',
                    (50, 250),  
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA)
                play_feedback_sound(feedback)
        
            cv2.putText(image_with_landmarks, f'Reps: {session.exercise.rep_count}', 
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 255, 0),
                    3,
                    cv2.LINE_AA)
                
            if session.exercise.last_rep_type == RepType.PARTIAL:
                current_time = time.time()

                if current_time - last_audio_time > audio_cooldown:
                    play_go_lower_sound()
                    last_audio_time = current_time
                    show_go_lower_message = True
                    message_start_time = current_time
                
                session.exercise.last_rep_type = None
                
                if show_go_lower_message:
                    if time.time() - message_start_time < 2:
                        cv2.putText(image_with_landmarks, f'Go Lower !', 
                                    (700, 700),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_AA)
                    else:
                        show_go_lower_message = False

                print(session.exercise.phase_history)

            ret, buffer = cv2.imencode('.jpg', image_with_landmarks)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            frame_count += 1
    finally:
        cap.release()
    
async def generate_rep_counts(session_id: str, session_manager: SessionManager):
    session = session_manager.get_session(session_id)
    if not session:
        yield {"error": "Session not found"}
        return
    
    last_reps = 0
    last_partial = 0
    
    try:
        while session.active:  
            with session.lock:
                counts = session.exercise.get_rep_counts()
            
            if counts["reps"] != last_reps or counts["partial_reps"] != last_partial:
                yield counts
                last_reps = counts["reps"]
                last_partial = counts["partial_reps"]
            
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Error in rep counts: {e}")