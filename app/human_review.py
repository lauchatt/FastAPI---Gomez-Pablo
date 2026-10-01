from dataclasses import dataclass


REVIEW_THRESHOLD = 0.30


@dataclass
class HumanReviewResult:
    """Resultado de una revisión humana sobre una pregunta."""

    category_name: str | None
    was_corrected: bool
    was_skipped: bool


def display_question_context(
    question_text: str,
    ai_suggestion: str,
    confidence: float,
    threshold: float = REVIEW_THRESHOLD,
    all_scores: dict[str, float] | None = None,
) -> None:
    """Muestra la información de una pregunta que requiere revisión."""

    print("=" * 64)
    print(f"REVISIÓN MANUAL REQUERIDA (confianza < {threshold:.0%})")
    print("=" * 64)

    print(f"\nPregunta: {question_text}")

    print(
        f"\nSugerencia de la IA: {ai_suggestion} "
        f"(confianza: {confidence:.0%})"
    )

    if all_scores:
        print("\nScores de todas las categorías:")

        sorted_scores = sorted(
            all_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        for index, (category, score) in enumerate(
            sorted_scores,
            start=1,
        ):
            print(
                f"  {index}. {category:<20} → {score:.0%}"
            )

    print("\n" + "=" * 64)


def ask_human_for_category(
    category_names: list[str],
) -> str | None:
    """Permite seleccionar manualmente una categoría."""

    print("\nOpciones:")

    for index, category in enumerate(
        category_names,
        start=1,
    ):
        print(f"  {index}. {category}")

    print("  S. Skip (omitir esta pregunta)")

    while True:
        choice = input("\nElegí una opción: ").strip()

        if choice.lower() == "s":
            return None

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(category_names):
                return category_names[number - 1]

        print(
            "❌ Opción inválida. "
            "Elegí un número válido o S para omitir."
        )


def review_question(
    question_text: str,
    ai_suggestion: str,
    confidence: float,
    category_names: list[str],
    threshold: float = REVIEW_THRESHOLD,
    all_scores: dict[str, float] | None = None,
) -> HumanReviewResult:

    if confidence >= threshold:
        return HumanReviewResult(
            category_name=ai_suggestion,
            was_corrected=False,
            was_skipped=False,
        )

    display_question_context(
        question_text=question_text,
        ai_suggestion=ai_suggestion,
        confidence=confidence,
        threshold=threshold,
        all_scores=all_scores,
    )

    chosen_category = ask_human_for_category(
        category_names
    )

    if chosen_category is None:
        return HumanReviewResult(
            category_name=None,
            was_corrected=False,
            was_skipped=True,
        )

    return HumanReviewResult(
        category_name=chosen_category,
        was_corrected=(
            chosen_category != ai_suggestion
        ),
        was_skipped=False,
    )