import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output,State,dash_table
import dash_bootstrap_components as dbc
 
 
def controlsRecursosAgricola(): 
    return dbc.Card(
    [
        html.Div(
            [
                
                dbc.Label("Campaña"),
                dcc.Dropdown(
                    id="drop_anio",
                    multi=False,
                    searchable= True,
                    placeholder= 'All',
                    options=[],
                    value=2020,
                    style={
                        
                        'font-size': "90%",
                        #'min-height': '2px',
                        },
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Cultivos"),
                dcc.Dropdown(
                    id="drop_cultivo",
                    multi=True,
                    searchable= True,
                    placeholder= '',
                    options=[],
                
                ),
                html.P()
            ]
        ),
        html.Div(
            [
                dbc.Badge("Recursos", pill=True, color="dark"),
                            dcc.RadioItems(id="recursos",
                                options=[
                                    {'label': 'Por Cantidad', 'value': 'cantidad'},
                                    {'label': 'Por Héctarea', 'value': 'hectarea'}, 
                                ],
                                value='cantidad',
                                labelStyle={'display': 'inline-block'}
                            ),
            ]
        ),
        html.Div(
            [
                dbc.Badge("Eje X", pill=True, color="dark"), 
                            dcc.RadioItems(id="radio-st",
                                options=[
                                    {'label': 'Fecha', 'value': 'fecha'},
                                    {'label': 'Semana', 'value': 'semana'},
                                ],
                                value='fecha',
                                labelStyle={'display': 'inline-block'}
                            ),
            ]
        ),
        html.Div([
            dbc.Badge("Variables", pill=True, color="dark"), 
            dcc.Checklist(
                                id="check-agricola",
                                options=[
                                    {'label': 'N', 'value': 'N         '},
                                    {'label': 'P', 'value': 'P         '},
                                    {'label': 'K', 'value': 'K         '},
                                    {'label': 'HM', 'value': 'HM'},
                                    {'label': 'JR', 'value': 'JR'},
                                    {'label': 'M3', 'value': 'M3'},
                                ],
                                value=['N         ', 'P         ','K         ',
                                        'HM','JR','M3'],
                                #inline=False,
                                #inline=True,     
                        ),
        ]),
        html.Div([
            dbc.Button("Ocultar Lotes", size="sm",id='collapse-button',color="dark"),
        ])
    ],
    body=True,
    )

def year_campaña():
    return html.Div(
            [
                
                dbc.Label("Campaña"),
                dcc.Dropdown(
                    id="drop_anio",
                    multi=False,
                    searchable= True,
                    placeholder= 'All',
                    options=[],
                    value=2020,
                    style={
                        
                        'font-size': "90%",
                        #'min-height': '2px',
                        },
                ),
            ]
        )
def cultivo_agricola():
    return html.Div(
            [
                dbc.Label("Cultivos"),
                dcc.Dropdown(
                    id="drop_cultivo",
                    multi=True,
                    searchable= True,
                    placeholder= '',
                    options=[],
                
                ),
            ]
        )
def variedad_agricola():
    return html.Div(
            [
                dbc.Label("Variedad"),
                dcc.Dropdown(
                    id="drop_variedad",
                    multi=False,
                    #searchable= True,
                    placeholder= '',
                    options=[],
                
                ),
            ]
        )

def recursos_agricola():
    return html.Div(
            [
                
                #dbc.Badge("Recursos", pill=True, color="dark"),
                            dcc.RadioItems(id="recursos",
                                options=[
                                    {'label': 'Por Cantidad', 'value': 'cantidad'},
                                    {'label': 'Por Héctarea', 'value': 'hectarea'}, 
                                ],
                                value='cantidad',
                                labelStyle={'display': 'inline-block'}
                            ),
            ]
        )
def serie_agricola():
    return html.Div(
            [
                #dbc.Badge("Eje X", pill=True, color="dark"), 
                            dcc.RadioItems(id="radio-st",
                                options=[
                                    {'label': 'Fecha', 'value': 'fecha'},
                                    {'label': 'Semana', 'value': 'semana'},
                                ],
                                value='semana',
                                labelStyle={'display': 'inline-block'}
                            ),
            ]
        ),
def variables_agricola():
    return html.Div([
            #dbc.Badge("Variables", pill=True, color="dark"), 
            dcc.Checklist(
                                id="check-agricola",
                                options=[
                                    {'label': 'N', 'value': 'N         '},
                                    {'label': 'P', 'value': 'P         '},
                                    {'label': 'K', 'value': 'K         '},
                                    {'label': 'HM', 'value': 'HM'},
                                    {'label': 'JR', 'value': 'JR'},
                                    {'label': 'M3', 'value': 'M3'},
                                ],
                                value=['N         ', 'P         ','K         ',
                                        'HM','JR','M3'],
                                #inline=False,
                                inline=True,     
                        ),
        ]),
def boton_ocultar_agricola():
    return html.Div([
            dbc.Button("Ocultar Lotes", size="sm",id='collapse-button',color="dark"),
        ])