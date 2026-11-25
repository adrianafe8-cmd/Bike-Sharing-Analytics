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

Fanaee-T, H. (2013). Bike Sharing Dataset [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894

Fanaee-T, H., & Gama, J. (2013). Event labeling combining ensemble detectors and background knowledge. Progress in Artificial Intelligence. https://doi.org/10.1007/s13748-013-0040-3