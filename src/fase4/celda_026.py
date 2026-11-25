
# ==========================================================
# FASE 4 - CELDA 14
# Baseline de clasificación
# ==========================================================

from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report
)

# ----------------------------------------------------------
# 1. Configuración de modelos
# ----------------------------------------------------------

baseline_logistico = LogisticRegression(
    penalty="l2",
    C=1.0,
    solver="lbfgs",
    max_iter=1000,
    class_weight=None,
    random_state=SEMILLA
)

baseline_dummy_clf = DummyClassifier(
    strategy="most_frequent"
)

# ----------------------------------------------------------
# 2. Entrenamiento de modelos
# ----------------------------------------------------------

baseline_logistico.fit(
    X_train_clf_final,
    y_train_clf
)

baseline_dummy_clf.fit(
    X_train_clf_final,
    y_train_clf
)

print("=== CONFIGURACIÓN DEL BASELINE ===")

print("Modelo principal: Regresión Logística")
print("Modelo de referencia: Dummy Classifier")

print(
    "Características utilizadas:",
    X_train_clf_final.shape[1]
)

print(
    "Registros de entrenamiento:",
    len(X_train_clf_final)
)

print("Class Weight: None")

print(
    "Clase mayoritaria:",
    y_train_clf.value_counts().idxmax()
)

print(
    "Iteraciones regresión logística:",
    baseline_logistico.n_iter_[0]
)

# ----------------------------------------------------------
# 3. Función de evaluación
# ----------------------------------------------------------

def evaluar_baseline_clf(
    nombre,
    modelo,
    conjunto,
    X_eval,
    y_eval
):

    predicciones = modelo.predict(X_eval)

    probabilidades = modelo.predict_proba(
        X_eval
    )[:, 1]

    return {
        "Modelo": nombre,
        "Conjunto": conjunto,

        "Accuracy": accuracy_score(
            y_eval, predicciones
        ),

        "Balanced_Accuracy": balanced_accuracy_score(
            y_eval, predicciones
        ),

        "Precision": precision_score(
            y_eval,
            predicciones,
            zero_division=0
        ),

        "Recall": recall_score(
            y_eval,
            predicciones,
            zero_division=0
        ),

        "F1": f1_score(
            y_eval,
            predicciones,
            zero_division=0
        ),

        "F1_Macro": f1_score(
            y_eval,
            predicciones,
            average="macro",
            zero_division=0
        ),

        "AUC_ROC": roc_auc_score(
            y_eval, probabilidades
        )
    }

# ----------------------------------------------------------
# 4. Evaluar entrenamiento, validación y prueba
# ----------------------------------------------------------

resultados_baseline_clf = []

for nombre, modelo in [
    ("Regresión Logística", baseline_logistico),
    ("Dummy Classifier", baseline_dummy_clf)
]:

    for conjunto, X_eval, y_eval in [
        (
            "Entrenamiento",
            X_train_clf_final,
            y_train_clf
        ),
        (
            "Validación",
            X_val_clf_final,
            y_val_clf
        ),
        (
            "Prueba",
            X_test_clf_final,
            y_test_clf
        )
    ]:

        resultados_baseline_clf.append(
            evaluar_baseline_clf(
                nombre,
                modelo,
                conjunto,
                X_eval,
                y_eval
            )
        )

tabla_baseline_clf = pd.DataFrame(
    resultados_baseline_clf
)

print("\n=== RESULTADOS BASELINE CLASIFICACIÓN ===")

display(tabla_baseline_clf.round(4))

# ----------------------------------------------------------
# 5. Comparación de métricas en prueba
# ----------------------------------------------------------

resultados_prueba_clf = (
    tabla_baseline_clf[
        tabla_baseline_clf["Conjunto"] == "Prueba"
    ]
    .set_index("Modelo")
)

metricas_clf = [
    "Accuracy",
    "Balanced_Accuracy",
    "Precision",
    "Recall",
    "F1",
    "F1_Macro",
    "AUC_ROC"
]

resultados_prueba_clf[metricas_clf].T.plot(
    kind="bar",
    figsize=(13, 6),
    rot=25
)

plt.title(
    "Comparación de modelos baseline de clasificación"
)

plt.ylabel("Puntuación")
plt.xlabel("Métrica")
plt.ylim(0, 1.1)
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()

plt.savefig(
    RESULTADOS / "comparacion_baseline_clasificacion.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# ----------------------------------------------------------
# 6. Matrices de confusión
# ----------------------------------------------------------

fig, axes = plt.subplots(
    1, 2,
    figsize=(12, 5)
)

for ax, nombre, modelo in [
    (
        axes[0],
        "Regresión Logística",
        baseline_logistico
    ),
    (
        axes[1],
        "Dummy Classifier",
        baseline_dummy_clf
    )
]:

    predicciones = modelo.predict(
        X_test_clf_final
    )

    matriz = confusion_matrix(
        y_test_clf,
        predicciones,
        labels=[0, 1]
    )

    sns.heatmap(
        matriz,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Baja", "Alta"],
        yticklabels=["Baja", "Alta"],
        ax=ax
    )

    ax.set_title(nombre)
    ax.set_xlabel("Clase predicha")
    ax.set_ylabel("Clase real")

plt.suptitle(
    "Matrices de confusión - Conjunto de prueba"
)

plt.tight_layout()

plt.savefig(
    RESULTADOS / "matrices_baseline_clasificacion.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# ----------------------------------------------------------
# 7. Curvas ROC
# ----------------------------------------------------------

plt.figure(figsize=(8, 6))

for nombre, modelo in [
    ("Regresión Logística", baseline_logistico),
    ("Dummy Classifier", baseline_dummy_clf)
]:

    probabilidades = modelo.predict_proba(
        X_test_clf_final
    )[:, 1]

    fpr, tpr, _ = roc_curve(
        y_test_clf,
        probabilidades
    )

    auc = roc_auc_score(
        y_test_clf,
        probabilidades
    )

    plt.plot(
        fpr,
        tpr,
        linewidth=2,
        label=f"{nombre} (AUC = {auc:.4f})"
    )

plt.plot(
    [0, 1],
    [0, 1],
    "k--",
    label="Referencia aleatoria"
)

plt.title("Curvas ROC - Modelos baseline")
plt.xlabel("Tasa de falsos positivos")
plt.ylabel("Tasa de verdaderos positivos")
plt.legend(loc="lower right")
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    RESULTADOS / "curvas_roc_baseline.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# ----------------------------------------------------------
# 8. Reporte detallado por clase
# ----------------------------------------------------------

pred_baseline_clf = baseline_logistico.predict(
    X_test_clf_final
)

print("\n=== REPORTE DE CLASIFICACIÓN ===")

print(
    classification_report(
        y_test_clf,
        pred_baseline_clf,
        labels=[0, 1],
        target_names=[
            "Demanda baja",
            "Demanda alta"
        ],
        zero_division=0
    )
)

# ----------------------------------------------------------
# 9. Comparación frente al Dummy Classifier
# ----------------------------------------------------------

f1_macro_logistico = resultados_prueba_clf.loc[
    "Regresión Logística", "F1_Macro"
]

f1_macro_dummy = resultados_prueba_clf.loc[
    "Dummy Classifier", "F1_Macro"
]

diferencia_f1_macro = (
    f1_macro_logistico - f1_macro_dummy
) * 100

print("\n=== COMPARACIÓN FINAL ===")

print(
    "F1 Macro Regresión Logística:",
    round(f1_macro_logistico, 4)
)

print(
    "F1 Macro Dummy Classifier:",
    round(f1_macro_dummy, 4)
)

print(
    "Diferencia F1 Macro:",
    round(diferencia_f1_macro, 2),
    "puntos porcentuales"
)

# ----------------------------------------------------------
# 10. Guardar resultados
# ----------------------------------------------------------

tabla_baseline_clf.to_csv(
    RESULTADOS / "metricas_baseline_clasificacion.csv",
    index=False
)

# ----------------------------------------------------------
# 11. Verificaciones finales
# ----------------------------------------------------------

assert baseline_logistico.n_features_in_ == 29

assert len(pred_baseline_clf) == 110

assert set(
    pred_baseline_clf
).issubset({0, 1})

assert np.isfinite(
    tabla_baseline_clf[metricas_clf].to_numpy()
).all()

assert baseline_logistico.n_iter_[0] < 1000

assert np.isclose(
    resultados_prueba_clf.loc[
        "Dummy Classifier", "AUC_ROC"
    ],
    0.5
)

print("\n=== VERIFICACIÓN FINAL ===")

print("Modelos entrenados: 2")
print("Características utilizadas: 29")
print("Entrenamiento exclusivo: Sí")
print("Métricas calculadas: 7")
print("Gráficos generados: 3")
print("Baseline de clasificación completado.")
