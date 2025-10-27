from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from server.models.base_model import Base

class Workout(Base):
    __tablename__ = "workout"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    duration: Mapped[int] = mapped_column(nullable=False)
    exercises: Mapped[List["Exercise"]] = relationship(
        back_populates="workout", cascade="all, delete-orphan"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="workouts")