import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify

def spoiler(text=""):
    return html.Div([
            dmc.Spoiler(
                #id=ids,
                showLabel="Mostrar más",
                hideLabel="Hide",
                maxHeight=50,
                children=[
                    dmc.Text(children=text)
                ],
            )
    ])