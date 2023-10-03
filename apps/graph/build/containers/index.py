from dash import Dash, dcc, html, Input, Output,State,dash_table
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
from apps.graph.test.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
#from apps.graph.data.transform_finanzas import balancePivot
from apps.graph.test.utils.frame import Column, Row, Div, Store, Download, Modal,Modal
from apps.graph.test.utils.crum import get_empresa,get_nombre_user
from apps.graph.test.utils.theme import themeProvider, Container,Contenedor
from PIL import Image

def card_index( img = '', title_card = '', description = '', url = ''):
    
    return Div([dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src = Image.open(f"apps/graph/build/containers/assets/{img}"),
                    height=360,
                )
            ),
            dmc.Group(
                [
                    dmc.Text(title_card, weight=500,size="lg"),
                    dmc.Badge("habilitado", color="green", variant="light"),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                description ,
                size="sm",
                color="dimmed",
            ),
        html.A(
            dmc.Button(
                "Ingresar",
                variant="light",
                color="blue",
                fullWidth=True,
                mt="md",
                radius="md",
            ),
            href=f"/{get_nombre_user()}/{url}"
        )
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        
    )])


def index():
    
    app = DjangoDash('index', external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)

    app.layout = Container([
        Row([
            Column([dmc.Title(f"Bienvenido {get_nombre_user()}", align="center"),])
            
        ]),
        Row([
            Column([html.P()])
            
        ]),
        Row([
            Column([
                card_index(img = "agricola.png",title_card= "Costos Agrícola", url='costos-campaña')
            ], size=4),#apps/graph/build/containers/assets/agricola.png
            Column([
                card_index(img = "finanzas.png",title_card= "Estado de Resultados",url='estado-resultados')
            ], size=4),
            Column([
                card_index(img = "ventas.png",title_card= "Ventas Clientes", url= 'comercial-cliente')
            ], size=4),
        ]),
    
    ])
        
    



                
            