#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Capturar el argumento de la línea de comandos
if len(sys.argv) < 2:
    print("Uso incorrecto. Debes proporcionar la ruta base.")
    print("Ejemplo de uso: ./plot_ensamble_boxplots.py /ruta/a/RHC_GP/")
    sys.exit(1)

base_dir = Path(sys.argv[1])
if not base_dir.is_dir():
    print(f"Error: El directorio '{base_dir}' no existe.")
    sys.exit(1)

# Rutas absolutas configuradas según la ruta base proporcionada
BASE_AGREGACIONES = base_dir / 'Agregacion_variables'
CARPETA_BOXPLOTS = base_dir / 'Ensamble_boxplots'
CARPETA_BOXPLOTS.mkdir(parents=True, exist_ok=True)

# Mapeo actualizado de archivos sin subcarpetas y con los nombres generados
ARCHIVOS_BOXPLOT = {
    'Precipitacion': ('precip_mensual.csv', '#1f77b4', 'Precipitacion acumulada (mm/mes)'),
    'Tmax': ('tmax_mensual.csv', '#d62728', 'Temperatura maxima (°C)'),
    'Tmed': ('tave_mensual.csv', '#ff7f0e', 'Temperatura media (°C)'),
    'Tmin': ('tmin_mensual.csv', '#9467bd', 'Temperatura minima (°C)'),
    'ET': ('et_mensual.csv', '#2ca02c', 'Evapotranspiracion acumulada (mm/mes)'),
    'Q': ('q_mensual.csv', '#17becf', 'Caudal (m³/s)'),
}

MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']


def leer_datos_mensuales(ruta):
    df = pd.read_csv(ruta)
    columna_fecha = 'time' if 'time' in df.columns else 'datetime'
    
    s_fecha = df[columna_fecha].astype(str).str.strip()
    df[columna_fecha] = pd.to_datetime(s_fecha, errors='coerce')
    df = df.dropna(subset=[columna_fecha]).copy()
    df['mes'] = df[columna_fecha].dt.month
    return df.set_index(columna_fecha).sort_index()


def estaciones_disponibles(datos):
    estaciones = set()
    for df in datos.values():
        estaciones.update(columna for columna in df.columns if columna != 'mes')
    return sorted(estaciones)


def crear_boxplots_estacion(datos, estacion):
    figura, ejes = plt.subplots(3, 2, figsize=(14, 12), squeeze=False)
    ejes = ejes.ravel()
    figura.patch.set_facecolor('white')
    figura.suptitle(
        f'Variabilidad mensual multianual - Subcuenca {estacion}',
        fontsize=16,
        fontweight='bold'
    )

    configuraciones = [
        (variable, color, etiqueta_y)
        for variable, (_, color, etiqueta_y) in ARCHIVOS_BOXPLOT.items()
    ]

    for eje, (variable, color, etiqueta_y) in zip(ejes, configuraciones):
        df = datos.get(variable)
        if df is None or estacion not in df.columns:
            eje.set_visible(False)
            continue

        serie = pd.to_numeric(df[estacion], errors='coerce')
        datos_por_mes = [
            serie[df['mes'] == mes].dropna().values
            for mes in range(1, 13)
        ]

        if not any(len(valores) for valores in datos_por_mes):
            eje.set_visible(False)
            continue

        boxplot = eje.boxplot(
            datos_por_mes,
            patch_artist=True,
            widths=0.65,
            showmeans=False,
            showfliers=True
        )

        for caja in boxplot['boxes']:
            caja.set_facecolor(color)
            caja.set_edgecolor('#1f1f1f')
            caja.set_alpha(0.85)
        for elemento in ('whiskers', 'caps', 'medians'):
            for linea in boxplot[elemento]:
                linea.set_color('#1f1f1f')
                linea.set_linewidth(1.0)

        eje.set_xticks(range(1, 13), MESES)
        eje.set_xlabel('Mes')
        eje.set_ylabel(etiqueta_y)
        eje.set_title(variable, loc='left', fontsize=12, fontweight='bold')
        eje.grid(True, axis='y', color='#cccccc', linewidth=0.8)
        eje.tick_params(colors='#262626')
        for borde in eje.spines.values():
            borde.set_color('#cccccc')

    figura.tight_layout(rect=(0, 0, 1, 0.96))
    nombre = f'Boxplots_mensuales_{estacion}'
    figura.savefig(CARPETA_BOXPLOTS / f'{nombre}.svg', format='svg', bbox_inches='tight')
    figura.savefig(CARPETA_BOXPLOTS / f'{nombre}.png', format='png', dpi=300, bbox_inches='tight')
    plt.close(figura)


datos_mensuales = {}
for variable, (archivo, color, etiqueta_y) in ARCHIVOS_BOXPLOT.items():
    ruta = BASE_AGREGACIONES / archivo
    
    # Alternativa por si el archivo de evapotranspiración tiene el nombre et_mensual.csv
    if not ruta.exists() and archivo == 'et_mm_mensual.csv':
        ruta_alt = BASE_AGREGACIONES / 'et_mensual.csv'
        if ruta_alt.exists():
            ruta = ruta_alt

    if not ruta.exists():
        print(f'ADVERTENCIA: no se encontró {ruta}')
        continue
    datos_mensuales[variable] = leer_datos_mensuales(ruta)

figuras_generadas = 0
for estacion in estaciones_disponibles(datos_mensuales):
    crear_boxplots_estacion(datos_mensuales, estacion)
    figuras_generadas += 1

print(f'Figuras generadas: {figuras_generadas}')
print(f'Archivos guardados en: {CARPETA_BOXPLOTS.resolve()}')
