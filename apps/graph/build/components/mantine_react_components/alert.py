import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback,dcc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc

def alert(ids=None,text="This alert will dismiss itself after 3 seconds!",title="Alerta", duration=3000,color="green"):
    return html.Div(
    [
        dmc.Alert(
            text,
            title=title,
            id=ids,
            color=color,
            duration=duration,
        ),
    ]
)