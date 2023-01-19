import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify



def radioGroup(ids,texto,value=[],size="sm",space="xs",orientacion="horizontal",children=[]):
    return  html.Div(
                [
                    dmc.RadioGroup(
                        id=ids,
                        #children=[dmc.Radio(label=i, value=i) for i in owo],
                        children=children,
                        value=value,
                        label=texto,
                        size=size,
                        spacing=space,
                        mt=1,
                        orientation=orientacion,
                    ),
                    
                ]
            )
def radioChild(list):
    return [dmc.Radio(label=i, value=i) for i in list]