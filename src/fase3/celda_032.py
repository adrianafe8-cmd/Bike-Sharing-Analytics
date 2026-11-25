
# ==========================================================
# FASE 3 - CELDA 18
# K-Means definitivo y perfil de los clústeres
# ==========================================================

from sklearn.cluster import KMeans

# Entrenar con el K seleccionado
modelo_kmeans_final = KMeans(
    n_clusters=mejor_k_cluster,
    random_state=SEMILLA,
    n_init=10
)

etiquetas_kmeans = modelo_kmeans_final.fit_predict(
    X_cluster_procesado
)

# Incorporar etiquetas al dataframe descriptivo
df_cluster["cluster_kmeans"] = etiquetas_kmeans

# Tamaño de cada clúster
tamano_clusters = (
    df_cluster["cluster_kmeans"]
    .value_counts()
    .sort_index()
)

print("Distribución de observaciones:")
display(tamano_clusters.to_frame("Cantidad de días"))

# Perfil de los clústeres
perfil_kmeans = (
    df_cluster
    .groupby("cluster_kmeans")
    .agg(
        dias=("cnt", "size"),
        demanda_promedio=("cnt", "mean"),
        demanda_mediana=("cnt", "median"),
        temperatura_promedio=("temp", "mean"),
        humedad_promedio=("hum", "mean"),
        viento_promedio=("windspeed", "mean"),
        proporcion_laborales=("workingday", "mean")
    )
    .round(3)
)

print("\nPerfil de los clústeres:")
display(perfil_kmeans)

# Gráfico de demanda promedio por clúster
plt.figure(figsize=(8, 4))

sns.barplot(
    data=df_cluster,
    x="cluster_kmeans",
    y="cnt",
    estimator="mean",
    errorbar=None
)

plt.title(
    "Demanda promedio de bicicletas por clúster"
)
plt.xlabel("Clúster K-Means")
plt.ylabel("Alquileres diarios promedio")
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()

ruta_perfil_kmeans = (
    RESULTADOS / "perfil_kmeans.png"
)

plt.savefig(
    ruta_perfil_kmeans,
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Verificaciones
assert len(etiquetas_kmeans) == 731

assert (
    df_cluster["cluster_kmeans"].nunique()
    == mejor_k_cluster
)

assert tamano_clusters.sum() == 731

print("Caracterización K-Means completada.")
