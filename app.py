"""Tablero local de seguimiento de obra con Streamlit."""

from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "outputs" / "avance_obra" / "datos_sinteticos_obra.xlsx"
CHART_DIR = BASE_DIR / "outputs" / "avance_obra" / "graficos"


st.set_page_config(page_title="Control de obra", page_icon="🏗️", layout="wide")
st.markdown(
    """
    <style>
      .stApp { background: #08070D; color: #F5F3FF; }
      [data-testid="stMetric"] { background: #171120; border: 1px solid #4C1D95;
        border-radius: 12px; padding: 14px; }
      [data-testid="stMetricLabel"] { color: #D8B4FE; }
      [data-testid="stMetricValue"] { color: #F5F3FF; }
      h1, h2, h3 { color: #D8B4FE; }
      div[data-testid="stExpander"] { border-color: #4C1D95; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def cargar_datos() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Lee las tres hojas del archivo Excel generado para el ejercicio."""
    curva_s = pd.read_excel(DATA_FILE, sheet_name="Curva S", header=2)
    partidas = pd.read_excel(DATA_FILE, sheet_name="Avance por partidas", header=2)
    resumen = pd.read_excel(DATA_FILE, sheet_name="Resumen", header=2)
    return curva_s, partidas, resumen


def main() -> None:
    st.title("Tablero de control de obra")
    st.caption("Ejercicio sintético · Corte a diciembre de 2026")

    if not DATA_FILE.exists():
        st.error("No se encontró el archivo Excel de datos. Ejecute primero generar_datos_sinteticos.mjs.")
        st.stop()

    curva_s, partidas, resumen = cargar_datos()
    avance_programado = curva_s["Avance fisico acumulado programado (%)"].iloc[-1]
    avance_real = curva_s["Avance fisico acumulado real (%)"].iloc[-1]
    desviacion = avance_real - avance_programado
    presupuesto = partidas["Presupuesto (COP)"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avance programado", f"{avance_programado:.1f}%")
    col2.metric("Avance real", f"{avance_real:.1f}%", f"{desviacion:.1f} p.p.")
    col3.metric("Presupuesto contractual", f"COP ${presupuesto / 1_000_000:,.0f} M")
    col4.metric("Partidas con retraso", int((partidas["Estado"] == "Con retraso").sum()))

    st.divider()
    izquierda, derecha = st.columns(2)
    with izquierda:
        st.subheader("Curva S")
        st.image(CHART_DIR / "curva_s_obra.png", use_container_width=True)
    with derecha:
        st.subheader("Avance por partidas")
        st.image(CHART_DIR / "avance_por_partidas.png", use_container_width=True)

    st.divider()
    with st.expander("Datos mensuales de la curva S", expanded=False):
        st.dataframe(curva_s, use_container_width=True, hide_index=True)
    with st.expander("Detalle por partidas", expanded=True):
        st.dataframe(partidas, use_container_width=True, hide_index=True)
    with st.expander("Resumen del proyecto", expanded=False):
        st.dataframe(resumen, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
