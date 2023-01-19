import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify



def button(text="",variant="filled",color="indigo",ids=None):
    
    return html.Div([dmc.Button(text,variant=variant,color=color,id=ids),])