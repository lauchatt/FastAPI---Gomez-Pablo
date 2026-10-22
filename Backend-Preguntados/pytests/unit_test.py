import pytest
from unittest.mock import patch, Mock

from app.main import root
from app.models import Question
from app.load_data import download_parquet


def test_root():
    result = root()

    assert result["message"] == "Questions API funcionando"
    assert "/questions" in result["endpoints"]
    assert "/questions/{id}" in result["endpoints"]


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


@patch("app.load_data.requests.get")
def test_download_parquet(mock_get, tmp_path):
    fake_response = Mock()
    fake_response.content = b"fake parquet content"
    fake_response.raise_for_status.return_value = None

    mock_get.return_value = fake_response

    path = download_parquet("https://example.com/test.parquet")

    assert path.endswith(".parquet")

    with open(path, "rb") as f:
        assert f.read() == b"fake parquet content"