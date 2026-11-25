
# ==========================================================
# FASE 3 - CELDA 20
# Perfil de clústeres de Agglomerative Clustering
# ==========================================================

# Construir perfil descriptivo
perfil_aglomerativo = (
    df_cluster
    .groupby("cluster_aglomerativo")
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

print("Perfil de Agglomerative Clustering:")
display(perfil_aglomerativo)

# Comparación gráfica de la demanda promedio
fig, axes = plt.subplots(
    1, 2,
    figsize=(12, 4)
)

sns.barplot(
    data=df_cluster,
    x="cluster_kmeans",
    y="cnt",
    estimator="mean",
    errorbar=None,
    ax=axes[0]
)

axes[0].set_title("K-Means")
axes[0].set_xlabel("Clúster")
axes[0].set_ylabel("Alquileres diarios promedio")

sns.barplot(
    data=df_cluster,
    x="cluster_aglomerativo",
    y="cnt",
    estimator="mean",
    errorbar=None,
    ax=axes[1]
)

axes[1].set_title("Agglomerative Clustering")
axes[1].set_xlabel("Clúster")
axes[1].set_ylabel("Alquileres diarios promedio")

for ax in axes:
    ax.grid(axis="y", alpha=0.25)

plt.suptitle(
    "Comparación de perfiles de demanda por algoritmo"
)

plt.tight_layout()

ruta_comparacion_clusters = (
    RESULTADOS / "comparacion_perfiles_clusters.png"
)

plt.savefig(
    ruta_comparacion_clusters,
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Verificaciones
assert perfil_aglomerativo["dias"].sum() == 731
assert len(perfil_aglomerativo) == 2

print("Caracterización de Agglomerative completada.")
