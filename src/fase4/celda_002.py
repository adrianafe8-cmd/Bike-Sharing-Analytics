
# ==========================================================
# FASE 4 - CELDA 2
# Configuración del entorno y carga del dataset
# ==========================================================

# Bibliotecas para manipulación de datos
import pandas as pd
import numpy as np

# Bibliotecas para visualización
import matplotlib.pyplot as plt
import seaborn as sns

# Bibliotecas para gestión de archivos
from pathlib import Path
import urllib.request
import zipfile

# Información del entorno
import sys
import sklearn

# Semilla para garantizar reproducibilidad
SEMILLA = 42
np.random.seed(SEMILLA)

# Creación de directorios
BASE = Path("/content/Fase_4_Bicicletas")
DATOS = BASE / "datos"
RESULTADOS = BASE / "resultados"

DATOS.mkdir(parents=True, exist_ok=True)
RESULTADOS.mkdir(parents=True, exist_ok=True)

# Fuente oficial del dataset
url = (
    "https://archive.ics.uci.edu/static/"
    "public/275/bike+sharing+dataset.zip"
)

ruta_zip = DATOS / "bike_sharing.zip"

# Descargar el dataset si no existe
if not ruta_zip.exists():
    urllib.request.urlretrieve(url, ruta_zip)

# Extraer los archivos
with zipfile.ZipFile(ruta_zip, "r") as archivo:
    archivo.extractall(DATOS)

# Cargar los registros diarios
ruta_dataset = DATOS / "day.csv"

df = pd.read_csv(ruta_dataset)

# Información del entorno
print("=== ENTORNO DE EJECUCIÓN ===")
print("Python:", sys.version.split()[0])
print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)
print("Scikit-learn:", sklearn.__version__)

# Información del dataset
print("\n=== DATASET ===")
print("Registros:", df.shape[0])
print("Columnas:", df.shape[1])
print("Ruta:", ruta_dataset)

display(df.head())

# Verificaciones iniciales
assert df.shape == (731, 16)
assert "cnt" in df.columns

print("\nCarga del dataset completada correctamente.")
