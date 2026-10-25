#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__all__ = ['MultiModelPlotter']
__version__ = '0.4'
__author__ = 'Camilo Rivera'

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class MultiModelBoxplotter:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.subbasins = ["S1", "S2", "S3", "S4", "S5", "S6"]
        self.models = ["gr4j", "hbv", "hymod"]
        
        # Diccionario para mapear números a nombres de meses
        self.meses = {
            1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 
            5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Ago', 
            9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
        }

    def plot_boxplot(self, subbasin):
        """Genera un boxplot multianual mensual de caudales en m³/s para una subcuenca."""
        
        # Construir rutas
        gr4j_dir = os.path.join(self.base_dir, f"gr4j_{subbasin}")
        hbv_dir = os.path.join(self.base_dir, f"hbv_{subbasin}")
        hymod_dir = os.path.join(self.base_dir, f"hymod_{subbasin}")

        results_gr4j = os.path.join(gr4j_dir, 'results.out')
        results_hbv = os.path.join(hbv_dir, 'results.out')
        results_hymod = os.path.join(hymod_dir, 'results.out')

        # Verificar archivos
        for filepath, model in zip([results_gr4j, results_hbv, results_hymod], self.models):
            if not os.path.exists(filepath):
                print(f"Advertencia: No se encontró results.out de {model.upper()} para {subbasin}")
                return

        print(f"\nProcesando Boxplot para Subcuenca {subbasin}...")
        
        # Leer datos y establecer índice
        df_gr4j = pd.read_csv(results_gr4j, parse_dates=["datetime"], index_col="datetime")
        df_hbv = pd.read_csv(results_hbv, parse_dates=["datetime"], index_col="datetime")
        df_hymod = pd.read_csv(results_hymod, parse_dates=["datetime"], index_col="datetime")

        # 1. Promediar valores a nivel mensual (.mean())
        try:
            df_gr4j_m = df_gr4j.resample('ME').mean().reset_index()
            df_hbv_m = df_hbv.resample('ME').mean().reset_index()
            df_hymod_m = df_hymod.resample('ME').mean().reset_index()
        except ValueError:
            # Compatibilidad con versiones anteriores de pandas
            df_gr4j_m = df_gr4j.resample('M').mean().reset_index()
            df_hbv_m = df_hbv.resample('M').mean().reset_index()
            df_hymod_m = df_hymod.resample('M').mean().reset_index()

        # 2. Agregar columnas 'Mes' y 'Modelo'
        df_gr4j_m['Mes'] = df_gr4j_m['datetime'].dt.month.map(self.meses)
        df_gr4j_m['Modelo'] = 'GR4J'
        
        df_hbv_m['Mes'] = df_hbv_m['datetime'].dt.month.map(self.meses)
        df_hbv_m['Modelo'] = 'HBV'
        
        df_hymod_m['Mes'] = df_hymod_m['datetime'].dt.month.map(self.meses)
        df_hymod_m['Modelo'] = 'HYMOD'

        # 3. Concatenar los 3 dataframes
        df_combinado = pd.concat([df_gr4j_m, df_hbv_m, df_hymod_m], ignore_index=True)

        # Configurar estilo y figura
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(12, 6))

        # Generar Boxplot agrupado
        sns.boxplot(
            data=df_combinado, 
            x="Mes", 
            y="q_m3s", 
            hue="Modelo",
            order=list(self.meses.values()),
            palette=["tab:blue", "tab:red", "tab:green"],
            linewidth=1.2,
            fliersize=3
        )

        # Detalles estéticos
        plt.title(f"Boxplot - Subcuenca {subbasin}", fontsize=14, fontweight='bold')
        plt.xlabel("Mes", fontsize=12)
        plt.ylabel("Caudal (m³/s)", fontsize=12)
        plt.legend(title="Modelo", loc="upper right", fontsize=10)
        plt.tight_layout()

        # Guardar automáticamente la gráfica
        out_dir = os.path.join(self.base_dir, "graficas_boxplots")
        os.makedirs(out_dir, exist_ok=True)
        
        ruta_guardado = os.path.join(out_dir, f"boxplot_{subbasin}.png")
        plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')

        # Mostrar gráfica
        print(f"Gráfica guardada en: {ruta_guardado}")
        print(f"Mostrando gráfica de la subcuenca {subbasin}. Cierra la ventana para continuar.")
        plt.show()
        plt.close('all')

    def run(self):
        """Flujo de ejecución principal."""
        for sub in self.subbasins:
            self.plot_boxplot(sub)
        print("\n¡Las 6 gráficas de boxplots han sido procesadas exitosamente!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso incorrecto. Debes proporcionar la ruta base.")
        print("Ejemplo de uso: python3 plot_boxplots.py /home/user/RHC_GP")
        sys.exit(1)

    base_directory = sys.argv[1]
    
    if not os.path.isdir(base_directory):
        print(f"Error: El directorio '{base_directory}' no existe.")
        sys.exit(1)

    app = MultiModelBoxplotter(base_directory)
    app.run()
