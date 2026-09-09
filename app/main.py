from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional

from app.database import get_db, engine, Base
from app.models import Question, Categorization
from app.categories import CATEGORIES

class QuestionCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    source: Optional[str] = None

class CategorizationUpdate(BaseModel):
    category_name: str

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
def get_by_category(
    category: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    results = (
        db.query(Question, Categorization)
        .join(
            Categorization,
            Question.id == Categorization.question_id,
        )
        .filter(Categorization.category_name == category)
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not results:
        return {
            "error": f"No se encontraron preguntas categorizadas como '{category}'"
        }

    return [
        {
            "id": question.id,
            "question": question.question,
            "answer": question.answer,
            "source": question.source,
            "category": categorization.category_name,
            "confidence_score": categorization.confidence_score,
            "is_automatic": categorization.is_automatic,
            "created_at": categorization.created_at,
        }
        for question, categorization in results
    ]

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

@app.get("/categories")
def list_categories():
    return CATEGORIES

@app.get("/categories/stats")
def category_stats(db: Session = Depends(get_db)):
    total_questions = db.query(
        func.count(Question.id)
    ).scalar()

    categorized = db.query(
        func.count(Categorization.id)
    ).scalar()

    uncategorized = total_questions - categorized

    automatic = db.query(
        func.count(Categorization.id)
    ).filter(
        Categorization.is_automatic.is_(True)
    ).scalar()

    manual = db.query(
        func.count(Categorization.id)
    ).filter(
        Categorization.is_automatic.is_(False)
    ).scalar()

    category_results = (
        db.query(
            Categorization.category_name,
            func.count(Categorization.id),
        )
        .group_by(Categorization.category_name)
        .all()
    )

    by_category = {
        category_name: count
        for category_name, count in category_results
    }

    return {
        "total_questions": total_questions,
        "categorized": categorized,
        "uncategorized": uncategorized,
        "automatic": automatic,
        "manual": manual,
        "by_category": by_category,
    }

@app.put("/categorizations/{categorization_id}")
def update_categorization(
    categorization_id: int,
    data: CategorizationUpdate,
    db: Session = Depends(get_db),
):
    categorization = (
        db.query(Categorization)
        .filter(Categorization.id == categorization_id)
        .first()
    )

    if not categorization:
        return {
            "error": "Categorización no encontrada"
        }

    valid_categories = [category["name"] for category in CATEGORIES]

    if data.category_name not in valid_categories:
        return {
        "error": f"Categoría inválida: '{data.category_name}'"
        }

    categorization.category_name = data.category_name
    categorization.is_automatic = False

    db.commit()
    db.refresh(categorization)

    return categorization