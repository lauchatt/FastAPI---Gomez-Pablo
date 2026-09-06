"""
Módulo de clasificación de texto usando IA.

Utiliza zero-shot classification de Hugging Face.
"""

from dataclasses import dataclass

from transformers import pipeline


@dataclass
class ClassificationResult:
    """
    Resultado de una clasificación.
    """

    category_name: str
    confidence_score: float
    all_scores: dict[str, float]


class AIClassifier:
    """
    Clasificador de texto basado en IA.
    """

    CATEGORY_LABELS = {
    "blocks": "Minecraft blocks, building materials, and block properties",

    "items": (
        "Minecraft items, tools, weapons, armor, food, ingredients, "
        "potions, and usable resources"
    ),

    "mobs": (
        "Minecraft mobs, creatures, their behavior, spawning, combat, "
        "and drops"
    ),

    "world": (
        "Minecraft biomes, dimensions, structures, terrain, "
        "world generation, caves, oceans, and exploration"
    ),

    "redstone": (
        "Minecraft redstone, mechanisms, circuits, components, "
        "and redstone contraptions"
    ),

    "commands": (
        "Minecraft commands, command syntax, command blocks, "
        "and command-related mechanics"
    ),

    "tutorials": (
        "Minecraft tutorials, tutorial hints, controls, HUD, "
        "interface, and instructions for learning how to play"
    ),

    "gameplay": (
        "Minecraft gameplay mechanics, inventory, trading, progression, "
        "achievements, statistics, and general game rules"
    ),

    "misc": (
        "Minecraft topics that do not fit into the other categories, "
        "including versions, history, development, and other miscellaneous topics"
    ),
}

    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        print(f"\nCargando modelo de IA: {model_name}...")

        self.model_name = model_name

        self.pipeline = pipeline(
            "zero-shot-classification",
            model=model_name,
        )

        print(f"Modelo cargado: {model_name}")

    def classify(
        self,
        text: str,
        candidate_labels: list[str],
    ) -> ClassificationResult:
        """
        Clasifica un texto contra las categorías candidatas.
        """

        model_labels = [
            self.CATEGORY_LABELS[label]
            for label in candidate_labels
        ]

        result = self.pipeline(
            text,
            candidate_labels=model_labels,
            hypothesis_template="This question is about {}.",
        )

        # Convertimos las etiquetas del modelo
        # nuevamente a nuestros nombres internos.
        label_to_name = {
            label: name
            for name, label in self.CATEGORY_LABELS.items()
        }

        all_scores = {}

        for label, score in zip(
            result["labels"],
            result["scores"],
        ):
            category_name = label_to_name[label]
            all_scores[category_name] = float(score)

        category_name = result["labels"][0]
        category_name = label_to_name[category_name]

        confidence_score = float(result["scores"][0])

        return ClassificationResult(
            category_name=category_name,
            confidence_score=confidence_score,
            all_scores=all_scores,
        )

    def classify_batch(
        self,
        texts: list[str],
        candidate_labels: list[str],
    ) -> list[ClassificationResult]:
        """
        Clasifica múltiples textos.
        """

        return [
            self.classify(text, candidate_labels)
            for text in texts
        ]