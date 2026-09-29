"""Descarga de los repos y ejecución aislada de cada herramienta."""

from __future__ import annotations

import os
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import streamlit as st

from herramientas import HERRAMIENTAS, Herramienta

CARPETA_BASE = Path(os.environ.get("HUB_CARPETA", Path(tempfile.gettempdir()) / "hub_herramientas"))


# ----------------------------------------------------------------------------
# Descarga y actualización de repos
# ----------------------------------------------------------------------------

def _git(*args, cwd=None) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    return r.stdout.strip()


@st.cache_resource(show_spinner=False)
def obtener_repo(h: Herramienta) -> Path:
    """Clona el repo la primera vez (solo la última versión). Queda en caché hasta 'Actualizar'."""
    carpeta = CARPETA_BASE / h.clave
    if not (carpeta / ".git").exists():
        if carpeta.exists():
            shutil.rmtree(carpeta)
        CARPETA_BASE.mkdir(parents=True, exist_ok=True)
        with st.spinner(f"Descargando {h.titulo} desde GitHub…"):
            _git("clone", "--depth", "1", "--branch", h.rama, h.repo, str(carpeta))
    return carpeta


def version(h: Herramienta) -> str:
    carpeta = CARPETA_BASE / h.clave
    if not (carpeta / ".git").exists():
        return "sin descargar"
    try:
        return _git("log", "-1", "--format=%h · %cd · %s", "--date=short", cwd=carpeta)
    except Exception:  # noqa: BLE001
        return "?"


def actualizar_todo() -> list[str]:
    """Trae la última versión de cada repo y limpia las cachés."""
    mensajes = []
    for h in HERRAMIENTAS:
        carpeta = CARPETA_BASE / h.clave
        try:
            if (carpeta / ".git").exists():
                _git("fetch", "--depth", "1", "origin", h.rama, cwd=carpeta)
                _git("reset", "--hard", "FETCH_HEAD", cwd=carpeta)
            else:
                obtener_repo(h)
            mensajes.append(f"✅ {h.titulo}: {version(h)}")
        except Exception as e:  # noqa: BLE001
            mensajes.append(f"❌ {h.titulo}: {e}")
    _olvidar_modulos(ninguna=True)
    obtener_repo.clear()
    st.cache_data.clear()
    return mensajes


# ----------------------------------------------------------------------------
# Ejecución aislada de cada herramienta
# ----------------------------------------------------------------------------

def _olvidar_modulos(excepto: Path | None = None, ninguna: bool = False) -> None:
    """Saca de sys.modules lo importado desde las carpetas de otras herramientas.

    Evita choques de nombres (ej. `core.py` de informe-predio vs. el paquete `core/`
    de compensación, o `app.py` de todas).
    """
    base = str(CARPETA_BASE)
    propia = None if (ninguna or excepto is None) else str(excepto)
    for nombre, modulo in list(sys.modules.items()):
        archivo = getattr(modulo, "__file__", None) or ""
        if archivo.startswith(base) and (propia is None or not archivo.startswith(propia)):
            del sys.modules[nombre]


def panel_ayuda(h: Herramienta) -> None:
    """Muestra el panel "Cómo usar" de la herramienta arriba en la barra lateral.

    Se dibuja antes de correr la app, así que queda encima de lo que la
    herramienta ponga en la barra lateral (uploaders, filtros…).
    """
    if not h.ayuda.strip():
        return
    with st.sidebar:
        with st.expander("ℹ️ Cómo usar", expanded=h.ayuda_abierta):
            st.markdown(h.ayuda)


def correr(h: Herramienta) -> None:
    panel_ayuda(h)
    try:
        carpeta = obtener_repo(h)
    except Exception as e:  # noqa: BLE001
        st.error(f"No se pudo descargar {h.titulo} ({h.repo}): {e}")
        return

    _olvidar_modulos(excepto=carpeta)
    sys.path[:] = [p for p in sys.path if not p.startswith(str(CARPETA_BASE))]
    sys.path.insert(0, str(carpeta))
    for var, valor in h.entorno.items():
        os.environ[var] = valor.format(carpeta=carpeta)

    runpy.run_path(str(carpeta / h.archivo), run_name="__main__")
