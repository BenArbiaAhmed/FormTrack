from exercise import *

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

