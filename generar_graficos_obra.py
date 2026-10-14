"""Genera gráficos de control de obra a partir del Excel sintético del proyecto."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_EXCEL = BASE_DIR / "outputs" / "avance_obra" / "datos_sinteticos_obra.xlsx"
CARPETA_GRAFICOS = BASE_DIR / "outputs" / "avance_obra" / "graficos"
FONDO = "#08070D"
PANEL = "#12101A"
MORADO = "#A855F7"
MORADO_CLARO = "#D8B4FE"
MORADO_OSCURO = "#6D28D9"
TEXTO = "#F5F3FF"
GRILLA = "#3B2A50"


def configurar_ejes(ax):
    """Aplica el estilo negro y morado compartido por los gráficos."""
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=TEXTO, labelsize=9)
    ax.xaxis.label.set_color(TEXTO)
    ax.yaxis.label.set_color(TEXTO)
    for borde in ax.spines.values():
        borde.set_color(GRILLA)
    ax.grid(axis="y", color=GRILLA, alpha=0.55, linewidth=0.7)
    ax.set_axisbelow(True)


def crear_curva_s(df_curva: pd.DataFrame) -> Path:
    """Crea la curva S acumulada de avance físico planificado y real."""
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=FONDO)
    configurar_ejes(ax)
    ax.plot(df_curva["Mes"], df_curva["Avance fisico acumulado programado (%)"], color=MORADO_CLARO, linestyle="--", linewidth=2.4, marker="o", markersize=4.5, label="Programado")
    ax.plot(df_curva["Mes"], df_curva["Avance fisico acumulado real (%)"], color=MORADO, linewidth=3.0, marker="o", markersize=5, label="Real")
    ax.fill_between(df_curva["Mes"], df_curva["Avance fisico acumulado real (%)"], color=MORADO_OSCURO, alpha=0.16)
    ax.set_title("Curva S de avance físico acumulado", color=TEXTO, fontsize=16, fontweight="bold", pad=16)
    ax.set_xlabel("Mes de obra", labelpad=10)
    ax.set_ylabel("Avance acumulado (%)", labelpad=10)
    ax.set_ylim(0, 105)
    ax.legend(facecolor=PANEL, edgecolor=GRILLA, labelcolor=TEXTO, loc="upper left")
    ax.annotate(f"{df_curva['Avance fisico acumulado real (%)'].iloc[-1]:.1f}% real", xy=(df_curva["Mes"].iloc[-1], df_curva["Avance fisico acumulado real (%)"].iloc[-1]), xytext=(-55, -28), textcoords="offset points", color=MORADO_CLARO, fontsize=10, arrowprops={"arrowstyle": "-", "color": MORADO_CLARO})
    fig.tight_layout()
    destino = CARPETA_GRAFICOS / "curva_s_obra.png"
    fig.savefig(destino, dpi=180, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    return destino


def crear_avance_por_partidas(df_partidas: pd.DataFrame) -> Path:
    """Compara el avance físico planificado y real de cada partida."""
    partidas = df_partidas.sort_values("Orden")
    posiciones = range(len(partidas))
    ancho = 0.36
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=FONDO)
    configurar_ejes(ax)
    ax.bar([p - ancho / 2 for p in posiciones], partidas["Avance fisico programado (%)"], width=ancho, color=MORADO_CLARO, label="Programado")
    barras_reales = ax.bar([p + ancho / 2 for p in posiciones], partidas["Avance fisico real (%)"], width=ancho, color=MORADO, label="Real")
    for barra, valor in zip(barras_reales, partidas["Avance fisico real (%)"]):
        ax.text(barra.get_x() + barra.get_width() / 2, valor + 2.2, f"{valor:.0f}%", ha="center", va="bottom", color=TEXTO, fontsize=9)
    ax.set_title("Avance físico por partidas", color=TEXTO, fontsize=16, fontweight="bold", pad=16)
    ax.set_ylabel("Avance (%)", labelpad=10)
    ax.set_ylim(0, 115)
    ax.set_xticks(list(posiciones))
    ax.set_xticklabels(partidas["Partida"], rotation=18, ha="right", color=TEXTO)
    ax.legend(facecolor=PANEL, edgecolor=GRILLA, labelcolor=TEXTO, loc="upper left")
    fig.tight_layout()
    destino = CARPETA_GRAFICOS / "avance_por_partidas.png"
    fig.savefig(destino, dpi=180, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    return destino


def main() -> None:
    if not ARCHIVO_EXCEL.exists():
        raise FileNotFoundError(f"No se encontró {ARCHIVO_EXCEL}. Ejecute primero generar_datos_sinteticos.mjs.")
    CARPETA_GRAFICOS.mkdir(parents=True, exist_ok=True)
    curva_s = pd.read_excel(ARCHIVO_EXCEL, sheet_name="Curva S", header=2)
    partidas = pd.read_excel(ARCHIVO_EXCEL, sheet_name="Avance por partidas", header=2)
    archivos = [crear_curva_s(curva_s), crear_avance_por_partidas(partidas)]
    print("Gráficos generados:")
    for archivo in archivos:
        print(f"- {archivo.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
