
# ==========================================================
# FASE 3 - CELDA 16
# Preparación de datos para aprendizaje no supervisado
# ==========================================================

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Usar el conjunto completo para análisis descriptivo
# no supervisado. No se entrenan modelos predictivos aquí.
df_cluster = crear_caracteristicas(
    df_modelo.copy()
)

# Variables meteorológicas
numericas_cluster = [
    "temp",
    "hum",
    "windspeed"
]

# Variables de calendario y clima
categoricas_cluster = [
    "season",
    "weathersit",
    "workingday",
    "yr"
]

variables_cluster = (
    numericas_cluster + categoricas_cluster
)

X_cluster = df_cluster[
    variables_cluster
].copy()

# Transformación de variables
preprocesador_cluster = ColumnTransformer([
    (
        "numericas",
        StandardScaler(),
        numericas_cluster
    ),
    (
        "categoricas",
        OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=False
        ),
        categoricas_cluster
    )
])

X_cluster_procesado = (
    preprocesador_cluster.fit_transform(
        X_cluster
    )
)

print(
    "Registros para clustering:",
    X_cluster_procesado.shape[0]
)

print(
    "Características transformadas:",
    X_cluster_procesado.shape[1]
)

print(
    "Variables originales:",
    variables_cluster
)

# Validaciones
assert X_cluster_procesado.shape[0] == 731

assert np.isfinite(
    X_cluster_procesado
).all()

assert not {
    "cnt", "casual", "registered"
}.intersection(variables_cluster)

print(
    "Preparación para clustering completada."
)
