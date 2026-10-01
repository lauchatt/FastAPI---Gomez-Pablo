"""
Módulo de clasificación de texto usando IA.

Utiliza zero-shot classification de Hugging Face.
"""

from dataclasses import dataclass

from transformers import pipeline

from app.categories import CATEGORIES


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
    Clasificador de texto basado en IA mediante zero-shot classification.
    """

    def __init__(
        self,
        model_name: str = (
            "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
        ),
    ):
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

        # Buscamos las categorías correspondientes
        # a los nombres internos recibidos.
        categories = [
            category
            for category in CATEGORIES
            if category["name"] in candidate_labels
        ]

        # Etiquetas que recibe el modelo.
        model_labels = [
            category["label"]
            for category in categories
        ]

        result = self.pipeline(
            text,
            candidate_labels=model_labels,
            hypothesis_template="This question is about {}.",
        )

        # Convertimos las etiquetas del modelo
        # nuevamente a nuestros nombres internos.
        label_to_name = {
            category["label"]: category["name"]
            for category in categories
        }

        all_scores = {}

        for label, score in zip(
            result["labels"],
            result["scores"],
        ):
            category_name = label_to_name[label]
            all_scores[category_name] = float(score)

        # La primera etiqueta es la que obtuvo mayor puntuación.
        category_name = label_to_name[result["labels"][0]]

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