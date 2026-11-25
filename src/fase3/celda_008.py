
# ==========================================================
# FASE 3 - CELDA 6
# Selección de variables y preprocesamiento
# ==========================================================

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Variables predictoras
numericas = [
    "temp",
    "hum",
    "windspeed",
    "temp_hum_interaccion"
]

categoricas = [
    "season",
    "weathersit",
    "workingday",
    "yr",
    "fin_de_semana"
]

predictores = numericas + categoricas

# Separar variables explicativas y objetivo
X_train = train_df[predictores].copy()
X_val = val_df[predictores].copy()
X_test = test_df[predictores].copy()

y_train = train_df["cnt"].copy()
y_val = val_df["cnt"].copy()
y_test = test_df["cnt"].copy()

# Transformación numérica y categórica
preprocesador = ColumnTransformer(
    transformers=[
        (
            "numericas",
            StandardScaler(),
            numericas
        ),
        (
            "categoricas",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categoricas
        )
    ]
)

# Ajustar SOLO con entrenamiento
X_train_procesado = preprocesador.fit_transform(X_train)

# Aplicar transformaciones aprendidas
X_val_procesado = preprocesador.transform(X_val)
X_test_procesado = preprocesador.transform(X_test)

print("Entrenamiento:", X_train_procesado.shape)
print("Validación:", X_val_procesado.shape)
print("Prueba:", X_test_procesado.shape)

# Verificaciones
assert X_train_procesado.shape[0] == 511
assert X_val_procesado.shape[0] == 109
assert X_test_procesado.shape[0] == 111

assert np.isfinite(X_train_procesado).all()
assert np.isfinite(X_val_procesado).all()
assert np.isfinite(X_test_procesado).all()

print("Preprocesamiento completado sin fuga de información.")
