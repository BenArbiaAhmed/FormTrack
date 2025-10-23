from exercise import *

class Squat(ExerciseTemplate):

    def __init__(self):
        super().__init__(name='squat', key_angles={'hip_knee_ankle': 90, 'asymmetry': 15, 'extended_leg': 160})

    
    def check_phase(self, angles):
        if(angles['right_knee'] is not None and angles['left_knee'] is not None):
            if(angles["right_knee"] >= self.key_angles["extended_leg"] and angles["left_knee"] >= self.key_angles["extended_leg"]):
                return ExercisePhase.START
            elif(self.key_angles["hip_knee_ankle"] <= angles["right_knee"] <= self.key_angles["extended_leg"]  and self.key_angles["hip_knee_ankle"] <= angles["left_knee"] <= self.key_angles["extended_leg"]):
                return ExercisePhase.TRANSITION
            elif(angles["right_knee"] <= 90 and angles["left_knee"] <= 90):
                return ExercisePhase.PEAK

