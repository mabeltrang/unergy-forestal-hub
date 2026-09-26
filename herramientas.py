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


HERRAMIENTAS = [
    Herramienta(
        clave="informe-predio",
        titulo="Informe de predio",
        icono="🗺️",
        repo="https://github.com/mabeltrang/informe-predio.git",
        descripcion="Clima y geomorfología del predio para el informe de aprovechamiento.",
        entorno={"CARTOGRAFIA_DIR": "{carpeta}/data"},
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
    ),
    Herramienta(
        clave="compensacion",
        titulo="Compensación",
        icono="🌱",
        repo="https://github.com/mabeltrang/analisis-compensacion-forestal.git",
        descripcion="FCAFU, ATC y adicionalidad según el Manual 2026.",
    ),
    Herramienta(
        clave="fgr06",
        titulo="FGR-06 CORPOBOYACÁ",
        icono="🌳",
        repo="https://github.com/mabeltrang/Formato-inventario-CORPOBOYACA.git",
        descripcion="Convierte el inventario al formato FGR-06 (Parte A y B).",
    ),
]
