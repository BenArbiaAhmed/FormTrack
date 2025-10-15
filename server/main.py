import numpy as np
import cv2
from pose_detector import PoseDetector

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
my_pose_detector = PoseDetector('model/pose_landmarker_full.task')
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break      
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_with_landmarks = my_pose_detector.detect_landmarks(data=rgb_frame)
    cv2.imshow('frame', image_with_landmarks)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()