
# ==========================================================
# FASE 4 - CELDA 5
# Detección de valores atípicos mediante IQR
# ==========================================================

# Variables cuantitativas que serán analizadas
variables_outliers = [
    "temp",
    "atemp",
    "hum",
    "windspeed",
    "cnt"
]

resultados_outliers = []

for variable in variables_outliers:

    # Calcular cuartiles
    q1 = df_limpio[variable].quantile(0.25)
    q3 = df_limpio[variable].quantile(0.75)

    # Rango intercuartílico
    iqr = q3 - q1

    # Límites estadísticos
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    # Identificar valores atípicos
    mascara = (
        (df_limpio[variable] < limite_inferior) |
        (df_limpio[variable] > limite_superior)
    )

    cantidad = int(mascara.sum())

    porcentaje = (
        cantidad / len(df_limpio)
    ) * 100

    resultados_outliers.append({
        "Variable": variable,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Limite_inferior": limite_inferior,
        "Limite_superior": limite_superior,
        "Outliers": cantidad,
        "Porcentaje": porcentaje
    })

# Consolidar resultados
tabla_outliers = pd.DataFrame(
    resultados_outliers
)

print("=== DIAGNÓSTICO DE VALORES ATÍPICOS ===")

display(tabla_outliers.round(4))

# Generar diagramas de caja
fig, axes = plt.subplots(
    2, 3,
    figsize=(15, 8)
)

axes = axes.flatten()

for i, variable in enumerate(variables_outliers):

    sns.boxplot(
        x=df_limpio[variable],
        ax=axes[i],
        color="steelblue"
    )

    axes[i].set_title(
        f"Distribución de {variable}"
    )

    axes[i].grid(
        axis="x",
        alpha=0.25
    )

# Eliminar espacio gráfico sobrante
fig.delaxes(axes[5])

plt.suptitle(
    "Detección de valores atípicos mediante IQR",
    fontsize=15
)

plt.tight_layout()

# Guardar evidencia
ruta_outliers = (
    RESULTADOS / "deteccion_outliers.png"
)

plt.savefig(
    ruta_outliers,
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Mostrar observaciones atípicas por variable
print("\n=== RESUMEN DE OUTLIERS ===")

for _, fila in tabla_outliers.iterrows():

    print(
        f"{fila['Variable']}: "
        f"{int(fila['Outliers'])} valores atípicos "
        f"({fila['Porcentaje']:.2f} %)"
    )

# Verificar que no se modificaron los datos
assert df_limpio.shape == (731, 16)
assert len(tabla_outliers) == 5

print("\nRegistros conservados:", len(df_limpio))
print("Gráfico guardado en:", ruta_outliers)
print("Diagnóstico de outliers completado.")
