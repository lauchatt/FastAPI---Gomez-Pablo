"""
Script principal de categorización automática.

Orquesta el flujo:
1. Carga las preguntas sin categorizar de la BD.
2. Clasifica las preguntas usando Sentence Transformers.
3. Guarda todas las predicciones automáticamente.
4. No solicita revisión humana.
5. Guarda la categoría y confianza en la tabla categorizations.

La revisión humana se realizará posteriormente sobre una muestra.
"""

from tqdm import tqdm

from app.database import SessionLocal
from app.models import Question, Categorization
from app.categories import get_category_names
from app.embedding_classifier import EmbeddingClassifier


def get_uncategorized_questions(db) -> list:
    """
    Obtiene todas las preguntas que todavía no tienen
    una categorización.
    """

    subquery = db.query(Categorization.question_id)

    questions = (
        db.query(Question)
        .filter(~Question.id.in_(subquery))
        .all()
    )

    return questions


def save_categorization(
    db,
    question_id: int,
    category_name: str,
    confidence_score: float,
) -> None:
    """
    Guarda una categorización automática en la base de datos.
    """

    try:
        categorization = Categorization(
            question_id=question_id,
            category_name=category_name,
            confidence_score=confidence_score,
            is_automatic=True,
        )

        db.add(categorization)
        db.commit()

    except Exception:
        db.rollback()
        raise


def categorize_all() -> None:
    """
    Clasifica automáticamente todas las preguntas pendientes.
    """

    db = SessionLocal()

    try:
        # 1. Cargar categorías
        category_names = get_category_names()

        # 2. Crear clasificador Embeddings (modelo base)
        classifier = EmbeddingClassifier()

        # 3. Obtener preguntas pendientes
        questions = get_uncategorized_questions(db)

        total = len(questions)

        # Contadores
        categorized_count = 0

        # 4. Mostrar resumen inicial
        print("\n" + "=" * 64)
        print("CATEGORIZACIÓN AUTOMÁTICA - EMBEDDING")
        print("=" * 64)

        print(f"Preguntas pendientes: {total}")

        print(
            f"Categorías disponibles: "
            f"{', '.join(category_names)}"
        )

        print("=" * 64 + "\n")

        if total == 0:
            print("No hay preguntas pendientes de categorizar.")
            return

        # 5. Procesar todas las preguntas
        for question in tqdm(
            questions,
            desc="Categorizando"
        ):

            result = classifier.classify(
                text=question.question,
                candidate_labels=category_names,
            )

            # 6. Guardar SIEMPRE la predicción
            save_categorization(
                db=db,
                question_id=question.id,
                category_name=result.category_name,
                confidence_score=result.confidence_score,
            )

            categorized_count += 1

        # 7. Resumen final
        print("\n" + "=" * 64)
        print("RESUMEN FINAL")
        print("=" * 64)

        print(f"Total procesadas: {total}")
        print(f"Categorizadas automáticamente: {categorized_count}")

        print("=" * 64)

    finally:
        db.close()


if __name__ == "__main__":
    categorize_all()