
# ==========================================================
# DASHBOARD GLOBAL - CELDA 3
# Carga y validación del dataset original
# ==========================================================

import urllib.request
import zipfile
import hashlib

# 1. Fuente oficial del dataset

URL_DATASET = (
    "https://archive.ics.uci.edu/static/public/"
    "275/bike+sharing+dataset.zip"
)

RUTA_ZIP = DATOS / "bike_sharing_dataset.zip"
RUTA_CSV = DATOS / "day.csv"

# 2. Descargar y extraer el dataset

if not RUTA_CSV.exists():

    urllib.request.urlretrieve(URL_DATASET, RUTA_ZIP)

    with zipfile.ZipFile(RUTA_ZIP, "r") as archivo:
        archivo.extract("day.csv", DATOS)

    print("Dataset descargado correctamente.")

else:
    print("Dataset disponible localmente.")

# 3. Verificar identidad del archivo

sha256 = hashlib.sha256(
    RUTA_CSV.read_bytes()
).hexdigest()

SHA256_ESPERADO = (
    "a6bcf826782d3c0fbfdcbeead17cd0884"
    "185a0dafe8ff10cd48a874ee7ba18be"
)

assert sha256 == SHA256_ESPERADO, (
    "El dataset no coincide con el utilizado en la Fase 4."
)

# 4. Cargar los datos originales

df_original = pd.read_csv(RUTA_CSV)

# Crear copia de trabajo para el dashboard

df = df_original.copy()

df["dteday"] = pd.to_datetime(df["dteday"])

# 5. Validar estructura

assert df.shape == (731, 16), (
    "Dimensiones inesperadas del dataset."
)

columnas_esperadas = [
    "instant", "dteday", "season", "yr",
    "mnth", "holiday", "weekday", "workingday",
    "weathersit", "temp", "atemp", "hum",
    "windspeed", "casual", "registered", "cnt"
]

assert list(df.columns) == columnas_esperadas

# 6. Diagnóstico inicial de calidad

total_faltantes = df.isna().sum().sum()

total_duplicados = df.duplicated().sum()

fechas_duplicadas = df["dteday"].duplicated().sum()

inconsistencias = (
    df["cnt"] != df["casual"] + df["registered"]
).sum()

# 7. Presentar resultados de validación

print("\n" + "=" * 60)
print("DASHBOARD GLOBAL - VALIDACIÓN DEL DATASET")
print("=" * 60)

print("Dataset: Bike Sharing")
print("Fuente: UCI Machine Learning Repository")
print("Archivo:", RUTA_CSV.name)
print("SHA-256:", sha256)
print("Identidad con Fase 4: OK")

print("\n=== DIMENSIONES ===")
print("Registros:", df.shape[0])
print("Variables:", df.shape[1])

print("\n=== PERIODO DE ANÁLISIS ===")
print("Fecha inicial:", df["dteday"].min().date())
print("Fecha final:", df["dteday"].max().date())

print("\n=== CALIDAD DE DATOS ===")
print("Valores faltantes:", total_faltantes)
print("Registros duplicados:", total_duplicados)
print("Fechas duplicadas:", fechas_duplicadas)
print("Inconsistencias en demanda:", inconsistencias)

print("\n=== TIPOS DE DATOS ===")
display(df.dtypes.to_frame("Tipo de dato"))

print("\n=== PRIMEROS CINCO REGISTROS ===")
display(df.head())

print("\nDataset cargado y validado correctamente.")
