"""
Evalúa el modelo Sentence Transformer fine-tuneado
sobre un dataset de evaluación independiente.

Utiliza:
    results/manual_review2.csv

Todas las preguntas del CSV se utilizan únicamente
para evaluación y no fueron utilizadas durante el
fine-tuning.

Guarda:
    results/fine_tuned_results.txt
"""

import csv
from pathlib import Path

from app.embedding_classifier import EmbeddingClassifier
from app.categories import get_category_names


# ============================================================
# CONFIGURACIÓN
# ============================================================

CSV_FILE = Path(
    "results/manual_review2.csv"
)

MODEL_PATH = "models/minecraft-embedding"

OUTPUT_FILE = Path(
    "results/fine_tuned_results.txt"
)


# ============================================================
# CARGAR DATASET
# ============================================================

def load_dataset():

    data = []

    with open(
        CSV_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            question = row["question"].strip()
            category = row["human_category"].strip()

            if not question or not category:
                continue

            data.append({
                "question_id": row["question_id"],
                "question": question,
                "category": category,
            })

    return data


# ============================================================
# EVALUACIÓN
# ============================================================

def evaluate_model(
    classifier,
    test_data,
    categories,
):

    results = []

    for item in test_data:

        result = classifier.classify(
            text=item["question"],
            candidate_labels=categories,
        )

        predicted_category = result.category_name
        human_category = item["category"]

        correct = (
            predicted_category == human_category
        )

        results.append({
            "question_id": item["question_id"],
            "question": item["question"],
            "human_category": human_category,
            "predicted_category": predicted_category,
            "confidence": result.confidence_score,
            "correct": correct,
        })

    return results


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("EVALUACIÓN DEL MODELO FINE-TUNEADO")
    print("=" * 70)

    # --------------------------------------------------------
    # Verificar archivos
    # --------------------------------------------------------

    if not CSV_FILE.exists():

        print(
            f"\n❌ No se encontró:"
            f"\n{CSV_FILE}"
        )

        return

    if not Path(MODEL_PATH).exists():

        print(
            f"\n❌ No se encontró el modelo:"
            f"\n{MODEL_PATH}"
        )

        return

    # --------------------------------------------------------
    # Cargar dataset
    # --------------------------------------------------------

    data = load_dataset()

    print(
        f"\nPreguntas a evaluar: {len(data)}"
    )

    # --------------------------------------------------------
    # Cargar categorías
    # --------------------------------------------------------

    categories = get_category_names()

    print(
        f"\nCategorías: {categories}"
    )

    # --------------------------------------------------------
    # Cargar modelo fine-tuneado
    # --------------------------------------------------------

    print(
        f"\nCargando modelo fine-tuneado:"
        f"\n{MODEL_PATH}"
    )

    classifier = EmbeddingClassifier(
        model_name=MODEL_PATH
    )

    print("\n✓ Modelo cargado")

    # --------------------------------------------------------
    # Evaluar
    # --------------------------------------------------------

    print(
        "\nEvaluando preguntas de "
        "manual_review2.csv..."
    )

    results = evaluate_model(
        classifier=classifier,
        test_data=data,
        categories=categories,
    )

    # --------------------------------------------------------
    # Calcular precisión
    # --------------------------------------------------------

    total = len(results)

    correct = sum(
        1
        for result in results
        if result["correct"]
    )

    errors = total - correct

    accuracy = (
        correct / total
        if total > 0
        else 0
    )

    # --------------------------------------------------------
    # Crear carpeta
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )

    # --------------------------------------------------------
    # Guardar TXT
    # --------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "EVALUACIÓN DEL MODELO FINE-TUNEADO\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            "Modelo: models/minecraft-embedding\n"
        )

        file.write(
            "Método: Sentence Transformers + fine-tuning\n"
        )

        file.write(
            "Dataset: results/manual_review2.csv\n"
        )

        file.write(
            f"Preguntas evaluadas: {total}\n\n"
        )

        file.write(
            "=" * 70 + "\n"
        )

        file.write(
            "RESULTADO\n"
        )

        file.write(
            "=" * 70 + "\n\n"
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

        # ----------------------------------------------------
        # Detalle de preguntas
        # ----------------------------------------------------

        for result in results:

            file.write(
                "=" * 70 + "\n"
            )

            file.write(
                f"ID: {result['question_id']}\n"
            )

            file.write(
                f"Pregunta: {result['question']}\n"
            )

            file.write(
                f"Humano: {result['human_category']}\n"
            )

            file.write(
                f"Fine-tuned: "
                f"{result['predicted_category']}\n"
            )

            file.write(
                f"Similitud: "
                f"{result['confidence']:.4f}\n"
            )

            file.write(
                f"Correcto: "
                f"{result['correct']}\n\n"
            )

        # ----------------------------------------------------
        # Resumen final
        # ----------------------------------------------------

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
            f"Total evaluadas: {total}\n"
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

    # --------------------------------------------------------
    # Mostrar resultado
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)

    print(
        f"Total evaluadas: {total}"
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
        f"\n✓ Resultado guardado en:"
        f"\n{OUTPUT_FILE}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()