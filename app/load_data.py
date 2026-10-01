import pandas as pd

from app.database import SessionLocal, engine
from app.models import Base, Question, Categorization


DATASET_FILE = "opentrivia.parquet"


def load_questions():

    # ========================================================
    # 1. RECREAR LAS TABLAS
    # ========================================================

    print("=" * 70)
    print("RECREANDO BASE DE DATOS")
    print("=" * 70)

    print("Eliminando tablas existentes...")

    Base.metadata.drop_all(bind=engine)

    print("✓ Tablas anteriores eliminadas.")

    print("Creando tablas nuevas...")

    Base.metadata.create_all(bind=engine)

    print("✓ Tablas creadas según models.py.")
    print()

    # ========================================================
    # 2. LEER PARQUET
    # ========================================================

    print("=" * 70)
    print("CARGANDO DATASET")
    print("=" * 70)

    df = pd.read_parquet(DATASET_FILE)

    print(f"Columnas: {list(df.columns)}")
    print(f"Preguntas: {len(df)}")
    print()

    # ========================================================
    # 3. INSERTAR PREGUNTAS
    # ========================================================

    session = SessionLocal()

    try:

        print("=" * 70)
        print("INSERTANDO PREGUNTAS")
        print("=" * 70)

        for _, row in df.iterrows():

            question = Question(
                question=row["question"],
                answer=row["answer"],
                option_1=row["option_1"],
                option_2=row["option_2"],
                option_3=row["option_3"],
                option_4=row["option_4"],
                category=None,
                source="OpenTriviaQA",
            )

            session.add(question)

        session.commit()

        print()
        print(
            f"✓ Se insertaron {len(df)} preguntas."
        )

    except Exception as e:

        session.rollback()

        print()
        print("=" * 70)
        print("ERROR")
        print("=" * 70)

        print(e)

    finally:

        session.close()


if __name__ == "__main__":
    load_questions()

