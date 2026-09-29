"""Tu front en Streamlit. Ya trae la conexión cableada: cambia solo la lógica.

Para publicarlo:  ./deploy.sh
Queda en:         https://hatchvps.com/iaang01/pablodavila/app/
"""
import pandas as pd
import streamlit as st

import db

st.set_page_config(page_title="Mi proyecto", layout="wide")

TABLA = "ventas"   # <- cambia esto por el nombre de TU tabla


# @st.cache_resource es la línea más importante de este archivo.
# Sin ella, Streamlit abre una conexión NUEVA cada vez que mueves un filtro, y
# con 36 alumnos a la vez eso agota la base. Con ella, la conexión se abre una
# sola vez y se reutiliza.
@st.cache_resource
def conexion():
    return db.conectar()


@st.cache_data(ttl=60)
def cargar(tabla: str) -> pd.DataFrame | None:
    try:
        return pd.read_sql_query(f'SELECT * FROM "{tabla}"', conexion())
    except Exception:
        return None


st.title("Mi proyecto")

datos = cargar(TABLA)

if datos is None or datos.empty:
    st.info(
        f"Aún no cargas tu tabla **{TABLA}**.\n\n"
        "Pídele a tu agente que la cargue y vuelve a recargar esta página."
    )
    st.stop()

st.caption(f"{len(datos):,} filas en «{TABLA}»")
st.dataframe(datos, use_container_width=True)

# --- A partir de aquí construye lo tuyo: filtros, gráficas, métricas ---
numericas = datos.select_dtypes("number").columns.tolist()
if numericas:
    col = st.selectbox("Columna a graficar", numericas)
    st.bar_chart(datos[col])
