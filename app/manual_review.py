"""
Revisión manual de una muestra de categorizaciones realizadas por IA.

Toma categorizaciones automáticas ya existentes en la BD,
selecciona una muestra y permite revisarlas desde consola.

El resultado se guarda en manual_review.csv.
"""

import csv
import os
import random

from app.database import SessionLocal
from app.models import Question, Categorization
from app.categories import get_category_names


CSV_FILE = "results/manual_review.csv"
SAMPLE_SIZE = 100


def load_categorizations(db):
    """
    Obtiene las categorizaciones automáticas existentes.
    """

    return (
        db.query(Categorization)
        .join(Question)
        .filter(Categorization.is_automatic == True)
        .all()
    )


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
            "ai_category",
            "ai_confidence",
            "human_category"
        ])


def save_review(
    question_id,
    question,
    ai_category,
    ai_confidence,
    human_category
):
    """
    Guarda una revisión en el CSV.
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
            ai_category,
            ai_confidence,
            human_category
        ])


def choose_category(category_names):
    """
    Permite seleccionar manualmente una categoría.
    """

    print("\nCategorías disponibles:")

    for i, category in enumerate(category_names, start=1):
        print(f"{i}. {category}")

    while True:

        choice = input("\nElegí la categoría correcta: ").strip()

        try:
            number = int(choice)

            if 1 <= number <= len(category_names):
                return category_names[number - 1]

        except ValueError:
            pass

        print("Opción inválida. Elegí un número de la lista.")


def review_question(categorization, category_names, current, total):
    """
    Muestra una pregunta y permite revisarla.
    """

    question = categorization.question

    print("\n" + "=" * 70)
    print(f"PREGUNTA {current}/{total}")
    print("=" * 70)

    print("\nPregunta:")
    print(question.question)

    print("\nPredicción de IA:")
    print(f"Categoría: {categorization.category_name}")
    print(f"Confianza: {categorization.confidence_score:.4f}")

    while True:

        answer = input("\n¿La IA acertó? [s/n]: ").strip().lower()

        if answer == "s":

            human_category = categorization.category_name
            break

        elif answer == "n":

            human_category = choose_category(category_names)
            break

        else:

            print("Escribí 's' para sí o 'n' para no.")

    save_review(
        question_id=question.id,
        question=question.question,
        ai_category=categorization.category_name,
        ai_confidence=categorization.confidence_score,
        human_category=human_category
    )

    print("\n✓ Guardado correctamente.")


def main():

    db = SessionLocal()

    try:

        category_names = get_category_names()

        create_csv()

        # Cargar todas las categorizaciones automáticas
        categorizations = load_categorizations(db)

        print("\n" + "=" * 70)
        print("REVISIÓN MANUAL DE CATEGORIZACIONES")
        print("=" * 70)

        print(
            f"\nCategorizaciones automáticas encontradas: "
            f"{len(categorizations)}"
        )

        # IDs que ya fueron revisados
        reviewed_ids = load_reviewed_ids()

        # Sacar las que ya revisamos
        pending = [
            c
            for c in categorizations
            if c.question_id not in reviewed_ids
        ]

        print(f"Preguntas ya revisadas: {len(reviewed_ids)}")
        print(f"Preguntas pendientes: {len(pending)}")

        if not pending:

            print("\nNo hay preguntas pendientes.")
            return

        # Mezclar aleatoriamente
        random.shuffle(pending)

        # Tomar como máximo las necesarias para llegar a 100
        remaining = SAMPLE_SIZE - len(reviewed_ids)

        if remaining <= 0:

            print("\nYa revisaste las 100 preguntas.")
            return

        sample = pending[:remaining]

        print(f"\nSe revisarán {len(sample)} preguntas.")
        print("El resultado se guardará en:", CSV_FILE)

        input("\nPresioná ENTER para comenzar...")

        # Revisar
        for index, categorization in enumerate(sample, start=1):

            current = len(reviewed_ids) + index

            review_question(
                categorization=categorization,
                category_names=category_names,
                current=current,
                total=SAMPLE_SIZE
            )

        print("\n" + "=" * 70)
        print("REVISIÓN FINALIZADA")
        print("=" * 70)

        print(f"\nRevisadas en esta sesión: {len(sample)}")
        print(f"Total revisadas: {len(reviewed_ids) + len(sample)}")
        print(f"Archivo: {CSV_FILE}")

    finally:

        db.close()


if __name__ == "__main__":
    main()

