
# ==========================================================
# FASE 4 - CELDA 16
# Verificación final y empaquetado de evidencias
# ==========================================================

import sys
import json
import shutil
import hashlib
import sklearn
import matplotlib
import seaborn

# ----------------------------------------------------------
# 1. Registrar versiones del entorno
# ----------------------------------------------------------

versiones = {
    "Python": sys.version.split()[0],
    "Pandas": pd.__version__,
    "NumPy": np.__version__,
    "Scikit-learn": sklearn.__version__,
    "Matplotlib": matplotlib.__version__,
    "Seaborn": seaborn.__version__,
    "Semilla": SEMILLA
}

print("=== ENTORNO DE REPRODUCIBILIDAD ===")

for biblioteca, version in versiones.items():
    print(f"{biblioteca}: {version}")

# Guardar configuración del entorno

with open(
    RESULTADOS / "entorno_ejecucion.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        versiones,
        archivo,
        indent=4,
        ensure_ascii=False
    )

# ----------------------------------------------------------
# 2. Verificar integridad de las particiones
# ----------------------------------------------------------

for problema, train, val, test in [

    (
        "Regresión",
        X_train_reg_final,
        X_val_reg_final,
        X_test_reg_final
    ),

    (
        "Clasificación",
        X_train_clf_final,
        X_val_clf_final,
        X_test_clf_final
    )

]:

    assert train.index.is_unique
    assert val.index.is_unique
    assert test.index.is_unique

    assert len(
        set(train.index) & set(val.index)
    ) == 0

    assert len(
        set(train.index) & set(test.index)
    ) == 0

    assert len(
        set(val.index) & set(test.index)
    ) == 0

    assert len(train) + len(val) + len(test) == 731

    assert train.shape[1] == 29
    assert val.shape[1] == 29
    assert test.shape[1] == 29

    assert train.columns.equals(val.columns)
    assert train.columns.equals(test.columns)

    print(f"\nParticiones de {problema}: OK")

# ----------------------------------------------------------
# 3. Verificar métricas finales
# ----------------------------------------------------------

assert np.isclose(
    resultados_prueba_reg.loc[
        "Regresión Lineal Simple", "RMSE"
    ],
    2568.0320,
    atol=0.01
)

assert np.isclose(
    resultados_prueba_clf.loc[
        "Regresión Logística", "Accuracy"
    ],
    0.9000,
    atol=0.0001
)

assert np.isclose(
    resultados_prueba_clf.loc[
        "Regresión Logística", "AUC_ROC"
    ],
    0.9751,
    atol=0.0001
)

print("\nMétricas de referencia: OK")

# ----------------------------------------------------------
# 4. Verificar evidencias
# ----------------------------------------------------------

for archivo in archivos_esperados:

    ruta = RESULTADOS / archivo

    assert ruta.exists(), f"Archivo faltante: {archivo}"

    assert ruta.stat().st_size > 0

print("Archivos obligatorios: OK")

# ----------------------------------------------------------
# 5. Identificación del dataset mediante SHA-256
# ----------------------------------------------------------

ruta_dataset = BASE / "datos" / "day.csv"

assert ruta_dataset.exists()

hash_dataset = hashlib.sha256(
    ruta_dataset.read_bytes()
).hexdigest()

print("\n=== IDENTIFICACIÓN DEL DATASET ===")

print("Archivo:", ruta_dataset.name)
print("SHA-256:", hash_dataset)

with open(
    RESULTADOS / "identificacion_dataset.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        {
            "archivo": ruta_dataset.name,
            "sha256": hash_dataset,
            "registros": 731,
            "variables_originales": 16
        },
        archivo,
        indent=4
    )

# ----------------------------------------------------------
# 6. Crear archivo ZIP de evidencias
# ----------------------------------------------------------

ruta_zip = shutil.make_archive(
    str(BASE / "Evidencias_Fase_4_Bicicletas"),
    "zip",
    root_dir=RESULTADOS
)

cantidad_archivos = sum(
    archivo.is_file()
    for archivo in RESULTADOS.iterdir()
)

# ----------------------------------------------------------
# 7. Resumen final
# ----------------------------------------------------------

print("\n" + "=" * 65)
print("PROYECTO INTEGRADOR - FASE 4")
print("=" * 65)

print("Dataset: Bike Sharing")
print("Registros conservados: 731")
print("Características finales: 29")
print("Modelos baseline entrenados: 4")
print("Requerimientos cumplidos: 12")
print("Requerimientos no aplicables: 1")
print("Archivos de evidencia:", cantidad_archivos)
print("Archivo ZIP:", ruta_zip)

print("\nVerificaciones de integridad: EXITOSAS")

print(
    "Reproducibilidad integral: "
    "pendiente de ejecutar desde un entorno limpio."
)

print("=" * 65)
print("FASE 4 - DESARROLLO COMPLETADO")
print("=" * 65)
