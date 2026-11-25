
from pathlib import Path
import sys
import time
import json
import hashlib
import nbformat
import pandas as pd

from nbclient import NotebookClient

REPO = Path(sys.argv[1])
ENTORNO = Path(sys.argv[2])

DOCS = REPO / "docs"
NOTEBOOKS = REPO / "notebooks/reproducibles"
DESTINO = REPO / "results/validacion/entorno_limpio"

assert Path(sys.prefix) == ENTORNO
assert sys.prefix != sys.base_prefix

print("Python utilizado:", sys.executable, flush=True)
print("Entorno aislado:", sys.prefix, flush=True)

configuracion = [
    ("fase1", "01_EDA_Bicicletas_Reconstruido.ipynb"),
    ("fase2", "02_Regresion_Bicicletas_Reproducible.ipynb"),
    ("fase3", "03_Modelado_Avanzado_Reproducible.ipynb"),
    ("fase4", "04_Preprocesamiento_Reproducible.ipynb"),
    ("dashboard", "05_Dashboard_Global_Reproducible.ipynb")
]

resultados = []

for fase, nombre in configuracion:

    print("\n" + "=" * 60, flush=True)
    print("EJECUTANDO:", fase.upper(), flush=True)
    print("=" * 60, flush=True)

    ruta = NOTEBOOKS / nombre

    assert ruta.exists(), ruta

    hash_antes = hashlib.sha256(
        ruta.read_bytes()
    ).hexdigest()

    nb = nbformat.read(ruta, as_version=4)

    # Verificar desde el propio kernel que se utiliza
    # realmente el entorno virtual seleccionado.
    celda_control = nbformat.v4.new_code_cell(
        "import sys\n"
        "from pathlib import Path\n"
        f"assert Path(sys.prefix) == Path({str(ENTORNO)!r})\n"
        "print('Kernel aislado confirmado:', sys.executable)"
    )

    nb.cells.insert(0, celda_control)

    inicio = time.perf_counter()

    estado = "OK"
    error = None

    try:

        cliente = NotebookClient(
            nb,
            timeout=1200,
            kernel_name="bike_sharing_limpio",
            allow_errors=False,
            resources={
                "metadata": {
                    "path": str(REPO)
                }
            }
        )

        cliente.execute()

    except Exception as e:

        estado = "ERROR"
        error = str(e)[-6000:]

    duracion = round(
        time.perf_counter() - inicio, 2
    )

    celdas = [
        c for c in nb.cells[1:]
        if c.cell_type == "code"
    ]

    ejecutadas = sum(
        c.execution_count is not None
        for c in celdas
    )

    errores = [
        {
            "tipo": s.get("ename"),
            "mensaje": s.get("evalue")
        }
        for c in nb.cells
        if c.cell_type == "code"
        for s in c.get("outputs", [])
        if s.get("output_type") == "error"
    ]

    hash_despues = hashlib.sha256(
        ruta.read_bytes()
    ).hexdigest()

    ruta_evidencia = (
        DESTINO / f"{fase}_entorno_limpio.ipynb"
    )

    nbformat.write(nb, ruta_evidencia)

    registro = {
        "fase": fase,
        "notebook": nombre,
        "estado": estado,
        "duracion_segundos": duracion,
        "celdas_codigo": len(celdas),
        "celdas_ejecutadas": ejecutadas,
        "notebook_fuente_conservado": (
            hash_antes == hash_despues
        ),
        "kernel_aislado_verificado": (
            estado == "OK"
        ),
        "errores": errores,
        "detalle_error": error,
        "evidencia": str(
            ruta_evidencia.relative_to(REPO)
        )
    }

    resultados.append(registro)

    print("Estado:", estado, flush=True)
    print("Duración:", duracion, "s", flush=True)
    print(
        "Celdas ejecutadas:",
        ejecutadas, "/", len(celdas),
        flush=True
    )

    if error:
        print(error, flush=True)

    # Guardar resultados después de cada notebook.
    (
        DOCS / "ejecucion_entorno_limpio.json"
    ).write_text(
        json.dumps(
            resultados,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

df = pd.DataFrame(resultados)

columnas = [
    "fase",
    "estado",
    "duracion_segundos",
    "celdas_codigo",
    "celdas_ejecutadas",
    "kernel_aislado_verificado",
    "notebook_fuente_conservado"
]

df[columnas].to_csv(
    DOCS / "ejecucion_entorno_limpio.csv",
    index=False
)

print("\n=== RESUMEN DE EJECUCIÓN ===", flush=True)

print(
    df[columnas].to_string(index=False),
    flush=True
)

exitosos = sum(
    r["estado"] == "OK"
    for r in resultados
)

resumen = {
    "notebooks_evaluados": len(resultados),
    "notebooks_exitosos": exitosos,
    "notebooks_con_error": len(resultados) - exitosos,
    "celdas_codigo": sum(
        r["celdas_codigo"] for r in resultados
    ),
    "celdas_ejecutadas": sum(
        r["celdas_ejecutadas"] for r in resultados
    ),
    "kernels_aislados_verificados": all(
        r["kernel_aislado_verificado"]
        for r in resultados
    ),
    "notebooks_fuente_conservados": all(
        r["notebook_fuente_conservado"]
        for r in resultados
    ),
    "ejecucion_notebooks_entorno_limpio": (
        exitosos == len(configuracion)
        and all(
            r["celdas_codigo"] == r["celdas_ejecutadas"]
            and not r["errores"]
            and r["notebook_fuente_conservado"]
            for r in resultados
        )
    ),
    "equivalencia_metricas_entorno_limpio_validada": False
}

(
    DOCS / "resumen_ejecucion_entorno_limpio.json"
).write_text(
    json.dumps(
        resumen,
        indent=4,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print("\n=== VALIDACIÓN FINAL ===", flush=True)

for clave, valor in resumen.items():
    print(f"{clave}: {valor}", flush=True)
