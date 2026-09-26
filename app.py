"""Hub de herramientas forestales.

No contiene el código de las herramientas: al arrancar descarga cada repo desde GitHub
(la última versión de su rama) y corre su app.py dentro de una pestaña.
Cada herramienta sigue siendo independiente en su propio repo.

Ejecutar:  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from herramientas import HERRAMIENTAS, Herramienta
from hub import actualizar_todo, correr, version

st.set_page_config(page_title="Herramientas forestales · Unergy", page_icon="🌳", layout="wide")


# ----------------------------------------------------------------------------
# Páginas
# ----------------------------------------------------------------------------

def inicio() -> None:
    st.title("Herramientas forestales")
    st.caption("Cada herramienta vive en su propio repo de GitHub; aquí se cargan todas en un solo lugar.")
    for h in HERRAMIENTAS:
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"### {h.icono} {h.titulo}\n{h.descripcion}")
            c1.caption(f"[{h.repo.removesuffix('.git')}]({h.repo.removesuffix('.git')}) · {version(h)}")
            c2.page_link(paginas[h.clave], label="Abrir", icon="➡️")

    st.divider()
    if st.button("🔄 Actualizar herramientas desde GitHub"):
        with st.spinner("Actualizando…"):
            for m in actualizar_todo():
                st.write(m)


def _pagina(h: Herramienta):
    def pagina():
        correr(h)
    pagina.__name__ = f"pagina_{h.clave.replace('-', '_')}"
    return pagina


paginas = {
    h.clave: st.Page(_pagina(h), title=h.titulo, icon=h.icono, url_path=h.clave)
    for h in HERRAMIENTAS
}
nav = st.navigation(
    [st.Page(inicio, title="Inicio", icon="🏠", default=True), *paginas.values()],
    position="top",
)
nav.run()
