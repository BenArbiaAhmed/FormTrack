from enum import Enum
from collections import deque
from typing import Dict, Tuple, Optional

class ExercisePhase(Enum):
    """Phases for exercise state machine"""
    START = "start"
    TRANSITION = "transition"
    PEAK = "peak"

class RepType(Enum):
    """Types of reps detected"""
    FULL = "full"
    PARTIAL = "partial"
    NONE = "none"

class ExerciseTemplate:
    """Base template for exercises"""
    def __init__(self, name: str, key_angles: Dict[str, int]):
        self.name = name
        self.key_angles = key_angles
        self.last_phase = None
        self.last_rep_type = None
        self.rep_count = 0
        self.phase_history = deque(maxlen=5)
    
    def check_phase(self, angles: Dict[str, float]) -> ExercisePhase:
        pass

    def detect_common_mistakes(self, angles: Dict[str, float]) -> str:
        pass
    
    def update(self, angles: Dict[str, float]) -> Tuple[int, int, ExercisePhase, RepType]:
        """Update state machine and return full reps, partial reps, current phase, and rep type"""
        current_phase = self.check_phase(angles)
        rep_type = RepType.NONE
        
        if current_phase is not None and current_phase != self.last_phase:
            self.phase_history.append(current_phase)
            self.last_phase = current_phase 
            rep_type = self.updateRepCount()
            
        return self.rep_count, current_phase, rep_type

    def updateRepCount(self) -> RepType:
        """Check for full or partial reps"""
        if len(self.phase_history) >= 5:
            if self._check_sequence([ExercisePhase.START, ExercisePhase.TRANSITION, 
                                    ExercisePhase.PEAK, ExercisePhase.TRANSITION, 
                                    ExercisePhase.START], 0):
                self.rep_count += 1
                self.last_rep_type = RepType.FULL
                for i in range(4):
                    self.phase_history.popleft()
                return RepType.FULL
        
        if len(self.phase_history) >= 3:
            for i in range(len(self.phase_history) - 2):
                if self._check_sequence([ExercisePhase.START, ExercisePhase.TRANSITION, 
                                        ExercisePhase.START], i):
                    self.last_rep_type = RepType.PARTIAL
                    for _ in range(2):
                        self.phase_history.popleft()
                    return RepType.PARTIAL
        
        return RepType.NONE
    
    def _check_sequence(self, target_sequence: list, start_idx: int) -> bool:
        """Helper to check if sequence exists at given position"""
        if start_idx + len(target_sequence) > len(self.phase_history):
            return False
        
        phase_list = list(self.phase_history)
        for i, phase in enumerate(target_sequence):
            if phase_list[start_idx + i] != phase:
                return False
        return True