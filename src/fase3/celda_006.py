
# ==========================================================
# FASE 3 - CELDA 5
# Ingeniería de características
# ==========================================================

def crear_caracteristicas(datos):
    """
    Crea variables derivadas sin utilizar la variable objetivo.
    """
    resultado = datos.copy()

    # 1. Identificar sábados y domingos
    # En pandas: lunes=0, domingo=6
    resultado["fin_de_semana"] = (
        resultado["dteday"].dt.dayofweek >= 5
    ).astype(int)

    # 2. Interacción entre temperatura y humedad
    resultado["temp_hum_interaccion"] = (
        resultado["temp"] * resultado["hum"]
    )

    return resultado


# Aplicar la misma transformación a cada conjunto
train_df = crear_caracteristicas(train_df)
val_df = crear_caracteristicas(val_df)
test_df = crear_caracteristicas(test_df)

# Verificar nuevas columnas
columnas_nuevas = [
    "fin_de_semana",
    "temp_hum_interaccion"
]

for nombre, datos in [
    ("Entrenamiento", train_df),
    ("Validación", val_df),
    ("Prueba", test_df)
]:
    assert all(
        columna in datos.columns
        for columna in columnas_nuevas
    )

    assert datos[columnas_nuevas].isna().sum().sum() == 0

    print(
        f"{nombre}: {datos.shape[0]} filas, "
        f"{datos.shape[1]} columnas"
    )

print("\nEjemplo de las nuevas características:")

display(
    train_df[
        [
            "dteday",
            "temp",
            "hum",
            "fin_de_semana",
            "temp_hum_interaccion",
            "cnt"
        ]
    ].head(10)
)

print("\nIngeniería de características completada.")
