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

# Paleta Unergy (la misma de la app de Compensación)
MORADO = "#7B4CC9"
MORADO_OSCURO = "#2D1B4E"
MORADO_CLARO = "#D9CEEF"
MORADO_FONDO = "#F0EBF9"
TEXTO = "#1A1A2E"
TEXTO_SUAVE = "#5A5A72"

# Íconos de línea propios (no emojis: se ven iguales en Windows, Mac y celular).
_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{}</svg>'
ICONOS = {
    # mapa plegado con un punto marcado
    "informe-predio": '<path d="M9 4 3.5 6v14L9 18l6 2 5.5-2V4L15 6 9 4Z"/><path d="M9 4v14M15 6v6"/>'
                      '<path d="M18.5 15.2c0 1.6-2 3.3-2 3.3s-2-1.7-2-3.3a2 2 0 0 1 4 0Z"/>',
    # escudo con chulo
    "forestguard": '<path d="M12 3 5 6v5.5c0 4.3 3 7.9 7 9.5 4-1.6 7-5.2 7-9.5V6l-7-3Z"/><path d="m8.8 12 2.2 2.2 4.3-4.4"/>',
    # resolución con reloj
    "cars": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h4"/><path d="M14 3v4h4M14 3l4 4v3"/>'
            '<path d="M8.5 10h5M8.5 13.5h3"/><circle cx="17" cy="17" r="4"/><path d="M17 15.2V17l1.2 1"/>',
    # brote
    "compensacion": '<path d="M12 21v-9"/><path d="M12 12C12 8 9.5 6 5 6c0 4 2.5 6 7 6Z"/>'
                    '<path d="M12 14.5c0-3.4 2.2-5.5 7-5.5 0 3.6-2.4 5.5-7 5.5Z"/><path d="M8 21h8"/>',
    # tabla que se convierte en formato
    "fgr06": '<rect x="3.5" y="4" width="11" height="13" rx="1.5"/><path d="M3.5 8.5h11M3.5 12.8h11M8 4v13"/>'
             '<path d="M17.5 9.5h3v10.5h-9V19.5"/><path d="m16 14.5 2-2-2-2"/>',
    # ficha con foto del árbol
    "fichas": '<rect x="4" y="3" width="16" height="18" rx="2"/><rect x="7" y="6" width="10" height="7" rx="1"/>'
              '<path d="M12 12.5V9.8m0 0 1.6-1.4M12 9.8 10.4 8.6"/><path d="M7.5 16h9M7.5 18.5h5.5"/>',
}

_CSS = f"""
<style>
  .stApp {{ background: #FFFFFF; }}
  .block-container {{ max-width: 1120px; padding-top: 4.5rem; }}

  .hub-cabecera {{
    background: {MORADO_OSCURO}; border-radius: 16px; padding: 30px 34px;
    display: flex; align-items: center; gap: 20px; margin-bottom: 30px;
    position: relative; overflow: hidden;
  }}
  /* copas de árboles en línea, muy tenues, a la derecha de la cabecera */
  .hub-cabecera::after {{
    content: ""; position: absolute; right: -10px; bottom: -6px; width: 340px; height: 120px;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 120' fill='none' stroke='%239B6FE8' stroke-width='2' opacity='.45'%3E%3Cpath d='M40 120V78M40 78c-16 0-26-10-26-24s12-26 26-26 26 12 26 26-10 24-26 24Z'/%3E%3Cpath d='M120 120V64M120 64c-22 0-36-14-36-32S100 0 120 0s36 14 36 32-14 32-36 32Z'/%3E%3Cpath d='M200 120V86M200 86c-12 0-20-8-20-19s9-20 20-20 20 9 20 20-8 19-20 19Z'/%3E%3Cpath d='M275 120V70M275 70c-19 0-31-12-31-28s13-29 31-29 31 13 31 29-12 28-31 28Z'/%3E%3C/svg%3E") no-repeat right bottom / contain;
    pointer-events: none;
  }}
  .hub-cabecera > * {{ position: relative; z-index: 1; }}
  @media (max-width: 700px) {{ .hub-cabecera::after {{ display: none; }} .hub-cabecera h1 {{ font-size: 1.5rem; }} }}
  .hub-marca {{
    width: 56px; height: 56px; border-radius: 14px; background: {MORADO};
    display: grid; place-items: center; color: #FFFFFF; flex: none;
  }}
  .hub-marca svg {{ width: 30px; height: 30px; }}
  .hub-cabecera h1 {{ color: #FFFFFF !important; font-size: 1.9rem; font-weight: 700; margin: 0; padding: 0; }}
  .hub-cabecera p {{ color: #C5B3F0 !important; margin: 4px 0 0; font-size: .95rem; }}

  .hub-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }}
  @media (max-width: 900px) {{ .hub-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
  @media (max-width: 560px) {{ .hub-grid {{ grid-template-columns: 1fr; }} }}

  .hub-tile {{
    display: flex; gap: 16px; align-items: flex-start; padding: 22px 22px 20px;
    background: #FFFFFF; border: 1.5px solid {MORADO_CLARO}; border-radius: 14px;
    text-decoration: none !important; color: {TEXTO} !important;
    transition: border-color .15s ease, background .15s ease;
  }}
  .hub-tile:hover, .hub-tile:focus-visible {{ border-color: {MORADO}; background: #FCFAFF; outline: none; }}
  .hub-tile:focus-visible {{ box-shadow: 0 0 0 3px {MORADO_CLARO}; }}
  .hub-icono {{
    width: 56px; height: 56px; border-radius: 14px; flex: none; display: grid; place-items: center;
    background: {MORADO_FONDO}; color: {MORADO}; transition: background .15s ease, color .15s ease;
  }}
  .hub-icono svg {{ width: 30px; height: 30px; }}
  .hub-tile:hover .hub-icono, .hub-tile:focus-visible .hub-icono {{ background: {MORADO}; color: #FFFFFF; }}
  .hub-texto {{ display: flex; flex-direction: column; gap: 5px; min-width: 0; }}
  .hub-nombre {{ font-weight: 700; font-size: 1.06rem; color: {MORADO_OSCURO}; }}
  .hub-desc {{ font-size: .86rem; line-height: 1.4; color: {TEXTO_SUAVE}; }}
  .stApp p.hub-pie {{ margin-top: 22px; font-size: .82rem; color: {TEXTO_SUAVE}; }}
  @media (prefers-reduced-motion: reduce) {{ .hub-tile, .hub-icono {{ transition: none; }} }}
</style>
"""


def inicio() -> None:
    hoja = ('<path d="M5 19c0-8 5.5-14 15-14 0 9.5-6 15-14 15"/><path d="M5 19c3-4.5 6.5-7.5 10-9.5"/>')
    st.markdown(
        _CSS
        + f'<div class="hub-cabecera"><div class="hub-marca">{_SVG.format(hoja)}</div>'
        '<div><h1>Herramientas forestales</h1>'
        '<p>Unergy · Equipo forestal</p></div></div>',
        unsafe_allow_html=True,
    )
    tiles = []
    for h in HERRAMIENTAS:
        destino = h.url or f"./{h.clave}"
        nueva = ' target="_blank" rel="noopener"' if h.url else ' target="_self"'
        icono = _SVG.format(ICONOS[h.clave]) if h.clave in ICONOS else h.icono
        tiles.append(
            f'<a class="hub-tile" href="{destino}"{nueva}>'
            f'<span class="hub-icono">{icono}</span>'
            f'<span class="hub-texto"><span class="hub-nombre">{h.titulo}</span>'
            f'<span class="hub-desc">{h.descripcion}</span></span></a>'
        )
    st.markdown('<div class="hub-grid">' + "".join(tiles) + "</div>"
                '<p class="hub-pie">Cada herramienta se abre en una pestaña nueva; esta página queda abierta.</p>',
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
