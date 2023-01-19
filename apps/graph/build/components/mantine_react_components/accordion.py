import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback,dcc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc

def accordion(texto='accordion',children=[],value='accordion',variant="default"):
    return html.Div(
        
        dmc.Accordion(
            variant=variant,
            children=[
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(children=[dmc.Text(texto, weight=700),]),
                        
                        dmc.AccordionPanel(children=children),
                    ],
                    value=value,
                ),
                
            ],
        )
    )