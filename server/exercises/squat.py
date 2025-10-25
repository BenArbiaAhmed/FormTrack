from exercise import *
from utils.landmarks_utils import calculate_distance_between_landmakrs

class Squat(ExerciseTemplate):

    def __init__(self):
        super().__init__(name='squat', key_angles={'hip_knee_ankle': 90, 'asymmetry': 15, 'extended_leg': 160})

    
    def check_phase(self, angles):
        right_knee = angles.get('right_knee')
        left_knee = angles.get('left_knee')
        
        visible_knees = [k for k in [right_knee, left_knee] if k is not None]
        
        if not visible_knees:
            return self.last_phase
        
        if len(visible_knees) == 1:
            active_knee = visible_knees[0]
        else:
            active_knee = sum(visible_knees) / len(visible_knees)
        
        if active_knee >= self.key_angles["extended_leg"]:
            return ExercisePhase.START
        elif active_knee >= self.key_angles["hip_knee_ankle"]:
            return ExercisePhase.TRANSITION
        else:
            return ExercisePhase.PEAK
        
    def detect_common_mistakes(self, angles):
        right_shoulder = angles.get("right_shoulder")
        left_shoulder = angles.get("left_shoulder")
        distance_threshold = calculate_distance_between_landmakrs(right_shoulder, left_shoulder)
        right_ankle = angles.get("right_ankle")
        left_ankle = angles.get("left_ankle")
        if(calculate_distance_between_landmakrs(right_ankle, left_ankle) > distance_threshold):
            feedback = "Bring legs closer !"
        else:
            feedback = "Good Form"
        return feedback

