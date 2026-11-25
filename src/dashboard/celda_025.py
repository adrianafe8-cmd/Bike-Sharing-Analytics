# ==========================================================
# DASHBOARD GLOBAL - CELDA 23
# Preparación del repositorio reproducible para GitHub
# Universidad de La Salle - Maestría en IA
# ==========================================================

import shutil
import zipfile
import hashlib
import json
import sys
import platform
import importlib.metadata as metadata

from pathlib import Path
from collections import Counter
from google.colab import files

# ==========================================================
# 1. CONFIGURACIÓN DE RUTAS
# ==========================================================

BASE = Path("/content")

REPO = BASE / "Bike-Sharing-Analytics"

ZIP_FINAL = BASE / "Bike-Sharing-Analytics_GitHub.zip"

HTML_ORIGINAL = BASE / "Bike_Sharing_Analytics.html"

ZIP_EVIDENCIAS = (
    BASE / "Dashboard_Global_Bicicletas_Entrega.zip"
)

CARPETAS = [
    "data",
    "notebooks",
    "src",
    "dashboard",
    "results",
    "docs"
]

# Crear estructura sin eliminar archivos existentes.

REPO.mkdir(parents=True, exist_ok=True)

for carpeta in CARPETAS:
    (REPO / carpeta).mkdir(
        parents=True,
        exist_ok=True
    )

print("=== ESTRUCTURA DEL REPOSITORIO ===")

for carpeta in CARPETAS:
    print(f"OK: {carpeta}/")

# ==========================================================
# 2. LOCALIZAR PAQUETE DE EVIDENCIAS
# ==========================================================

if not ZIP_EVIDENCIAS.exists():

    candidatos = [
        p for p in BASE.rglob(
            "Dashboard_Global_Bicicletas_Entrega.zip"
        )
        if REPO not in p.parents
    ]

    if candidatos:
        ZIP_EVIDENCIAS = candidatos[0]

assert ZIP_EVIDENCIAS.exists(), (
    "No se encontró el ZIP de evidencias generado "
    "en la celda 20."
)

print("\n=== PAQUETE DE EVIDENCIAS ===")
print("Archivo:", ZIP_EVIDENCIAS.name)

# ==========================================================
# 3. EXTRAER EVIDENCIAS
# ==========================================================

TEMP = BASE / "evidencias_repo_temporal"

TEMP.mkdir(exist_ok=True)

with zipfile.ZipFile(ZIP_EVIDENCIAS, "r") as z:

    assert z.testzip() is None, (
        "El ZIP de evidencias presenta errores."
    )

    # Validar rutas antes de extraer archivos.

    for miembro in z.infolist():

        destino = (TEMP / miembro.filename).resolve()

        assert destino.is_relative_to(TEMP.resolve()), (
            "Ruta no permitida dentro del ZIP."
        )

    z.extractall(TEMP)

archivos = [
    p for p in TEMP.rglob("*")
    if p.is_file()
]

print("Archivos recuperados:", len(archivos))

# ==========================================================
# 4. ORGANIZAR ARCHIVOS POR TIPO
# ==========================================================

inventario = []
omitidos = []

EXTENSIONES_PERMITIDAS = {
    ".csv", ".json", ".png", ".jpg", ".jpeg",
    ".svg", ".ipynb", ".py", ".r", ".md",
    ".txt", ".pdf", ".docx", ".xlsx", ".yaml",
    ".yml", ".html", ".parquet", ".webp"
}

def calcular_sha256(ruta):

    return hashlib.sha256(
        ruta.read_bytes()
    ).hexdigest()

def copiar_archivo(origen, destino):

    destino.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy2(origen, destino)

    inventario.append({
        "archivo": str(destino.relative_to(REPO)),
        "bytes": destino.stat().st_size,
        "sha256": calcular_sha256(destino)
    })

for archivo in archivos:

    extension = archivo.suffix.lower()

    nombre = archivo.name.lower()

    relativa = archivo.relative_to(TEMP)

    # Excluir archivos potencialmente sensibles.

    if (
        nombre.startswith(".env")
        or any(
            palabra in nombre
            for palabra in [
                "credentials",
                "secret",
                "password",
                "token",
                "private_key"
            ]
        )
        or extension not in EXTENSIONES_PERMITIDAS
    ):

        omitidos.append(str(relativa))
        continue

    # Dataset original.

    if nombre in ["day.csv", "hour.csv"]:

        destino = REPO / "data" / archivo.name

    # Notebooks originales.

    elif extension == ".ipynb":

        destino = REPO / "notebooks" / relativa

    # Scripts Python y R.

    elif extension in [".py", ".r"]:

        destino = REPO / "src" / relativa

    # Dependencias originales: conservar como evidencia.

    elif nombre in [
        "requirements.txt",
        "environment.yml",
        "environment.yaml"
    ]:

        destino = REPO / "docs" / relativa

    # Documentación.

    elif extension in [
        ".md", ".pdf", ".docx", ".txt"
    ]:

        destino = REPO / "docs" / relativa

    # Evidencias, métricas, tablas y gráficas.

    else:

        destino = REPO / "results" / relativa

    copiar_archivo(archivo, destino)

print("\n=== ORGANIZACIÓN DE ARCHIVOS ===")
print("Archivos copiados:", len(inventario))
print("Archivos omitidos:", len(omitidos))

# ==========================================================
# 5. INCORPORAR DASHBOARD HTML
# ==========================================================

assert HTML_ORIGINAL.exists(), (
    "No se encontró el HTML generado en la celda 22."
)

HTML_DESTINO = REPO / "dashboard" / "index.html"

copiar_archivo(
    HTML_ORIGINAL,
    HTML_DESTINO
)

assert calcular_sha256(HTML_ORIGINAL) == (
    calcular_sha256(HTML_DESTINO)
)

print("\n=== DASHBOARD HTML ===")
print("Archivo:", HTML_DESTINO.name)

print(
    "Tamaño MB:",
    round(
        HTML_DESTINO.stat().st_size / 1024**2,
        2
    )
)

print("Integridad SHA256: OK")

# ==========================================================
# 6. GENERAR REQUIREMENTS.TXT
# ==========================================================

# Registrar las versiones instaladas en el entorno actual.
# Posteriormente deben contrastarse con las dependencias
# de los notebooks originales de cada fase.

PAQUETES = [
    "numpy",
    "pandas",
    "scipy",
    "scikit-learn",
    "statsmodels",
    "matplotlib",
    "seaborn",
    "plotly",
    "dash",
    "dash-bootstrap-components",
    "flask",
    "joblib",
    "ipython",
    "ipykernel",
    "jupyter",
    "nbformat",
    "openpyxl",
    "rpy2"
]

dependencias = {}
no_instaladas = []

for paquete in PAQUETES:

    try:

        dependencias[paquete] = (
            metadata.version(paquete)
        )

    except metadata.PackageNotFoundError:

        no_instaladas.append(paquete)

requirements = "\n".join(
    f"{paquete}=={version}"
    for paquete, version in sorted(
        dependencias.items()
    )
)

(REPO / "requirements.txt").write_text(
    requirements + "\n",
    encoding="utf-8"
)

print("\n=== DEPENDENCIAS DEL ENTORNO ===")
print(requirements)

print("\nPaquetes no instalados:")
print(no_instaladas)

# Registrar versiones adicionales del entorno.

entorno = {
    "python": sys.version,
    "plataforma": platform.platform(),
    "dependencias": dependencias,
    "paquetes_no_instalados": no_instaladas,
    "origen": "Entorno actual de Google Colab",
    "reproducibilidad_desde_cero": "Pendiente"
}

(REPO / "docs" / "entorno_ejecucion.json").write_text(
    json.dumps(
        entorno,
        indent=4,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

# ==========================================================
# 7. GENERAR README DEL PROYECTO
# ==========================================================
readme = """
# Bike Sharing Analytics

## Proyecto Integrador de Ciencia de Datos

Universidad de La Salle
Maestría en Inteligencia Artificial

Autora: Adriana Patricia Fernández Infante

## Descripción

Análisis descriptivo y predictivo de la demanda
de bicicletas compartidas.

## Fases del proyecto

1. Análisis exploratorio de datos.
2. Regresión simple y múltiple.
3. Modelado avanzado.
4. Preprocesamiento y modelos baseline.

## Dashboard interactivo

https://adrianafe8-cmd.github.io/Bike-Sharing-Analytics/Dashboard/index.html

El dashboard contiene:

- 5 pestañas.
- 47 gráficas interactivas.
- 41 tablas.
- 25 imágenes originales.
- Filtros dinámicos.

## Dataset

Bike Sharing Dataset - UCI Machine Learning Repository.

- Archivo: day.csv.
- Observaciones: 731.
- Variables: 16.
- Periodo: 2011-2012.
- DOI: 10.24432/C5W894.

Fuente:
https://archive.ics.uci.edu/dataset/275/bike-sharing-dataset

## Estructura del repositorio

- data/: datos originales.
- notebooks/: notebooks de análisis.
- src/: código fuente.
- dashboard/: dashboard interactivo.
- results/: resultados y evidencias.
- docs/: documentación técnica.

## Instalación

Crear un entorno virtual de Python.

Instalar dependencias mediante:

    pip install -r requirements.txt

## Ejecución

1. Revisar las rutas de los datasets.
2. Ejecutar los notebooks en orden.
3. Consultar los resultados.
4. Abrir dashboard/index.html en el navegador.

Las secciones en R requieren un entorno compatible.

## Resultados principales

- Total de alquileres: 3.292.679.
- Promedio diario: 4.504,35.
- Crecimiento anual: 64,88%.
- Usuarios registrados: 81,17%.

## Limitaciones metodológicas

La fase 1 fue reconstruida desde el dataset original.

Los modelos no fueron reentrenados durante
la consolidación del dashboard.

Las métricas de protocolos diferentes no son
directamente comparables.

Las dependencias corresponden al entorno actual
de consolidación en Google Colab.

La reproducibilidad integral desde cero
está pendiente de validación.

## Referencia

Fanaee-T, H. (2013). Bike Sharing Dataset.
UCI Machine Learning Repository.
https://doi.org/10.24432/C5W894
"""

(REPO / "README.md").write_text(
    readme.strip() + "\n",
    encoding="utf-8"
)

# ==========================================================
# 8. CONFIGURACIÓN PARA GITHUB
# ==========================================================

gitignore = """
__pycache__/
*.pyc
.ipynb_checkpoints/
.venv/
venv/
.env
.env.*
*.pem
*.key
credentials.json
.DS_Store
Thumbs.db
"""

(REPO / ".gitignore").write_text(
    gitignore.strip() + "\n",
    encoding="utf-8"
)

(REPO / ".nojekyll").touch()

print("\n=== ARCHIVOS DE CONFIGURACIÓN ===")
print("README.md: OK")
print("requirements.txt: OK")
print(".gitignore: OK")
print(".nojekyll: OK")

# ==========================================================
# 9. VALIDAR CONTENIDO DEL REPOSITORIO
# ==========================================================

print("\n=== INVENTARIO POR CARPETA ===")

conteos = {}

for carpeta in CARPETAS:

    contenido = [
        p for p in (REPO / carpeta).rglob("*")
        if p.is_file()
    ]

    conteos[carpeta] = len(contenido)

    print(f"{carpeta:15s}: {len(contenido)} archivos")

notebooks_encontrados = sorted(
    (REPO / "notebooks").rglob("*.ipynb")
)

scripts_encontrados = sorted(
    p for p in (REPO / "src").rglob("*")
    if p.is_file()
    and p.suffix.lower() in [".py", ".r"]
)

print("\n=== NOTEBOOKS RECUPERADOS ===")

for archivo in notebooks_encontrados:
    print(archivo.relative_to(REPO))

print("\n=== SCRIPTS RECUPERADOS ===")

for archivo in scripts_encontrados:
    print(archivo.relative_to(REPO))

# ==========================================================
# 10. IDENTIFICAR PENDIENTES
# ==========================================================

pendientes = []

if not (REPO / "data" / "day.csv").exists():
    pendientes.append("Incorporar dataset day.csv.")

if len(notebooks_encontrados) < 4:
    pendientes.append("Incorporar notebooks faltantes.")

if not scripts_encontrados:
    pendientes.append("Preparar código fuente en src/.")

pendientes.extend([
    "Incorporar notebook global definitivo.",
    "Verificar dependencias originales de cada fase.",
    "Verificar entorno R.",
    "Revisar credenciales y datos privados.",
    "Revisar rutas absolutas.",
    "Incorporar informe técnico final.",
    "Validar ejecución desde un entorno limpio.",
    "Validar interacciones del dashboard web."
])

print("\n=== PENDIENTES IDENTIFICADOS ===")

for i, pendiente in enumerate(pendientes, 1):
    print(f"{i}. {pendiente}")

# ==========================================================
# 11. MANIFIESTO DE INTEGRIDAD
# ==========================================================

manifiesto = {
    "proyecto": "Bike Sharing Analytics",
    "autora": "Adriana Patricia Fernández Infante",
    "archivos_por_carpeta": conteos,
    "notebooks_recuperados": [
        str(p.relative_to(REPO))
        for p in notebooks_encontrados
    ],
    "scripts_recuperados": [
        str(p.relative_to(REPO))
        for p in scripts_encontrados
    ],
    "archivos_omitidos": omitidos,
    "pendientes": pendientes,
    "modelos_reentrenados": 0,
    "archivos": [
        {
            "ruta": str(p.relative_to(REPO)),
            "bytes": p.stat().st_size,
            "sha256": calcular_sha256(p)
        }
        for p in sorted(REPO.rglob("*"))
        if p.is_file()
        and p.name != "manifiesto_integridad.json"
    ]
}

(REPO / "docs" / "manifiesto_integridad.json").write_text(
    json.dumps(
        manifiesto,
        indent=4,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

# ==========================================================
# 12. GENERAR ZIP PARA GITHUB
# ==========================================================

with zipfile.ZipFile(
    ZIP_FINAL,
    "w",
    compression=zipfile.ZIP_DEFLATED
) as z:

    for archivo in sorted(REPO.rglob("*")):

        if archivo.is_file():

            z.write(
                archivo,
                archivo.relative_to(REPO.parent)
            )

with zipfile.ZipFile(ZIP_FINAL, "r") as z:

    assert z.testzip() is None

    total_archivos = len(z.namelist())

# ==========================================================
# 13. RESULTADOS FINALES
# ==========================================================

print("\n" + "=" * 60)
print("PAQUETE PARA REPOSITORIO REPRODUCIBLE")
print("=" * 60)

print("Repositorio:", REPO.name)
print("Carpetas principales:", len(CARPETAS))
print("Total archivos:", total_archivos)
print("Notebooks:", len(notebooks_encontrados))
print("Scripts:", len(scripts_encontrados))
print("Dependencias registradas:", len(dependencias))
print("Modelos reentrenados: 0")
print("Integridad del ZIP: OK")

print("\nArchivo generado:", ZIP_FINAL.name)

print(
    "Tamaño MB:",
    round(ZIP_FINAL.stat().st_size / 1024**2, 2)
)

print("\nEstado: paquete preparado para revisión.")
print("Reproducibilidad completa: pendiente.")

# ==========================================================
# 14. DESCARGAR PAQUETE
# ==========================================================

files.download(str(ZIP_FINAL))