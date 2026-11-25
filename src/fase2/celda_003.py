import io, zipfile, urllib.request, subprocess, shutil
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from IPython.display import display

SEMILLA = 42
SALIDA = Path('/content/resultados_regresion_bicicletas') if Path('/content').exists() else Path('resultados_regresion_bicicletas')
SALIDA.mkdir(parents=True, exist_ok=True)
sns.set_theme(style='whitegrid')
print('Librerías listas. Carpeta:', SALIDA.resolve())