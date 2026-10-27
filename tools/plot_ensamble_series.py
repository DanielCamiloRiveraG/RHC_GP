#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Gráficas de series temporales para todas las estaciones y frecuencias

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Capturar el argumento de la línea de comandos
if len(sys.argv) < 2:
    print("Uso incorrecto. Debes proporcionar la ruta base.")
    print("Ejemplo de uso: ./plot_ensamble_series.py /ruta/a/RHC_GP/")
    sys.exit(1)

base_dir = Path(sys.argv[1])
if not base_dir.is_dir():
    print(f"Error: El directorio '{base_dir}' no existe.")
    sys.exit(1)

# Construir rutas absolutas desde el directorio base ingresado por parámetro
BASE_AGREGACIONES = base_dir / 'Agregacion_variables'
CARPETA_SALIDA = base_dir / 'Ensamble_series_temporales'
CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)

COLORES = {
    'precipitacion': '#1f77b4',  # azul de la serie de referencia
    'Tmax': '#d62728',  # Rojo
    'Tmed': '#ff7f0e',  # Naranja
    'Tmin': '#f1c40f',  # Amarillo
    'et': '#2ca02c',
    'q': '#17becf'
}

ARCHIVOS = {
    'precipitacion': 'precip',
    'Tmax': 'tmax',
    'Tmed': 'tave',
    'Tmin': 'tmin',
    'et': 'et',
    'q': 'q'
}


def leer_agregacion(ruta):
    """Lee un CSV agregado y devuelve un DataFrame indexado por fecha."""
    df = pd.read_csv(ruta)
    columna_fecha = 'time' if 'time' in df.columns else 'datetime'
    
    # Convertir columna a string limpiando espacios
    s_fecha = df[columna_fecha].astype(str).str.strip()
    
    # Si la fecha es de 4 dígitos (ej. "1981"), formatearla como "1981-01-01"
    s_fecha = s_fecha.apply(lambda x: f"{x}-01-01" if (len(x) == 4 and x.isdigit()) else x)
    
    df[columna_fecha] = pd.to_datetime(s_fecha, errors='coerce')
    df = df.dropna(subset=[columna_fecha]).set_index(columna_fecha)
    df.index.name = 'Fecha'
    return df.apply(pd.to_numeric, errors='coerce').sort_index()


def cargar_frecuencia(frecuencia):
    datos = {}
    for variable, prefijo in ARCHIVOS.items():
        posibles_rutas = [
            BASE_AGREGACIONES / f'{prefijo}_{frecuencia}.csv'
        ]
        
        # Variación 'diario.csv' en lugar de 'diaria.csv' (ej: q_diario.csv)
        if frecuencia == 'diaria':
            posibles_rutas.append(BASE_AGREGACIONES / f'{prefijo}_diario.csv')
            
        # Variaciones para evapotranspiración (et_mm vs et)
        if prefijo == 'et_mm':
            posibles_rutas.append(BASE_AGREGACIONES / f'et_{frecuencia}.csv')
            if frecuencia == 'diaria':
                posibles_rutas.append(BASE_AGREGACIONES / f'et_diario.csv')

        ruta_encontrada = None
        for r in posibles_rutas:
            if r.exists():
                ruta_encontrada = r
                break

        if ruta_encontrada:
            datos[variable] = leer_agregacion(ruta_encontrada)
        else:
            print(f'ADVERTENCIA: no se encontró {BASE_AGREGACIONES / f"{prefijo}_{frecuencia}.csv"}')
    return datos


def estaciones_disponibles(datos):
    estaciones = set()
    for df in datos.values():
        estaciones.update(df.columns)
    return sorted(estaciones)


def dibujar_serie(ax, df, estacion, color, etiqueta, linewidth=1.1):
    if df is not None and estacion in df.columns:
        serie = df[estacion].dropna()
        if not serie.empty:
            ax.plot(serie.index, serie, color=color, linewidth=linewidth, label=etiqueta)


for frecuencia in ('diaria', 'mensual', 'anual'):
    datos = cargar_frecuencia(frecuencia)
    for estacion in estaciones_disponibles(datos):
        figura, ejes = plt.subplots(4, 1, figsize=(16, 11), sharex=False)
        figura.patch.set_facecolor('white')
        figura.suptitle(
            f'Series temporales - estación {estacion} ({frecuencia})',
            fontsize=15,
            color='#333333',
            y=0.995
        )

        dibujar_serie(ejes[0], datos.get('precipitacion'), estacion,
                      COLORES['precipitacion'], 'Precipitación')
        ejes[0].set_ylabel('P (mm)')
        ejes[0].set_title('Precipitación', loc='left', color='#333333')

        for variable, etiqueta in (
            ('Tmax', 'Tmax'),
            ('Tmed', 'Tmed'),
            ('Tmin', 'Tmin')
        ):
            dibujar_serie(
                ejes[1],
                datos.get(variable),
                estacion,
                COLORES[variable],
                etiqueta,
                linewidth=1.0
            )
        ejes[1].set_ylabel('T (°C)')
        ejes[1].set_title('Temperaturas', loc='left', color='#333333')

        dibujar_serie(ejes[2], datos.get('et'), estacion,
                      COLORES['et'], 'ET')
        ejes[2].set_ylabel('ET (mm)')
        ejes[2].set_title('Evapotranspiración', loc='left', color='#333333')

        dibujar_serie(ejes[3], datos.get('q'), estacion,
                      COLORES['q'], 'Q')
        ejes[3].set_ylabel('Q (m³/s)')
        ejes[3].set_title('Caudal', loc='left', color='#333333')
        ejes[3].set_xlabel('Fecha')

        for eje in ejes:
            eje.set_facecolor('white')
            eje.grid(True, linestyle='--', linewidth=0.8, color='gray', alpha=0.4)
            eje.tick_params(colors='#333333')
            for borde in eje.spines.values():
                borde.set_color('#333333')
            eje.legend(loc='upper right', frameon=False)
            
            # Formato de eje X adaptado según la frecuencia
            eje.xaxis.set_major_locator(mdates.AutoDateLocator())
            if frecuencia == 'anual':
                eje.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            else:
                eje.xaxis.set_major_formatter(mdates.ConciseDateFormatter(eje.xaxis.get_major_locator()))

        figura.tight_layout(rect=(0, 0, 1, 0.98))
        carpeta_frecuencia = CARPETA_SALIDA / frecuencia
        carpeta_frecuencia.mkdir(parents=True, exist_ok=True)
        nombre = f'Serie_Tiempo_{estacion}_{frecuencia}'
        figura.savefig(carpeta_frecuencia / f'{nombre}.svg', format='svg', bbox_inches='tight')
        figura.savefig(carpeta_frecuencia / f'{nombre}.png', format='png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(figura)

print(f'Gráficas guardadas en: {CARPETA_SALIDA.resolve()}')
