
# ==========================================================
# FASE 3 - CELDA 2
# Importación de librerías y carga del dataset
# ==========================================================

from pathlib import Path
import urllib.request
import zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Reproducibilidad
SEMILLA = 42
np.random.seed(SEMILLA)

# Carpetas del proyecto
BASE = Path("/content/Fase_3_Bicicletas")
DATOS = BASE / "datos"
RESULTADOS = BASE / "resultados"

DATOS.mkdir(parents=True, exist_ok=True)
RESULTADOS.mkdir(parents=True, exist_ok=True)

# Dataset oficial UCI Bike Sharing
URL = (
    "https://archive.ics.uci.edu/static/public/"
    "275/bike+sharing+dataset.zip"
)

archivo_zip = DATOS / "bike_sharing.zip"
archivo_csv = DATOS / "day.csv"

# Descargar solo si el CSV todavía no existe
if not archivo_csv.exists():
    urllib.request.urlretrieve(URL, archivo_zip)

    with zipfile.ZipFile(archivo_zip, "r") as archivo:
        archivo.extract("day.csv", path=DATOS)

# Cargar datos
df = pd.read_csv(archivo_csv)

print("Dataset cargado correctamente")
print("Dimensiones:", df.shape)
print("Columnas:", df.columns.tolist())

display(df.head())
