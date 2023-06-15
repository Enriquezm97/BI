import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify
### DASH PLOTLY "options" - MANTINE "data"
def select(ids,texto,place="Todos",value=None,data=[],clearable=True,size='md'):
    return  html.Div(
        dmc.Select(
            id=ids,
            #data=data,#["USDINR", "EURUSD", "USDTWD", "USDJPY"],
            data=data,
            label=texto,
            clearable=clearable,
            placeholder=place,
            style={'font-size': "90%"},
            value=value,
            size=size
            #searchable=True,
            #style={"width": 200},
            #icon=DashIconify(icon="radix-icons:magnifying-glass"),
            #rightSection=DashIconify(icon="radix-icons:chevron-down"),
        )

    )

def multiSelect(ids='w',texto='',place="",value=None,data=[],size='md'):
    return html.Div(
        dmc.MultiSelect(
                    #data=["React", "Angular", "Svelte", "Vue"],
                    id=ids,
                    label=texto,
                    placeholder=place,
                    searchable=True,
                    nothingFound="Opción no encontrada",
                    value=value,
                    data=data,
                    style={'font-size': "80%"},
                    size=size
                    
                )
    )
    