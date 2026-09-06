"""
Clasificador de texto usando Sentence Transformers.

Utiliza embeddings de texto y similitud coseno para encontrar
la categoría más relacionada con una pregunta.
"""

from dataclasses import dataclass

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class ClassificationResult:
    """
    Resultado de una clasificación.
    """

    category_name: str
    confidence_score: float
    all_scores: dict[str, float]


class EmbeddingClassifier:
    """
    Clasificador basado en embeddings + similitud coseno.
    """

    CATEGORY_DESCRIPTIONS = {
        "blocks": [
            "Minecraft blocks",
            "Minecraft building blocks",
            "Minecraft building materials",
            "Minecraft block properties",
            "Minecraft stone, wood and decorative blocks",
        ],

        "items": [
            "Minecraft items",
            "Minecraft tools and weapons",
            "Minecraft food and ingredients",
            "Minecraft armor",
            "Minecraft potions",
            "Minecraft usable resources",
        ],

        "mobs": [
            "Minecraft mobs",
            "Minecraft creatures",
            "Minecraft hostile and passive creatures",
            "Minecraft mob behavior",
            "Minecraft mob spawning",
            "Minecraft mob combat",
            "Minecraft mob drops",
        ],

        "world": [
            "Minecraft biomes",
            "Minecraft dimensions",
            "Minecraft structures",
            "Minecraft world generation",
            "Minecraft terrain",
            "Minecraft caves and oceans",
            "Minecraft vegetation",
            "Minecraft exploration",
        ],

        "redstone": [
            "Minecraft redstone",
            "Minecraft redstone components",
            "Minecraft redstone mechanisms",
            "Minecraft redstone circuits",
            "Minecraft redstone contraptions",
            "Minecraft redstone devices",
            "Minecraft redstone automation",
        ],

        "commands": [
            "Minecraft commands",
            "Minecraft command syntax",
            "Minecraft command blocks",
            "Minecraft command usage",
            "Minecraft teleport commands",
            "Minecraft commands and command mechanics",
        ],

        "tutorials": [
            "Minecraft tutorials",
            "Minecraft tutorial hints",
            "Minecraft controls",
            "Minecraft HUD",
            "Minecraft user interface",
            "Minecraft instructions for learning how to play",
            "Minecraft beginner instructions",
        ],

        "gameplay": [
            "Minecraft gameplay mechanics",
            "Minecraft inventory",
            "Minecraft trading",
            "Minecraft progression",
            "Minecraft achievements",
            "Minecraft statistics",
            "Minecraft game rules",
            "Minecraft general gameplay",
        ],

        "misc": [
            "Minecraft game versions",
            "Minecraft development history",
            "Minecraft game development",
            "Minecraft resource packs",
            "Minecraft books",
            "Minecraft official content",
            "Minecraft miscellaneous topics",
            "Minecraft topics that do not fit other categories",
        ],
    }
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        """
        Carga el modelo de Sentence Transformers.
        """

        print(f"\nCargando modelo de embeddings: {model_name}...")

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

        # Precalculamos los embeddings de las categorías.
        # No tiene sentido volver a calcularlos para cada pregunta.
        self.category_embeddings = {}

        for category, descriptions in self.CATEGORY_DESCRIPTIONS.items():
            self.category_embeddings[category] = self.model.encode(
                descriptions,
                normalize_embeddings=True,
            )

        print(f"Modelo cargado: {model_name}")

    def classify(
        self,
        text: str,
        candidate_labels: list[str],
    ) -> ClassificationResult:
        """
        Clasifica una pregunta comparándola con múltiples
        descripciones de cada categoría.
        """

        # Embedding de la pregunta
        text_embedding = self.model.encode(
            [text],
            normalize_embeddings=True,
        )

        all_scores = {}

        for category in candidate_labels:

            # Embeddings ya calculados de esta categoría
            category_embeddings = self.category_embeddings[category]

            # Comparar pregunta contra todas las descripciones
            similarities = cosine_similarity(
                text_embedding,
                category_embeddings,
            )[0]

            # Nos quedamos con la mejor coincidencia
            best_similarity = max(similarities)

            all_scores[category] = float(best_similarity)

        # Buscar la categoría con mayor similitud
        category_name = max(
            all_scores,
            key=all_scores.get,
        )

        confidence_score = all_scores[category_name]

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
        Clasifica múltiples preguntas.
        """

        return [
            self.classify(
                text=text,
                candidate_labels=candidate_labels,
            )
            for text in texts
        ]