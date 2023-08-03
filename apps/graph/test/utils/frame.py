import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_mantine_components as dmc
def Column(content=[],size=12):
      return dbc.Col(content,width=size,className=f"col-xl-{size} col-md-{size} col-sm-12 col-12 mb-1",style={'padding-left': '7px','padding-right': '10px'})

def Row(content=[]):
    return dbc.Row(content)

def Div(content=[],id='', style = {}):
    return html.Div(children=content,id=id, style = style)



def Store(id='data-values'):
    return dcc.Store(id=id)

def Download():
    return dcc.Download(id="download")

def Modal(id = 'modal', size='xl', style = {"max-width": "none", "width": "90%", "max-height":"none", "height":"90%"}, is_open=False):
    return html.Div([dbc.Modal(id = id,size = size,style = style, is_open= is_open)])

def Graph(id = '', figure = {}):
    return dcc.Graph(id = id , figure = figure)

def Divider():
    return html.Div(dmc.Divider(variant="solid"))




