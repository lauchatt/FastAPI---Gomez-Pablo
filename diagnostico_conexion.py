"""
Script de diagnóstico: captura los bytes exactos que psycopg2
no puede decodificar al conectarse, para ver el error real.
"""

import psycopg2

DATABASE_URL = "postgresql://admin:admin123@localhost:5432/questions_db"

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✓ Conexión exitosa, no hay ningún problema.")
    conn.close()

except UnicodeDecodeError as e:
    print("Se encontró el error de decodificación. Bytes en crudo:")
    print(repr(e.object))
    print()
    print("Intentando decodificar como Latin-1 (para ver el mensaje real):")
    try:
        print(e.object.decode("latin-1"))
    except Exception:
        print("(no se pudo ni con latin-1)")

except Exception as e:
    print(f"Otro tipo de error (esto es más normal de ver): {type(e).__name__}")
    print(str(e))
