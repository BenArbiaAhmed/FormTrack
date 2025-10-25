from exercise import *
from utils.landmarks_utils import calculate_distance_between_landmakrs
from utils.landmarks_utils import calculate_joint_angle

class Pushup(ExerciseTemplate):

    def __init__(self):
        super().__init__(name='pushup', key_angles={'shoulder_elbow_wrist': 90, 'asymmetry': 15, 'extended_arm': 160})


    def check_phase(self, angles):
        right_elbow = angles.get('right_elbow')
        left_elbow = angles.get('left_elbow')
    
        visible_elbows = [e for e in [right_elbow, left_elbow] if e is not None]
    
        if not visible_elbows:
            return self.last_phase
        
        if len(visible_elbows) == 1:
            active_elbow = visible_elbows[0]
        else:
            active_elbow = sum(visible_elbows) / len(visible_elbows)
        
        if active_elbow >= self.key_angles["extended_arm"]:
            return ExercisePhase.START
        elif active_elbow >= self.key_angles["shoulder_elbow_wrist"]:
            return ExercisePhase.TRANSITION
        else:
            return ExercisePhase.PEAK
        
    def detect_common_mistakes(self, landmarks):
        right_shoulder = landmarks.get("right_shoulder")
        left_shoulder = landmarks.get("left_shoulder")
        right_wrist = landmarks.get("right_wrist")
        left_wrist = landmarks.get("left_wrist")
        right_knee = landmarks.get("right_knee")
        left_knee = landmarks.get("left_knee")
        right_hip = landmarks.get("right_hip")
        left_hip = landmarks.get("left_hip")
        
        feedback = ""
        
        # Check arm width
        if right_shoulder and left_shoulder and right_wrist and left_wrist:
            distance_threshold = calculate_distance_between_landmakrs(right_shoulder, left_shoulder)
            if calculate_distance_between_landmakrs(right_wrist, left_wrist) > distance_threshold * 1.5:
                feedback += "Bring arms closer !\n"
        
        # Check back alignment
        visible_shoulders = [s for s in [right_shoulder, left_shoulder] if s is not None]
        visible_hips = [h for h in [right_hip, left_hip] if h is not None]
        visible_knees = [k for k in [right_knee, left_knee] if k is not None]
        
        if not visible_shoulders or not visible_hips or not visible_knees:
            return feedback if feedback else "Good Form"
        
        if len(visible_shoulders) == 1:
            active_shoulder = visible_shoulders[0]
        else:
            active_shoulder = visible_shoulders[0]  # Use first one since we can't average landmarks
            
        if len(visible_hips) == 1:
            active_hip = visible_hips[0]
        else:
            active_hip = visible_hips[0]
            
        if len(visible_knees) == 1:
            active_knee = visible_knees[0]
        else:
            active_knee = visible_knees[0]
        
        back_angle = calculate_joint_angle(active_shoulder, active_hip, active_knee)
        if back_angle < 150:
            feedback += "Straighten Back !"
        
        if feedback == "":
            feedback = "Good Form"
        return feedback
