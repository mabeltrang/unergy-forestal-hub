# Hub de herramientas forestales

Una sola app de Streamlit con pestañas para:

- Informe de predio
- ForestGuard
- Seguimiento CARs
- Compensación
- FGR-06 CORPOBOYACÁ

**El hub no contiene el código de las herramientas.** Al arrancar descarga cada repo desde GitHub, en la última versión de su rama `main`, y corre su `app.py` dentro de una pestaña. Cada herramienta sigue siendo independiente: tiene su repo y su app publicada, y se puede cambiar sin tocar el hub.

## Cómo llegan los cambios

1. Haces un cambio y un commit en el repo de una herramienta.
2. En el hub, vas a **Inicio → 🔄 Actualizar herramientas**, o le das Reboot en Streamlit Cloud.

## Archivos

| Archivo | Para qué |
|---|---|
| `app.py` | Menú, descarga de repos y ejecución aislada de cada herramienta |
| `herramientas.py` | Lista de herramientas: repo, rama y variables de entorno |
| `requirements.txt` | Dependencias de Python de todas las herramientas juntas |
| `packages.txt` | Paquetes del sistema (GDAL, tesseract…) |
| `.streamlit/secrets.toml.example` | Plantilla de secretos. Los valores reales **no** van en el repo. |

## Secretos

Se configuran en Streamlit Cloud → app del hub → **Settings → Secrets**:

- `ANTHROPIC_API_KEY`, para ForestGuard.
- `[gee_credentials]`, para Compensación. Es el mismo bloque que ya tiene la app de compensación en sus Secrets.

## Agregar una herramienta

1. Agrega una entrada en `herramientas.py`.
2. Agrega sus dependencias a `requirements.txt` y `packages.txt`.

## Limitación conocida

Todas las herramientas corren en el mismo proceso. Si dos personas usan herramientas distintas exactamente al mismo tiempo, las variables de entorno y los módulos cargados se comparten. Para uso individual o de un equipo pequeño no es un problema.
