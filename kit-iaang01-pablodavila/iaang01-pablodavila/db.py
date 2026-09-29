"""Conexión a tu base de datos. No necesitas cambiar nada aquí.

Este archivo decide solo por dónde conectarse:
  · corriendo en el servidor  -> DATABASE_URL       (pasa por el pooler)
  · corriendo en tu compu     -> DATABASE_URL_LOCAL (necesita ./tunel.sh)

La detección mira si hay /.dockerenv, que solo existe dentro de un contenedor.
Es la forma más simple de distinguir "estoy desplegado" de "estoy en la laptop"
sin que tú tengas que acordarte de cambiar una variable.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

EN_EL_SERVIDOR = Path("/.dockerenv").exists()


def url() -> str:
    if EN_EL_SERVIDOR:
        u = os.getenv("DATABASE_URL")
    else:
        u = os.getenv("DATABASE_URL_LOCAL") or os.getenv("DATABASE_URL")
    if not u:
        raise RuntimeError(
            "No encuentro la conexión. Revisa que el archivo .env esté junto a tu código."
        )
    return u


def conectar():
    """Una conexión nueva. Para scripts sueltos y para cargar datos."""
    import psycopg
    return psycopg.connect(url())


def leer_tabla(nombre: str):
    """Devuelve la tabla completa como DataFrame de pandas.

    Si la tabla todavía no existe devuelve None en vez de reventar, para que el
    front pueda mostrar un mensaje amable en lugar de una pantalla de error.
    """
    import pandas as pd
    if not nombre.replace("_", "").isalnum():
        raise ValueError("Nombre de tabla inválido: usa solo letras, números y _")
    try:
        with conectar() as cx:
            return pd.read_sql_query(f'SELECT * FROM "{nombre}"', cx)
    except Exception:
        return None
