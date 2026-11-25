# Bike Sharing Analytics

## Proyecto integrador de Ciencia de Datos

- Universidad de La Salle
- Maestría en Inteligencia Artificial
- Autora: Adriana Patricia Fernández Infante
- Año: 2026

## Descripción

Proyecto orientado al análisis, modelado y visualización
de la demanda diaria de alquiler de bicicletas mediante
Python, R, Dash, Plotly y aprendizaje automático.

## Dashboard interactivo

[Consultar dashboard publicado](https://adrianafe8-cmd.github.io/Bike-Sharing-Analytics/dashboard/index.html)

## Objetivo general

Analizar los patrones de demanda del sistema de bicicletas
compartidas y evaluar modelos estadísticos y de aprendizaje
automático para apoyar la toma de decisiones.

## Dataset

- Nombre: Bike Sharing Dataset.
- Fuente: UCI Machine Learning Repository.
- Archivo: day.csv.
- Registros: 731.
- Variables: 16.
- Periodo: 2011-2012.
- Valores faltantes: 0.
- Registros duplicados: 0.
- DOI: https://doi.org/10.24432/C5W894
- Fuente: https://archive.ics.uci.edu/dataset/275/bike-sharing-dataset

## Fases del proyecto

| Fase | Descripción |
|---|---|
| 1 | Análisis exploratorio y estadístico |
| 2 | Regresión simple y múltiple en Python y R |
| 3 | Modelado avanzado, clasificación y clustering |
| 4 | Preprocesamiento y modelos baseline |
| Dashboard | Integración y visualización interactiva |

## Resultados destacados

- 3.292.679 alquileres registrados.
- Crecimiento anual de la demanda: 64,88 %.
- 47 gráficas interactivas.
- 41 tablas de resultados.
- 25 imágenes de evidencia.
- Cinco vistas principales del dashboard.

## Estructura del repositorio

    Bike-Sharing-Analytics/
        data/
        notebooks/
            evidencias/
            reproducibles/
        src/
        dashboard/
            index.html
        results/
        docs/
        requirements.txt
        requirements-lock.txt
        verificar_proyecto.py
        README.md
        .nojekyll

| Directorio | Contenido |
|---|---|
| data | Dataset |
| notebooks | Notebooks originales y reproducibles |
| src | Código fuente y utilidades |
| dashboard | Dashboard HTML |
| results | Resultados y evidencias |
| docs | Documentación técnica |

## Requisitos de ejecución

- Python 3.13.18.
- R 4.6.1.
- Linux.
- 21 dependencias Python con versiones exactas.

El entorno fue validado mediante Google Colab.
R debe estar instalado previamente en el sistema operativo.
rpy2 puede requerir bibliotecas de desarrollo de R.

## Instalación

Ejecutar los siguientes comandos desde una terminal:

    git clone https://github.com/adrianafe8-cmd/Bike-Sharing-Analytics.git
    cd Bike-Sharing-Analytics
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    python -m pip check
    python verificar_proyecto.py

Si venv presenta problemas con ensurepip, utilizar
virtualenv como alternativa, tal como se hizo en Colab.

El archivo requirements-lock.txt contiene las versiones
registradas mediante pip freeze.

## Ejecución de notebooks

Los notebooks reproducibles se encuentran en
notebooks/reproducibles/.

Orden de ejecución:

1. 01_EDA_Bicicletas_Reconstruido.ipynb
2. 02_Regresion_Bicicletas_Reproducible.ipynb
3. 03_Modelado_Avanzado_Reproducible.ipynb
4. 04_Preprocesamiento_Reproducible.ipynb
5. 05_Dashboard_Global_Reproducible.ipynb

Para utilizar JupyterLab, instalarlo adicionalmente:

    python -m pip install jupyterlab
    python -m ipykernel install --user --name bike-sharing
    jupyter lab

Seleccionar el kernel bike-sharing y ejecutar cada
notebook desde el inicio.

Antes de regenerar el dashboard, respaldar y retirar
results/reproduccion/dashboard si existe, para evitar
interferencias de archivos anteriores.

## Reproducibilidad experimental

| Indicador | Resultado |
|---|---|
| Dependencias verificadas | 21/21 |
| Conflictos de dependencias | 0 |
| Notebooks ejecutados en entorno aislado | 5/5 |
| Celdas ejecutadas | 93/93 |
| Comparaciones equivalentes | 67/67 |
| Equivalencia de resultados evaluados | 100 % |
| Variables de importancia verificadas | 12/12 |

Tolerancias numéricas:

- Relativa: 1e-6.
- Absoluta: 1e-8.

La diferencia inicial en una tabla de importancia
de variables correspondió al orden de presentación.
La comparación por variable confirmó la equivalencia
de los valores reportados.

## Evidencias de validación

- docs/validacion_entorno_limpio.json
- docs/ejecucion_entorno_limpio.csv
- docs/resumen_ejecucion_entorno_limpio.json
- docs/equivalencia_final_entorno_limpio.json
- docs/comparacion_final_entorno_limpio.csv
- docs/validacion_importancia_entorno_limpio.csv

## Consideraciones metodológicas

- La fase 1 reproducible corresponde a una reconstrucción
  del análisis exploratorio.
- Los notebooks originales disponibles se conservan
  como evidencia.
- El dashboard integra resultados históricos y no
  reentrena los modelos.
- R utiliza la instalación del sistema anfitrión.
- La equivalencia del 100 % corresponde a las
  67 comparaciones evaluadas.
- No se afirma identidad binaria de todos los archivos.
- Los protocolos de partición temporal y aleatoria
  limitan la comparación directa entre modelos.
- La versión HTML no reproduce necesariamente todas
  las funcionalidades del servidor Dash.
- La ejecución en Windows no fue validada.

## Referencia

Fanaee-T, H. (2013). Bike Sharing Dataset.
UCI Machine Learning Repository.
https://doi.org/10.24432/C5W894


## Optimización de la publicación

La versión pública excluye respaldos redundantes
y archivos HTML individuales regenerables.

Se conservan el dashboard principal, los notebooks,
los datos, el código fuente, las evidencias originales
y los resultados de validación.

Los archivos HTML individuales pueden regenerarse
mediante los notebooks reproducibles.

El directorio Dashboard conserva la compatibilidad
con el enlace publicado inicialmente.
