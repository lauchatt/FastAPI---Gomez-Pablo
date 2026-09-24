"""
Revisión manual de una muestra de preguntas.

Toma preguntas directamente desde la tabla questions,
selecciona una muestra aleatoria y permite asignarles
manualmente una categoría.

El resultado se guarda en manual_review.csv.
"""

import csv
import os
import random

from app.database import SessionLocal
from app.models import Question
from app.categories import get_category_names


CSV_FILE = "results/manual_review.csv"
SAMPLE_SIZE = 100


def load_questions(db):
    """
    Obtiene todas las preguntas disponibles.
    """
    return db.query(Question).all()


def load_reviewed_ids():
    """
    Lee el CSV existente y devuelve los IDs que ya fueron revisados.

    Esto permite cerrar el programa y continuar después
    sin perder el progreso.
    """

    reviewed_ids = set()

    if not os.path.exists(CSV_FILE):
        return reviewed_ids

    with open(
        CSV_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            reviewed_ids.add(int(row["question_id"]))

    return reviewed_ids


def create_csv():
    """
    Crea el archivo CSV si todavía no existe.
    """

    if os.path.exists(CSV_FILE):
        return

    # Crear la carpeta results si no existe
    os.makedirs(
        os.path.dirname(CSV_FILE),
        exist_ok=True
    )

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "question_id",
            "question",
            "human_category"
        ])


def save_review(
    question_id,
    question,
    human_category
):
    """
    Guarda una revisión manual en el CSV.
    """

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            question_id,
            question,
            human_category
        ])


def choose_category(category_names):
    """
    Permite seleccionar manualmente una categoría.
    """

    print("\nCategorías disponibles:")

    for i, category in enumerate(
        category_names,
        start=1
    ):
        print(f"{i}. {category}")

    while True:

        choice = input(
            "\nElegí la categoría correcta: "
        ).strip()

        try:

            number = int(choice)

            if 1 <= number <= len(category_names):
                return category_names[number - 1]

        except ValueError:
            pass

        print(
            "Opción inválida. "
            "Elegí un número de la lista."
        )


def review_question(
    question,
    category_names,
    current,
    total
):
    """
    Muestra una pregunta y permite asignarle
    manualmente una categoría.
    """

    print("\n" + "=" * 70)
    print(f"PREGUNTA {current}/{total}")
    print("=" * 70)

    print("\nPregunta:")
    print(question.question)

    print("\nRespuesta:")
    print(question.answer)

    human_category = choose_category(
        category_names
    )

    save_review(
        question_id=question.id,
        question=question.question,
        human_category=human_category
    )

    print("\n✓ Guardado correctamente.")


def main():

    db = SessionLocal()

    try:

        category_names = get_category_names()

        create_csv()

        # Cargar preguntas directamente
        questions = load_questions(db)

        print("\n" + "=" * 70)
        print("REVISIÓN MANUAL DE PREGUNTAS")
        print("=" * 70)

        print(
            f"\nPreguntas encontradas: "
            f"{len(questions)}"
        )

        # IDs que ya fueron revisados
        reviewed_ids = load_reviewed_ids()

        # Sacar las que ya revisamos
        pending = [
            question
            for question in questions
            if question.id not in reviewed_ids
        ]

        print(
            f"Preguntas ya revisadas: "
            f"{len(reviewed_ids)}"
        )

        print(
            f"Preguntas pendientes: "
            f"{len(pending)}"
        )

        if not pending:

            print(
                "\nNo hay preguntas pendientes."
            )

            return

        # Mezclar aleatoriamente
        random.shuffle(pending)

        # Cantidad restante hasta llegar a 100
        remaining = (
            SAMPLE_SIZE
            - len(reviewed_ids)
        )

        if remaining <= 0:

            print(
                "\nYa revisaste las "
                f"{SAMPLE_SIZE} preguntas."
            )

            return

        sample = pending[:remaining]

        print(
            f"\nSe revisarán "
            f"{len(sample)} preguntas."
        )

        print(
            "El resultado se guardará en:",
            CSV_FILE
        )

        input(
            "\nPresioná ENTER para comenzar..."
        )

        # Revisar preguntas
        for index, question in enumerate(
            sample,
            start=1
        ):

            current = (
                len(reviewed_ids)
                + index
            )

            review_question(
                question=question,
                category_names=category_names,
                current=current,
                total=SAMPLE_SIZE
            )

        print("\n" + "=" * 70)
        print("REVISIÓN FINALIZADA")
        print("=" * 70)

        print(
            f"\nRevisadas en esta sesión: "
            f"{len(sample)}"
        )

        print(
            f"Total revisadas: "
            f"{len(reviewed_ids) + len(sample)}"
        )

        print(
            f"Archivo: {CSV_FILE}"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()

