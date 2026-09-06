"""
Módulo de revisión humana por consola.

Cuando la IA no tiene suficiente confianza (score < threshold),
este módulo le pregunta al usuario por terminal qué categoría corresponde.
"""


def display_question_context(
    question_text: str,
    ai_suggestion: str,
    confidence: float,
    all_scores: dict[str, float]
) -> None:
    """
    Muestra al usuario la pregunta, la sugerencia de la IA y los scores.
    """

    print("=" * 64)
    print("REVISIÓN MANUAL REQUERIDA (confianza < 70%)")
    print("=" * 64)

    print(f"\nPregunta: {question_text}")

    print(
        f"\nSugerencia de la IA: {ai_suggestion} "
        f"(confianza: {confidence:.0%})"
    )

    print("\nScores de todas las categorías:")

    # Ordenar de mayor a menor score
    sorted_scores = sorted(
        all_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for index, (category, score) in enumerate(sorted_scores, start=1):
        print(f"  {index}. {category:<20} → {score:.0%}")

    print("\n" + "=" * 64)


def ask_human_for_category(categories: list[dict[str, str]]) -> str | None:
    """
    Le pide al usuario que elija una categoría por consola.
    """

    print("\nOpciones:")

    for index, category in enumerate(categories, start=1):
        print(f"  {index}. {category['label']}")

    print("  S. Skip (omitir esta pregunta)")

    while True:
        choice = input("\nElegí una opción: ").strip()

        if choice.lower() == "s":
            return None

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(categories):
                return categories[number - 1]["name"]

        print("❌ Opción inválida. Elegí un número válido o S para omitir.")


def confirm_ai_suggestion(
    ai_suggestion: str,
    confidence: float
) -> bool:
    """
    Pregunta al usuario si acepta la sugerencia de la IA.
    """

    print(
        f'\n¿Aceptás la sugerencia "{ai_suggestion}" '
        f"({confidence:.0%})? [S/n]: ",
        end=""
    )

    answer = input().strip()

    if answer == "" or answer.lower() == "s":
        return True

    if answer.lower() == "n":
        return False

    # Si escribe algo distinto, volvemos a preguntar
    print("❌ Respuesta inválida. Ingresá S o N.")
    return confirm_ai_suggestion(ai_suggestion, confidence)