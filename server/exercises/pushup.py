from exercise import *

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
