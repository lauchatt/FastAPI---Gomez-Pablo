"""
Evalúa Zero-Shot sobre las mismas preguntas
revisadas manualmente.

Utiliza:
    results/manual_review.csv

para obtener:
    - question_id
    - human_category

Genera:
    results/zero_shot_results.txt
"""

import csv
from pathlib import Path

from app.zero_shot_classifier import AIClassifier
from app.categories import get_category_names
from app.database import SessionLocal
from app.models import Question


MANUAL_REVIEW_FILE = Path(
    "results/manual_review2.csv"
)


def load_manual_reviews():
    """
    Carga las revisiones humanas.

    Retorna:
        question_id -> datos de la revisión
    """

    reviews = {}

    with open(
        MANUAL_REVIEW_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            question_id = int(row["question_id"])

            reviews[question_id] = row

    return reviews


def main():

    print("EVALUACIÓN ZERO-SHOT")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Verificar CSV
    # ---------------------------------------------------------

    if not MANUAL_REVIEW_FILE.exists():

        print(
            f"No se encontró: {MANUAL_REVIEW_FILE}"
        )

        return

    # ---------------------------------------------------------
    # 2. Cargar revisiones humanas
    # ---------------------------------------------------------

    manual_reviews = load_manual_reviews()

    print(
        f"Preguntas revisadas manualmente: "
        f"{len(manual_reviews)}"
    )

    # ---------------------------------------------------------
    # 3. Crear carpeta de resultados
    # ---------------------------------------------------------

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    output_txt = (
        results_dir /
        "zero_shot_results.txt"
    )


    # ---------------------------------------------------------
    # 4. Cargar clasificador
    # ---------------------------------------------------------

    classifier = AIClassifier()

    categories = get_category_names()

    print(
        f"Categorías: {categories}"
    )

    # ---------------------------------------------------------
    # 5. Obtener las mismas preguntas de la BD
    # ---------------------------------------------------------

    db = SessionLocal()

    try:

        question_ids = list(
            manual_reviews.keys()
        )

        questions = (
            db.query(Question)
            .filter(
                Question.id.in_(question_ids)
            )
            .all()
        )

    finally:

        db.close()

    # Mantener el orden del CSV
    questions_by_id = {
        question.id: question
        for question in questions
    }

    questions = [
        questions_by_id[question_id]
        for question_id in question_ids
        if question_id in questions_by_id
    ]

    print(
        f"Preguntas encontradas en BD: "
        f"{len(questions)}"
    )

    # ---------------------------------------------------------
    # 6. Clasificación
    # ---------------------------------------------------------

    results = []

    for question in questions:

        result = classifier.classify(
            text=question.question,
            candidate_labels=categories,
        )

        human_category = manual_reviews[
            question.id
        ]["human_category"]

        correct = (
            result.category_name ==
            human_category
        )

        results.append(
            (
                question,
                result,
                human_category,
                correct,
            )
        )

        print("\n" + "=" * 70)
        print(f"ID: {question.id}")
        print(f"Pregunta: {question.question}")
        print(f"Humano: {human_category}")
        print(f"Zero-Shot: {result.category_name}")
        print(
            f"Confianza: "
            f"{result.confidence_score:.2%}"
        )
        print(
            f"Correcto: "
            f"{'SI' if correct else 'NO'}"
        )

    # ---------------------------------------------------------
    # 7. Calcular precisión
    # ---------------------------------------------------------

    total = len(results)

    correct_count = sum(
        1
        for _, _, _, correct in results
        if correct
    )

    error_count = total - correct_count

    accuracy = (
        correct_count / total
        if total > 0
        else 0
    )

    # ---------------------------------------------------------
    # 9. Guardar TXT
    # ---------------------------------------------------------

    with open(
        output_txt,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "RESULTADOS - ZERO-SHOT CLASSIFICATION\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            "Modelo: facebook/bart-large-mnli\n"
        )

        file.write(
            "Método: Zero-Shot Classification\n"
        )

        file.write(
            f"Preguntas evaluadas: {total}\n\n"
        )

        # Resultados individuales

        for (
            question,
            result,
            human_category,
            correct,
        ) in results:

            file.write(
                "=" * 70 + "\n"
            )

            file.write(
                f"ID: {question.id}\n"
            )

            file.write(
                f"Pregunta: {question.question}\n"
            )

            file.write(
                f"Humano: {human_category}\n"
            )

            file.write(
                f"Zero-Shot: "
                f"{result.category_name}\n"
            )

            file.write(
                f"Confianza: "
                f"{result.confidence_score:.2%}\n"
            )

            file.write(
                f"Correcto: "
                f"{correct}\n"
            )

            file.write("\n")

        # Resumen

        file.write("\n")
        file.write("=" * 70 + "\n")
        file.write("RESUMEN\n")
        file.write("=" * 70 + "\n")

        file.write(
            f"Preguntas evaluadas: {total}\n"
        )

        file.write(
            f"Aciertos: {correct_count}\n"
        )

        file.write(
            f"Errores: {error_count}\n"
        )

        file.write(
            f"Precisión: {accuracy:.2%}\n"
        )

    # ---------------------------------------------------------
    # 10. Mostrar resumen
    # ---------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RESULTADO FINAL - ZERO-SHOT")
    print("=" * 70)

    print(
        f"Preguntas evaluadas: {total}"
    )

    print(
        f"Aciertos: {correct_count}"
    )

    print(
        f"Errores: {error_count}"
    )

    print(
        f"Precisión: {accuracy:.2%}"
    )

    print(
        f"Resultados: {output_txt}"
    )


if __name__ == "__main__":
    main()