"""
Evalúa Sentence Transformers sobre las preguntas
revisadas manualmente.

Utiliza:
    results/manual_review2.csv

para obtener:
    - question_id
    - human_category

Guarda:
    results/embeddings_results.txt
"""

import csv
from pathlib import Path

from app.embedding_classifier import EmbeddingClassifier
from app.categories import get_category_names
from app.database import SessionLocal
from app.models import Question


MANUAL_REVIEW_FILE = Path(
    "results/manual_review2.csv"
)


def load_manual_decisions():
    """
    Carga las decisiones humanas del CSV.

    Retorna un diccionario:
        question_id -> datos de la revisión humana
    """

    decisions = {}

    with open(
        MANUAL_REVIEW_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            question_id = int(
                row["question_id"]
            )

            decisions[question_id] = row

    return decisions


def main():

    print("\n" + "=" * 70)
    print("TEST EMBEDDING CLASSIFIER")
    print("=" * 70)

    # ---------------------------------------------------------
    # Verificar CSV
    # ---------------------------------------------------------

    if not MANUAL_REVIEW_FILE.exists():

        print(
            f"\n❌ No se encontró:"
            f"\n{MANUAL_REVIEW_FILE}"
        )

        return

    # ---------------------------------------------------------
    # Cargar decisiones humanas
    # ---------------------------------------------------------

    manual_decisions = load_manual_decisions()

    print(
        f"\nPreguntas a evaluar: "
        f"{len(manual_decisions)}"
    )

    # ---------------------------------------------------------
    # Crear carpeta de resultados
    # ---------------------------------------------------------

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    output_txt = (
        results_dir /
        "embeddings_results.txt"
    )

    # ---------------------------------------------------------
    # Cargar modelo
    # ---------------------------------------------------------

    classifier = EmbeddingClassifier()

    categories = get_category_names()

    print(
        f"\nCategorías: {categories}"
    )

    # ---------------------------------------------------------
    # Obtener las mismas preguntas de la BD
    # ---------------------------------------------------------

    db = SessionLocal()

    try:

        question_ids = list(
            manual_decisions.keys()
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
    # Clasificación
    # ---------------------------------------------------------

    results = []

    for question in questions:

        result = classifier.classify(
            text=question.question,
            candidate_labels=categories,
        )

        human_category = manual_decisions[
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

        sorted_scores = sorted(
            result.all_scores.values(),
            reverse=True,
        )

        difference = (
            sorted_scores[0]
            - sorted_scores[1]
        )

        print("\n" + "=" * 70)
        print(f"ID: {question.id}")
        print(f"Pregunta: {question.question}")
        print(f"Humano: {human_category}")
        print(
            f"Embeddings: "
            f"{result.category_name}"
        )
        print(
            f"Similitud: "
            f"{result.confidence_score:.4f}"
        )
        print(
            f"Diferencia con segunda categoría: "
            f"{difference:.4f}"
        )
        print(
            f"Correcto: "
            f"{'SI' if correct else 'NO'}"
        )

    # ---------------------------------------------------------
    # CALCULAR PRECISIÓN
    # ---------------------------------------------------------

    total = len(results)

    correct = sum(
        1
        for _, _, _, is_correct in results
        if is_correct
    )

    errors = total - correct

    accuracy = (
        correct / total
        if total > 0
        else 0
    )

    # ---------------------------------------------------------
    # Guardar resultados TXT
    # ---------------------------------------------------------

    with open(
        output_txt,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "RESULTADOS - SENTENCE TRANSFORMERS\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            "Modelo: all-MiniLM-L6-v2\n"
        )

        file.write(
            "Método: Embeddings + similitud coseno\n"
        )

        file.write(
            "Dataset: results/manual_review2.csv\n"
        )

        file.write(
            f"Preguntas evaluadas: {total}\n"
        )

        file.write(
            f"Aciertos: {correct}\n"
        )

        file.write(
            f"Errores: {errors}\n"
        )

        file.write(
            f"Precisión: {accuracy:.2%}\n\n"
        )

        # -----------------------------------------------------
        # Detalle de preguntas
        # -----------------------------------------------------

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
                f"Embeddings: "
                f"{result.category_name}\n"
            )

            file.write(
                f"Similitud: "
                f"{result.confidence_score:.4f}\n"
            )

            file.write(
                f"Correcto: "
                f"{correct}\n"
            )

            file.write("\n")

        # -----------------------------------------------------
        # Resumen
        # -----------------------------------------------------

        file.write(
            "=" * 70 + "\n"
        )

        file.write(
            "RESUMEN FINAL\n"
        )

        file.write(
            "=" * 70 + "\n"
        )

        file.write(
            f"Preguntas evaluadas: {total}\n"
        )

        file.write(
            f"Aciertos: {correct}\n"
        )

        file.write(
            f"Errores: {errors}\n"
        )

        file.write(
            f"Precisión: {accuracy:.2%}\n"
        )

    # ---------------------------------------------------------
    # Mostrar resumen
    # ---------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RESULTADO FINAL - EMBEDDINGS")
    print("=" * 70)

    print(
        f"Preguntas evaluadas: {total}"
    )

    print(
        f"Aciertos: {correct}"
    )

    print(
        f"Errores: {errors}"
    )

    print(
        f"Precisión: {accuracy:.2%}"
    )

    print(
        f"\n✓ Resultado:"
        f"\n{output_txt}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()