import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify

def drawer(componentes=[]):
    return html.Div(dmc.Drawer(
                        title="Filtros",
                        id="drawer",
                        padding="md",
                        children=componentes,
                        closeOnClickOutside=False,
                        closeOnEscape=True,
                        lockScroll=False,
                        withOverlay=False,
                        size="250px"
                    ),
                )