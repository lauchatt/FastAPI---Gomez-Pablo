
"""
Tests de Data Quality:

Verifican que los datos almacenados en la base de datos
mantengan una estructura y valores razonables.
"""

from app.models import Question


def test_ids_validos(db_session):
    """
    Los IDs deben ser enteros positivos.
    """
    questions = db_session.query(Question).all()

    for question in questions:
        assert isinstance(question.id, int)
        assert question.id > 0


def test_campos_obligatorios_no_sean_nulos(db_session):
    """
    Los campos question y answer son obligatorios,
    por lo tanto no deberían contener valores nulos.
    """
    questions = db_session.query(Question).all()

    for question in questions:
        assert question.question is not None
        assert question.answer is not None


def test_preguntas_no_estan_vacias(db_session):
    """
    Las preguntas no deben contener texto vacío.
    """
    questions = db_session.query(Question).all()

    for question in questions:
        assert question.question.strip() != ""


def test_respuestas_no_estan_vacias(db_session):
    """
    Las respuestas no deben contener texto vacío.
    """
    questions = db_session.query(Question).all()

    for question in questions:
        assert question.answer.strip() != ""


def test_longitud_category(db_session):
    """
    Si existe una categoría, no debe superar los 100 caracteres,
    que es el límite definido en el modelo.
    """
    questions = db_session.query(Question).all()

    for question in questions:
        if question.category is not None:
            assert len(question.category) <= 100


def test_longitud_source(db_session):
    """
    Si existe una fuente, no debe superar los 255 caracteres,
    que es el límite definido en el modelo.
    """
    questions = db_session.query(Question).all()

    for question in questions:
        if question.source is not None:
            assert len(question.source) <= 255

