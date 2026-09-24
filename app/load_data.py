import pandas as pd

from app.database import SessionLocal, engine
from app.models import Base, Question, Categorization


DATASET_FILE = "opentrivia.parquet"


def load_questions():

    Base.metadata.create_all(bind=engine)

    df = pd.read_parquet(DATASET_FILE)

    print(f"Columnas: {list(df.columns)}")
    print(f"Preguntas: {len(df)}")

    session = SessionLocal()

    try:

        # Eliminar categorizaciones anteriores
        deleted_categories = session.query(Categorization).delete()

        print(
            f"Se eliminaron {deleted_categories} categorizaciones anteriores."
        )

        # Eliminar preguntas anteriores
        deleted_questions = session.query(Question).delete()

        print(
            f"Se eliminaron {deleted_questions} preguntas anteriores."
        )

        # Insertar las nuevas preguntas
        for _, row in df.iterrows():

            question = Question(
                question=row["question"],
                answer=row["answer"],
                category=None,
                source=None,
            )

            session.add(question)

        session.commit()

        print(
            f"Se insertaron {len(df)} preguntas."
        )

    except Exception as e:

        session.rollback()
        print(f"Error: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    load_questions()
    