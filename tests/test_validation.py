"""
Tests de validación: 
verifican que la API maneje correctamente
datos inválidos, faltantes o con tipos incorrectos.
"""


def test_pregunta_inexistente_devuelve_error(client):
    """Pedir un ID que no existe debe devolver el mensaje de error, no un 500."""
    response = client.get("/questions/99999")
    assert response.status_code == 200  # API actual devuelve 200 con {"error": ...}
    data = response.json()
    assert "error" in data
    assert data["error"] == "Pregunta no encontrada"


def test_id_invalido_tipo_string(client):
    """Pedir un ID que no es un número entero debe rechazarse (422)."""
    response = client.get("/questions/no-es-un-numero")
    assert response.status_code == 422


def test_id_negativo(client):
    """Un ID negativo no debería romper la API."""
    response = client.get("/questions/-1")
    # FastAPI acepta como int válido (-1), pero no debe encontrar nada ni romperse
    assert response.status_code == 200
    data = response.json()
    assert "error" in data


def test_limit_invalido_tipo_string(client):
    """El parámetro limit debe ser numérico; si no lo es, se rechaza."""
    response = client.get("/questions", params={"limit": "abc"})
    assert response.status_code == 422


def test_skip_negativo_no_rompe(client):
    """Un skip negativo no debe causar un error 500."""
    response = client.get("/questions", params={"skip": -5})
    assert response.status_code in (200, 422)


def test_limit_cero_devuelve_lista_vacia(client, sample_question):
    """Con limit=0 no debe devolver ningún resultado."""
    response = client.get("/questions", params={"limit": 0})
    assert response.status_code == 200
    assert response.json() == []


def test_limit_muy_grande_no_rompe(client, sample_question):
    """Un limit gigante no debe causar error, solo devuelve lo que hay."""
    response = client.get("/questions", params={"limit": 999999})
    assert response.status_code == 200
    assert isinstance(response.json(), list)