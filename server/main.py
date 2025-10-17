import numpy as np
import cv2
from pose_detector import PoseDetector
from utils.landmarks_utils import get_landmarks_dict, calculate_joint_angle

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

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    timestamp_ms = int(frame_count * 1000 / fps)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_with_landmarks, landmarks = my_pose_detector.detect_landmarks(
        data=rgb_frame, 
        timestamp_ms=timestamp_ms
    )
    if landmarks.pose_world_landmarks:
        pose_world_landmarks = landmarks.pose_world_landmarks[0]
        landmarks_dict = get_landmarks_dict(pose_world_landmarks)
    cv2.imshow('frame', image_with_landmarks)
    
    frame_count += 1
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()