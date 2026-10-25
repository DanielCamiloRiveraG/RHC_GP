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

class MultiModelDistributionPlotter:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.subbasins = ["S1", "S2", "S3", "S4", "S5", "S6"]
        self.models = ["gr4j", "hbv", "hymod"]
        self.colors = {"GR4J": "tab:blue", "HBV": "tab:red", "HYMOD": "tab:green"}

    def plot_distribution(self, subbasin):
        """Genera y guarda las gráficas de distribución de probabilidad (KDE y CDF) en m³/s para una subcuenca."""
        
        # 1. Construir rutas
        gr4j_dir = os.path.join(self.base_dir, f"gr4j_{subbasin}")
        hbv_dir = os.path.join(self.base_dir, f"hbv_{subbasin}")
        hymod_dir = os.path.join(self.base_dir, f"hymod_{subbasin}")

        results_gr4j = os.path.join(gr4j_dir, 'results.out')
        results_hbv = os.path.join(hbv_dir, 'results.out')
        results_hymod = os.path.join(hymod_dir, 'results.out')

        # 2. Verificar existencia de archivos
        for filepath, model in zip([results_gr4j, results_hbv, results_hymod], self.models):
            if not os.path.exists(filepath):
                print(f"Advertencia: No se encontró results.out de {model.upper()} para {subbasin}")
                return

        print(f"\nProcesando Distribuciones de Probabilidad para Subcuenca {subbasin}...")
        
        # 3. Cargar datos
        df_gr4j = pd.read_csv(results_gr4j, parse_dates=["datetime"])
        df_hbv = pd.read_csv(results_hbv, parse_dates=["datetime"])
        df_hymod = pd.read_csv(results_hymod, parse_dates=["datetime"])

        # Asignar etiqueta de modelo
        df_gr4j['Modelo'] = 'GR4J'
        df_hbv['Modelo'] = 'HBV'
        df_hymod['Modelo'] = 'HYMOD'

        # Concatenar dataframes en formato largo
        df_combinado = pd.concat([df_gr4j, df_hbv, df_hymod], ignore_index=True)

        # 4. Configurar lienzo (2 subgráficas: PDF/KDE a la izquierda, CDF a la derecha)
        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # Panel 1: Función de Densidad de Probabilidad (KDE)
        sns.kdeplot(
            data=df_combinado,
            x="q_m3s",
            hue="Modelo",
            palette=self.colors,
            fill=True,
            alpha=0.25,
            linewidth=1.5,
            ax=axes[0]
        )
        axes[0].set_title(f"Densidad de Probabilidad (PDF) - Subcuenca {subbasin}", fontsize=13, fontweight='bold')
        axes[0].set_xlabel("Caudal Q (m³/s)", fontsize=11)
        axes[0].set_ylabel("Densidad", fontsize=11)

        # Panel 2: Función de Distribución Acumulada Empírica (ECDF)
        sns.ecdfplot(
            data=df_combinado,
            x="q_m3s",
            hue="Modelo",
            palette=self.colors,
            linewidth=1.5,
            ax=axes[1]
        )
        axes[1].set_title(f"Distribución Acumulada (CDF) - Subcuenca {subbasin}", fontsize=13, fontweight='bold')
        axes[1].set_xlabel("Caudal Q (m³/s)", fontsize=11)
        axes[1].set_ylabel("Probabilidad Acumulada P(X ≤ x)", fontsize=11)

        # Configuración de títulos y márgenes para evitar recortado superior
        plt.suptitle(
            f"Distribución de Probabilidad de Caudales - Subcuenca {subbasin}", 
            fontsize=15, 
            fontweight='bold', 
            y=0.98
        )
        
        # Reserva el 7% superior del lienzo para el título
        plt.tight_layout(rect=[0, 0, 1, 0.93])

        # Crear carpeta de salidas si no existe
        out_dir = os.path.join(self.base_dir, "graficas_distribuciones")
        os.makedirs(out_dir, exist_ok=True)

        # Guardar la gráfica en disco
        ruta_guardado = os.path.join(out_dir, f"distribucion_{subbasin}.png")
        plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')

        # Mostrar la gráfica y cerrar limpiamente
        print(f"Gráfica guardada en: {ruta_guardado}")
        print(f"Mostrando distribución para {subbasin}. Cierra la ventana para continuar.")
        plt.show()
        plt.close('all')

    def run(self):
        """Flujo de ejecución principal."""
        for sub in self.subbasins:
            self.plot_distribution(sub)
        print("\n¡Las 6 gráficas de distribución de probabilidad han sido generadas y guardadas exitosamente!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso incorrecto. Debes proporcionar la ruta base.")
        print("Ejemplo de uso: python3 plot_distribuciones.py /home/user/RHC_GP")
        sys.exit(1)

    base_directory = sys.argv[1]
    
    if not os.path.isdir(base_directory):
        print(f"Error: El directorio '{base_directory}' no existe.")
        sys.exit(1)

    app = MultiModelDistributionPlotter(base_directory)
    app.run()
