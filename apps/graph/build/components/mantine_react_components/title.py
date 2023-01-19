import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify



def title(text="",order=1,ids='id'):
    
    return html.Div([dmc.Title(text, order=order,id=ids)])