
"""
Fine-tuning de Sentence Transformers usando las revisiones humanas.

Utiliza:
    results/manual_review.csv

El dataset se divide en:
    80% entrenamiento
    20% evaluación

El modelo se entrena para acercar las preguntas a su categoría
correcta y alejar las preguntas de categorías incorrectas.

Guarda los resultados en:
    results/fine_tuning_results.txt
"""

import csv
import random
from pathlib import Path

from sentence_transformers import (
    SentenceTransformer,
    InputExample,
    losses,
)
from torch.utils.data import DataLoader


# ============================================================
# CONFIGURACIÓN
# ============================================================

CSV_FILE = Path("results/manual_review.csv")

MODEL_NAME = "all-MiniLM-L6-v2"

OUTPUT_DIR = Path("models/questions-embedding")

RESULTS_DIR = Path("results")

RESULTS_TXT = RESULTS_DIR / "fine_tuning_results.txt"

TRAIN_RATIO = 0.80

EPOCHS = 3

BATCH_SIZE = 8

SEED = 42


# ============================================================
# CARGAR DATASET
# ============================================================

def load_dataset():
    """
    Carga las preguntas y categorías humanas desde el CSV.
    """

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
                "question": question,
                "category": category,
            })

    return data


# ============================================================
# DIVISIÓN TRAIN / TEST
# ============================================================

def split_dataset(data):
    """
    Divide el dataset manteniendo la proporción de categorías.
    """

    random.seed(SEED)

    categories = {}

    for item in data:

        category = item["category"]

        if category not in categories:
            categories[category] = []

        categories[category].append(item)

    train_data = []
    test_data = []

    for category, items in categories.items():

        random.shuffle(items)

        split_index = max(
            1,
            int(len(items) * TRAIN_RATIO)
        )

        train_data.extend(
            items[:split_index]
        )

        test_data.extend(
            items[split_index:]
        )

    random.shuffle(train_data)
    random.shuffle(test_data)

    return train_data, test_data


# ============================================================
# CREAR EJEMPLOS DE ENTRENAMIENTO
# ============================================================

def create_training_examples(
    train_data,
    categories,
):
    """
    Crea pares:

        pregunta + categoría correcta

    utilizando ejemplos positivos y negativos.
    """

    examples = []

    for item in train_data:

        question = item["question"]
        correct_category = item["category"]

        # Ejemplo positivo
        examples.append(
            InputExample(
                texts=[
                    question,
                    correct_category,
                ],
                label=1.0,
            )
        )

        # Ejemplo negativo
        negative_categories = [
            category
            for category in categories
            if category != correct_category
        ]

        if negative_categories:

            negative_category = random.choice(
                negative_categories
            )

            examples.append(
                InputExample(
                    texts=[
                        question,
                        negative_category,
                    ],
                    label=0.0,
                )
            )

    return examples


# ============================================================
# EVALUACIÓN
# ============================================================

def evaluate_model(
    model,
    test_data,
    categories,
):
    """
    Evalúa qué categoría obtiene mayor similitud
    para cada pregunta.

    También devuelve el detalle de cada evaluación.
    """

    correct = 0

    evaluation_results = []

    # Calcular embeddings de categorías una sola vez
    category_embeddings = model.encode(
        categories,
        normalize_embeddings=True,
    )

    for item in test_data:

        question = item["question"]
        human_category = item["category"]

        question_embedding = model.encode(
            question,
            normalize_embeddings=True,
        )

        scores = []

        for category_embedding in category_embeddings:

            score = float(
                question_embedding
                @ category_embedding
            )

            scores.append(score)

        predicted_category = categories[
            scores.index(max(scores))
        ]

        is_correct = (
            predicted_category == human_category
        )

        if is_correct:
            correct += 1

        evaluation_results.append({
            "question": question,
            "human_category": human_category,
            "predicted_category": predicted_category,
            "correct": is_correct,
        })

    total = len(test_data)

    accuracy = (
        correct / total
        if total > 0
        else 0
    )

    return (
        correct,
        total,
        accuracy,
        evaluation_results,
    )


# ============================================================
# GUARDAR RESULTADOS
# ============================================================

def save_results(
    correct,
    total,
    accuracy,
    evaluation_results,
    train_total,
):
    """
    Guarda los resultados de la evaluación en un TXT.
    """

    RESULTS_DIR.mkdir(
        exist_ok=True
    )

    with open(
        RESULTS_TXT,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "RESULTADOS - FINE-TUNING\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            f"Modelo base: {MODEL_NAME}\n"
        )

        file.write(
            f"Modelo fine-tuneado: {OUTPUT_DIR}\n"
        )

        file.write(
            f"Epochs: {EPOCHS}\n"
        )

        file.write(
            f"Batch size: {BATCH_SIZE}\n"
        )

        file.write(
            f"Seed: {SEED}\n\n"
        )

        file.write(
            "DATOS DEL ENTRENAMIENTO\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        file.write(
            f"Preguntas utilizadas para entrenamiento: "
            f"{train_total}\n"
        )

        file.write(
            f"Preguntas utilizadas para evaluación: "
            f"{total}\n\n"
        )

        file.write(
            "RESULTADO\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        file.write(
            f"Preguntas evaluadas: {total}\n"
        )

        file.write(
            f"Aciertos: {correct}\n"
        )

        file.write(
            f"Errores: {total - correct}\n"
        )

        file.write(
            f"Precisión: {accuracy:.2%}\n\n"
        )

        file.write(
            "=" * 70 + "\n"
        )

        file.write(
            "DETALLE DE LAS PREGUNTAS EVALUADAS\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        for index, result in enumerate(
            evaluation_results,
            start=1,
        ):

            file.write(
                f"Pregunta {index}\n"
            )

            file.write(
                f"Texto: {result['question']}\n"
            )

            file.write(
                f"Categoría humana: "
                f"{result['human_category']}\n"
            )

            file.write(
                f"Categoría predicha: "
                f"{result['predicted_category']}\n"
            )

            file.write(
                f"Correcto: "
                f"{result['correct']}\n"
            )

            file.write(
                "-" * 70 + "\n\n"
            )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("FINE-TUNING - SENTENCE TRANSFORMERS")
    print("=" * 70)

    # --------------------------------------------------------
    # Verificar CSV
    # --------------------------------------------------------

    if not CSV_FILE.exists():

        print(
            f"\n❌ No se encontró el archivo:"
            f"\n{CSV_FILE}"
        )

        return

    # --------------------------------------------------------
    # Cargar dataset
    # --------------------------------------------------------

    data = load_dataset()

    print(
        f"\nPreguntas disponibles: {len(data)}"
    )

    # --------------------------------------------------------
    # Categorías
    # --------------------------------------------------------

    categories = sorted(
        set(
            item["category"]
            for item in data
        )
    )

    print(
        f"Categorías encontradas: {len(categories)}"
    )

    for category in categories:

        count = sum(
            1
            for item in data
            if item["category"] == category
        )

        print(
            f"  {category:<12} → {count}"
        )

    # --------------------------------------------------------
    # Dividir dataset
    # --------------------------------------------------------

    train_data, test_data = split_dataset(data)

    print("\nDivisión del dataset:")

    print(
        f"  Entrenamiento: {len(train_data)}"
    )

    print(
        f"  Evaluación:    {len(test_data)}"
    )

    # --------------------------------------------------------
    # Cargar modelo
    # --------------------------------------------------------

    print(
        f"\nCargando modelo: {MODEL_NAME}"
    )

    model = SentenceTransformer(
        MODEL_NAME
    )

    # --------------------------------------------------------
    # Crear ejemplos
    # --------------------------------------------------------

    train_examples = create_training_examples(
        train_data=train_data,
        categories=categories,
    )

    print(
        f"\nEjemplos de entrenamiento: "
        f"{len(train_examples)}"
    )

    # --------------------------------------------------------
    # DataLoader
    # --------------------------------------------------------

    train_dataloader = DataLoader(
        train_examples,
        shuffle=True,
        batch_size=BATCH_SIZE,
    )

    # --------------------------------------------------------
    # Loss
    # --------------------------------------------------------

    train_loss = losses.CosineSimilarityLoss(
        model=model
    )

    # --------------------------------------------------------
    # Fine-tuning
    # --------------------------------------------------------

    print("\nIniciando fine-tuning...")

    model.fit(
        train_objectives=[
            (
                train_dataloader,
                train_loss,
            )
        ],
        epochs=EPOCHS,
        warmup_steps=10,
        output_path=str(OUTPUT_DIR),
        show_progress_bar=True,
    )

    print(
        f"\n✓ Modelo guardado en:"
        f"\n{OUTPUT_DIR}"
    )

    # --------------------------------------------------------
    # Evaluación
    # --------------------------------------------------------

    print("\nEvaluando modelo...")

    (
        correct,
        total,
        accuracy,
        evaluation_results,
    ) = evaluate_model(
        model=model,
        test_data=test_data,
        categories=categories,
    )

    # --------------------------------------------------------
    # Guardar resultados
    # --------------------------------------------------------

    save_results(
        correct=correct,
        total=total,
        accuracy=accuracy,
        evaluation_results=evaluation_results,
        train_total=len(train_data),
    )

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RESULTADO DEL FINE-TUNING")
    print("=" * 70)

    print(
        f"Preguntas de evaluación: {total}"
    )

    print(
        f"Aciertos: {correct}"
    )

    print(
        f"Errores: {total - correct}"
    )

    print(
        f"Precisión: {accuracy:.2%}"
    )

    print(
        f"\n✓ Resultados guardados en:"
        f"\n{RESULTS_TXT}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()

