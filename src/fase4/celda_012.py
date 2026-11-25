
# ==========================================================
# FASE 4 - CELDA 7
# Ingeniería de características
# ==========================================================

def crear_caracteristicas(datos):

    # Preservar el dataframe recibido
    datos = datos.copy()

    # 1. Indicador de fin de semana
    datos["fin_de_semana"] = (
        datos["dteday"].dt.dayofweek >= 5
    ).astype(int)

    # 2. Interacción temperatura y humedad
    datos["temp_hum_interaccion"] = (
        datos["temp"] * datos["hum"]
    )

    # 3 y 4. Representación cíclica del mes
    datos["mes_sin"] = np.sin(
        2 * np.pi * (datos["mnth"] - 1) / 12
    )

    datos["mes_cos"] = np.cos(
        2 * np.pi * (datos["mnth"] - 1) / 12
    )

    return datos


# Aplicar ingeniería de características
df_features = crear_caracteristicas(df_limpio)

variables_derivadas = [
    "fin_de_semana",
    "temp_hum_interaccion",
    "mes_sin",
    "mes_cos"
]

print("=== INGENIERÍA DE CARACTERÍSTICAS ===")

print("Dimensión original:", df_limpio.shape)
print("Dimensión transformada:", df_features.shape)
print("Variables nuevas:", len(variables_derivadas))

# Visualizar las características generadas
print("\n=== EJEMPLO DE VARIABLES DERIVADAS ===")

display(
    df_features[
        ["dteday", "temp", "hum", "mnth"]
        + variables_derivadas
    ].head(10).round(4)
)

# Estadísticas descriptivas
print("\n=== ESTADÍSTICAS DESCRIPTIVAS ===")

display(
    df_features[variables_derivadas]
    .describe()
    .round(4)
)

# Distribución de días
print("\n=== DISTRIBUCIÓN DE DÍAS ===")

display(
    df_features["fin_de_semana"]
    .value_counts()
    .sort_index()
    .rename(index={
        0: "Lunes a viernes",
        1: "Fin de semana"
    })
    .to_frame("Cantidad")
)

# Visualización de la codificación cíclica
meses_ciclicos = (
    df_features[
        ["mnth", "mes_sin", "mes_cos"]
    ]
    .drop_duplicates()
    .sort_values("mnth")
)

plt.figure(figsize=(7, 7))

plt.scatter(
    meses_ciclicos["mes_sin"],
    meses_ciclicos["mes_cos"],
    s=100,
    color="steelblue"
)

for _, fila in meses_ciclicos.iterrows():

    plt.annotate(
        str(int(fila["mnth"])),
        (
            fila["mes_sin"],
            fila["mes_cos"]
        ),
        xytext=(8, 8),
        textcoords="offset points"
    )

plt.title("Representación cíclica de los meses")
plt.xlabel("Componente seno")
plt.ylabel("Componente coseno")
plt.axhline(0, color="gray", alpha=0.4)
plt.axvline(0, color="gray", alpha=0.4)
plt.axis("equal")
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    RESULTADOS / "ingenieria_caracteristicas.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Verificaciones de integridad
assert df_features.shape == (731, 20)

assert df_limpio.shape == (731, 16)

assert df_features[
    variables_derivadas
].isna().sum().sum() == 0

assert set(
    df_features["fin_de_semana"].unique()
) == {0, 1}

assert np.allclose(
    df_features["mes_sin"]**2 +
    df_features["mes_cos"]**2,
    1
)

assert df_features["cnt"].equals(
    df_limpio["cnt"]
)

print("\nIngeniería de características completada.")
