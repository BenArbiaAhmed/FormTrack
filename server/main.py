import numpy as np
import cv2
from pose_detector import PoseDetector
from utils.landmarks_utils import get_landmarks_dict, calculate_joint_angle
from exercises.squat import Squat

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
my_pose_detector = PoseDetector('model/pose_landmarker_full.task')
if not cap.isOpened():
    print("Cannot open camera")
    exit()

frame_count = 0
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 30

squat = Squat()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    landmarks_dict = {}
    right_knee = None
    left_knee = None

    timestamp_ms = int(frame_count * 1000 / fps)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_with_landmarks, landmarks = my_pose_detector.detect_landmarks(
        data=rgb_frame, 
        timestamp_ms=timestamp_ms
    )
    if landmarks.pose_world_landmarks:
        pose_world_landmarks = landmarks.pose_world_landmarks[0]
        landmarks_dict = get_landmarks_dict(pose_world_landmarks)

    if landmarks_dict.get('right_hip') and landmarks_dict.get('right_knee') and landmarks_dict.get('right_ankle'):
        right_knee = calculate_joint_angle(landmarks_dict['right_hip'], landmarks_dict['right_knee'], landmarks_dict['right_ankle'])
    if landmarks_dict.get('left_hip') and landmarks_dict.get('left_knee') and landmarks_dict.get('left_ankle'):
        left_knee = calculate_joint_angle(landmarks_dict['left_hip'], landmarks_dict['left_knee'], landmarks_dict['left_ankle'])
    if(right_knee is not None and left_knee is not None):
        rep_count, current_phase = squat.update({'right_knee': right_knee, 'left_knee': left_knee})
        cv2.putText(image_with_landmarks, f'Phase: {current_phase}', 
                    (50, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (255, 255, 0),  # Cyan
                    2,
                    cv2.LINE_AA)
    print(squat.phase_history)
    cv2.putText(image_with_landmarks, f'Reps: {squat.rep_count}', 
                (50, 100),  # Position (x, y)
                cv2.FONT_HERSHEY_SIMPLEX,  # Font
                2,  # Font scale
                (0, 255, 0),  # Color (BGR) - Green
                3,  # Thickness
                cv2.LINE_AA)  # Line type
    
        
    cv2.imshow('frame', image_with_landmarks)
    
    frame_count += 1
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()