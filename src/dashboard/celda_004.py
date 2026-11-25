
# ==========================================================
# DASHBOARD GLOBAL - CELDA 4
# Consolidación de evidencias de las fases anteriores
# ==========================================================

from google.colab import files
import zipfile
import shutil
import io

# 1. Definir los archivos requeridos

archivos_requeridos = {
    "fase 2 y fase 3.zip": "Fases_2_3",
    "Evidencias_Fase_4_Bicicletas.zip": "Fase_4"
}

# 2. Crear directorio para almacenar los ZIP originales

CARPETA_ZIP = EVIDENCIAS / "archivos_originales"
CARPETA_ZIP.mkdir(parents=True, exist_ok=True)

# 3. Solicitar únicamente los archivos que no existan

faltantes = [
    nombre
    for nombre in archivos_requeridos
    if not (CARPETA_ZIP / nombre).exists()
]

if faltantes:

    print("Selecciona los siguientes archivos ZIP:")

    for nombre in faltantes:
        print("-", nombre)

    archivos_cargados = files.upload()

    for nombre, contenido in archivos_cargados.items():

        if nombre in archivos_requeridos:

            ruta = CARPETA_ZIP / nombre
            ruta.write_bytes(contenido)

            print("Archivo almacenado:", nombre)

        else:
            print("Archivo no reconocido:", nombre)

# 4. Verificar disponibilidad de archivos

for nombre in archivos_requeridos:

    assert (CARPETA_ZIP / nombre).exists(), (
        f"No se encontró el archivo requerido: {nombre}"
    )

# 5. Extraer las evidencias por fase

inventario = []

for nombre, carpeta in archivos_requeridos.items():

    ruta_zip = CARPETA_ZIP / nombre

    destino = EVIDENCIAS / carpeta
    destino.mkdir(parents=True, exist_ok=True)

    assert zipfile.is_zipfile(ruta_zip), (
        f"Archivo ZIP inválido: {nombre}"
    )

    with zipfile.ZipFile(ruta_zip, "r") as archivo:

        # Verificar integridad del ZIP

        assert archivo.testzip() is None, (
            f"Archivo ZIP corrupto: {nombre}"
        )

        # Extraer archivos

        archivo.extractall(destino)

    # 6. Construir inventario de evidencias

    for ruta in sorted(destino.rglob("*")):

        if ruta.is_file():

            inventario.append({
                "Grupo": carpeta,
                "Archivo": ruta.name,
                "Formato": ruta.suffix.lower(),
                "Tamaño_KB": round(
                    ruta.stat().st_size / 1024, 2
                ),
                "Ruta": str(ruta)
            })

# 7. Consolidar inventario

df_inventario = pd.DataFrame(inventario)

assert not df_inventario.empty, (
    "No se encontraron archivos de evidencia."
)

# 8. Resumen por grupo y formato

resumen_evidencias = pd.crosstab(
    df_inventario["Grupo"],
    df_inventario["Formato"],
    margins=True,
    margins_name="Total"
)

# 9. Guardar inventario

df_inventario.to_csv(
    RESULTADOS / "inventario_evidencias.csv",
    index=False
)

# 10. Presentar resultados

print("\n" + "=" * 60)
print("DASHBOARD GLOBAL - INVENTARIO DE EVIDENCIAS")
print("=" * 60)

print("Archivos ZIP procesados:",
      len(archivos_requeridos))

print("Total de archivos extraídos:",
      len(df_inventario))

print("\n=== RESUMEN POR GRUPO Y FORMATO ===")

display(resumen_evidencias)

print("\n=== NOTEBOOKS DISPONIBLES ===")

display(
    df_inventario.loc[
        df_inventario["Formato"] == ".ipynb",
        ["Grupo", "Archivo", "Tamaño_KB"]
    ]
)

print("\n=== INFORMES DISPONIBLES ===")

display(
    df_inventario.loc[
        df_inventario["Formato"].isin([".pdf", ".docx"]),
        ["Grupo", "Archivo", "Tamaño_KB"]
    ]
)

print("\n=== ARCHIVOS CSV DISPONIBLES ===")

display(
    df_inventario.loc[
        df_inventario["Formato"] == ".csv",
        ["Grupo", "Archivo", "Tamaño_KB"]
    ]
)

print("\nInventario guardado correctamente.")
print("Consolidación de evidencias finalizada.")
