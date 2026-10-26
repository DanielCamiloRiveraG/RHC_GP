#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__all__ = ['QEnsembleAggregator']
__version__ = '0.1'
__author__ = 'Camilo Rivera'

import os
import sys
import pandas as pd

class QEnsembleAggregator:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.subbasins = ["S1", "S2", "S3", "S4", "S5", "S6"]
        self.models = ["gr4j", "hbv", "hymod"]
        
        # Pesos por subcuenca y modelo para la combinación lineal de caudales
        self.weights = {
            "S1": {"gr4j": 0.994973546259482, "hbv": 0.00114768877124778, "hymod": 0.00387750882627332},
            "S2": {"gr4j": 0.56514190461542,  "hbv": 0.293166599835398,  "hymod": 0.0560413863631292},
            "S3": {"gr4j": 0.742464195632472, "hbv": 0.195589692327237,  "hymod": 0.0612036451257586},
            "S4": {"gr4j": 0.645079505434598, "hbv": 0.262423703916963,  "hymod": 0.0918516322508173},
            "S5": {"gr4j": 0.823496301642481, "hbv": 0.0363505258196888, "hymod": 0.0566534920776043},
            "S6": {"gr4j": 0.997561445388559, "hbv": -0.00283488998225412, "hymod": 0.00238951645711794}
        }

    def process_q_ensemble(self):
        """Procesa y calcula el ensamble ponderado de caudales (q_m3s) para las 6 subcuencas."""
        daily_ensemble_dict = {}

        print("\nProcesando ensamble de caudales ('q_m3s') a través de las 18 carpetas...")

        for subbasin in self.subbasins:
            subbasin_q = None

            for model in self.models:
                results_path = os.path.join(self.base_dir, f"{model}_{subbasin}", "results.out")

                if not os.path.exists(results_path):
                    print(f"Error: No se encontró el archivo results.out para {model}_{subbasin} en {results_path}")
                    return

                # Cargar CSV con la primera columna (datetime) como índice
                df = pd.read_csv(results_path, parse_dates=[0], index_col=0)
                
                # Extraer la última columna (q_m3s)
                q_model = df.iloc[:, -1]
                
                # Multiplicar por el peso correspondiente
                w = self.weights[subbasin][model]
                q_weighted = q_model * w

                if subbasin_q is None:
                    subbasin_q = q_weighted
                else:
                    subbasin_q += q_weighted

            daily_ensemble_dict[subbasin] = subbasin_q

        # Consolidar DataFrame diario con las 6 subcuencas ensambladas (time, S1, S2, S3, S4, S5, S6)
        df_daily = pd.DataFrame(daily_ensemble_dict)
        df_daily.index.name = "time"

        # Promedios mensuales y anuales de caudal (m3/s)
        try:
            df_monthly = df_daily.resample('ME').mean()
            df_yearly = df_daily.resample('YE').mean()
        except ValueError:
            # Compatibilidad con versiones anteriores de pandas
            df_monthly = df_daily.resample('M').mean()
            df_yearly = df_daily.resample('Y').mean()

        # Dar formato a las fechas en los índices agregados
        df_monthly.index = df_monthly.index.strftime('%Y-%m')
        df_yearly.index = df_yearly.index.strftime('%Y')

        # Definir la carpeta de salida 'Agregacion_variables'
        out_dir = os.path.join(self.base_dir, "Agregacion_variables")
        os.makedirs(out_dir, exist_ok=True)

        file_d = os.path.join(out_dir, "q_diario.csv")
        file_m = os.path.join(out_dir, "q_mensual.csv")
        file_a = os.path.join(out_dir, "q_anual.csv")

        # Guardar archivos CSV redondeados a 6 decimales
        df_daily.to_csv(file_d, float_format='%.6f')
        df_monthly.to_csv(file_m, float_format='%.6f')
        df_yearly.to_csv(file_a, float_format='%.6f')

        print(f"Archivos de ensamble guardados exitosamente en '{out_dir}':")
        print(f"  - {os.path.basename(file_d)}")
        print(f"  - {os.path.basename(file_m)}")
        print(f"  - {os.path.basename(file_a)}")

    def run(self):
        """Flujo de ejecución principal."""
        self.process_q_ensemble()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso incorrecto. Debes proporcionar la ruta base.")
        print("Ejemplo de uso: python3 procesar_q.py /ruta/a/RHC_GP")
        sys.exit(1)

    base_directory = sys.argv[1]

    if not os.path.isdir(base_directory):
        print(f"Error: El directorio '{base_directory}' no existe.")
        sys.exit(1)

    app = QEnsembleAggregator(base_directory)
    app.run()
