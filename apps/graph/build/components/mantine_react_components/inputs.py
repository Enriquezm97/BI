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

def inputNumPercent(ids='input-num',label="Number input",value=10,minimo=0,maximo=100):
    return html.Div(
        dmc.NumberInput(
            id=ids,
            label=label,
            value=value,
            precision=1,
            min=minimo,
            step=1,
            max=maximo,
            #style={"width": 100},
            icon=DashIconify(icon="feather:percent"),
            #size="md",
        )
    )
