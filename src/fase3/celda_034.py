
# ==========================================================
# FASE 3 - CELDA 19
# Clustering jerárquico aglomerativo
# ==========================================================

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import (
    silhouette_score,
    adjusted_rand_score
)

# Modelo jerárquico con el mismo número de clústeres
modelo_aglomerativo = AgglomerativeClustering(
    n_clusters=mejor_k_cluster,
    linkage="ward"
)

etiquetas_aglomerativo = (
    modelo_aglomerativo.fit_predict(
        X_cluster_procesado
    )
)

# Incorporar etiquetas al dataframe
df_cluster["cluster_aglomerativo"] = (
    etiquetas_aglomerativo
)

# Silueta de ambos algoritmos
silueta_kmeans = silhouette_score(
    X_cluster_procesado,
    etiquetas_kmeans
)

silueta_aglomerativo = silhouette_score(
    X_cluster_procesado,
    etiquetas_aglomerativo
)

# Coincidencia de agrupamientos, independiente
# de los números asignados a las etiquetas
ari = adjusted_rand_score(
    etiquetas_kmeans,
    etiquetas_aglomerativo
)

comparacion_clustering = pd.DataFrame([
    {
        "Algoritmo": "K-Means",
        "Clusters": mejor_k_cluster,
        "Silueta": silueta_kmeans
    },
    {
        "Algoritmo": "Agglomerative",
        "Clusters": mejor_k_cluster,
        "Silueta": silueta_aglomerativo
    }
])

print("Comparación de algoritmos:")
display(
    comparacion_clustering.style.format({
        "Silueta": "{:.4f}"
    })
)

print(
    "Índice Rand ajustado (ARI):",
    round(ari, 4)
)

print("\nDistribución Agglomerative:")
display(
    df_cluster["cluster_aglomerativo"]
    .value_counts()
    .sort_index()
    .to_frame("Cantidad de días")
)

# Verificaciones
assert len(etiquetas_aglomerativo) == 731
assert len(np.unique(etiquetas_aglomerativo)) == 2

assert np.isfinite(
    [silueta_kmeans, silueta_aglomerativo, ari]
).all()

print("Clustering jerárquico completado.")
