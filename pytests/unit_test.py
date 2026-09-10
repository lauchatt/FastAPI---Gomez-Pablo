
import pytest
from unittest.mock import patch, Mock

from app.main import root
from app.models import Question
from app.load_data import download_parquet


""" Testea la función raíz de la API sin hacer una petición HTTP """
def test_root():
    result = root()

    assert result["message"] == "Questions API funcionando"
    assert "/questions" in result["endpoints"]
    assert "/questions/{id}" in result["endpoints"]


"""Testea que el modelo Question se cree correctamente
y que sus atributos tengan los valores esperados."""
def test_question_model():
    question = Question(
        question="How do I craft a sword?",
        answer="You need sticks and iron.",
        category="crafting",
        source="minecraft"
    )

    assert question.question == "How do I craft a sword?"
    assert question.answer == "You need sticks and iron."
    assert question.category == "crafting"
    assert question.source == "minecraft"


""" Reemplaza requests.get por un Mock para no hacer una petición real a Internet durante el test."""
@patch("app.load_data.requests.get")
def test_download_parquet(mock_get, tmp_path):

    # Creamos una respuesta HTTP simulada.
    fake_response = Mock()
    fake_response.content = b"fake parquet content"
    fake_response.raise_for_status.return_value = None


    mock_get.return_value = fake_response

    # Ejecutamos la función que queremos probar.
    path = download_parquet("https://example.com/test.parquet")

    # Comprobamos que se haya creado un archivo Parquet.
    assert path.endswith(".parquet")

    # Comprobamos que el archivo tenga el contenido esperado.
    with open(path, "rb") as f:
        assert f.read() == b"fake parquet content"
