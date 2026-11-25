"""
Configuración centralizada del proyecto Bike Sharing Analytics.

Permite localizar los recursos del repositorio sin depender
de rutas absolutas de Google Colab.
"""

from pathlib import Path

# El archivo se encuentra en src/utils/config.py.
ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
NOTEBOOKS_DIR = ROOT / "notebooks"
RESULTS_DIR = ROOT / "results"
DOCS_DIR = ROOT / "docs"
DASHBOARD_DIR = ROOT / "dashboard"

DATASET = DATA_DIR / "day.csv"

if not DATASET.is_file():
    raise FileNotFoundError(
        f"No se encontró el dataset: {DATASET}"
    )
