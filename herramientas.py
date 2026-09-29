"""Lista de herramientas que carga el hub.

Cada herramienta vive en su propio repo de GitHub y sigue siendo una app independiente.
Para agregar una nueva, añade una entrada aquí (y sus dependencias a requirements.txt).
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Herramienta:
    clave: str                # identificador corto (carpeta local y URL de la pestaña)
    titulo: str               # nombre en el menú
    icono: str
    repo: str                 # URL del repo en GitHub
    descripcion: str
    rama: str = "main"
    archivo: str = "app.py"   # script principal dentro del repo
    # Variables de entorno que necesita la app. "{carpeta}" se reemplaza por la carpeta local del repo.
    entorno: dict = field(default_factory=dict)
    # Panel "Cómo usar" que el hub muestra en la barra lateral (Markdown).
    # Déjalo vacío si la herramienta ya trae su propio panel (ej. ForestGuard).
    ayuda: str = ""
    # False = el panel arranca plegado (útil si la herramienta ya pone
    # uploaders o filtros en la barra lateral, para no empujarlos hacia abajo).
    ayuda_abierta: bool = True


HERRAMIENTAS = [
    Herramienta(
        clave="informe-predio",
        titulo="Informe de predio",
        icono="🗺️",
        repo="https://github.com/mabeltrang/informe-predio.git",
        descripcion="Clima y geomorfología del predio para el informe de aprovechamiento.",
        entorno={"CARTOGRAFIA_DIR": "{carpeta}/data"},
        ayuda="""
1. Sube el **KMZ** del predio
2. Elige el rango de años para el clima (por defecto 2015–2025)
3. Haz clic en **Analizar predio**
4. Copia o descarga los bloques de texto y el Word

**Qué genera:**
- **Clima**: precipitación y temperatura mensual (NASA POWER) con sus gráficas
- **Zona de vida** de Holdridge a partir de biotemperatura y precipitación
- **Geomorfología**: unidad UC que intersecta el predio
- **Mapa satelital** del predio

*El análisis usa el centroide del polígono; si el predio es muy grande o alargado, revisa que el clima sea representativo.*
""",
    ),
    Herramienta(
        clave="forestguard",
        titulo="ForestGuard",
        icono="🛡️",
        repo="https://github.com/mabeltrang/ForestGuard-Pro.git",
        descripcion="Validador de consistencia del paquete documental del permiso.",
    ),
    Herramienta(
        clave="cars",
        titulo="Seguimiento CARs",
        icono="📑",
        repo="https://github.com/mabeltrang/CARS_nuevo.git",
        descripcion="Tiempos de trámite y seguimiento de actos administrativos de las CARs.",
        ayuda="""
1. La app carga el Excel **Fechas_CARS.xlsx** del repo
2. Si tienes una versión más nueva, súbela en **Reemplazar el Excel** (abajo)
3. Ajusta los **Filtros**: solo empresas y tipo de trámite
4. Revisa los tiempos promedio y las pestañas

**Pestañas:**
- **¿Quién sale más rápido?**: ranking de trámites
- **Tendencia**: cómo cambian los tiempos en el tiempo
- **Detalle**: tabla completa

*Los trámites con fechas inconsistentes se excluyen de los promedios.*
""",
        ayuda_abierta=False,
    ),
    Herramienta(
        clave="compensacion",
        titulo="Compensación",
        icono="🌱",
        repo="https://github.com/mabeltrang/analisis-compensacion-forestal.git",
        descripcion="FCAFU, ATC y adicionalidad según el Manual 2026.",
        ayuda="""
1. Sube el **KMZ del proyecto** (folders *Proyecto* y *Coberturas vegetales*)
2. Sube el **inventario forestal** (Excel)
3. Revisa el **DAP mínimo** y la **CAR** (si la dejas vacía se detecta sola)
4. Recorre las pestañas y exporta en **📥 Exportar**

**Qué calcula (Manual 2026):**
- **FCAFU** por cobertura (criterios A, B y C)
- **ATC** por rango geográfico R1–R6
- **Tasa BAU** por municipio, SZH y ZH (Hansen GFC)
- **Adicionalidad** a 3, 5, 10 y 15 años
- **Vedas y amenaza** (MADS/CITES/IUCN + CARs) cruzadas con el inventario

*Sin archivos puedes usar igual la pestaña Consulta y Vedas. Requiere conexión a Google Earth Engine.*
""",
        ayuda_abierta=False,
    ),
    Herramienta(
        clave="fgr06",
        titulo="FGR-06 CORPOBOYACÁ",
        icono="🌳",
        repo="https://github.com/mabeltrang/Formato-inventario-CORPOBOYACA.git",
        descripcion="Convierte el inventario al formato FGR-06 (Parte A y B).",
        ayuda="""
1. Sube el **inventario** (.xlsx, hoja *Inventario*)
2. Sube el **KMZ/KML** del predio *(opcional, recomendado)*
3. Revisa los avisos en amarillo
4. Descarga el **FGR-06** en Excel

**Con el KMZ la app además:**
- Calcula el **área del predio**
- Obtiene **altitud y pendiente**
- Avisa si hay **árboles fuera del polígono**

**Vista previa:** pestañas Parte A, Especies y Parte B.

*Las especies sin precio por m³ quedan vacías en el Excel: llénalas a mano.*
""",
    ),
]
