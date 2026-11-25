# ==========================================================
# DASHBOARD GLOBAL - CELDA 22
# Exportación a HTML autónomo e interactivo
# ==========================================================

import json
import html as html_lib
import re
from pathlib import Path
from collections import Counter
from plotly.utils import PlotlyJSONEncoder
from plotly.offline import get_plotlyjs
from google.colab import files

# ==========================================================
# 1. CONFIGURACIÓN
# ==========================================================

RUTA_HTML = Path("/content/Bike_Sharing_Analytics.html")

nombres_pestanas = {
    "resumen": "Resumen ejecutivo",
    "fase1": "Fase 1 - Análisis exploratorio",
    "fase2": "Fase 2 - Regresión",
    "fase3": "Fase 3 - Modelado avanzado",
    "fase4": "Fase 4 - Preprocesamiento"
}

contador_html = Counter()
graficas_html = {}
tablas_html = {}

def escapar(valor):
    return html_lib.escape(str(valor), quote=True)

def serializar(objeto):
    return json.dumps(
        objeto,
        cls=PlotlyJSONEncoder,
        ensure_ascii=False
    ).replace("</", "<\\/")

# ==========================================================
# 2. CONVERTIR COMPONENTES DASH A HTML
# ==========================================================

def convertir_componente(componente):

    if componente is None:
        return ""

    if isinstance(componente, (str, int, float)):
        return escapar(componente)

    if isinstance(componente, (list, tuple)):
        return "".join(
            convertir_componente(c)
            for c in componente
        )

    if not hasattr(componente, "to_plotly_json"):
        return escapar(componente)

    informacion = componente.to_plotly_json()
    tipo = informacion["type"]
    props = informacion.get("props", {})

    hijos = props.get("children", "")
    identificador = props.get("id", "")

    # Gráficas Plotly
    if tipo == "Graph":

        contador_html["graficas"] += 1

        gid = (
            identificador
            if isinstance(identificador, str)
            and identificador
            else f"grafica-{contador_html['graficas']}"
        )

        figura = props.get("figure", {})

        if hasattr(figura, "to_plotly_json"):
            figura = figura.to_plotly_json()

        graficas_html[gid] = figura

        return (
            f'<div class="graph-card">'
            f'<div class="plot" id="{escapar(gid)}"></div>'
            f'</div>'
        )

    # Tablas interactivas
    if tipo == "DataTable":

        contador_html["tablas"] += 1

        tid = f"tabla-{contador_html['tablas']}"

        tablas_html[tid] = {
            "columnas": props.get("columns", []),
            "datos": props.get("data", []),
            "pagina": props.get("page_size", 10) or 10
        }

        return f"""
        <div class="table-card" id="{tid}">
            <input type="search"
                   placeholder="Buscar en la tabla..."
                   oninput="filtrarTabla('{tid}', this.value)">
            <div class="table-scroll">
                <table></table>
            </div>
            <div class="pagination"></div>
        </div>
        """

    # Imágenes originales
    if tipo == "Img":

        contador_html["imagenes"] += 1

        src = props.get("src", "")
        alt = props.get("alt", "Evidencia original")

        return (
            f'<img class="evidencia" '
            f'src="{escapar(src)}" '
            f'alt="{escapar(alt)}" loading="lazy">'
        )

    # Los filtros originales se sustituyen por controles JS.
    if identificador in [
        "filtro-anio",
        "filtro-usuario",
        "filtro-granularidad"
    ]:
        return ""

    if identificador == "kpis-filtrados":
        return '<div id="kpis-filtrados"></div>'

    # Secciones desplegables
    if tipo == "AccordionItem":

        titulo = escapar(
            props.get("title", "Consultar información")
        )

        return (
            f"<details><summary>{titulo}</summary>"
            f"{convertir_componente(hijos)}</details>"
        )

    if tipo == "Accordion":
        return convertir_componente(hijos)

    # Hipervínculos
    if tipo in ["A", "Link"]:

        href = escapar(props.get("href", "#"))

        return (
            f'<a href="{href}" target="_blank" '
            f'rel="noopener noreferrer">'
            f'{convertir_componente(hijos)}</a>'
        )

    # Componentes estructurales
    etiquetas = {
        "H1": "h1",
        "H2": "h2",
        "H3": "h3",
        "H4": "h4",
        "H5": "h5",
        "H6": "h6",
        "P": "p",
        "Span": "span",
        "Strong": "strong",
        "B": "strong",
        "Small": "small",
        "Ul": "ul",
        "Ol": "ol",
        "Li": "li",
        "Pre": "pre",
        "Code": "code",
        "Label": "label",
        "Markdown": "div"
    }

    if tipo == "Br":
        return "<br>"

    if tipo == "Hr":
        return "<hr>"

    etiqueta = etiquetas.get(tipo, "div")

    clases = {
        "Row": "layout-row",
        "Col": "layout-col",
        "Card": "card",
        "CardBody": "card-body",
        "CardHeader": "card-header",
        "Alert": "alert",
        "Badge": "badge"
    }

    clase = clases.get(tipo, "")

    # Conservar estilos visuales relevantes
    estilos = props.get("style", {}) or {}

    estilos_permitidos = {
        "color",
        "backgroundColor",
        "fontSize",
        "fontWeight",
        "textAlign",
        "padding",
        "marginBottom",
        "borderRadius"
    }

    css = []

    for clave, valor in estilos.items():

        if clave in estilos_permitidos:

            clave_css = re.sub(
                r"([A-Z])",
                lambda m: "-" + m.group(1).lower(),
                clave
            )

            if isinstance(valor, (int, float)):

                if clave != "fontWeight":
                    valor = f"{valor}px"

            css.append(f"{clave_css}:{valor}")

    estilo = escapar(";".join(css))

    # Ajustar distribución de columnas Bootstrap
    if tipo == "Col":

        ancho = props.get(
            "lg",
            props.get("md", 12)
        )

        if isinstance(ancho, int):
            clase += f" col-{ancho}"

    return (
        f'<{etiqueta} class="{clase}" style="{estilo}">'
        f'{convertir_componente(hijos)}'
        f'</{etiqueta}>'
    )

# ==========================================================
# 3. RECUPERAR LAS CINCO VISTAS
# ==========================================================

contenido_vistas = {}

for nombre, funcion in vistas_dashboard.items():

    contenido_vistas[nombre] = convertir_componente(
        funcion()
    )

print("Vistas recuperadas:", len(contenido_vistas))
print("Gráficas recuperadas:", contador_html["graficas"])
print("Tablas recuperadas:", contador_html["tablas"])
print("Imágenes recuperadas:", contador_html["imagenes"])

assert len(contenido_vistas) == 5
assert contador_html["graficas"] == 47
assert contador_html["tablas"] == 41
assert contador_html["imagenes"] == 25
assert len(graficas_html) == 47

# ==========================================================
# 4. PREPARAR DATOS PARA FILTROS JAVASCRIPT
# ==========================================================

datos_filtros = df[
    ["dteday", "cnt", "casual", "registered"]
].copy()

datos_filtros["dteday"] = (
    datos_filtros["dteday"].dt.strftime("%Y-%m-%d")
)

datos_json = serializar(
    datos_filtros.to_dict("records")
)

assert len(datos_filtros) == 731

# ==========================================================
# 5. CONTROLES INTERACTIVOS
# ==========================================================

controles_html = """
<div class="filter-panel">

    <div>
        <label>Año</label>
        <select id="anio-html" onchange="actualizarDemanda()">
            <option value="todos">Todos los años</option>
            <option value="2011">2011</option>
            <option value="2012">2012</option>
        </select>
    </div>

    <div>
        <label>Tipo de usuario</label>
        <select id="usuario-html"
                onchange="actualizarDemanda()">
            <option value="cnt">Todos los usuarios</option>
            <option value="casual">Casuales</option>
            <option value="registered">Registrados</option>
        </select>
    </div>

    <div>
        <label>Granularidad</label>
        <select id="granularidad-html"
                onchange="actualizarDemanda()">
            <option value="mensual">Mensual</option>
            <option value="diaria">Diaria</option>
        </select>
    </div>

    <button onclick="restablecerFiltros()">
        Restablecer filtros
    </button>

</div>
"""

# ==========================================================
# 6. DISEÑO VISUAL DEL DASHBOARD
# ==========================================================

css_dashboard = """
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #F1F5F9;
    color: #334155;
}

header {
    background: #142C49;
    color: white;
    padding: 32px 5%;
}

header h1 {
    margin: 0 0 10px;
    font-size: 32px;
}

header p {
    color: #CBD5E1;
    margin: 5px 0;
}

nav {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 18px 3%;
    background: white;
    border-bottom: 1px solid #CBD5E1;
    position: sticky;
    top: 0;
    z-index: 100;
}

nav button {
    border: none;
    padding: 12px 16px;
    border-radius: 7px;
    background: #E2E8F0;
    color: #142C49;
    cursor: pointer;
    font-weight: bold;
}

nav button.active {
    background: #2563EB;
    color: white;
}

main {
    max-width: 1700px;
    margin: auto;
    padding: 24px;
}

.tab-panel {
    display: none;
}

.tab-panel.active {
    display: block;
}

.layout-row {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 16px;
}

.layout-col {
    flex: 1 1 220px;
    min-width: 0;
}

.col-12 {
    flex: 1 1 100%;
}

.col-6 {
    flex: 1 1 calc(50% - 16px);
}

.col-4 {
    flex: 1 1 calc(33.33% - 16px);
}

.col-3 {
    flex: 1 1 calc(25% - 16px);
}

.card, .graph-card, .table-card {
    background: white;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px #142C490D;
    margin-bottom: 16px;
    overflow: hidden;
}

.card-body {
    padding: 18px;
}

.card-header {
    padding: 14px;
    font-weight: bold;
    background: #F8FAFC;
}

.graph-card {
    padding: 10px;
}

.plot {
    width: 100%;
    height: 450px;
}

.alert {
    background: #E0F2FE;
    border-left: 4px solid #0284C7;
    padding: 16px;
    border-radius: 8px;
    margin: 15px 0;
}

.filter-panel {
    display: flex;
    flex-wrap: wrap;
    align-items: end;
    gap: 18px;
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
}

.filter-panel > div {
    flex: 1 1 180px;
}

label {
    display: block;
    font-weight: bold;
    margin-bottom: 6px;
}

select, input {
    padding: 10px;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    width: 100%;
    background: white;
    color: #334155;
}

button {
    cursor: pointer;
}

.filter-panel button, .pagination button {
    background: #142C49;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 6px;
}

button:disabled {
    opacity: 0.4;
    cursor: default;
}

.kpi-grid {
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
    margin: 18px 0;
}

.kpi {
    padding: 20px;
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}

.kpi strong {
    display: block;
    color: #2563EB;
    font-size: 27px;
    margin-top: 8px;
}

details {
    background: white;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    margin: 10px 0;
    padding: 15px;
}

summary {
    font-weight: bold;
    color: #142C49;
    cursor: pointer;
    padding: 8px;
}

.table-card {
    padding: 15px;
}

.table-scroll {
    overflow-x: auto;
    margin-top: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

th, td {
    border-bottom: 1px solid #E2E8F0;
    padding: 10px;
    text-align: left;
}

th {
    background: #142C49;
    color: white;
    cursor: pointer;
}

tr:nth-child(even) {
    background: #F8FAFC;
}

.pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    gap: 10px;
}

.evidencia {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 15px auto;
    border-radius: 8px;
}

footer {
    padding: 25px;
    text-align: center;
    background: #142C49;
    color: #CBD5E1;
    font-size: 13px;
}

@media (max-width: 900px) {
    .layout-col {
        flex: 1 1 100%;
    }

    main {
        padding: 12px;
    }
}
"""

# ==========================================================
# 7. JAVASCRIPT: NAVEGACIÓN, GRÁFICAS Y TABLAS
# ==========================================================

javascript_dashboard = """
const formato = new Intl.NumberFormat('es-CO');
const estadoTablas = {};
const graficasRenderizadas = new Set();

function abrirPestana(nombre) {

    document.querySelectorAll('.tab-panel')
        .forEach(p => p.classList.remove('active'));

    document.querySelectorAll('nav button')
        .forEach(b => b.classList.remove('active'));

    const panel = document.getElementById('panel-' + nombre);

    panel.classList.add('active');

    document.getElementById('btn-' + nombre)
        .classList.add('active');

    renderizarPanel(panel);

    window.scrollTo({top: 0, behavior: 'instant'});
}

function renderizarPanel(panel) {

    panel.querySelectorAll('.plot').forEach(elemento => {

        if (elemento.offsetWidth === 0) return;

        const id = elemento.id;
        const figura = GRAFICAS[id];

        if (!figura) return;

        if (!graficasRenderizadas.has(id)) {

            const layout = {
                ...figura.layout,
                autosize: true,
                height: 450
            };

            delete layout.width;

            graficasRenderizadas.add(id);

            Plotly.newPlot(
                elemento,
                figura.data || [],
                layout,
                {
                    responsive: true,
                    displaylogo: false,
                    scrollZoom: false,
                    toImageButtonOptions: {
                        format: 'png',
                        scale: 2
                    }
                }
            ).then(() => {

                if (id === 'grafica-demanda-filtrada') {
                    actualizarDemanda();
                }

            }).catch(error => {
                graficasRenderizadas.delete(id);
                console.error(error);
            });

        } else if (elemento._fullLayout) {

            Plotly.Plots.resize(elemento);
        }
    });

    panel.querySelectorAll('.table-card')
        .forEach(elemento => {

            if (!estadoTablas[elemento.id]) {

                estadoTablas[elemento.id] = {
                    pagina: 0,
                    filtro: '',
                    columna: null,
                    ascendente: true
                };

                renderizarTabla(elemento.id);
            }
        });
}

function renderizarTabla(id) {

    const info = TABLAS[id];
    const estado = estadoTablas[id];
    const contenedor = document.getElementById(id);

    if (!info || !estado || !contenedor) return;

    let datos = info.datos.filter(fila =>
        Object.values(fila).some(valor =>
            String(valor ?? '').toLowerCase()
                .includes(estado.filtro.toLowerCase())
        )
    );

    if (estado.columna !== null) {

        datos.sort((a, b) => {

            const x = a[estado.columna];
            const y = b[estado.columna];

            let resultado;

            if (typeof x === 'number'
                && typeof y === 'number') {

                resultado = x - y;

            } else {

                resultado = String(x ?? '')
                    .localeCompare(
                        String(y ?? ''),
                        'es',
                        {numeric: true}
                    );
            }

            return estado.ascendente
                ? resultado
                : -resultado;
        });
    }

    const tamano = info.pagina;
    const paginas = Math.max(
        1, Math.ceil(datos.length / tamano)
    );

    estado.pagina = Math.min(
        estado.pagina, paginas - 1
    );

    const inicio = estado.pagina * tamano;

    const tabla = contenedor.querySelector('table');

    tabla.replaceChildren();

    const cabecera = tabla.createTHead().insertRow();

    info.columnas.forEach(columna => {

        const th = document.createElement('th');

        th.textContent = columna.name;

        th.onclick = () => {

            if (estado.columna === columna.id) {
                estado.ascendente = !estado.ascendente;
            } else {
                estado.columna = columna.id;
                estado.ascendente = true;
            }

            estado.pagina = 0;

            renderizarTabla(id);
        };

        cabecera.appendChild(th);
    });

    const cuerpo = tabla.createTBody();

    datos.slice(inicio, inicio + tamano)
        .forEach(fila => {

            const tr = cuerpo.insertRow();

            info.columnas.forEach(columna => {

                const td = tr.insertCell();

                td.textContent = fila[columna.id] ?? '';
            });
        });

    const paginacion = contenedor.querySelector('.pagination');

    paginacion.innerHTML = `
        <button onclick="cambiarPagina('${id}', -1)"
            ${estado.pagina === 0 ? 'disabled' : ''}>
            Anterior
        </button>

        <span>
            Página ${estado.pagina + 1} de ${paginas}
            | ${datos.length} registros
        </span>

        <button onclick="cambiarPagina('${id}', 1)"
            ${estado.pagina >= paginas - 1 ? 'disabled' : ''}>
            Siguiente
        </button>
    `;
}

function filtrarTabla(id, texto) {

    estadoTablas[id].filtro = texto;
    estadoTablas[id].pagina = 0;

    renderizarTabla(id);
}

function cambiarPagina(id, cambio) {

    estadoTablas[id].pagina = Math.max(
        0, estadoTablas[id].pagina + cambio
    );

    renderizarTabla(id);
}

// ========================================================
// FILTROS DE DEMANDA
// ========================================================

function actualizarDemanda() {

    const anio = document.getElementById('anio-html').value;

    const usuario =
        document.getElementById('usuario-html').value;

    const granularidad =
        document.getElementById('granularidad-html').value;

    const filtrados = DATOS.filter(fila =>
        anio === 'todos'
        || fila.dteday.startsWith(anio)
    );

    const total = filtrados.reduce(
        (suma, fila) => suma + Number(fila[usuario]), 0
    );

    const promedio = total / filtrados.length;

    const totalGlobal = DATOS.reduce(
        (suma, fila) => suma + Number(fila.cnt), 0
    );

    const participacion = total / totalGlobal * 100;

    document.getElementById('kpis-filtrados').innerHTML = `
        <div class="kpi-grid">

            <div class="kpi">
                Alquileres filtrados
                <strong>${formato.format(total)}</strong>
            </div>

            <div class="kpi">
                Promedio diario
                <strong>${promedio.toLocaleString(
                    'es-CO',
                    {maximumFractionDigits: 2}
                )}</strong>
            </div>

            <div class="kpi">
                Días observados
                <strong>${filtrados.length}</strong>
            </div>

            <div class="kpi">
                Participación global
                <strong>${participacion.toFixed(2)}%</strong>
            </div>

        </div>
    `;

    const grupos = {};

    filtrados.forEach(fila => {

        const fecha = granularidad === 'mensual'
            ? fila.dteday.slice(0, 7) + '-01'
            : fila.dteday;

        grupos[fecha] = (
            grupos[fecha] || 0
        ) + Number(fila[usuario]);
    });

    const fechas = Object.keys(grupos).sort();

    const anios = [...new Set(
        fechas.map(fecha => fecha.slice(0, 4))
    )];

    const colores = ['#2563EB', '#0D9488'];

    const series = anios.map((periodo, i) => {

        const x = fechas.filter(
            fecha => fecha.startsWith(periodo)
        );

        return {
            x: x,
            y: x.map(fecha => grupos[fecha]),
            type: 'scatter',
            mode: 'lines+markers',
            name: periodo,
            line: {color: colores[i % colores.length]}
        };
    });

    const grafica = document.getElementById(
        'grafica-demanda-filtrada'
    );

    if (grafica) {

        Plotly.react(
            grafica,
            series,
            {
                title: {
                    text: 'Demanda de bicicletas filtrada'
                },
                autosize: true,
                height: 450,
                xaxis: {
                    title: 'Fecha',
                    type: 'date'
                },
                yaxis: {title: 'Alquileres'},
                paper_bgcolor: '#FFFFFF',
                plot_bgcolor: '#FFFFFF',
                margin: {l: 65, r: 30, t: 65, b: 65}
            },
            {
                responsive: true,
                displaylogo: false
            }
        );
    }
}

function restablecerFiltros() {

    document.getElementById('anio-html').value = 'todos';

    document.getElementById('usuario-html').value = 'cnt';

    document.getElementById(
        'granularidad-html'
    ).value = 'mensual';

    actualizarDemanda();
}

// Renderizar gráficas dentro de acordeones al abrirlos.

document.addEventListener('toggle', evento => {

    if (evento.target.tagName === 'DETAILS'
        && evento.target.open) {

        requestAnimationFrame(() =>
            renderizarPanel(evento.target)
        );
    }

}, true);

window.addEventListener('DOMContentLoaded', () => {

    abrirPestana('resumen');
});
"""

# ==========================================================
# 8. CONSTRUIR DOCUMENTO HTML
# ==========================================================

botones = "".join(
    f'<button id="btn-{nombre}" '
    f'onclick="abrirPestana(\'{nombre}\')">'
    f'{escapar(titulo)}</button>'
    for nombre, titulo in nombres_pestanas.items()
)

paneles = ""

for nombre, contenido in contenido_vistas.items():

    if nombre == "resumen":

        contenido = contenido.replace(
            '<div id="kpis-filtrados"></div>',
            controles_html +
            '<div id="kpis-filtrados"></div>',
            1
        )

    paneles += (
        f'<section class="tab-panel" id="panel-{nombre}">'
        f'{contenido}</section>'
    )

documento_html = f"""
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>Bike Sharing Analytics</title>

    <style>
        {css_dashboard}
    </style>

    <script>
        {get_plotlyjs()}
    </script>

</head>

<body>

<header>

    <h1>BIKE SHARING ANALYTICS</h1>

    <p>Dashboard Global - Proyecto Integrador</p>

    <p>Universidad de La Salle |
       Maestría en Inteligencia Artificial</p>

    <p>Adriana Patricia Fernández Infante</p>

</header>

<nav>
    {botones}
</nav>

<main>
    {paneles}
</main>

<footer>

    Proyecto Integrador de Ciencia de Datos |
    2026 | Universidad de La Salle

    <br><br>

    Versión HTML autónoma |
    47 gráficas | 41 tablas | 25 imágenes

    <br><br>

    Dataset: UCI Bike Sharing |
    DOI: 10.24432/C5W894

</footer>

<script>

    const DATOS = {datos_json};

    const GRAFICAS = {serializar(graficas_html)};

    const TABLAS = {serializar(tablas_html)};

    {javascript_dashboard}

</script>

</body>
</html>
"""

# ==========================================================
# 9. GUARDAR Y VALIDAR ARCHIVO
# ==========================================================

RUTA_HTML.write_text(
    documento_html,
    encoding="utf-8"
)

assert RUTA_HTML.exists()
assert RUTA_HTML.stat().st_size > 0

assert "grafica-demanda-filtrada" in graficas_html

assert 'id="kpis-filtrados"' in documento_html

assert 'id="anio-html"' in documento_html

assert all(
    f'id="panel-{nombre}"' in documento_html
    for nombre in nombres_pestanas
)

# Verificar que las imágenes estén incorporadas.

imagenes_embebidas = re.findall(
    r'<img[^>]+src="data:image/',
    documento_html
)

assert len(imagenes_embebidas) == 25

# Verificar datos para los filtros.

assert int(datos_filtros["cnt"].sum()) == 3292679

assert int(
    datos_filtros.loc[
        datos_filtros["dteday"].str.startswith("2012"),
        "cnt"
    ].sum()
) == 2049576

assert int(
    datos_filtros.loc[
        datos_filtros["dteday"].str.startswith("2012"),
        "registered"
    ].sum()
) == 1676811

# ==========================================================
# 10. RESULTADOS DE EXPORTACIÓN
# ==========================================================

print("\n" + "=" * 60)
print("EXPORTACIÓN HTML AUTÓNOMA")
print("=" * 60)

print("\n=== COMPONENTES EXPORTADOS ===")
print("Pestañas:", len(contenido_vistas))
print("Gráficas:", contador_html["graficas"])
print("Tablas:", contador_html["tablas"])
print("Imágenes:", contador_html["imagenes"])
print("Imágenes embebidas:", len(imagenes_embebidas))
print("Registros para filtros:", len(datos_filtros))

print("\n=== FUNCIONALIDADES INCORPORADAS ===")
print("Navegación por pestañas: OK")
print("Biblioteca Plotly incorporada: OK")
print("Filtros JavaScript incorporados: OK")
print("Búsqueda y ordenamiento de tablas: OK")
print("Paginación de tablas: OK")
print("Acordeones desplegables: OK")
print("Integridad de datos: OK")
print("Modelos reentrenados: 0")

print("\n=== ARCHIVO GENERADO ===")
print("Nombre:", RUTA_HTML.name)
print(
    "Tamaño MB:",
    round(RUTA_HTML.stat().st_size / 1024**2, 2)
)
print("Ruta:", RUTA_HTML)

print("\nExportación HTML finalizada.")
print("Pendiente: validación funcional en el navegador.")

# ==========================================================
# 11. DESCARGAR ARCHIVO
# ==========================================================

files.download(str(RUTA_HTML))