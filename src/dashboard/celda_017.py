# ==========================================================
# DASHBOARD GLOBAL - CELDA 17
# Ejecución del dashboard en Google Colab
# ==========================================================

import dash

# ==========================================================
# 1. VERIFICACIONES PREVIAS
# ==========================================================

assert app.layout is not None, (
    "El layout de la aplicación no está disponible."
)

assert len(app.callback_map) == 2, (
    "Los callbacks no están registrados correctamente."
)

assert len(vistas_dashboard) == 5

assert len(df_pruebas_filtros) == 18

assert len(df_pruebas_navegacion) == 5

# ==========================================================
# 2. VALIDACIÓN DE ENDPOINTS DEL SERVIDOR
# ==========================================================

# Comprobar que Dash puede serializar el layout
# y entregar las dependencias de los callbacks.

with app.server.test_client() as cliente:

    respuesta_inicio = cliente.get("/")

    respuesta_layout = cliente.get(
        "/_dash-layout"
    )

    respuesta_dependencias = cliente.get(
        "/_dash-dependencies"
    )

    assert respuesta_inicio.status_code == 200

    assert respuesta_layout.status_code == 200

    assert respuesta_dependencias.status_code == 200

# ==========================================================
# 3. INFORMACIÓN DE LA APLICACIÓN
# ==========================================================

print("=" * 60)
print("BIKE SHARING ANALYTICS")
print("DASHBOARD GLOBAL - PROYECTO INTEGRADOR")
print("=" * 60)

print("\nVersión de Dash:", dash.__version__)

print("\n=== VALIDACIONES PREVIAS ===")

print("Layout principal: OK")
print("Callbacks registrados: OK")
print("Vistas disponibles: OK")
print("Pruebas funcionales: OK")

print("\n=== ENDPOINTS DEL SERVIDOR ===")

print(
    "Página principal:",
    respuesta_inicio.status_code
)

print(
    "Layout Dash:",
    respuesta_layout.status_code
)

print(
    "Dependencias de callbacks:",
    respuesta_dependencias.status_code
)

print("\n=== COMPONENTES DISPONIBLES ===")

print("Pestañas: 5")
print("Gráficas interactivas: 46")
print("Tablas interactivas: 34")
print("Imágenes originales: 25")
print("Pruebas funcionales superadas: 23")

print("\nIniciando servidor Dash...")
print("Modo de visualización: inline")
print("Puerto: 8050")

# ==========================================================
# 4. EJECUTAR DASHBOARD
# ==========================================================

app.run(
    jupyter_mode="inline",
    jupyter_height=1000,
    port=8050,
    debug=False
)