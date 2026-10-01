"""
Script principal de categorización.

Orquesta el flujo:
1. Carga las preguntas sin categorizar de la BD.
2. Clasifica las preguntas usando EmbeddingClassifier.
3. Si la confianza es menor al 55%, solicita revisión humana.
4. Guarda la categorización final en la BD.
5. Guarda las correcciones humanas en results/manual_review.csv.
6. Al finalizar, muestra cuántas preguntas quedan sin categorizar.
"""

import csv
import os

from tqdm import tqdm

from app.database import SessionLocal
from app.models import Question, Categorization
from app.categories import get_category_names
from app.embedding_classifier import EmbeddingClassifier
from app.human_review import review_question, REVIEW_THRESHOLD


MANUAL_REVIEW_FILE = "results/manual_review.csv"


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


def count_uncategorized_questions(db) -> int:
    """
    Cuenta cuántas preguntas todavía no tienen una categorización,
    sin traer los objetos completos (más liviano que
    get_uncategorized_questions cuando solo necesitamos el número).
    """

    subquery = db.query(Categorization.question_id)

    count = (
        db.query(Question)
        .filter(~Question.id.in_(subquery))
        .count()
    )

    return count


def save_categorization(
    db,
    question_id: int,
    category_name: str,
    confidence_score: float,
    is_automatic: bool,
) -> None:
    """
    Guarda una categorización en la base de datos.
    """

    try:
        categorization = Categorization(
            question_id=question_id,
            category_name=category_name,
            confidence_score=confidence_score,
            is_automatic=is_automatic,
        )

        db.add(categorization)
        db.commit()

    except Exception:
        db.rollback()
        raise


def save_manual_review(
    question_id: int,
    question_text: str,
    ai_category: str,
    ai_confidence: float,
    human_category: str | None,
    was_corrected: bool,
    was_skipped: bool,
) -> None:
    """
    Guarda una revisión humana en results/manual_review.csv.
    """

    os.makedirs(
        os.path.dirname(MANUAL_REVIEW_FILE),
        exist_ok=True,
    )

    file_exists = os.path.exists(MANUAL_REVIEW_FILE)

    with open(
        MANUAL_REVIEW_FILE,
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(
                [
                    "question_id",
                    "question",
                    "ai_category",
                    "ai_confidence",
                    "human_category",
                    "was_corrected",
                    "was_skipped",
                ]
            )

        writer.writerow(
            [
                question_id,
                question_text,
                ai_category,
                ai_confidence,
                human_category,
                was_corrected,
                was_skipped,
            ]
        )


def categorize_all() -> None:
    """
    Clasifica todas las preguntas pendientes.
    """

    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. CARGAR CATEGORÍAS
        # ---------------------------------------------------------

        category_names = get_category_names()

        # ---------------------------------------------------------
        # 2. CREAR CLASIFICADOR
        # ---------------------------------------------------------

        classifier = EmbeddingClassifier()

        # ---------------------------------------------------------
        # 3. OBTENER PREGUNTAS
        # ---------------------------------------------------------

        questions = get_uncategorized_questions(db)

        total = len(questions)

        categorized_count = 0
        manual_review_count = 0
        corrected_count = 0
        skipped_count = 0

        # ---------------------------------------------------------
        # 4. RESUMEN INICIAL
        # ---------------------------------------------------------

        print("\n" + "=" * 64)
        print("CATEGORIZACIÓN AUTOMÁTICA - EMBEDDING")
        print("=" * 64)

        print(f"Preguntas pendientes: {total}")

        print(
            f"Categorías disponibles: "
            f"{', '.join(category_names)}"
        )

        print(
            f"Umbral de revisión humana: "
            f"{REVIEW_THRESHOLD:.0%}"
        )

        print("=" * 64 + "\n")

        if total == 0:
            print(
                "No hay preguntas pendientes de categorizar."
            )
            return

        # ---------------------------------------------------------
        # 5. PROCESAR PREGUNTAS
        # ---------------------------------------------------------

        for question in tqdm(
            questions,
            desc="Categorizando",
        ):

            result = classifier.classify(
                text=question.question,
                candidate_labels=category_names,
            )

            # -----------------------------------------------------
            # 6. REVISIÓN HUMANA SI CONFIANZA < 55%
            # -----------------------------------------------------

            review = review_question(
                question_text=question.question,
                ai_suggestion=result.category_name,
                confidence=result.confidence_score,
                category_names=category_names,
                threshold=REVIEW_THRESHOLD,
                all_scores=result.all_scores,
            )

            # -----------------------------------------------------
            # 7. SI HUBO SKIP
            # -----------------------------------------------------

            if review.was_skipped:

                save_manual_review(
                    question_id=question.id,
                    question_text=question.question,
                    ai_category=result.category_name,
                    ai_confidence=result.confidence_score,
                    human_category=None,
                    was_corrected=False,
                    was_skipped=True,
                )

                skipped_count += 1
                continue

            # -----------------------------------------------------
            # 8. DETERMINAR CATEGORÍA FINAL
            # -----------------------------------------------------

            final_category = review.category_name

            # Esto no debería ocurrir, pero evita guardar None.
            if final_category is None:
                continue

            # -----------------------------------------------------
            # 9. DETERMINAR SI FUE AUTOMÁTICA O HUMANA
            # -----------------------------------------------------

            was_automatic = not (
                result.confidence_score < REVIEW_THRESHOLD
            )

            # -----------------------------------------------------
            # 10. GUARDAR CATEGORIZACIÓN
            # -----------------------------------------------------

            save_categorization(
                db=db,
                question_id=question.id,
                category_name=final_category,
                confidence_score=result.confidence_score,
                is_automatic=was_automatic,
            )

            categorized_count += 1

            # -----------------------------------------------------
            # 11. GUARDAR REVISIÓN HUMANA
            # -----------------------------------------------------

            if result.confidence_score < REVIEW_THRESHOLD:

                manual_review_count += 1

                if review.was_corrected:
                    corrected_count += 1

                save_manual_review(
                    question_id=question.id,
                    question_text=question.question,
                    ai_category=result.category_name,
                    ai_confidence=result.confidence_score,
                    human_category=final_category,
                    was_corrected=review.was_corrected,
                    was_skipped=False,
                )

        # ---------------------------------------------------------
        # 12. RESUMEN FINAL
        # ---------------------------------------------------------

        # Se vuelve a consultar la BD (en lugar de asumir
        # remaining == skipped_count) para que el número refleje el
        # estado real, incluso si algo falló al guardar en el medio.
        remaining_count = count_uncategorized_questions(db)

        print("\n" + "=" * 64)
        print("RESUMEN FINAL")
        print("=" * 64)

        print(f"Total procesadas: {total}")
        print(
            f"Categorizadas: {categorized_count}"
        )
        print(
            f"Revisiones humanas: {manual_review_count}"
        )
        print(
            f"Correcciones humanas: {corrected_count}"
        )
        print(
            f"Preguntas omitidas: {skipped_count}"
        )
        print(
            f"Preguntas que faltan categorizar: {remaining_count}"
        )

        print(
            f"\nRevisiones guardadas en: "
            f"{MANUAL_REVIEW_FILE}"
        )

        print("=" * 64)

    finally:
        db.close()


if __name__ == "__main__":
    categorize_all()