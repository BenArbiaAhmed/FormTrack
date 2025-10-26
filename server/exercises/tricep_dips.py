from exercise import *
from utils.landmarks_utils import calculate_distance_between_landmakrs

class TricepDips(ExerciseTemplate):

    def __init__(self):
        super().__init__(name='tricep_dips', key_angles={'shoulder_elbow_wrist': 110, 'asymmetry': 15, 'extended_arm': 140})


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
        
    def detect_common_mistakes(self, angles):
        right_shoulder = angles.get("right_shoulder")
        left_shoulder = angles.get("left_shoulder")
        distance_threshold = calculate_distance_between_landmakrs(right_shoulder, left_shoulder)
        right_wrist = angles.get("right_wrist")
        left_wrist = angles.get("left_wrist")
        feedback=""
        if(calculate_distance_between_landmakrs(right_wrist, left_wrist) > distance_threshold):
            feedback = "Bring arms closer !\n"
        return feedback
