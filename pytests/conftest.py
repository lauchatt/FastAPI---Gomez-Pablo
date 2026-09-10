import os

os.environ["TESTING"] = "1"
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models import Question

# Base de datos SQLite en memoria, exclusiva para los tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # mantiene la misma conexión en memoria durante todo el test
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Reemplaza la dependencia get_db() para usar la base de test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Le decimos a FastAPI que use la base de test en lugar de Postgres
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """Crea las tablas antes de cada test y las borra después (test limpio y aislado)."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Cliente HTTP para llamar a la API en los tests."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_question(db_session):
    """Crea una pregunta de ejemplo en la base de test, lista para usar."""
    question = Question(
        question="¿Cuál es la capital de Argentina?",
        answer="Buenos Aires",
        category="geografia",
        source="test",
    )
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    return question