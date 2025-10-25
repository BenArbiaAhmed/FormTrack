import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from collections import deque

class ExercisePhase(Enum):
    """Phases for exercise state machine"""
    START = "start"
    TRANSITION = "transition"
    PEAK = "peak"


class ExerciseTemplate:
    """Base template for exercises"""
    def __init__(self, name: str, key_angles: Dict[str, int]):
        self.name = name
        self.key_angles = key_angles
        self.last_phase = None
        self.rep_count = 0
        self.phase_history = deque(maxlen=5)
    
    def check_phase(self, angles: Dict[str, float]) -> ExercisePhase:
        pass
    
    def update(self, angles: Dict[str, float]) -> Tuple[int, ExercisePhase]:
        """Update state machine and return rep count and current phase"""
        current_phase = self.check_phase(angles)
        if current_phase is not None and current_phase != self.last_phase:
            self.phase_history.append(current_phase)
            self.last_phase = current_phase 
            self.updateRepCount()
        return self.rep_count, current_phase

    def updateRepCount(self):
        if len(self.phase_history) >= 5:
            if (self.phase_history[0] == ExercisePhase.START and self.phase_history[1] == ExercisePhase.TRANSITION and self.phase_history[2] == ExercisePhase.PEAK and self.phase_history[3] == ExercisePhase.TRANSITION and self.phase_history[4] == ExercisePhase.START):
                self.rep_count += 1
                for i in range(4):
                    self.phase_history.popleft()
                