import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_questions():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/questions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_question_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/questions/999999")
    assert response.status_code == 200
    assert "error" in response.json()


@pytest.mark.asyncio
async def test_stats():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/stats")
    assert response.status_code == 200
    assert "total" in response.json()
    assert "by_category" in response.json()


@pytest.mark.asyncio
async def test_create_question():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/questions", json={
            "question": "¿Cuanto daño hace un creeper en normal?",
            "answer": "43 puntos.",
            "category": "Creeper"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "¿Cuanto daño hace un creeper en normal?"