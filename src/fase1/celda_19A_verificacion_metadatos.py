# ==========================================================
# DASHBOARD GLOBAL - CELDA 19A
# Verificación de metadatos y categorías estacionales
# ==========================================================

from datetime import datetime, timezone
from pathlib import Path

# ==========================================================
# 1. VERIFICAR CODIFICACIÓN DE ESTACIONES
# ==========================================================

df_verificacion_estaciones = (
    df.assign(Mes=df["dteday"].dt.month)
    .groupby(["season", "Mes"])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=range(1, 13), fill_value=0)
)

df_periodos_estaciones = (
    df.groupby(["season", "yr"])
    .agg(
        Fecha_inicial=("dteday", "min"),
        Fecha_final=("dteday", "max"),
        Registros=("dteday", "size")
    )
    .reset_index()
)

print("=" * 60)
print("VERIFICACIÓN DE METADATOS")
print("=" * 60)

print("\n=== DISTRIBUCIÓN DE ESTACIONES POR MES ===")
print(df_verificacion_estaciones.to_string())

print("\n=== PERIODOS POR ESTACIÓN Y AÑO ===")
print(df_periodos_estaciones.to_string(index=False))

# ==========================================================
# 2. VERIFICAR CODIFICACIÓN DE DÍAS DE LA SEMANA
# ==========================================================

dias_semana = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
}

df_verificacion_dias = (
    df.assign(
        Dia_real=df["dteday"].dt.dayofweek.map(dias_semana)
    )[["weekday", "Dia_real"]]
    .drop_duplicates()
    .sort_values("weekday")
    .reset_index(drop=True)
)

print("\n=== CODIFICACIÓN DE DÍAS ===")
print(df_verificacion_dias.to_string(index=False))

# ==========================================================
# 3. VERIFICAR FECHAS DE ARCHIVOS
# ==========================================================

print("\n=== FECHAS DE LOS ARCHIVOS ===")

for ruta in [RUTA_ZIP, RUTA_CSV]:

    ruta = Path(ruta)

    fecha_modificacion = datetime.fromtimestamp(
        ruta.stat().st_mtime,
        tz=timezone.utc
    )

    print("Archivo:", ruta.name)
    print("Última modificación UTC:",
          fecha_modificacion.isoformat())

# ==========================================================
# 4. VERIFICAR LICENCIA EN REPOSITORIO UCI
# ==========================================================

try:

    import requests

    respuesta = requests.get(
        "https://archive.ics.uci.edu/api/dataset?id=275",
        timeout=30
    )

    respuesta.raise_for_status()

    metadata_uci = respuesta.json().get("data", {})

    print("\n=== METADATOS OFICIALES UCI ===")

    for campo, valor in metadata_uci.items():

        if any(
            palabra in campo.lower()
            for palabra in [
                "license",
                "licence",
                "doi",
                "date",
                "year",
                "name"
            ]
        ):

            print(f"{campo}: {valor}")

except Exception as error:

    print("\nNo fue posible consultar la API de UCI.")
    print("Detalle:", str(error))

# ==========================================================
# 5. REFERENCIAS BIBLIOGRÁFICAS
# ==========================================================

referencia_dataset = (
    "Fanaee-T, H. (2013). Bike Sharing Dataset "
    "[Dataset]. UCI Machine Learning Repository. "
    "https://doi.org/10.24432/C5W894"
)

referencia_articulo = (
    "Fanaee-T, H., & Gama, J. (2013). "
    "Event labeling combining ensemble detectors "
    "and background knowledge. "
    "Progress in Artificial Intelligence. "
    "https://doi.org/10.1007/s13748-013-0040-3"
)

print("\n=== REFERENCIAS BIBLIOGRÁFICAS ===")
print(referencia_dataset)
print(referencia_articulo)

# ==========================================================
# 6. VALIDACIONES
# ==========================================================

assert df_verificacion_estaciones.to_numpy().sum() == 731
assert len(df_verificacion_dias) == 7
assert len(df) == 731
assert int(df["cnt"].sum()) == total_alquileres

print("\n=== VALIDACIONES ===")
print("Distribución estacional: OK")
print("Codificación semanal: OK")
print("Integridad del dataset: OK")
print("Modelos reentrenados: 0")
print("\nVerificación de metadatos finalizada.")