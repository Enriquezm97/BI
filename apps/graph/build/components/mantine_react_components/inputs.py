import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify


def inputNumber():
    return html.Div(
        dmc.NumberInput(
            label="Number input with decimal steps",
            value=0.05,
            precision=2,
            min=-1,
            step=0.01,
            max=1,
            style={"width": 250},
        )
    )