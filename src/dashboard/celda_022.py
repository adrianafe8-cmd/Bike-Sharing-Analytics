# ==========================================================
# DASHBOARD GLOBAL - CELDA 21
# Visualización definitiva del dashboard
# ==========================================================

print("=" * 60)
print("BIKE SHARING ANALYTICS")
print("Dashboard Global - Proyecto Integrador")
print("Universidad de La Salle")
print("Maestría en Inteligencia Artificial")
print("=" * 60)

print("\nVersión definitiva del dashboard")
print("Pestañas: 5")
print("Gráficas interactivas: 47")
print("Tablas interactivas: 41")
print("Imágenes originales: 25")
print("Pruebas funcionales: 23/23")
print("\nIniciando aplicación Dash...\n")

app.run(
    jupyter_mode="inline",
    jupyter_height=1200,
    port=8050,
    debug=False
)