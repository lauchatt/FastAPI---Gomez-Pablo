import pandas as pd
import requests
import tempfile
import os
from app.database import SessionLocal, engine
from app.models import Base, Question
from app.categories import CATEGORIES

BASE_URL = "https://huggingface.co/datasets/rlyapin/OpenTriviaQA/resolve/main"


def download_parquet(url: str) -> str:
    print(f"Descargando {url}...")
    r = requests.get(url, stream=True)
    r.raise_for_status()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
    tmp.write(r.content)
    tmp.close()
    return tmp.name


def load_category(categoria: dict[str, str]) -> pd.DataFrame:
    config = categoria["dataset_config"]
    url = f"{BASE_URL}/{config}/data.parquet"
    parquet_path = download_parquet(url)
    df = pd.read_parquet(parquet_path)
    os.unlink(parquet_path)
    df["categoria_local"] = categoria["name"]
    return df


def load_questions():
    Base.metadata.create_all(bind=engine)

    dataframes = [load_category(categoria) for categoria in CATEGORIES]
    df = pd.concat(dataframes, ignore_index=True)

    print(f"Columnas disponibles: {list(df.columns)}")
    print(f"Filas totales: {len(df)}")
    print(df["categoria_local"].value_counts())

    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            question = Question(
                question=row.get("question", ""),
                answer=row.get("answer", ""),
                category=row.get("categoria_local", None),
                source=f"rlyapin/OpenTriviaQA/{row.get('categoria_local', '')}",
            )
            session.add(question)

        session.commit()
        print(f"Se insertaron {len(df)} preguntas correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    load_questions()