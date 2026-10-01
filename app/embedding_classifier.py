
"""
Clasificador de texto usando Sentence Transformers.

Utiliza embeddings de texto y similitud coseno para encontrar
la categoría más relacionada con una pregunta.
"""

from dataclasses import dataclass

import torch
from sentence_transformers import SentenceTransformer

from app.categories import CATEGORIES


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

    Utiliza BGE-large para generar embeddings y compara cada
    pregunta contra las descripciones de las categorías.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-large-en-v1.5",
        batch_size: int = 32,
    ):
        """
        Carga el modelo de Sentence Transformers.

        Args:
            model_name: Modelo de embeddings de Hugging Face.
            batch_size: Cantidad de preguntas procesadas
                        simultáneamente en GPU.
        """

        print(f"\nCargando modelo de embeddings: {model_name}...")

        self.model_name = model_name
        self.batch_size = batch_size

        # Usar GPU si está disponible.
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Dispositivo utilizado: {self.device}")

        self.model = SentenceTransformer(
            model_name,
            device=self.device,
        )

        # ---------------------------------------------------------
        # PREPARAR LAS CATEGORÍAS
        # ---------------------------------------------------------

        self.category_names = [
            category["name"]
            for category in CATEGORIES
        ]

        self.category_labels = {
            category["name"]: category["label"]
            for category in CATEGORIES
        }

        self.category_descriptions = {
            category["name"]: category["description"]
            for category in CATEGORIES
        }

        # ---------------------------------------------------------
        # CREAR TEXTOS PARA LOS EMBEDDINGS
        # ---------------------------------------------------------
        #
        # Usamos label + description para darle al embedding
        # información suficiente sobre cada categoría.
        #
        # Ejemplo:
        #
        # "Science and technology questions.
        #  Questions about science, technology..."
        #
        # ---------------------------------------------------------

        category_texts = [
            (
                f"{category['label']}. "
                f"{category['description']}"
            )
            for category in CATEGORIES
        ]

        # ---------------------------------------------------------
        # PRECALCULAR EMBEDDINGS
        # ---------------------------------------------------------

        print("Calculando embeddings de las categorías...")

        category_embeddings = self.model.encode(
            category_texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            convert_to_tensor=True,
            show_progress_bar=False,
        )

        # Como los embeddings están normalizados,
        # producto punto = similitud coseno.
        self.category_embeddings = category_embeddings

        print(f"Modelo cargado: {model_name}")
        print(f"Categorías cargadas: {len(self.category_names)}")

    def classify(
        self,
        text: str,
        candidate_labels: list[str],
    ) -> ClassificationResult:
        """
        Clasifica una pregunta.

        Args:
            text: Pregunta a clasificar.
            candidate_labels: Categorías permitidas.

        Returns:
            ClassificationResult con la categoría elegida,
            confianza y puntuaciones de todas las categorías.
        """

        results = self.classify_batch(
            [text],
            candidate_labels,
        )

        return results[0]

    def classify_batch(
        self,
        texts: list[str],
        candidate_labels: list[str],
    ) -> list[ClassificationResult]:
        """
        Clasifica múltiples preguntas utilizando batch real.

        Las preguntas se convierten a embeddings en grupos para
        aprovechar la GPU.
        """

        if not texts:
            return []

        # ---------------------------------------------------------
        # VALIDAR CATEGORÍAS
        # ---------------------------------------------------------

        for category in candidate_labels:
            if category not in self.category_names:
                raise ValueError(
                    f"Categoría desconocida: {category}"
                )

        # Índices de las categorías solicitadas.
        category_indices = [
            self.category_names.index(category)
            for category in candidate_labels
        ]

        # Seleccionamos solamente los embeddings necesarios.
        selected_category_embeddings = (
            self.category_embeddings[category_indices]
        )

        # ---------------------------------------------------------
        # EMBEDDINGS DE LAS PREGUNTAS
        # ---------------------------------------------------------

        text_embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            convert_to_tensor=True,
            show_progress_bar=True,
        )

        # ---------------------------------------------------------
        # SIMILITUD COSENO
        # ---------------------------------------------------------
        #
        # Como tanto las preguntas como las categorías están
        # normalizadas:
        #
        # cosine_similarity(A, B) == A @ B.T
        #
        # Esto es mucho más eficiente que llamar a sklearn
        # pregunta por pregunta.
        # ---------------------------------------------------------

        similarity_matrix = (
            text_embeddings
            @ selected_category_embeddings.T
        )

        results = []

        # ---------------------------------------------------------
        # CREAR RESULTADOS
        # ---------------------------------------------------------

        for row in similarity_matrix:

            all_scores = {
                category: float(score)
                for category, score in zip(
                    candidate_labels,
                    row,
                )
            }

            category_name = max(
                all_scores,
                key=all_scores.get,
            )

            confidence_score = all_scores[category_name]

            results.append(
                ClassificationResult(
                    category_name=category_name,
                    confidence_score=confidence_score,
                    all_scores=all_scores,
                )
            )

        return results

