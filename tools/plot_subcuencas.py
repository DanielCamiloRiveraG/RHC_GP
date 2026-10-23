#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__all__ = ['MultiModelPlotter']
__version__ = '0.5'
__author__ = 'Camilo Rivera'

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

class MultiModelPlotter:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.subbasins = ["S1", "S2", "S3", "S4", "S5", "S6"]
        self.models = ["gr4j", "hbv", "hymod"]

        # Mapeo de nombres legibles y colores individuales por modelo
        self.model_names = {"gr4j": "GR4J", "hbv": "HBV", "hymod": "HYMOD"}
        self.model_colors = {"gr4j": "tab:blue", "hbv": "tab:red", "hymod": "tab:green"}

        # Áreas de las subcuencas en m²
        self.areas_subcuencas = {
            'S1': 61276000,
            'S2': 100297800,
            'S3': 304502200,
            'S4': 802847000,
            'S5': 292264900,
            'S6': 1800002600
        }
        
        # Constante de conversión de mm/día a m/s
        self.k = 1 / (1000 * 86400)

    def _crear_grafica(self, df_model, model_key, titulo, ylabel, ruta_guardado, col="q_m3s"):
        """Función auxiliar para generar y guardar una gráfica individual por modelo."""
        plt.figure(figsize=(12, 6))
        
        color = self.model_colors[model_key]
        model_name = self.model_names[model_key]
        
        # Graficar únicamente el modelo especificado
        plt.plot(df_model.index, df_model[col], color=color, label=f"Simulada ({model_name})", linewidth=1.2, alpha=0.85)

        # Detalles estéticos
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.xlabel("Fecha", fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.legend(loc="upper right", fontsize=10)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        
        # Guardar en disco y liberar memoria sin mostrar en pantalla
        plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_subbasin(self, subbasin):
        """Genera y guarda 9 gráficas individuales (3 frecuencias x 3 modelos) para una subcuenca."""
        
        # 1. Rutas
        gr4j_dir = os.path.join(self.base_dir, f"gr4j_{subbasin}")
        hbv_dir = os.path.join(self.base_dir, f"hbv_{subbasin}")
        hymod_dir = os.path.join(self.base_dir, f"hymod_{subbasin}")

        results_gr4j = os.path.join(gr4j_dir, 'results.out')
        results_hbv = os.path.join(hbv_dir, 'results.out')
        results_hymod = os.path.join(hymod_dir, 'results.out')

        paths = {"gr4j": results_gr4j, "hbv": results_hbv, "hymod": results_hymod}

        # 2. Verificación de existencia de archivos
        for model_key, filepath in paths.items():
            if not os.path.exists(filepath):
                print(f"Advertencia: No se encontró results.out de {model_key.upper()} para {subbasin}")
                return

        print(f"Procesando Subcuenca {subbasin}...")
        
        area = self.areas_subcuencas[subbasin]

        # 3. Leer datos y aplicar conversión a m³/s
        dfs_diarios = {}
        dfs_mensuales = {}
        dfs_anuales = {}

        for model_key, filepath in paths.items():
            df = pd.read_csv(filepath, parse_dates=["datetime"], index_col="datetime")
            # Conversión de caudal de mm/día a m³/s (Q = q_mm * k * área)
            df["q_m3s"] = df["q_mm"] * self.k * area
            dfs_diarios[model_key] = df

            # Agrupación por promedio
            try:
                dfs_mensuales[model_key] = df.resample('ME').mean()
                dfs_anuales[model_key] = df.resample('YE').mean()
            except ValueError:
                dfs_mensuales[model_key] = df.resample('M').mean()
                dfs_anuales[model_key] = df.resample('Y').mean()

        # 4. Crear directorio de salidas
        out_dir = os.path.join(self.base_dir, "graficas_series")
        os.makedirs(out_dir, exist_ok=True)

        # 5. Generar y guardar las 9 gráficas individuales para esta subcuenca
        freq_config = [
            ("diaria", "Diario", "Caudal Q (m³/s)", dfs_diarios),
            ("mensual", "Mensual Promedio", "Caudal Q (m³/s)", dfs_mensuales),
            ("anual", "Anual Promedio", "Caudal Q (m³/s)", dfs_anuales)
        ]

        for freq_key, freq_title, ylabel, dfs_dict in freq_config:
            for model_key in self.models:
                m_name = self.model_names[model_key]
                titulo = f"Caudal {freq_title} - Subcuenca {subbasin} ({m_name})"
                ruta_guardado = os.path.join(out_dir, f"serie_{freq_key}_{subbasin}_{model_key}.png")
                
                self._crear_grafica(
                    df_model=dfs_dict[model_key],
                    model_key=model_key,
                    titulo=titulo,
                    ylabel=ylabel,
                    ruta_guardado=ruta_guardado,
                    col="q_m3s"
                )

        print(f" -> Guardadas 9 gráficas para la subcuenca {subbasin}")

    def run(self):
        """Flujo de ejecución principal."""
        print("Iniciando procesamiento de series de tiempo...")
        for sub in self.subbasins:
            self.plot_subbasin(sub)
        print("\n¡Las 54 gráficas han sido procesadas y guardadas exitosamente en la carpeta 'graficas_series'!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso incorrecto. Debes proporcionar la ruta base.")
        print("Ejemplo de uso: python3 plot_subcuencas.py /home/user/RHC_GP")
        sys.exit(1)

    base_directory = sys.argv[1]
    
    if not os.path.isdir(base_directory):
        print(f"Error: El directorio '{base_directory}' no existe.")
        sys.exit(1)

    app = MultiModelPlotter(base_directory)
    app.run()
