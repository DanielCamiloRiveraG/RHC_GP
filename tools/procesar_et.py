#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__all__ = ['ETAggregator']
__version__ = '0.1'
__author__ = 'Camilo Rivera'

import os
import sys
import pandas as pd

class ETAggregator:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.subbasins = ["S1", "S2", "S3", "S4", "S5", "S6"]

    def process_et(self):
        """Procesa la evapotranspiración (et_mm) de 'results.out' para las 6 subcuencas en GR4J."""
        data_dict = {}

        print("\nProcesando 'et_mm' (Evapotranspiración) para las 6 subcuencas (Modelo GR4J)...")

        for subbasin in self.subbasins:
            # Ruta al archivo results.out del modelo GR4J
            results_path = os.path.join(self.base_dir, f"gr4j_{subbasin}", "results.out")

            if not os.path.exists(results_path):
                print(f"Error: No se encontró el archivo results.out para {subbasin} en {results_path}")
                return

            # Cargar CSV tomando la primera columna (datetime) como índice
            df = pd.read_csv(results_path, parse_dates=[0], index_col=0)
            
            # Seleccionar la penúltima columna (et_mm)
            data_dict[subbasin] = df.iloc[:, -2]

        # Consolidar las 6 subcuencas en un DataFrame diario (time, S1, S2, S3, S4, S5, S6)
        df_daily = pd.DataFrame(data_dict)
        df_daily.index.name = "time"

        # Resample mensual y anual (suma acumulada de evapotranspiración en mm)
        try:
            df_monthly = df_daily.resample('ME').sum()
            df_yearly = df_daily.resample('YE').sum()
        except ValueError:
            # Compatibilidad con versiones anteriores de pandas
            df_monthly = df_daily.resample('M').sum()
            df_yearly = df_daily.resample('Y').sum()

        # Dar formato de fecha a los índices
        df_monthly.index = df_monthly.index.strftime('%Y-%m')
        df_yearly.index = df_yearly.index.strftime('%Y')

        # Crear carpeta de salida 'Agregacion_variables'
        out_dir = os.path.join(self.base_dir, "Agregacion_variables")
        os.makedirs(out_dir, exist_ok=True)

        file_d = os.path.join(out_dir, "et_diaria.csv")
        file_m = os.path.join(out_dir, "et_mensual.csv")
        file_a = os.path.join(out_dir, "et_anual.csv")

        # Guardar archivos CSV redondeados a 3 decimales
        df_daily.to_csv(file_d, float_format='%.3f')
        df_monthly.to_csv(file_m, float_format='%.3f')
        df_yearly.to_csv(file_a, float_format='%.3f')

        print(f"Archivos guardados exitosamente en la carpeta '{out_dir}':")
        print(f"  - {os.path.basename(file_d)}")
        print(f"  - {os.path.basename(file_m)}")
        print(f"  - {os.path.basename(file_a)}")

    def run(self):
        """Flujo de ejecución principal."""
        self.process_et()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso incorrecto. Debes proporcionar la ruta base.")
        print("Ejemplo de uso: python3 procesar_et.py /ruta/a/RHC_GP")
        sys.exit(1)

    base_directory = sys.argv[1]

    if not os.path.isdir(base_directory):
        print(f"Error: El directorio '{base_directory}' no existe.")
        sys.exit(1)

    app = ETAggregator(base_directory)
    app.run()
