
# ==========================================================
# FASE 4 - CELDA 9
# Análisis y decisión de tratamiento del desbalance
# ==========================================================

from sklearn.utils.class_weight import compute_class_weight

# ----------------------------------------------------------
# 1. Distribución de clases en entrenamiento
# ----------------------------------------------------------

conteo_clases = (
    y_train_clf.value_counts()
    .sort_index()
)

clase_mayoritaria = conteo_clases.idxmax()
clase_minoritaria = conteo_clases.idxmin()

n_mayoritaria = int(conteo_clases.max())
n_minoritaria = int(conteo_clases.min())

# Calcular índice de desbalance
imbalance_ratio = n_mayoritaria / n_minoritaria

porcentaje_minoritario = (
    n_minoritaria / len(y_train_clf)
) * 100

print("=== DIAGNÓSTICO DE DESBALANCE ===")

print("Clase mayoritaria:", clase_mayoritaria)
print("Observaciones:", n_mayoritaria)

print("Clase minoritaria:", clase_minoritaria)
print("Observaciones:", n_minoritaria)

print(
    "Imbalance Ratio:",
    round(imbalance_ratio, 4)
)

print(
    "Porcentaje clase minoritaria:",
    round(porcentaje_minoritario, 2), "%"
)

# ----------------------------------------------------------
# 2. Calcular pesos de clase como alternativa
# ----------------------------------------------------------

clases = np.sort(y_train_clf.unique())

pesos = compute_class_weight(
    class_weight="balanced",
    classes=clases,
    y=y_train_clf
)

tabla_pesos = pd.DataFrame({
    "Clase": clases,
    "Observaciones": [
        conteo_clases[c] for c in clases
    ],
    "Peso_balanceado": pesos
})

print("\n=== PESOS DE CLASE POTENCIALES ===")

display(tabla_pesos.round(4))

# ----------------------------------------------------------
# 3. Evaluación de alternativas
# ----------------------------------------------------------

tabla_balanceo = pd.DataFrame([
    {
        "Tecnica": "SMOTE",
        "Aplicada": "No",
        "Justificacion":
            "No se evidencia desbalance severo"
    },
    {
        "Tecnica": "ADASYN",
        "Aplicada": "No",
        "Justificacion":
            "No se requiere generar datos sintéticos"
    },
    {
        "Tecnica": "Class Weight",
        "Aplicada": "No",
        "Justificacion":
            "Alternativa para experimentos posteriores"
    },
    {
        "Tecnica": "Distribución original",
        "Aplicada": "Sí",
        "Justificacion":
            "Ambas clases tienen representación suficiente"
    }
])

print("\n=== EVALUACIÓN DE ALTERNATIVAS ===")

display(tabla_balanceo)

# ----------------------------------------------------------
# 4. Conservar los datos originales
# ----------------------------------------------------------

X_train_clf_balanceado = X_train_clf.copy()
y_train_clf_balanceado = y_train_clf.copy()

# ----------------------------------------------------------
# 5. Visualización de la distribución
# ----------------------------------------------------------

plt.figure(figsize=(8, 5))

barras = plt.bar(
    ["Demanda baja", "Demanda alta"],
    conteo_clases.values,
    color=["steelblue", "darkorange"]
)

plt.bar_label(barras, padding=3)

plt.title("Distribución de clases en entrenamiento")
plt.ylabel("Cantidad de observaciones")
plt.ylim(0, n_mayoritaria * 1.15)
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()

plt.savefig(
    RESULTADOS / "analisis_desbalance.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# ----------------------------------------------------------
# 6. Guardar evidencias
# ----------------------------------------------------------

tabla_balanceo.to_csv(
    RESULTADOS / "estrategia_balanceo.csv",
    index=False
)

tabla_pesos.to_csv(
    RESULTADOS / "pesos_clases.csv",
    index=False
)

# ----------------------------------------------------------
# 7. Verificaciones
# ----------------------------------------------------------

assert len(X_train_clf_balanceado) == 511

assert y_train_clf_balanceado.equals(
    y_train_clf
)

assert X_train_clf_balanceado.equals(
    X_train_clf
)

assert y_train_clf_balanceado.nunique() == 2

print("\n=== DECISIÓN METODOLÓGICA ===")
print("Balanceo artificial aplicado: No")
print("Class Weight aplicado: No")
print("Registros conservados:", len(X_train_clf))
print("Datos sintéticos generados: 0")

print("\nAnálisis de desbalance completado.")
