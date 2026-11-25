# ==========================================================
# DASHBOARD GLOBAL - CELDA 20
# Actualización, validación y exportación final
# ==========================================================

import shutil
import json
import hashlib
import platform
from importlib.metadata import version
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# ==========================================================
# 1. CONFIRMAR LICENCIA DEL DATASET
# ==========================================================

df_ficha_tecnica.loc[
    df_ficha_tecnica["Campo"] == "Licencia",
    "Valor"
] = "Creative Commons Attribution 4.0 International (CC BY 4.0)"

df_ficha_tecnica = pd.concat([
    df_ficha_tecnica,
    pd.DataFrame([
        {
            "Campo": "Fuente oficial de licencia",
            "Valor": (
                "https://archive.ics.uci.edu/"
                "dataset/275/bike-sharing-dataset"
            )
        },
        {
            "Campo": "URL de licencia",
            "Valor": (
                "https://creativecommons.org/licenses/by/4.0/"
            )
        }
    ])
], ignore_index=True).drop_duplicates(
    subset="Campo",
    keep="last"
)

complementos_fase1["ficha_tecnica"] = df_ficha_tecnica

df_ficha_tecnica.to_csv(
    FASE1 / "ficha_tecnica.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 2. ACTUALIZAR INVENTARIO EJECUTIVO
# ==========================================================

inventario_fases.loc[
    inventario_fases["Fase"] == "Fase 1",
    "Graficas_interactivas"
] = 12

inventario_fases.loc[
    inventario_fases["Fase"] == "Fase 1",
    "Estado"
] = "Consolidado y complementado"

inventario_fases.to_csv(
    RESULTADOS / "inventario_fases.csv",
    index=False,
    encoding="utf-8-sig"
)

figuras_resumen["evidencias_por_fase"] = px.bar(
    inventario_fases,
    x="Fase",
    y=[
        "Graficas_interactivas",
        "Imagenes_originales"
    ],
    barmode="group",
    title="Evidencias integradas por fase",
    labels={
        "value": "Cantidad",
        "variable": "Tipo de evidencia"
    },
    color_discrete_sequence=[
        "#2563EB",
        "#0D9488"
    ],
    template="plotly_white"
)

figuras_resumen[
    "evidencias_por_fase"
].update_layout(
    height=450,
    legend_title_text="Tipo de evidencia"
)

# Actualizar las copias exportadas de esta gráfica.

for ruta in RESULTADOS.rglob(
    "evidencias_por_fase.html"
):

    figuras_resumen[
        "evidencias_por_fase"
    ].write_html(ruta)

for ruta in RESULTADOS.rglob(
    "evidencias_por_fase.json"
):

    figuras_resumen[
        "evidencias_por_fase"
    ].write_json(ruta)

# ==========================================================
# 3. ACTUALIZAR INVENTARIO DE NAVEGACIÓN
# ==========================================================

df_inventario_vistas = df_inventario_final.copy()

df_inventario_vistas.to_csv(
    RESULTADOS / "inventario_vistas_dashboard.csv",
    index=False,
    encoding="utf-8-sig"
)

resultados_navegacion_final = []

for nombre, funcion in vistas_dashboard.items():

    componentes = list(
        recorrer_componentes(funcion())
    )

    graficas = sum(
        isinstance(c, dcc.Graph)
        for c in componentes
    )

    esperadas = int(
        df_inventario_final.loc[
            df_inventario_final["Vista"] == nombre,
            "Graficas"
        ].iloc[0]
    )

    assert graficas == esperadas

    resultados_navegacion_final.append({
        "Pestana": nombre,
        "Graficas_esperadas": esperadas,
        "Graficas_recuperadas": graficas,
        "Estado": "OK"
    })

df_pruebas_navegacion = pd.DataFrame(
    resultados_navegacion_final
)

df_pruebas_navegacion.to_csv(
    CARPETA_VALIDACIONES / "pruebas_navegacion.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 4. ACTUALIZAR LAYOUT DEL DASHBOARD
# ==========================================================

app.layout = html.Div([

    encabezado_dashboard,

    dbc.Container([

        navegacion_dashboard,

        dcc.Loading(
            html.Div(
                id="contenido-dashboard",
                children=vista_resumen()
            ),
            type="circle"
        ),

        pie_dashboard

    ], fluid=True, className="px-3 px-lg-4")

], style={
    "backgroundColor": ESTILO_FONDO,
    "minHeight": "100vh",
    "fontFamily": "Arial, sans-serif",
    "color": ESTILO_TEXTO
})

# ==========================================================
# 5. DOCUMENTAR ENTORNO DE EJECUCIÓN
# ==========================================================

paquetes = [
    "pandas",
    "numpy",
    "scipy",
    "scikit-learn",
    "plotly",
    "dash",
    "dash-bootstrap-components",
    "requests"
]

versiones = {
    paquete: version(paquete)
    for paquete in paquetes
}

entorno_final = {
    "Python": platform.python_version(),
    "Sistema_operativo": platform.platform(),
    "Fecha_exportacion": datetime.now(
        ZoneInfo("America/Bogota")
    ).isoformat(),
    "Semilla": SEMILLA,
    "Bibliotecas": versiones
}

(RESULTADOS / "entorno_ejecucion.json").write_text(
    json.dumps(
        entorno_final,
        indent=4,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

(BASE_DASHBOARD / "requirements.txt").write_text(
    "\n".join(
        f"{paquete}=={numero_version}"
        for paquete, numero_version
        in versiones.items()
    ) + "\n",
    encoding="utf-8"
)

# ==========================================================
# 6. VERIFICAR IDENTIDAD DEL DATASET
# ==========================================================

hash_dataset = hashlib.sha256(
    RUTA_CSV.read_bytes()
).hexdigest()

hash_esperado = (
    "a6bcf826782d3c0fbfdcbeead17cd0884"
    "185a0dafe8ff10cd48a874ee7ba18be"
)

assert hash_dataset == hash_esperado

identidad_dataset = {
    "Nombre": "Bike Sharing Dataset",
    "Archivo": "day.csv",
    "DOI": "10.24432/C5W894",
    "Licencia": "CC BY 4.0",
    "Registros": len(df),
    "Variables": df.shape[1],
    "SHA256": hash_dataset,
    "URL": URL_DATASET
}

(RESULTADOS / "identidad_dataset.json").write_text(
    json.dumps(
        identidad_dataset,
        indent=4,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

# ==========================================================
# 7. GENERAR DOCUMENTACIÓN DE REPRODUCIBILIDAD
# ==========================================================

readme_final = """
# BIKE SHARING ANALYTICS

## Dashboard global - Proyecto Integrador

Universidad de La Salle
Maestría en Inteligencia Artificial
Asignatura: Ciencia de Datos
Estudiante: Adriana Patricia Fernández Infante

## Descripción

Dashboard interactivo desarrollado con Python, Dash,
Plotly y Bootstrap para integrar las cuatro fases
del Proyecto Integrador de Ciencia de Datos.

## Componentes

- 5 pestañas de navegación.
- 47 gráficas interactivas.
- 41 tablas interactivas.
- 25 imágenes originales.
- 3 filtros dinámicos.
- 2 callbacks registrados.
- 23 pruebas funcionales automatizadas.

## Dataset

Bike Sharing Dataset - UCI Machine Learning Repository.
Archivo utilizado: day.csv.
731 observaciones diarias.
16 variables originales.
Periodo: 2011-2012.
Licencia: Creative Commons Attribution 4.0 International.

DOI: https://doi.org/10.24432/C5W894

## Reproducción en Google Colab

1. Abrir el notebook principal del dashboard.
2. Conectar un entorno de ejecución.
3. Ejecutar las celdas en orden.
4. Cuando la celda 4 lo solicite, cargar los archivos ZIP
   originales incluidos en evidencias/archivos_originales.
5. Ejecutar las celdas de consolidación e integración.
6. Después de la celda 20, ejecutar nuevamente la celda 17
   para visualizar la versión definitiva del dashboard.

## Archivos requeridos por el notebook

- fase 2 y fase 3.zip
- Evidencias_Fase_4_Bicicletas.zip

## Procedencia de resultados

Fase 1:
EDA reconstruido desde el dataset original debido a
la ausencia del notebook inicial.

Fases 2 y 3:
Resultados recuperados de los notebooks originales.

Fase 4:
Resultados recuperados desde las evidencias originales.

No se reentrenaron modelos durante la consolidación.

## Consideraciones metodológicas

Las métricas de clasificación de las fases 3 y 4
corresponden a diferentes protocolos de partición.

No deben interpretarse como una comparación directa
del desempeño de los modelos.

El umbral de clasificación de Fase 4 fue heredado de
Fase 3, con posible solapamiento de observaciones.

## Disponibilidad de la aplicación

El servidor Dash ejecutado desde Google Colab es temporal.
Para volver a visualizarlo, se debe ejecutar el notebook.

Las gráficas HTML exportadas permiten consultar
visualizaciones individuales fuera de Colab.

## Referencias
"""

readme_final += (
    "\n" + referencia_dataset
    + "\n\n" + referencia_articulo
    + "\n"
)

(BASE_DASHBOARD / "README.md").write_text(
    readme_final.strip(),
    encoding="utf-8"
)

# ==========================================================
# 8. VALIDACIONES FINALES DE LA APLICACIÓN
# ==========================================================

assert len(vistas_dashboard) == 5

assert df_inventario_final["Graficas"].sum() == 47

assert df_inventario_final["Tablas"].sum() == 41

assert df_inventario_final["Imagenes"].sum() == 25

assert len(app.callback_map) == 2

assert len(df_pruebas_filtros) == 18

assert len(df_pruebas_navegacion) == 5

assert int(df["cnt"].sum()) == 3292679

assert inventario_fases[
    "Graficas_interactivas"
].sum() == 39

assert len(figuras_resumen) == 8

with app.server.test_client() as cliente:

    estados_http = {
        ruta: cliente.get(ruta).status_code
        for ruta in [
            "/",
            "/_dash-layout",
            "/_dash-dependencies"
        ]
    }

assert all(
    estado == 200
    for estado in estados_http.values()
)

# ==========================================================
# 9. EXPORTAR INVENTARIO Y VALIDACIONES
# ==========================================================

validacion_final = {
    "Pestanas": 5,
    "Graficas_interactivas": 47,
    "Tablas_interactivas": 41,
    "Imagenes_originales": 25,
    "Componentes_interfaz": int(
        df_inventario_final["Componentes"].sum()
    ),
    "Callbacks": len(app.callback_map),
    "Pruebas_filtros": len(df_pruebas_filtros),
    "Pruebas_navegacion": len(df_pruebas_navegacion),
    "Modelos_reentrenados": 0,
    "Identidad_dataset": "OK",
    "Licencia": "CC BY 4.0",
    "Endpoints": estados_http
}

(RESULTADOS / "validacion_final_dashboard.json").write_text(
    json.dumps(
        validacion_final,
        indent=4,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

# ==========================================================
# 10. GENERAR ZIP DE ENTREGA
# ==========================================================

ruta_exportacion = Path(
    "/content/Dashboard_Global_Bicicletas_Entrega"
)

archivo_final = Path(
    shutil.make_archive(
        str(ruta_exportacion),
        "zip",
        root_dir=BASE_DASHBOARD
    )
)

# Verificar la integridad del archivo ZIP.

with zipfile.ZipFile(archivo_final, "r") as archivo:

    assert archivo.testzip() is None

    contenido_zip = archivo.namelist()

    assert "README.md" in contenido_zip
    assert "requirements.txt" in contenido_zip
    assert "datos/day.csv" in contenido_zip

    assert (
        "resultados/validacion_final_dashboard.json"
        in contenido_zip
    )

    assert (
        "evidencias/archivos_originales/fase 2 y fase 3.zip"
        in contenido_zip
    )

    assert (
        "evidencias/archivos_originales/"
        "Evidencias_Fase_4_Bicicletas.zip"
        in contenido_zip
    )

cantidad_archivos = sum(
    not nombre.endswith("/")
    for nombre in contenido_zip
)

peso_zip_mb = (
    archivo_final.stat().st_size / 1024**2
)

# ==========================================================
# 11. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("DASHBOARD GLOBAL - EXPORTACIÓN FINAL")
print("=" * 60)

print("\n=== INVENTARIO DEFINITIVO ===")
print(df_inventario_final.to_string(index=False))

print("\n=== VALIDACIONES FINALES ===")

for indicador, valor in validacion_final.items():

    print(f"{indicador}: {valor}")

print("\n=== PAQUETE DE ENTREGA ===")

print("Archivo:", archivo_final.name)
print("Cantidad de archivos:", cantidad_archivos)
print("Tamaño MB:", round(peso_zip_mb, 2))
print("Integridad ZIP: OK")
print("README: OK")
print("Requirements: OK")
print("Evidencias originales: OK")
print("Identidad del dataset: OK")
print("Licencia verificada: OK")

print("\nRuta del archivo:")
print(archivo_final)

print("\nExportación finalizada correctamente.")

# ==========================================================
# 12. DESCARGAR PAQUETE DE ENTREGA
# ==========================================================

from google.colab import files

files.download(str(archivo_final))