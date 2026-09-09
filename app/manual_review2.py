"""
Crea un conjunto NUEVO de 100 preguntas para la evaluación final.

Excluye todas las preguntas que aparecen en:
    results/manual_review.csv

Muestra cada pregunta en consola para que el usuario
seleccione manualmente su human_category mediante un número.

Las respuestas se guardan inmediatamente en:
    results/manual_review2.csv

Si el programa se cierra, al volver a ejecutarlo
continúa desde donde quedó.

Formato:
    question_id,question,human_category
"""

import csv
from pathlib import Path

from app.database import SessionLocal
from app.models import Question


# ============================================================
# CONFIGURACIÓN
# ============================================================

MANUAL_REVIEW_FILE = Path(
    "results/manual_review.csv"
)

OUTPUT_FILE = Path(
    "results/manual_review2.csv"
)

NUMBER_OF_QUESTIONS = 100


# ============================================================
# CATEGORÍAS
# ============================================================

from app.categories import CATEGORIES


# ============================================================
# CARGAR IDS DEL MANUAL REVIEW ORIGINAL
# ============================================================

def load_used_question_ids():
    """
    Obtiene los question_id que ya fueron utilizados
    en manual_review.csv.
    """

    used_ids = set()

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

            used_ids.add(question_id)

    return used_ids


# ============================================================
# CARGAR IDS YA CLASIFICADOS EN MANUAL_REVIEW2
# ============================================================

def load_completed_question_ids():
    """
    Obtiene los question_id que ya fueron clasificados
    y guardados en manual_review2.csv.

    Esto permite continuar el trabajo si el programa
    se cerró anteriormente.
    """

    completed_ids = set()

    if not OUTPUT_FILE.exists():
        return completed_ids

    with open(
        OUTPUT_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row.get("question_id"):

                completed_ids.add(
                    int(row["question_id"])
                )

    return completed_ids


# ============================================================
# CREAR CSV SI NO EXISTE
# ============================================================

def create_output_file_if_needed():
    """
    Crea manual_review2.csv solamente si no existe.

    IMPORTANTE:
    No utiliza 'w' si el archivo ya existe, por lo que
    no se pierde el progreso anterior.
    """

    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )

    if not OUTPUT_FILE.exists():

        with open(
            OUTPUT_FILE,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "question_id",
                "question",
                "human_category",
            ])


# ============================================================
# MOSTRAR CATEGORÍAS
# ============================================================

def show_categories():

    print("\nCategorías:")

    for index, category in enumerate(
        CATEGORIES,
        start=1
    ):

        print(
            f"  {index}. {category['name']}"
        )


# ============================================================
# PEDIR CATEGORÍA
# ============================================================

def ask_category():

    while True:

        show_categories()

        answer = input(
            f"\nElegí una categoría (1-{len(CATEGORIES)}): "
        ).strip()

        try:

            number = int(answer)

        except ValueError:

            print(
                f"\n Ingresá un número del 1 al {len(CATEGORIES)}."
            )

            continue

        if 1 <= number <= len(CATEGORIES):

            return CATEGORIES[number - 1]["name"]

        print(
            "\n Número inválido."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("CREAR EVALUACIÓN FINAL")
    print("=" * 70)

    # --------------------------------------------------------
    # Verificar manual_review.csv
    # --------------------------------------------------------

    if not MANUAL_REVIEW_FILE.exists():

        print(
            f"\n No se encontró:"
            f"\n{MANUAL_REVIEW_FILE}"
        )

        return

    # --------------------------------------------------------
    # Cargar IDs utilizados anteriormente
    # --------------------------------------------------------

    used_ids = load_used_question_ids()

    print(
        f"\nPreguntas utilizadas anteriormente: "
        f"{len(used_ids)}"
    )

    # --------------------------------------------------------
    # Crear CSV si no existe
    # --------------------------------------------------------

    create_output_file_if_needed()

    # --------------------------------------------------------
    # Cargar preguntas ya clasificadas
    # --------------------------------------------------------

    completed_ids = load_completed_question_ids()

    print(
        f"Preguntas ya clasificadas en esta evaluación: "
        f"{len(completed_ids)}"
    )

    # --------------------------------------------------------
    # Consultar BD
    # --------------------------------------------------------

    db = SessionLocal()

    try:

        questions = (
            db.query(Question)
            .filter(
                ~Question.id.in_(used_ids)
            )
            .order_by(
                Question.id
            )
            .limit(
                NUMBER_OF_QUESTIONS
            )
            .all()
        )

    finally:

        db.close()

    # --------------------------------------------------------
    # Verificar cantidad
    # --------------------------------------------------------

    if len(questions) < NUMBER_OF_QUESTIONS:

        print(
            f"\n Solo se encontraron "
            f"{len(questions)} preguntas nuevas."
        )

        print(
            f"Se necesitan "
            f"{NUMBER_OF_QUESTIONS}."
        )

        return

    # --------------------------------------------------------
    # Filtrar preguntas ya clasificadas
    # --------------------------------------------------------

    pending_questions = [
        question
        for question in questions
        if question.id not in completed_ids
    ]

    if not pending_questions:

        print("\n✓ Las 100 preguntas ya fueron clasificadas.")
        print(
            f"\nArchivo:"
            f"\n{OUTPUT_FILE}"
        )

        return

    print(
        f"\nPreguntas pendientes: "
        f"{len(pending_questions)}"
    )

    # --------------------------------------------------------
    # ABRIR CSV EN MODO APPEND
    # --------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        # ----------------------------------------------------
        # Procesar preguntas
        # ----------------------------------------------------

        for question in pending_questions:

            # Número real dentro de las 100 preguntas
            current_number = (
                len(completed_ids) + 1
            )

            print("\n")
            print("=" * 70)
            print(
                f"PREGUNTA {current_number}/{NUMBER_OF_QUESTIONS}"
            )
            print("=" * 70)

            print(
                f"\nID: {question.id}"
            )

            print(
                f"\n{question.question}"
            )

            # ------------------------------------------------
            # Seleccionar categoría
            # ------------------------------------------------

            category = ask_category()

            # ------------------------------------------------
            # Guardar inmediatamente
            # ------------------------------------------------

            writer.writerow([
                question.id,
                question.question,
                category,
            ])

            file.flush()

            completed_ids.add(
                question.id
            )

            print(
                f"\n✓ Guardado: {category}"
            )

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("✓ EVALUACIÓN COMPLETADA")
    print("=" * 70)

    print(
        f"\nArchivo:"
        f"\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()