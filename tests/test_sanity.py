"""
Tests de sanidad: 
chequeos básicos de que la aplicación
arranca correctamente y responde, sin probar lógica de negocio compleja.
"""


def test_app_importa_sin_errores():
    """La app de FastAPI se puede importar sin que explote nada."""
    from app.main import app
    assert app is not None


def test_root_responde_200(client):
    """El endpoint raíz responde correctamente."""
    response = client.get("/")
    assert response.status_code == 200


def test_root_devuelve_json(client):
    """El endpoint raíz devuelve un JSON con la estructura esperada."""
    response = client.get("/")
    data = response.json()
    assert "message" in data
    assert "endpoints" in data


def test_endpoint_questions_existe(client):
    """El endpoint /questions responde (no da 404)."""
    response = client.get("/questions")
    assert response.status_code != 404


def test_docs_disponible(client):
    """La documentación interactiva de Swagger está disponible."""
    response = client.get("/docs")
    assert response.status_code == 200