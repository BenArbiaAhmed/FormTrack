import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

class ExercisePhase(Enum):
    """Phases for exercise state machine"""
    IDLE = "idle"
    DOWN = "down"
    UP = "up"


class AngleThreshold:
    """Angle thresholds for exercise phases"""
    down_min: float
    down_max: float
    up_min: float
    up_max: float

class ExerciseTemplate:
    """Base template for exercises"""
    def __init__(self, name: str, key_angles: Dict[str, AngleThreshold]):
        self.name = name
        self.key_angles = key_angles
        self.phase = ExercisePhase.IDLE
        self.rep_count = 0
        self.phase_history = []
        self.confidence_threshold = 0.5
    
    def check_phase(self, angles: Dict[str, float]) -> ExercisePhase:
        pass
    
    def update(self, angles: Dict[str, float]) -> Tuple[int, ExercisePhase]:
        """Update state machine and return rep count and current phase"""
        current_phase = self.check_phase(angles)
        
    
        if self.phase == ExercisePhase.IDLE:
            if current_phase == ExercisePhase.DOWN:
                self.phase = ExercisePhase.DOWN
                
        elif self.phase == ExercisePhase.DOWN:
            if current_phase == ExercisePhase.UP:
                self.phase = ExercisePhase.UP
                self.rep_count += 1
                
        elif self.phase == ExercisePhase.UP:
            if current_phase == ExercisePhase.DOWN:
                self.phase = ExercisePhase.DOWN
        
        self.phase_history.append(self.phase)
        return self.rep_count, self.phase