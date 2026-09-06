from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    source = Column(String(255), nullable=True)

class Categorization(Base):
    """
    Registra la categorización de cada pregunta.
    Guarda tanto las decisiones automáticas de la IA como las manuales del humano.
    """

    __tablename__ = "categorizations"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    category_name = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    is_automatic = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    question = relationship("Question", backref="categorizations")