"""
Verificación inicial del repositorio Bike Sharing Analytics.

Comprueba la estructura, integridad del dataset,
dependencias instaladas y disponibilidad de R.

No entrena modelos ni modifica los resultados originales.

Ejecutar desde la raíz:
python verificar_proyecto.py
"""

from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

import hashlib
import shutil
import sys

from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parent

errores = []

print("=== BIKE SHARING ANALYTICS ===")
print("Python:", sys.version)

# Verificar estructura.

for carpeta in [
    "data",
    "notebooks",
    "src",
    "dashboard",
    "results",
    "docs"
]:

    existe = (ROOT / carpeta).is_dir()

    print(carpeta, "OK" if existe else "FALTA")

    if not existe:
        errores.append(f"Carpeta faltante: {carpeta}")

# Verificar archivos requeridos.

for nombre in [
    "README.md",
    "requirements.txt",
    "data/day.csv",
    "dashboard/index.html"
]:

    existe = (ROOT / nombre).is_file()

    print(nombre, "OK" if existe else "FALTA")

    if not existe:
        errores.append(f"Archivo faltante: {nombre}")

# Verificar integridad del dataset.

dataset = ROOT / "data" / "day.csv"

hash_esperado = (
    "a6bcf826782d3c0fbfdcbeead17cd0884"
    "185a0dafe8ff10cd48a874ee7ba18be"
)

if dataset.exists():

    hash_actual = hashlib.sha256(
        dataset.read_bytes()
    ).hexdigest()

    integridad = hash_actual == hash_esperado

    print("Integridad dataset:", "OK" if integridad else "ERROR")

    if not integridad:
        errores.append("SHA256 del dataset diferente")

# Verificar versiones de dependencias.

requirements = ROOT / "requirements.txt"

if requirements.exists():

    for linea in requirements.read_text(
        encoding="utf-8"
    ).splitlines():

        linea = linea.strip()

        if not linea or linea.startswith("#"):
            continue

        requisito = Requirement(linea)

        try:

            instalada = version(requisito.name)

            coincide = requisito.specifier.contains(
                instalada,
                prereleases=True
            )

            print(
                requisito.name,
                instalada,
                "OK" if coincide else "REVISAR"
            )

            if not coincide:
                errores.append(
                    f"Versión diferente: {requisito.name}"
                )

        except PackageNotFoundError:

            errores.append(
                f"Paquete no instalado: {requisito.name}"
            )

# Verificar disponibilidad de R.

rscript = shutil.which("Rscript")

print(
    "Rscript:",
    "Disponible" if rscript else "No disponible"
)

if not rscript:
    errores.append(
        "Rscript requerido para la sección R de Fase 2"
    )

# Verificar dimensiones del dataset.

if dataset.exists():

    try:

        import pandas as pd

        df = pd.read_csv(dataset)

        print("Dimensiones:", df.shape)
        print("Valores faltantes:", df.isna().sum().sum())
        print("Duplicados:", df.duplicated().sum())

        if df.shape != (731, 16):
            errores.append("Dimensiones inesperadas")

        if df.isna().sum().sum() != 0:
            errores.append("Valores faltantes inesperados")

        if df.duplicated().sum() != 0:
            errores.append("Duplicados inesperados")

    except Exception as error:

        errores.append(
            f"Error al leer dataset: {type(error).__name__}"
        )

print("\n=== RESULTADO DE VERIFICACIÓN ===")

if errores:

    for error in errores:
        print("REVISAR:", error)

    print("Verificación inicial: NO SUPERADA")

    sys.exit(1)

else:

    print("Verificación inicial: SUPERADA")
    print("Modelos reentrenados: 0")
    print("Ejecución integral de notebooks: no evaluada")

    sys.exit(0)
