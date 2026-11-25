# Validación experimental de reproducibilidad

## Entorno

- Python 3.13.18.
- R 4.6.1.
- Linux mediante Google Colab.
- Entorno virtual Python aislado.

## Resultados

- 21 dependencias verificadas.
- Cinco notebooks ejecutados correctamente.
- 93 celdas ejecutadas.
- 67 comparaciones equivalentes.
- 12 variables de importancia verificadas.
- Notebooks fuente conservados.

## Incidencias y soluciones

1. Error de ensurepip: se utilizó virtualenv.

2. Configuración heredada de Google Colab:
   se aisló la configuración del kernel y se
   desactivaron las extensiones heredadas.

3. Archivos anteriores del dashboard:
   se respaldaron los resultados y se ejecutó
   nuevamente desde una carpeta limpia.

4. Diferencias en el orden de variables:
   se compararon los valores por identificador
   y se confirmó su equivalencia.

## Alcance

La validación demuestra la ejecución integral
en el entorno evaluado y la equivalencia de
los resultados seleccionados.

No implica identidad binaria de todos los archivos
ni validación en otros sistemas operativos.

## Tolerancias

- Relativa: 1e-6.
- Absoluta: 1e-8.
