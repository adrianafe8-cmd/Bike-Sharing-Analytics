
# ==========================================================
# FASE 4 - CELDA 4
# Análisis de ausencia y decisión de imputación
# ==========================================================

# Calcular cantidad total de datos
total_celdas = df_limpio.size

# Calcular valores faltantes y válidos
total_faltantes = int(
    df_limpio.isna().sum().sum()
)

total_validos = total_celdas - total_faltantes

porcentaje_ausencia = (
    total_faltantes / total_celdas
) * 100

print("=== ANÁLISIS DE AUSENCIA ===")
print("Total de celdas:", total_celdas)
print("Valores válidos:", total_validos)
print("Valores faltantes:", total_faltantes)
print(
    "Porcentaje de ausencia:",
    round(porcentaje_ausencia, 4), "%"
)

# Evaluación de alternativas de tratamiento
alternativas_imputacion = pd.DataFrame([
    {
        "Tecnica": "Eliminación de registros",
        "Aplicada": "No",
        "Justificacion": "No existen registros incompletos"
    },
    {
        "Tecnica": "Media",
        "Aplicada": "No",
        "Justificacion": "No existen valores faltantes"
    },
    {
        "Tecnica": "Mediana",
        "Aplicada": "No",
        "Justificacion": "No existen valores faltantes"
    },
    {
        "Tecnica": "KNNImputer",
        "Aplicada": "No",
        "Justificacion": "No se requiere imputación"
    },
    {
        "Tecnica": "IterativeImputer",
        "Aplicada": "No",
        "Justificacion": "No se requiere imputación"
    },
    {
        "Tecnica": "Conservación de datos originales",
        "Aplicada": "Sí",
        "Justificacion": "Preserva toda la información válida"
    }
])

print("\n=== EVALUACIÓN DE ALTERNATIVAS ===")
display(alternativas_imputacion)

# Visualizar completitud de los datos
completitud = (
    df_limpio.notna().mean() * 100
).sort_values()

plt.figure(figsize=(10, 6))

completitud.plot(
    kind="barh",
    color="steelblue"
)

plt.title("Porcentaje de completitud por variable")
plt.xlabel("Datos válidos (%)")
plt.ylabel("Variable")
plt.xlim(0, 105)
plt.grid(axis="x", alpha=0.25)
plt.tight_layout()

plt.savefig(
    RESULTADOS / "completitud_datos.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Decisión metodológica
if total_faltantes == 0:
    print("\nMecanismo de ausencia: No identificable.")
    print("Imputación requerida: No.")
    print("Decisión: Conservar los datos originales.")
else:
    raise ValueError(
        "Se requiere analizar el mecanismo de ausencia."
    )

# Verificaciones
assert df_limpio.shape == (731, 16)
assert total_faltantes == 0
assert porcentaje_ausencia == 0

print("\nAnálisis de ausencia completado.")
