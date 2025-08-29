from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from .base import Base, created_at

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[created_at]
    
    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    
class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str]
    text: Mapped[str]
    created_at: Mapped[created_at]