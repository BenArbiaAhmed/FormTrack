import numpy as np
import math

def get_landmarks_dict(pose_world_landmarks, visibility_threshold=0.1):
    landmarks = {}
    
    landmark_names = [
        'nose', 'left_eye_inner', 'left_eye', 'left_eye_outer',
        'right_eye_inner', 'right_eye', 'right_eye_outer',
        'left_ear', 'right_ear', 'mouth_left', 'mouth_right',
        'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist', 'left_pinky', 'right_pinky',
        'left_index', 'right_index', 'left_thumb', 'right_thumb',
        'left_hip', 'right_hip', 'left_knee', 'right_knee',
        'left_ankle', 'right_ankle', 'left_heel', 'right_heel',
        'left_foot_index', 'right_foot_index'
    ]
    
    for i, name in enumerate(landmark_names):
        landmark = pose_world_landmarks[i]
        
        
        if landmark.visibility >= visibility_threshold:
            landmarks[name] = landmark
        else:
            landmarks[name] = None 
    
    return landmarks


def calculate_joint_angle(point1, point2, point3):

    angle1 = math.atan2(point1.y - point2.y, point1.x - point2.x)
    angle2 = math.atan2(point3.y - point2.y, point3.x - point2.x)
    angle_radians = angle2 - angle1
    angle_radians = math.atan2(math.sin(angle_radians), math.cos(angle_radians))
    angle_degrees = math.degrees(angle_radians)
    return abs(angle_degrees)