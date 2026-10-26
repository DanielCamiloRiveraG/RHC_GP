#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__all__ = ['MeteoAggregator']
__version__ = '0.1'
__author__ = 'Camilo Rivera'

import os
import sys
import pandas as pd

class MeteoAggregator:
    def __init__(self, base_dir, model="gr4j"):
        self.base_dir = base_dir
        self.model = model
        self.subbasins = ["S1", "S2", "S3", "S4", "S5", "S6"]
        
        # Mapeo de columnas según metadatos (1=tave, 2=tmin, 3=tmax, 4=precip)
        # La precipitación suma (.sum), las temperaturas promedian (.mean)
        self.variables = {
            'tave': {'col_idx': 1, 'agg': 'mean'},
            'tmin': {'col_idx': 2, 'agg': 'mean'},
            'tmax': {'col_idx': 3, 'agg': 'mean'},
            'precip': {'col_idx': 4, 'agg': 'sum'}
        }

    def process_variable(self, var_name='precip'):
        """Procesa y agrupa la variable seleccionada para las 6 subcuencas a nivel diario, mensual y anual."""
        if var_name not in self.variables:
            print(f"Error: La variable '{var_name}' no es válida. Opciones: {list(self.variables.keys())}")
            return

        var_info = self.variables[var_name]
        agg_type = var_info['agg']
        col_idx = var_info['col_idx']

        data_dict = {}

        print(f"\nProcesando variable '{var_name}' para las 6 subcuencas...")

        for subbasin in self.subbasins:
            # Buscar archivo meteo.in dentro de la carpeta del modelo o de la subcuenca
            meteo_path = os.path.join(self.base_dir, f"{self.model}_{subbasin}", "meteo.in")
            if not os.path.exists(meteo_path):
                meteo_path = os.path.join(self.base_dir, subbasin, "meteo.in")

            if not os.path.exists(meteo_path):
                print(f"Error: No se encontró el archivo meteo.in para {subbasin} en {meteo_path}")
                return

            # Cargar CSV tomando la primera columna como fechas
            df = pd.read_csv(meteo_path, parse_dates=[0], index_col=0)
            
            # Seleccionar la columna correspondiente por índice
            data_dict[subbasin] = df.iloc[:, col_idx - 1]

        # Consolidar todas las subcuencas en un DataFrame diario (time, S1, S2, S3, S4, S5, S6)
        df_daily = pd.DataFrame(data_dict)
        df_daily.index.name = "time"

        # Resample mensual y anual aplicando suma o promedio según el tipo
        try:
            if agg_type == 'sum':
                df_monthly = df_daily.resample('ME').sum()
                df_yearly = df_daily.resample('YE').sum()
            else:
                df_monthly = df_daily.resample('ME').mean()
                df_yearly = df_daily.resample('YE').mean()
        except ValueError:
            # Compatibilidad con versiones anteriores de pandas
            if agg_type == 'sum':
                df_monthly = df_daily.resample('M').sum()
                df_yearly = df_daily.resample('Y').sum()
            else:
                df_monthly = df_daily.resample('M').mean()
                df_yearly = df_daily.resample('Y').mean()

        # Dar formato a las fechas en los agregados
        df_monthly.index = df_monthly.index.strftime('%Y-%m')
        df_yearly.index = df_yearly.index.strftime('%Y')

        # Directorio de salida especifico
        out_dir = os.path.join(self.base_dir, "Agregacion_variables")
        os.makedirs(out_dir, exist_ok=True)

        file_d = os.path.join(out_dir, f"{var_name}_diaria.csv")
        file_m = os.path.join(out_dir, f"{var_name}_mensual.csv")
        file_a = os.path.join(out_dir, f"{var_name}_anual.csv")

        # Guardar resultados con 3 decimales
        df_daily.to_csv(file_d, float_format='%.3f')
        df_monthly.to_csv(file_m, float_format='%.3f')
        df_yearly.to_csv(file_a, float_format='%.3f')

        print(f"Archivos guardados exitosamente en la carpeta '{out_dir}':")
        print(f"  - {os.path.basename(file_d)}")
        print(f"  - {os.path.basename(file_m)}")
        print(f"  - {os.path.basename(file_a)}")

    def run(self, var_name='precip'):
        """Flujo de ejecución principal."""
        self.process_variable(var_name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso incorrecto. Debes proporcionar la ruta base.")
        print("Ejemplo de uso: python3 procesar_meteo.py /ruta/a/RHC_GP [variable] [modelo]")
        print("Variables disponibles: precip (por defecto), tave, tmin, tmax")
        sys.exit(1)

    base_directory = sys.argv[1]
    variable = sys.argv[2] if len(sys.argv) > 2 else 'precip'
    model_name = sys.argv[3] if len(sys.argv) > 3 else 'gr4j'

    if not os.path.isdir(base_directory):
        print(f"Error: El directorio '{base_directory}' no existe.")
        sys.exit(1)

    app = MeteoAggregator(base_directory, model=model_name)
    app.run(var_name=variable)
