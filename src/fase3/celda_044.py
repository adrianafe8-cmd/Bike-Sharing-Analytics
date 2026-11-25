
# ==========================================================
# FASE 3 - CELDA 24
# Consolidación y verificación de resultados
# ==========================================================

print("=" * 55)
print("RESUMEN FINAL - FASE 3")
print("=" * 55)

print("\n1. REGRESIÓN - CONJUNTO DE PRUEBA")
display(tabla_regresion_test.round(4))

print("\n2. CLASIFICACIÓN - CONJUNTO DE PRUEBA")
display(tabla_clasificacion_test.round(4))

print("\n3. CLUSTERING - COMPARACIÓN")
display(comparacion_clustering.round(4))

print("\n4. CONFIGURACIONES SELECCIONADAS")
print("Ridge alpha:", mejor_alpha)
print("Random Forest Regressor:", mejor_config_rf)
print("KNN k:", mejor_k)
print(
    "Random Forest Classifier:",
    int(mejor_config_rf_clf["n_estimators"]),
    mejor_config_rf_clf["max_depth"],
    int(mejor_config_rf_clf["min_samples_leaf"])
)
print("K-Means K:", mejor_k_cluster)

# Verificar archivos de resultados
archivos_esperados = [
    "comparacion_regresion.png",
    "comparacion_clasificacion.png",
    "kmeans_codo_silueta.png",
    "perfil_kmeans.png",
    "comparacion_perfiles_clusters.png",
    "importancia_variables_regresion.png",
    "evaluacion_final_regresion.png",
    "evaluacion_final_clasificacion.png"
]

print("\n5. VERIFICACIÓN DE GRÁFICOS")

archivos_faltantes = []

for nombre in archivos_esperados:
    ruta = RESULTADOS / nombre

    if ruta.exists():
        print("OK:", nombre)
    else:
        print("FALTA:", nombre)
        archivos_faltantes.append(nombre)

assert not archivos_faltantes, (
    f"Faltan archivos: {archivos_faltantes}"
)

assert len(tabla_regresion_test) == 2
assert len(tabla_clasificacion_test) == 2
assert len(comparacion_clustering) == 2

print("\nVERIFICACIÓN FINAL COMPLETADA.")
