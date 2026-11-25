
# ==========================================================
# FASE 3 - CELDA 17
# K-Means: método del codo y coeficiente de silueta
# ==========================================================

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

valores_k_cluster = range(2, 11)

resultados_kmeans = []

for k in valores_k_cluster:

    modelo = KMeans(
        n_clusters=k,
        random_state=SEMILLA,
        n_init=10
    )

    etiquetas = modelo.fit_predict(
        X_cluster_procesado
    )

    inercia = modelo.inertia_

    silueta = silhouette_score(
        X_cluster_procesado,
        etiquetas
    )

    resultados_kmeans.append({
        "K": k,
        "Inercia": inercia,
        "Silueta": silueta
    })

tabla_kmeans = pd.DataFrame(
    resultados_kmeans
)

display(
    tabla_kmeans.style.format({
        "Inercia": "{:.2f}",
        "Silueta": "{:.4f}"
    })
)

# Selección automática por silueta
mejor_k_cluster = int(
    tabla_kmeans.loc[
        tabla_kmeans["Silueta"].idxmax(),
        "K"
    ]
)

print(
    "Mejor K según silueta:",
    mejor_k_cluster
)

# Visualización
fig, axes = plt.subplots(
    1, 2,
    figsize=(13, 4)
)

# Método del codo
axes[0].plot(
    tabla_kmeans["K"],
    tabla_kmeans["Inercia"],
    marker="o"
)

axes[0].set_title(
    "Método del codo - K-Means"
)
axes[0].set_xlabel(
    "Número de clústeres (K)"
)
axes[0].set_ylabel("Inercia")
axes[0].grid(alpha=0.3)

# Coeficiente de silueta
axes[1].plot(
    tabla_kmeans["K"],
    tabla_kmeans["Silueta"],
    marker="o"
)

axes[1].axvline(
    mejor_k_cluster,
    color="red",
    linestyle="--",
    label=f"Mejor K = {mejor_k_cluster}"
)

axes[1].set_title(
    "Coeficiente de silueta - K-Means"
)
axes[1].set_xlabel(
    "Número de clústeres (K)"
)
axes[1].set_ylabel(
    "Silueta promedio"
)
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()

ruta_kmeans = (
    RESULTADOS / "kmeans_codo_silueta.png"
)

plt.savefig(
    ruta_kmeans,
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Verificaciones
assert len(tabla_kmeans) == 9
assert 2 <= mejor_k_cluster <= 10

assert np.isfinite(
    tabla_kmeans[
        ["Inercia", "Silueta"]
    ].to_numpy()
).all()

print(
    "Análisis K-Means completado."
)
print(
    "Gráfico guardado en:",
    ruta_kmeans
)
