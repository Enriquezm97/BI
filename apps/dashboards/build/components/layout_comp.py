import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_mantine_components as dmc


def Column(content=[],size=12,margin_top = 0):
      return dbc.Col(content,width=size,className=f"col-xl-{size} col-md-{size} col-sm-12 col-12 mb-1",style={'padding-left': '7px','padding-right': '10px','margin-top':margin_top,"position": "static"})

def Row(content=[]):
    return dbc.Row(content)

def Div(content=[],id='', style = {}):
    return html.Div(children=content,id=id, style = style)



def Store(id='data-values'):
    return dcc.Store(id=id)

def Download():
    return dcc.Download(id="download")


def Graph(id = '', figure = {}):
    return dcc.Graph(id = id , figure = figure)

def Divider():
    return html.Div(dmc.Divider(variant="solid"))

def Modal(titulo = '',id = '', fullScreen = False, size = "75%"):
    return html.Div([dmc.Modal(title = titulo, id = id, fullScreen=fullScreen, zIndex=10000, size= size )])


def themeProvider(content = []):
    return dmc.MantineProvider(
                    id='mantine-provider',
                    withGlobalStyles=True,
                    theme={},
                    inherit=True,
                    children=dmc.Container(content,fluid=True,id='container')
     )

def Container(content=[]):
    return dmc.NotificationsProvider(content)#,fluid=True,id='container'


def Contenedor(content = []):
    return dmc.Container(children= content)