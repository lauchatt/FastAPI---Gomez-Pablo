""" Tests de integración: 
prueban el flujo completo — API + base de datos trabajando juntas, simulando uso real.
"""
from app.models import Question


def test_flujo_completo_crear_y_listar(client, db_session):
    """ Simula el flujo real: se insertan preguntas en la base y se verifica que la API los devuelva ."""
    # Se ponen Los datos directamente en la base, como haría load_data.py
    preguntas = [
        Question(question="¿Qué es Python?", answer="Un lenguaje de programación", category="tech"),
        Question(question="¿Qué es FastAPI?", answer="Un framework web", category="tech"),
    ]
    db_session.add_all(preguntas)
    db_session.commit()

    # La API debe poder ponerlas en listas
    response = client.get("/questions")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["question"] == "¿Qué es Python?"
    assert data[1]["question"] == "¿Qué es FastAPI?"


def test_flujo_completo_obtener_por_id(client, sample_question):
    """
    Integra la creación de datos con la consulta por ID:
    la pregunta creada debe poder recuperarse correctamente.
    """
    response = client.get(f"/questions/{sample_question.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == sample_question.id
    assert data["question"] == "¿Cuál es la capital de Argentina?"
    assert data["answer"] == "Buenos Aires"
    assert data["category"] == "geografia"


def test_paginacion_skip_limit(client, db_session):
    """
    Verifica que la paginación (skip/limit) funcione integrando
    múltiples filas reales de la base con los parámetros de la API.
    """
    preguntas = [
        Question(question=f"Pregunta {i}", answer=f"Respuesta {i}", category="test")
        for i in range(15)
    ]
    db_session.add_all(preguntas)
    db_session.commit()

    # Primera página
    response = client.get("/questions", params={"skip": 0, "limit": 10})
    assert len(response.json()) == 10

    # Segunda página
    response = client.get("/questions", params={"skip": 10, "limit": 10})
    assert len(response.json()) == 5


def test_base_de_datos_persiste_entre_requests(client, db_session):
    """
    Verifica que una pregunta insertada en un request
    siga disponible en un request posterior (persistencia real).
    """
    pregunta = Question(question="¿Persiste esto?", answer="Sí", category="test")
    db_session.add(pregunta)
    db_session.commit()
    db_session.refresh(pregunta)

    # Primer request: la trae por ID
    r1 = client.get(f"/questions/{pregunta.id}")
    assert r1.status_code == 200

    # Segundo request: la trae también en el listado
    r2 = client.get("/questions")
    ids = [q["id"] for q in r2.json()]
    assert pregunta.id in ids