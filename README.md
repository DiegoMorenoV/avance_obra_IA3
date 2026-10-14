# Gráficos de curva S y avance de obra

Este ejercicio contiene datos sintéticos para una obra de edificación de 12 meses y seis partidas. Los valores representan un escenario verosímil: se observa una desviación en los meses intermedios y una recuperación parcial hacia el cierre.

## Archivos

- `outputs/avance_obra/datos_sinteticos_obra.xlsx`: datos base con las hojas `Curva S` y `Avance por partidas`.
- `generar_graficos_obra.py`: lee el Excel y produce los gráficos PNG.
- `outputs/avance_obra/graficos/curva_s_obra.png`: comparación acumulada programado vs. real.
- `outputs/avance_obra/graficos/avance_por_partidas.png`: avance programado vs. real por partida.

## Ejecución

En PowerShell, desde la raíz del proyecto:

```powershell
.\.venv\Scripts\Activate.ps1
python generar_graficos_obra.py
```

El script usa `pandas` para leer el archivo Excel y `matplotlib` para crear los gráficos. La función `configurar_ejes` concentra la apariencia común: fondo negro, panel oscuro, texto claro y acentos morados. Esto mantiene una identidad visual uniforme en ambos resultados.

La curva S toma los porcentajes de avance físico acumulado mensual. El gráfico por partidas compara el avance físico programado y el real al corte del mes 12.

## Tablero web local

Para iniciar la página con Streamlit:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

El navegador abrirá el tablero local con indicadores, los dos gráficos y el detalle de los datos en tablas desplegables.
