"""Hub de herramientas forestales.

Funciona como lanzador: cada herramienta corre en su propia app de Streamlit Cloud y el
hub muestra un acceso a cada una. Una herramienta sin `url` en herramientas.py se sigue
corriendo dentro del hub (descarga su repo y ejecuta su app.py).
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

_CSS_TILES = """
<style>
.hub-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
            gap: 18px; margin: 8px 0 24px; }
.hub-tile { display: flex; flex-direction: column; align-items: center; justify-content: center;
            gap: 10px; padding: 26px 14px; border-radius: 14px; text-align: center;
            border: 1px solid rgba(128,128,128,.25); background: rgba(128,128,128,.06);
            text-decoration: none !important; color: inherit !important;
            transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease; }
.hub-tile:hover { transform: translateY(-3px); border-color: #7B3FE4;
                  box-shadow: 0 6px 18px rgba(123,63,228,.18); }
.hub-icono { font-size: 54px; line-height: 1; }
.hub-nombre { font-weight: 600; font-size: 1.02rem; }
.hub-desc { font-size: .8rem; opacity: .7; line-height: 1.25; }
</style>
"""


def inicio() -> None:
    st.title("Herramientas forestales")
    st.caption("Haz clic en una herramienta: se abre en una pestaña nueva y esta queda abierta para volver.")
    tiles = []
    for h in HERRAMIENTAS:
        destino = h.url or f"./{h.clave}"
        nueva = ' target="_blank" rel="noopener"' if h.url else ' target="_self"'
        tiles.append(
            f'<a class="hub-tile" href="{destino}"{nueva}>'
            f'<span class="hub-icono">{h.icono}</span>'
            f'<span class="hub-nombre">{h.titulo}</span>'
            f'<span class="hub-desc">{h.descripcion}</span></a>'
        )
    st.markdown(_CSS_TILES + '<div class="hub-grid">' + "".join(tiles) + "</div>",
                unsafe_allow_html=True)

    internas = [h for h in HERRAMIENTAS if not h.url]
    if internas:  # solo hace falta si alguna herramienta todavía corre dentro del hub
        st.divider()
        if st.button("🔄 Actualizar herramientas desde GitHub"):
            with st.spinner("Actualizando…"):
                for m in actualizar_todo():
                    st.write(m)


def _pagina(h: Herramienta):
    def pagina():
        if h.url:  # la herramienta corre en su propia app: aquí solo el acceso
            st.title(f"{h.icono} {h.titulo}")
            st.write(h.descripcion)
            st.link_button("Abrir la herramienta ↗", h.url, type="primary")
            st.caption("Se abre en una pestaña nueva, en su propia app.")
            if h.ayuda.strip():
                st.markdown(h.ayuda)
            return
        correr(h)
    pagina.__name__ = f"pagina_{h.clave.replace('-', '_')}"
    return pagina


# Herramientas con app propia: el menú de arriba abre directo su link (pestaña nueva).
# Las que no tienen link siguen corriendo dentro del hub como página.
paginas = {
    h.clave: st.Page(_pagina(h), title=h.titulo, icon=h.icono, url_path=h.clave)
    for h in HERRAMIENTAS if not h.url
}
nav = st.navigation(
    [st.Page(inicio, title="Inicio", icon="🏠", default=True), *paginas.values()],
    position="top" if paginas else "hidden",
)
nav.run()
