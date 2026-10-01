
from pathlib import Path
import random
import re
import subprocess
import sys

import pandas as pd


# ============================================================
# CONFIGURACIÓN
# ============================================================

REPO_URL = "https://github.com/uberspot/OpenTriviaQA.git"
REPO_DIR = Path("OpenTriviaQA")
CATEGORIES_DIR = REPO_DIR / "categories"

OUTPUT_FILE = Path("opentrivia.parquet")

# Semilla para que el resultado sea reproducible.
# Si querés una mezcla diferente, cambiá este número.
RANDOM_SEED = 42

# Solo aceptamos preguntas con exactamente 4 opciones.
REQUIRED_OPTIONS = 4


# ============================================================
# DESCARGAR / ACTUALIZAR REPOSITORIO
# ============================================================

def download_repository():
    """
    Clona OpenTriviaQA utilizando sparse-checkout.

    Solamente se obtiene la carpeta:
        categories/

    No se descargan los archivos del resto del repositorio.
    """

    # --------------------------------------------------------
    # Si ya existe, no volvemos a clonar
    # --------------------------------------------------------

    if REPO_DIR.exists():

        # Verificamos que realmente tenga categories
        if CATEGORIES_DIR.exists():

            print("=" * 70)
            print("OPENTRIVIAQA YA EXISTE")
            print("=" * 70)
            print("Usando la carpeta categories existente.\n")

            return

        else:
            print("=" * 70)
            print("CARPETA INCOMPLETA")
            print("=" * 70)
            print(
                "Existe OpenTriviaQA, pero no existe categories."
            )
            print("Eliminando carpeta para volver a descargar...\n")

            import shutil

            try:
                shutil.rmtree(REPO_DIR)
            except Exception as e:
                print(
                    f"No se pudo eliminar {REPO_DIR}: {e}"
                )
                print(
                    "\nCerrá VS Code, terminales o cualquier "
                    "programa que esté usando la carpeta."
                )
                sys.exit(1)

    # --------------------------------------------------------
    # CLONAR REPOSITORIO
    # --------------------------------------------------------

    print("=" * 70)
    print("DESCARGANDO OPENTRIVIAQA")
    print("=" * 70)

    print("Configurando sparse-checkout...")
    print("Solo se descargará la carpeta: categories/")
    print()

    result = subprocess.run(
        [
            "git",
            "clone",
            "--depth", "1",
            "--filter=blob:none",
            "--sparse",
            REPO_URL,
            str(REPO_DIR),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:

        print("Error descargando el repositorio:")
        print(result.stderr)

        # Mostrar también stdout por si Git dejó información útil
        if result.stdout:
            print(result.stdout)

        sys.exit(1)

    # --------------------------------------------------------
    # CONFIGURAR SPARSE CHECKOUT
    # --------------------------------------------------------

    print("Configurando sparse-checkout...")

    result = subprocess.run(
        [
            "git",
            "-C",
            str(REPO_DIR),
            "sparse-checkout",
            "set",
            "categories",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:

        print("Error configurando sparse-checkout:")
        print(result.stderr)

        if result.stdout:
            print(result.stdout)

        sys.exit(1)

    # --------------------------------------------------------
    # VERIFICAR
    # --------------------------------------------------------

    if not CATEGORIES_DIR.exists():

        print(
            "ERROR: categories no fue encontrada después "
            "del sparse-checkout."
        )

        sys.exit(1)

    print()
    print("✓ Repositorio configurado correctamente.")
    print("✓ Solo se utilizará la carpeta categories.")
    print()


# ============================================================
# LIMPIEZA
# ============================================================

def clean_text(text: str) -> str:
    """
    Limpia espacios innecesarios y saltos de línea.
    """

    if text is None:
        return ""

    text = text.replace("\r", " ")
    text = text.replace("\n", " ")

    # Reemplazar múltiples espacios
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# NORMALIZACIÓN PARA DUPLICADOS
# ============================================================

def normalize_for_comparison(text: str) -> str:
    """
    Normaliza texto para detectar duplicados.

    No modifica el texto final.
    """

    text = text.lower().strip()

    # Eliminar espacios repetidos
    text = re.sub(r"\s+", " ", text)

    # Eliminar espacios antes/después de puntuación
    text = re.sub(
        r"\s+([,.!?;:])",
        r"\1",
        text,
    )

    return text


# ============================================================
# PARSER
# ============================================================

def parse_file(file_path: Path):
    """
    Parsea un archivo de OpenTriviaQA.

    Formato esperado:

    #Q Pregunta
    ^ Respuesta correcta
    A opción
    B opción
    C opción
    D opción
    """

    questions = []

    try:

        # utf-8-sig elimina un posible BOM
        text = file_path.read_text(
            encoding="utf-8-sig",
            errors="replace",
        )

    except Exception as e:

        print(
            f"No se pudo leer {file_path}: {e}"
        )

        return questions

    lines = text.splitlines()

    current_question = None
    current_answer = None
    current_options = []

    def save_current_question():

        nonlocal current_question
        nonlocal current_answer
        nonlocal current_options

        if not current_question:
            return

        # Necesitamos exactamente 4 opciones.
        if len(current_options) != REQUIRED_OPTIONS:
            return

        question = clean_text(
            current_question
        )

        answer = clean_text(
            current_answer
        )

        options = [
            clean_text(option)
            for _, option in current_options
        ]

        # ----------------------------------------------------
        # Validaciones básicas
        # ----------------------------------------------------

        if not question:
            return

        if not answer:
            return

        if any(
            not option
            for option in options
        ):
            return

        # ----------------------------------------------------
        # Verificar opciones duplicadas
        # ----------------------------------------------------

        normalized_options = [
            normalize_for_comparison(option)
            for option in options
        ]

        if len(set(normalized_options)) != REQUIRED_OPTIONS:
            return

        # ----------------------------------------------------
        # Verificar respuesta correcta
        # ----------------------------------------------------

        normalized_answer = (
            normalize_for_comparison(answer)
        )

        if normalized_answer not in normalized_options:
            return

        # ----------------------------------------------------
        # Mezclar opciones
        # ----------------------------------------------------

        random.shuffle(options)

        questions.append(
            {
                "question": question,
                "answer": answer,
                "options": options,
                "source": "OpenTriviaQA",
                "source_file": str(file_path),
            }
        )

    # --------------------------------------------------------
    # Procesar líneas
    # --------------------------------------------------------

    for raw_line in lines:

        line = raw_line.strip()

        # Nueva pregunta
        if line.startswith("#Q"):

            # Guardar pregunta anterior
            save_current_question()

            current_question = (
                line[2:].strip()
            )

            current_answer = None
            current_options = []

            continue

        # Respuesta correcta
        if line.startswith("^"):

            current_answer = (
                line[1:].strip()
            )

            continue

        # Opciones:
        #
        # A ...
        # B ...
        # C ...
        # D ...
        #
        # También soportamos E, F, etc.
        match = re.match(
            r"^([A-Z])\s+(.+)$",
            line,
        )

        if match:

            letter = match.group(1)

            option_text = (
                match.group(2).strip()
            )

            current_options.append(
                (
                    letter,
                    option_text,
                )
            )

    # Guardar última pregunta
    save_current_question()

    return questions


# ============================================================
# ELIMINAR DUPLICADOS
# ============================================================

def remove_duplicates(questions):

    """
    Elimina preguntas duplicadas.
    """

    unique = []
    seen = set()

    duplicates = 0

    for item in questions:

        normalized_question = (
            normalize_for_comparison(
                item["question"]
            )
        )

        key = normalized_question

        if key in seen:

            duplicates += 1
            continue

        seen.add(key)

        unique.append(item)

    return unique, duplicates


# ============================================================
# CONSTRUIR DATAFRAME
# ============================================================

def build_dataframe(questions):

    """
    Convierte las preguntas parseadas
    a un DataFrame.
    """

    rows = []

    for item in questions:

        options = item["options"]

        rows.append(
            {
                "question": item["question"],
                "answer": item["answer"],
                "option_1": options[0],
                "option_2": options[1],
                "option_3": options[2],
                "option_4": options[3],
                "source": item["source"],
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# VALIDACIÓN FINAL
# ============================================================

def validate_dataframe(df):

    """
    Hace una última validación antes
    de generar el Parquet.
    """

    if df.empty:

        raise ValueError(
            "El DataFrame está vacío."
        )

    required_columns = [
        "question",
        "answer",
        "option_1",
        "option_2",
        "option_3",
        "option_4",
        "source",
    ]

    # --------------------------------------------------------
    # Verificar columnas
    # --------------------------------------------------------

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Faltan columnas: {missing}"
        )

    # --------------------------------------------------------
    # Verificar valores nulos
    # --------------------------------------------------------

    for column in required_columns:

        nulls = df[column].isna().sum()

        if nulls > 0:

            raise ValueError(
                f"La columna '{column}' tiene "
                f"{nulls} valores nulos."
            )

    # --------------------------------------------------------
    # Verificar respuestas
    # --------------------------------------------------------

    invalid_answers = 0

    for _, row in df.iterrows():

        options = {
            normalize_for_comparison(
                row["option_1"]
            ),
            normalize_for_comparison(
                row["option_2"]
            ),
            normalize_for_comparison(
                row["option_3"]
            ),
            normalize_for_comparison(
                row["option_4"]
            ),
        }

        answer = normalize_for_comparison(
            row["answer"]
        )

        if answer not in options:

            invalid_answers += 1

    if invalid_answers > 0:

        raise ValueError(
            f"{invalid_answers} preguntas tienen "
            "una respuesta correcta que no aparece "
            "entre sus cuatro opciones."
        )

    # --------------------------------------------------------
    # Verificar duplicados
    # --------------------------------------------------------

    duplicated = (
        df["question"]
        .duplicated()
        .sum()
    )

    if duplicated > 0:

        raise ValueError(
            f"Hay {duplicated} preguntas duplicadas."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Semilla
    # --------------------------------------------------------

    random.seed(RANDOM_SEED)

    print()
    print("=" * 70)
    print("CONVERSOR OPENTRIVIAQA → PARQUET")
    print("=" * 70)
    print()

    # --------------------------------------------------------
    # 1. Descargar repositorio
    # --------------------------------------------------------

    download_repository()

    # --------------------------------------------------------
    # 2. Buscar archivos
    # --------------------------------------------------------

    print("=" * 70)
    print("BUSCANDO ARCHIVOS")
    print("=" * 70)

    files = [
        file
        for file in CATEGORIES_DIR.rglob("*")
        if file.is_file()
    ]

    print(
        f"Archivos encontrados: {len(files)}"
    )

    print()

    # --------------------------------------------------------
    # 3. Parsear archivos
    # --------------------------------------------------------

    print("=" * 70)
    print("PROCESANDO ARCHIVOS")
    print("=" * 70)

    all_questions = []

    total_files_processed = 0

    for file_path in files:

        print(
            f"Procesando: {file_path}"
        )

        questions = parse_file(
            file_path
        )

        all_questions.extend(
            questions
        )

        total_files_processed += 1

    # --------------------------------------------------------
    # Resultado del parseo
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("RESULTADO DEL PARSEO")
    print("=" * 70)

    print(
        f"Archivos procesados: "
        f"{total_files_processed}"
    )

    print(
        f"Preguntas válidas encontradas: "
        f"{len(all_questions)}"
    )

    # --------------------------------------------------------
    # 4. Eliminar duplicados
    # --------------------------------------------------------

    all_questions, duplicates = (
        remove_duplicates(
            all_questions
        )
    )

    print(
        f"Preguntas duplicadas eliminadas: "
        f"{duplicates}"
    )

    print(
        f"Preguntas finales: "
        f"{len(all_questions)}"
    )

    if not all_questions:

        print(
            "\nNo se encontraron "
            "preguntas válidas."
        )

        sys.exit(1)

    # --------------------------------------------------------
    # 5. Construir DataFrame
    # --------------------------------------------------------

    df = build_dataframe(
        all_questions
    )

    # --------------------------------------------------------
    # 6. Validación
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("VALIDANDO DATASET")
    print("=" * 70)

    validate_dataframe(df)

    print("✓ Columnas correctas")
    print("✓ Sin valores nulos")
    print("✓ 4 opciones por pregunta")
    print("✓ Respuestas correctas válidas")
    print("✓ Sin preguntas duplicadas")

    # --------------------------------------------------------
    # 7. Mezclar dataset
    # --------------------------------------------------------

    df = df.sample(
        frac=1,
        random_state=RANDOM_SEED,
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # 8. Guardar Parquet
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("GUARDANDO PARQUET")
    print("=" * 70)

    df.to_parquet(
        OUTPUT_FILE,
        engine="pyarrow",
        index=False,
    )

    print(
        f"✓ Archivo generado: "
        f"{OUTPUT_FILE}"
    )

    print(
        f"✓ Preguntas: "
        f"{len(df)}"
    )

    print(
        f"✓ Tamaño: "
        f"{OUTPUT_FILE.stat().st_size / 1024 / 1024:.2f} MB"
    )

    # --------------------------------------------------------
    # 9. Mostrar ejemplos
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("EJEMPLOS")
    print("=" * 70)

    for index, row in df.head(5).iterrows():

        print()

        print(
            f"Pregunta {index + 1}:"
        )

        print(
            f"  {row['question']}"
        )

        print(
            f"  A) {row['option_1']}"
        )

        print(
            f"  B) {row['option_2']}"
        )

        print(
            f"  C) {row['option_3']}"
        )

        print(
            f"  D) {row['option_4']}"
        )

        print(
            f"  ✓ Correcta: "
            f"{row['answer']}"
        )

    # --------------------------------------------------------
    # FIN
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("CONVERSIÓN COMPLETADA")
    print("=" * 70)
    print()


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    main()

