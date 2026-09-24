import pandas as pd
import requests
import tempfile
import os


BASE_URL = "https://huggingface.co/datasets/rlyapin/OpenTriviaQA/resolve/main"

CATEGORIES = [
    "animals",
    "brain-teasers",
    "celebrities",
    "entertainment",
    "for-kids",
    "general",
    "geography",
    "history",
    "hobbies",
    "humanities",
    "literature",
    "movies",
    "music",
    "newest",
    "people",
    "rated",
    "religion-faith",
    "science-technology",
    "sports",
    "television",
    "video-games",
    "world",
]


def download_parquet(url):
    response = requests.get(url)
    response.raise_for_status()

    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".parquet"
    )

    tmp.write(response.content)
    tmp.close()

    return tmp.name


def main():

    dataframes = []

    for folder in CATEGORIES:

        url = f"{BASE_URL}/{folder}/data.parquet"

        print(f"Descargando {folder}...")

        path = download_parquet(url)

        df = pd.read_parquet(path)

        os.unlink(path)

        # SOLO nos interesan estas dos columnas
        df = df[["question", "answer"]]

        dataframes.append(df)

    # Unir todas las preguntas
    final_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    # Guardar un único archivo
    final_df.to_parquet(
        "opentrivia.parquet",
        index=False
    )

    print()
    print("Conversión terminada.")
    print(f"Total de preguntas: {len(final_df)}")
    print(f"Columnas: {list(final_df.columns)}")
    print()
    print(final_df.head())


if __name__ == "__main__":
    main()