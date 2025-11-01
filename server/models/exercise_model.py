from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from server.models.base_model import Base
import enum
from sqlalchemy import Enum
from sqlalchemy import Enum as SQLAlchemyEnum


class ExerciseName(enum.Enum):
    squat = "squat"
    pushup = "pushup"
    tricep_dip = "tricep_dip"

class Exercise(Base):
    __tablename__ = "exercise"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[ExerciseName] = mapped_column(
        SQLAlchemyEnum(ExerciseName),
        nullable=False
    )
    workout_id: Mapped[int] = mapped_column(ForeignKey("workout.id"))
    workout: Mapped["Workout"] = relationship(back_populates="exercises")
    duration: Mapped[int] = mapped_column(nullable=False)
    repetitions: Mapped[int] = mapped_column(nullable=False)
    partial_reps: Mapped[Optional[int]] = mapped_column(nullable=True)