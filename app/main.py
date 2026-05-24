from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import Base, Question
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional

class QuestionCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    source: Optional[str] = None

app = FastAPI(title="Questions API", version="1.0.0")

@app.post("/questions")
def create_question(data: QuestionCreate, db: Session = Depends(get_db)):
    question = Question(
        question=data.question,
        answer=data.answer,
        category=data.category,
        source=data.source,
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Questions API funcionando", "endpoints": ["/questions", "/questions/{id}"]}


@app.get("/questions")
def list_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    questions = db.query(Question).offset(skip).limit(limit).all()
    return questions

@app.get("/questions/category/{category}")
def get_by_category(category: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    questions = (
        db.query(Question)
        .filter(Question.category.ilike(f"%{category}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )
    if not questions:
        return {"error": f"No se encontraron preguntas para la categoría '{category}'"}
    return questions

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Question.id)).scalar()
    by_category = (
        db.query(Question.category, func.count(Question.id))
        .group_by(Question.category)
        .all()
    )
    return {
        "total": total,
        "by_category": [{"category": cat, "count": count} for cat, count in by_category]
    }

@app.get("/questions/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return {"error": "Pregunta no encontrada"}
    return question
