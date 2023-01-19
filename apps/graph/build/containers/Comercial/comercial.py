from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from dash_bootstrap_templates import ThemeSwitchAIO
from apps.graph.data.data import *
from apps.graph.build.components.comercial import *
from apps.graph.build.components.draw.bar import *
from apps.graph.data.transform_comercial import *
import dash_mantine_components as dmc
from apps.graph.build.components.mantine_react_components.loaders import loadingOverlay
from apps.graph.build.components.mantine_react_components.selects import select
from apps.graph.build.components.mantine_react_components.radio import radioGroup
from apps.graph.build.components.mantine_react_components.actionIcon import btnFilter
from apps.graph.build.components.bootstrap_components.offcanvas import offcanvas
from apps.graph.build.components.mantine_react_components.title import title
from apps.graph.utils.callback import *
template_theme1 = "zephyr"
template_theme2 = "slate"
url_theme1 = dbc.themes.BOOTSTRAP
url_theme2 = dbc.themes.SLATE
color_variado=px.colors.qualitative.Dark2+px.colors.qualitative.Prism

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)
external_stylesheets=[dbc.themes.BOOTSTRAP]


def informeVentas(empresa,staff_comment):
    
    df_informe_ventas=dataVentasEmpresa(empresa)

    #df_informe_ventas=df_ventas_detalle
    app = DjangoDash('ventas1', external_stylesheets=external_stylesheets,)

    app.layout = html.Div([

            dbc.Row([
                dbc.Col([ThemeSwitchAIO(aio_id="theme",icons={"left": "bi bi-moon", "right": "bi bi-sun"},themes=[url_theme1, url_theme2])],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([
                    html.H3(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                    html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                    ],width=10,className="col-xl-10 col-md-12 col-sm-12 col-12 mb-3")
            ]),
            dbc.Row([
                dbc.Col([
                        select("year","Año")
                        #dbc.Label('Año'),
                        #dcc.Dropdown(
                        #        id='year',
                        #        multi=False,
                        #        searchable= True,
                        #        placeholder= 'All',
                        #        options=[],
                        #        value=sorted(df_informe_ventas['YEAR'].unique())[-1],
                        #        style={'font-size': "80%"},
                        #)
                    ],
                    width=1,className="col-xl-1 col-md-12 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                        select("cliente","Cliente")
                        
                    ],
                    width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"), 
                    dbc.Col([
                        select("cultivo","Cultivo")
                        
                    ],
                    width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                        select("variedad","Variedad")
                        
                    ],
                    width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                        radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                   children=[dmc.Radio(label='S/', value='Soles'),dmc.Radio(label='$', value='Dolares'),

                        ]),
                        
                    ],
                    width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),

            ]),
            dbc.Row([
                dbc.Col([
                    loadingOverlay(dbc.Card(dcc.Graph(id='card'),className="shadow-sm")),
                    html.P(),
                    loadingOverlay(dbc.Card(dcc.Graph(id='bar-naviera'),className="shadow-sm"))
                    
                ],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            loadingOverlay(dbc.Card(dcc.Graph(id='pais_top_facturado'),className="shadow-sm"))
                    ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),

                        dbc.Col([
                            loadingOverlay(dbc.Card(dcc.Graph(id='cultivo_top_facturado'),className="shadow-sm"))
                            
                        ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                        loadingOverlay(dbc.Card(dcc.Graph(id='mes_top'),className="shadow-sm")),
                        
                    ]),
                    #dbc.Card(dcc.Graph(id='pais_top_facturado'),className="shadow-sm"),
                ],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
            
            #dbc.Col([
            #    dbc.Card(dcc.Graph(id='bar_top_cultivo'),className="shadow-sm")
            #],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3")
            ]),
            html.Div(id='comentario')
            
    ])
    @app.callback(
        Output("comentario","children"),
        Input("year","value"),)
    def staff(year):
        if staff_comment == 1 or staff_comment == True:
            trash=dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.Div('Esto es una prueba')
                ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            ])
        else :
            trash=html.Div('-')
        return trash

    @app.callback(
        Output("year","data"),
        Output("cultivo","data"),
        Output("variedad","data"),
        Output("cliente","data"),
        #Output('filter-data', 'data'),
        Input("year","value"),
        Input("cultivo","value"),
        Input("variedad","value"),
        #Input("cultivo","value"),
        Input("cliente","value"),
        
        
        )
    def ventas(year,cultivo,variedad,cliente):
        
        df_ventas=df_informe_ventas.groupby(['YEAR','RAZON_SOCIAL','CULTIVO','VARIEDAD'])[['IMPORTEMOF']].sum().reset_index()

        if year==None and cultivo == None and variedad== None and cliente==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None:    
            options=df_ventas[df_ventas['YEAR']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None:    
            options=df_ventas[df_ventas['CULTIVO']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None:    
            options=df_ventas[df_ventas['VARIEDAD']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None:    
            options=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

        
        elif year==None and cultivo != None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]

        elif year==None and cultivo != None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]


        option_year=[{'label': i, 'value': i} for i in options['YEAR'].unique()] 
        option_cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()] 
        option_variedad=[{'label': i, 'value': i} for i in options['VARIEDAD'].unique()] 
        option_cliente=[{'label': i, 'value': i} for i in options['RAZON_SOCIAL'].unique()] 
        return option_year,option_cultivo,option_variedad,option_cliente

    @app.callback(
        
        Output("title","children"),
        Output("subtitle","children"),
        Input("year","value"),
        Input("cultivo","value"),
        Input("cliente","value"),
        Input("radio-moneda","value"),
        
        )
    def title_ventas(year,cultivo,cliente,moneda):
        general='Informe de Ventas'+' '+str(moneda)
        if year == None:
            title=general
        else:
            title=general+' '+str(year)
        if cliente == None and cultivo == None:
            subtitle=''
        elif cliente != None and cultivo == None:
            subtitle=str(cliente)
        elif cliente != None and cultivo != None:
            subtitle=str(cliente)+' '+str(cultivo)
            
        return title,subtitle


    @app.callback(
        Output("card","figure"),
        Output("bar-naviera","figure"),
        Output("pais_top_facturado","figure"),
        Output("cultivo_top_facturado","figure"),
        Output("mes_top","figure"),
        #Output("bar_top_cultivo","figure"),
        #Input('filter-data', 'data'),
        Input("year","value"),
        Input("cultivo","value"),
        Input("variedad","value"),
        Input("cliente","value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input("radio-moneda","value")
        )
    def ventas(year,cultivo,variedad,cliente,toggle,radio):
        df_ventas=df_informe_ventas
        #options=pd.read_json(data, orient='split')
        if year==None and cultivo == None and variedad== None and cliente==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None:    
            options=df_ventas[df_ventas['YEAR']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None:    
            options=df_ventas[df_ventas['CULTIVO']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None:    
            options=df_ventas[df_ventas['VARIEDAD']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None:    
            options=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

        
        elif year==None and cultivo != None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]

        elif year==None and cultivo != None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]


        #card
        if radio=='Soles':
            importe='IMPORTEMOF'
        elif radio=='Dolares':
            importe='IMPORTEMEX'
        total=options[importe].sum()
        #bar naviera top
        df_naviera_top_facturado=options.groupby(['DESCRIPCION'])[[importe]].sum().sort_values(importe,ascending=True).tail(15).reset_index()#.head(15)
        #PAIS PIE
        df_pais_pie=options.groupby(['PAIS'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
        #TOP DE CULTIVOS
        df_cultivo_top=options.groupby(['CULTIVO'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
        #MES TOP
        df_mes_top=options.groupby(['MES_TEXT','MONTH'])[[importe]].sum().reset_index().sort_values('MONTH',ascending=True).reset_index()
        df_mes_top['%']=(df_mes_top[importe]/options[importe].sum())*100
        #CULTIVO PESO
        #df_cultivo_peso=options.groupby(['CULTIVO'])[['PESONETO_PRODUCTO']].sum().reset_index().sort_values('PESONETO_PRODUCTO',ascending=True)#
        #TEMPLATE STYLES
        template = template_theme1 if toggle else template_theme2

        return card(total,template,importe),barNaviera(df_naviera_top_facturado,template,importe,radio,'Producto'),paisFacturado(df_pais_pie,template,importe),cultivoFacturado(df_cultivo_top,template,importe),mesTop(df_mes_top,template,importe)#,barCultivo(df_cultivo_peso,template)

def ventasExportacion(empresa,staff_comment):
    
    df_ventas_expo=dataVentasEmpresa(empresa)
    #df_ventas_expo=df_ventas_detalle
    app = DjangoDash(
        'ventas_exportacion',
        external_stylesheets=external_stylesheets,
    )
    app.layout = html.Div([
        dbc.Row([
                dbc.Col([ThemeSwitchAIO(aio_id="theme",icons={"left": "bi bi-moon", "right": "bi bi-sun"},themes=[url_theme1, url_theme2])],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([
                    html.H3(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                    html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                    ],width=10,className="col-xl-10 col-md-12 col-sm-12 col-12 mb-3")
            ]),
        dbc.Row([
                    dbc.Col([
                        #value=sorted(df_ventas_expo['YEAR'].unique())[-1],
                        #select("year","Año"),
                        select(ids="year",texto="Año",place="")
                        
                    ],
                    width=1,className="col-xl-1 col-md-12 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                        select(ids="cliente",texto="Cliente",place="")
                       
                                    ],
                    width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"), 
                    dbc.Col([
                        select(ids="cultivo",texto="Cultivo",place="")
                        
                        
                    ]),
                    dbc.Col([
                        select(ids="variedad",texto="Variedad",place="")
                        
                    ],
                    width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                         radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                   children=[dmc.Radio(label='S/', value='Soles'),dmc.Radio(label='$', value='Dolares'),

                        ]),
                    ],
                    width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),
        ]),
 
        dbc.Row([
            dbc.Col([
                            dbc.Row(
                                    [

                                        dbc.Col(loadingOverlay(dbc.Card(dcc.Graph(id='card-export'),className="shadow-sm")),width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                                        

                                    
                                    ],
                                    
                                ),
                    
                            dbc.Row(
                                    [

                                        dbc.Col(loadingOverlay(dbc.Card(dcc.Graph(id='pie-export'),className="shadow-sm")),width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                                        
                                    
                                    ],
                                
                                ),
                    
                    
                    
                    ],width=5,className="col-xl-5 col-md-12 col-sm-12 col-12 mb-3"),
                    
                    dbc.Col(loadingOverlay(dbc.Card(dcc.Graph(id='map-vpais'),className="shadow-sm")),width=7,className="col-xl-7 col-md-12 col-sm-12 col-12 mb-3"),
                ],
                
            ),#

        dbc.Row(
                [
                    dbc.Col(loadingOverlay(dbc.Card(dcc.Graph(id='bar-mesvariedad'),className="shadow-sm")),width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                    #dbc.Col(html.Div(id='cultivo_cel')),dbc.Card(dcc.Graph(id='map-vpais'),className="shadow-sm")
                    #dbc.Col(dbc.Card(dcc.Graph(id='bar-mesformato'),className="shadow-sm"),width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                ],
                
            ),
        html.Div(id='comentario')

    ])
    @app.callback(
        Output("year","data"),
        Output("cultivo","data"),
        Output("variedad","data"),
        Output("cliente","data"),
        #Output('filter-data', 'data'),
        Input("year","value"),
        Input("cultivo","value"),
        Input("variedad","value"),
        #Input("cultivo","value"),
        Input("cliente","value"),
        )
    def ventas(year,cultivo,variedad,cliente):
        
        df_ventas=df_ventas_expo.groupby(['YEAR','RAZON_SOCIAL','CULTIVO','VARIEDAD'])[['IMPORTEMOF']].sum().reset_index()
        if year==None and cultivo == None and variedad== None and cliente==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None:    
            options=df_ventas[df_ventas['YEAR']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None:    
            options=df_ventas[df_ventas['CULTIVO']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None:    
            options=df_ventas[df_ventas['VARIEDAD']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None:    
            options=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

        
        elif year==None and cultivo != None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]

        elif year==None and cultivo != None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]


        option_year=[{'label': i, 'value': i} for i in options['YEAR'].unique()] 
        option_cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()] 
        option_variedad=[{'label': i, 'value': i} for i in options['VARIEDAD'].unique()] 
        option_cliente=[{'label': i, 'value': i} for i in options['RAZON_SOCIAL'].unique()] 
        return option_year,option_cultivo,option_variedad,option_cliente

    @app.callback(
        Output("comentario","children"),
        Input("year","value"),)
    def staff(year):
        if staff_comment == 1 or staff_comment == True:
            trash=dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.Div('Esto es una prueba')
                ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            ])
        else :
            trash=html.Div('-')
        return trash

    @app.callback(
        
        Output("title","children"),
        Output("subtitle","children"),
        Input("year","value"),
        Input("cultivo","value"),
        Input("cliente","value"),
        Input("radio-moneda","value"),
        
        )
    def title_ventas(year,cultivo,cliente,moneda):
        general='Informe de Ventas '+' '+str(moneda)
        if year == None:
            title=general
        else:
            title=general+' '+str(year)
        if cliente == None and cultivo == None:
            subtitle=''
        elif cliente != None and cultivo == None:
            subtitle=str(cliente)
        elif cliente != None and cultivo != None:
            subtitle=str(cliente)+' '+str(cultivo)
            
        return title,subtitle

        
    @app.callback(
        Output('card-export', 'figure'),
        Output('pie-export', 'figure'),
        Output('bar-mesvariedad', 'figure'),
        #Output('bar-mesformato', 'figure'),
        Output('map-vpais', 'figure'),
        [Input("year","value"),
         Input("cultivo","value"),
         Input("variedad","value"),
         Input("cliente","value"),
         Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
         Input("radio-moneda","value")
        ]#rbtn_dinero
    )   
    def update_card_VentasExport(year,cultivo,variedad,cliente,toggle,radio):
        
        df_ventas=df_ventas_expo
        if year==None and cultivo == None and variedad== None and cliente==None:
            df=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None:    
            df=df_ventas[df_ventas['YEAR']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None:    
            df=df_ventas[df_ventas['CULTIVO']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None:    
            df=df_ventas[df_ventas['VARIEDAD']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None:    
            df=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None:
            df=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None:
            df=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None:
            df=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

        
        elif year==None and cultivo != None and variedad== None and cliente!=None:
            df=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None:
            df=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None:
            df=df_ventas[(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente==None:
            df=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None:
            df=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None:
            df=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]

        elif year==None and cultivo != None and variedad!= None and cliente!=None:
            df=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None:
            df=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]


        if radio=='Soles':
            importe='IMPORTEMOF'
            simbolo="S/"
            
        elif radio=='Dolares':
            importe='IMPORTEMEX'
            simbolo="$"
        
        #card
        total=df[importe].sum()
        
        #pie
        df_totalv_variedad=df.groupby(['VARIEDAD'])[[importe]].sum().reset_index()
        #bar exportación

        df_exportacion=df.groupby(['FECHA','RAZON_SOCIAL'])[[importe]].sum().reset_index()
        num= df_exportacion[importe].max()
        if num>999999:
            df_exportacion['total_resumen']=df_exportacion[importe]/1000000
            title='(Millón)'
        elif num<999999:
            df_exportacion['total_resumen']=df_exportacion[importe]/1000
            title='(Mil)'
        elif num <1000:
            df_exportacion['total_resumen']=df_exportacion[importe]/1
            title=''
        
        #BAR EXPORTACION 2

        df_totalv_meses_peso=df.groupby(['MONTH','MES_TEXT','UNDEX'])[[importe]].sum().sort_values('MONTH',ascending=True).reset_index()
        num2= df_totalv_meses_peso[importe].max()
        
        if num2>999999:
           
            title2='(Millón)'
            df_totalv_meses_peso['total_resumen']=df_totalv_meses_peso[importe]/1000000
        elif num2<999999:
            title2='(Mil)'
            df_totalv_meses_peso['total_resumen']=df_totalv_meses_peso[importe]/1000
        elif num2 <1000:
            title2=''
            df_totalv_meses_peso['total_resumen']=df_totalv_meses_peso[importe]/1
        
        #MAP

        df_ventas_for_pais=df.groupby(['PAIS','latitud','longitud'])[[importe]].sum().reset_index()
        #df_ventas_for_pais=df_ventas_for_pais[df_ventas_for_pais['latitud'].notnull()]
        df_ventas_for_pais=df_ventas_for_pais[df_ventas_for_pais[importe]>0]

        template = template_theme1 if toggle else template_theme2
        line_graph = px.line(df_exportacion, x="FECHA", y="total_resumen",title=f'Serie de Tiempo de Ventas {title}',template='none',hover_data=['RAZON_SOCIAL'])
        line_graph.update_layout(height=400,margin=dict(l=55, r=30, t=70, b=40),xaxis_title='Fecha',
            yaxis_title=radio,)
        line_graph.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
        

        
        return (Cards.cardPrefix(total,'Ventas Totales',None,None,simbolo,template),
                #PieChartLegendLeft(df_totalv_variedad['VARIEDAD'],df_totalv_variedad['IMPORTEMOF'],'Total Ventas por Variedad'),
                Piechart.legendLeft(df_totalv_variedad['VARIEDAD'],df_totalv_variedad[importe],'Ventas por Variedad',template),
                #Barchart.horizontalExport(df_exportacion,'FECHA','total_resumen',None,f'Ventas por Mes por Tipo de Venta {title}',False,'FECHA',radio,importe,template),
                line_graph,
                #Barchart.horizontalExport(df_totalv_meses_peso,'MES_TEXT','total_resumen','UNDEX',f'Ventas por Mes y Formato {title}',False,'Mes',radio,importe,template),
                Maps.mapPais(df_ventas_for_pais,'latitud','longitud','PAIS',importe,template),
                )


    @app.callback(
    Output("collapse", "is_open"),
    [Input("hide", "n_clicks")],
    [State("collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
        
def TableDtScrolling_no_color(dff,font_size='14px'):
    
    
    fig = dash_table.DataTable(#id=idd, 
                                    columns=[{"name": c, "id": c,
                                     "type": "numeric", "format": Format(group=",", precision=2,scheme="f")} for c in dff
                                     ],
                                    
                                    style_cell={
                                            #'width': '100px',
                                            #'minWidth': '100px',
                                            #'maxWidth': '100px',
                                            'overflow': 'hidden',
                                            'textOverflow': 'ellipsis',
                                            'text_align': 'left',
                                            'font-family': 'sans-serif',
                                            'font-size': font_size,
                                        },
                                    style_header={
                                            'backgroundColor': '#f7f7f7',
                                            'fontWeight': 'bold',
                                            'text-align': 'center',
                                            'font-family': 'sans-serif',
                                            'font-size': '14px',
                                        },
                                    style_data_conditional=[
                                        {
                                            'if': {
                                                'filter_query': '{Importe} < 1',
                                                'column_id': 'Importe'
                                            },
                                            'backgroundColor': '#FF4136',
                                            'color': 'white'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{Importe} > 0',
                                                'column_id': 'Importe'
                                            },
                                            'backgroundColor': '#0074D9',
                                            'color': 'white'
                                        },
                                        
                                        
                                        
                                        
                                    ],
                                    data=dff.to_dict('records'),
                                    page_action='none',
                                    sort_action="native",
                                    style_table={'height': '310px','overflowY': 'auto'},

                                 )
    #return dbc.Card(dbc.CardHeader("Card header"),dbc.CardBody([fig]),color="primary", outline=True),
    return fig
def ventas1(empresa,staff_comment):
    
    df_ventas_expo=dataVentasEmpresa(empresa)

    app = DjangoDash('dashventas1', external_stylesheets=[url_theme1, dbc.icons.BOOTSTRAP, dbc_css])#
    
    df_ventas_d=changeVentasCol(df_ventas_expo)
    app.layout = html.Div([
            dbc.Row([   
                        dbc.Col([
                            html.H3(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                            html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})

                           ],width=10,className="col-xl-10 col-md-10 col-sm-12 col-12 mb-3"),
                        dbc.Col([
                            btnFilter(),
                            offcanvas(componentes=[
                                select(ids="year",texto="Año",value=sorted(df_ventas_d['Año'].unique())[-1]),
                                select(ids="cliente",texto="Cliente"),
                                select(ids="cultivo",texto="Cultivo"),
                                select(ids="variedad",texto="Variedad"),
                                radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                          children=[dmc.Radio(label='S/', value='Soles'),
                                                    dmc.Radio(label='$', value='Dolares'),
                                          ]),
                            ]),
                        ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                        
                        
                    ]),
              

            dbc.Row([
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-1'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([
                    dbc.Row([
                       dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2_1'),className="shadow-sm"))],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                       dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2_2'),className="shadow-sm"))],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                       dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2_3'),className="shadow-sm"))],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                       #dbc.Col([Graph_notshadow(graph2_4)],width=3,className="col-xl-3 col-md-6 col-sm-12 col-12 mb-3")
                    ]),
                    dbc.Row([
                       dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-3'),className="shadow-sm"))],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                    ])
                ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3")
            ]),

            dbc.Row([
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-4'),className="shadow-sm"))],width=7,className="col-xl-7 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([
                #    dcc.Download(id="download"),
                loadingOverlay(html.Div(id='graph-5',style={'max-height': '350px','overflow': "auto"}),)
                    
                    
                #    dbc.Row(
                #            [
                                
                #                dbc.Col(
                #                    [
                #                        dbc.Button(
                #                            "Descargar Datos", id="btn_excel"
                #                        ),
                #                    ]
                #                ),
                #            ]
                #        ),
                ],width=5,className="col-xl-5 col-md-12 col-sm-12 col-12 mb-3")
            ]),
            html.Div(id='comentario')
        ])
    offcanvasAction(app)

    @app.callback(
            Output("year","data"),
            Output("cultivo","data"),
            Output("variedad","data"),
            Output("cliente","data"),
            #Output('filter-data', 'data'),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            #Input("cultivo","value"),
            Input("cliente","value"),
            
            )
    def filter_ventas(year,cultivo,variedad,cliente):
        df_ventas=df_ventas_d.groupby(['Año','Cliente','Cultivo','Variedad'])[['Importe en Soles']].sum().reset_index()

        if year==None and cultivo == None and variedad== None and cliente==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None:    
            options=df_ventas[df_ventas['Año']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None:    
            options=df_ventas[df_ventas['Cultivo']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None:    
            options=df_ventas[df_ventas['Variedad']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None:    
            options=df_ventas[df_ventas['Cliente']==cliente]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cliente']==cliente)]

        
        elif year==None and cultivo != None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]

        elif year==None and cultivo != None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)]


        option_year=[{'label': i, 'value': i} for i in options['Año'].unique()] 
        option_cultivo=[{'label': i, 'value': i} for i in options['Cultivo'].unique()] 
        option_variedad=[{'label': i, 'value': i} for i in options['Variedad'].unique()] 
        option_cliente=[{'label': i, 'value': i} for i in options['Cliente'].unique()] 
        return option_year,option_cultivo,option_variedad,option_cliente
    
    @app.callback(
        Output("comentario","children"),
        Input("year","value"),)
    def staff(year):
        if staff_comment == 1 or staff_comment == True:
            trash=dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.Div('Esto es una prueba')
                ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            ])
        else :
            trash=html.Div('-')
        return trash

    @app.callback(
            
            Output("title","children"),
            Output("subtitle","children"),
            Input("year","value"),
            Input("cultivo","value"),
            Input("cliente","value"),
            Input("radio-moneda","value"),
            
            )
    def title_ventas(year,cultivo,cliente,moneda):
        general='Ventas'+' '+str(moneda)
        if year == None:
            title=general
        else:
            title=general+' '+str(year)
        if cliente == None and cultivo == None:
            subtitle=''
        elif cliente != None and cultivo == None:
            subtitle=str(cliente)
        elif cliente != None and cultivo != None:
            subtitle=str(cliente)+' '+str(cultivo)
            
        return title,subtitle

    @app.callback(
            Output("graph-1","figure"),
            Output("graph2_1","figure"),
            Output("graph2_2","figure"),
            Output("graph2_3","figure"),
            Output("graph-3","figure"),
            Output("graph-4","figure"),
            Output("graph-5","children"),
            #Output("graph-5","columns"),
            
            #Output("download", "data"),
            #Output("graph-st","figure"),
            #Output("1","figure"),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            Input("cliente","value"),
            Input("radio-moneda","value"),
            #Input("btn_csv", "n_clicks"),
            #State("dropdown", "value"),
            #prevent_initial_call=True,
            #Input(ThemeSwitchAIO.ids.switch("theme"), "value"),

            )
    def ventas(year,cultivo,variedad,cliente,radio):#,n_clicks_btn, download_type
            if year==None and cultivo == None and variedad== None and cliente==None:
                options=df_ventas_d

            elif year!=None and cultivo == None and variedad== None and cliente==None:    
                options=df_ventas_d[df_ventas_d['Año']==year]
            elif year==None and cultivo != None and variedad== None and cliente==None:    
                options=df_ventas_d[df_ventas_d['Cultivo']==cultivo]
            
            elif year==None and cultivo == None and variedad!= None and cliente==None:    
                options=df_ventas_d[df_ventas_d['Variedad']==variedad]
            
            elif year==None and cultivo == None and variedad== None and cliente!=None:    
                options=df_ventas_d[df_ventas_d['Cliente']==cliente]
            
            elif year!=None and cultivo != None and variedad== None and cliente==None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Cultivo']==cultivo)]
            
            elif year!=None and cultivo == None and variedad!= None and cliente==None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Variedad']==variedad)]
            
            elif year!=None and cultivo == None and variedad== None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Cliente']==cliente)]

            
            elif year==None and cultivo != None and variedad== None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Cliente']==cliente)]
            
            elif year==None and cultivo != None and variedad!= None and cliente==None:
                options=df_ventas_d[(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Variedad']==variedad)]
            
            elif year==None and cultivo == None and variedad!= None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Variedad']==variedad)&(df_ventas_d['Cliente']==cliente)]
            
            elif year!=None and cultivo != None and variedad!= None and cliente==None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Variedad']==variedad)]

            elif year!=None and cultivo != None and variedad== None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Cliente']==cliente)]
            
            elif year!=None and cultivo == None and variedad!= None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Variedad']==variedad)&(df_ventas_d['Cliente']==cliente)]

            elif year==None and cultivo != None and variedad!= None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Variedad']==variedad)&(df_ventas_d['Cliente']==cliente)]
            
            elif year!=None and cultivo != None and variedad!= None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Variedad']==variedad)&(df_ventas_d['Cliente']==cliente)&(df_ventas_d['Año']==year)]

            if radio=='Soles':
                importe='Importe en Soles'
            else:
                importe='Importe en Dolares'
            #df_filter=options.groupby([ejex])[[color]].sum().reset_index()#,color
            df_productos_top15=options.groupby(['Producto'])[[importe]].sum().sort_values(importe,ascending=True).tail(15).reset_index()
            top_productos = go.Figure()
            top_productos.add_trace(go.Bar(x=df_productos_top15[importe],y=df_productos_top15['Producto'],text=df_productos_top15[importe],orientation='h',
                                                textposition='outside',texttemplate='%{text:.2s}',#,marker_color=px.colors.qualitative.Dark24,#marker_color=colors,
                                                hovertemplate =
                                                    '<br><b>Producto</b>:%{y}'+
                                                    '<br><b>Importe($)</b>: %{x}<br>',
                                                marker_color="#145f82",
                                                hoverlabel=dict(
                                                font_size=10,
                                                ),
                                                name=''
                                            ))#.2s

            top_productos.update_layout(title={'text':'Productos más Vendidos'},titlefont={'size': 15},template='none')
            top_productos.update_layout(autosize=True,height=490,margin=dict(l=200,r=20,b=40,t=40),yaxis=dict(titlefont_size=7,tickfont_size=7))
            top_productos.update_layout(xaxis_title=radio,yaxis_title="",legend_title="")
            top_productos.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
            
            df_mes_top=options.groupby(['Mes','MONTH'])[[importe,'Peso']].sum().reset_index().sort_values('MONTH',ascending=True)
            df_mes_top['Promedio']=df_mes_top[importe].mean()
            df_mes_top=df_mes_top[(df_mes_top[importe]!=0) & (df_mes_top['Peso']!=0)]
            mes_top = go.Figure()
            mes_top.add_trace(go.Bar(x=df_mes_top['Mes'],y=df_mes_top[importe],text=df_mes_top[importe],orientation='v',textposition='outside',texttemplate='%{text:.2s}',name='Importe',marker_color="#145f82"))#,marker_color="#01B8AA"
            mes_top.update_layout(
                                        title={
                                                'text':'Ventas Mensuales por Kilogramos',
                                                    #'y': 0.93,
                                                    #'x': 0.5,
                                                    #'xanchor': 'center',
                                                    #'yanchor': 'top',
                                        },
                                        titlefont={'size': 15},
                                        uniformtext_minsize=8,# uniformtext_mode='hide',
                                        template='none')
            mes_top.update_layout(
                        autosize=True,
                        #width=100,
                        height=360,
                        margin=dict(
                            l=50,
                            r=60,
                            b=50,
                            t=70,

                        ),

                        xaxis=dict(
                            
                            showticklabels=True,

                            tickfont=dict(
                                    #family='Arial',
                                    #color='black',
                                    size=11
                                    )
                        ),
                        yaxis=dict(
                            #gridcolor='#F2F2F2',
                            #showline=True,
                            #showgrid=True,
                            #ticks='outside',
                            tickfont=dict(
                                    #family='Arial',
                                    #color='black',
                                    size=11
                                    )
                        )
                        
                        ) 
            if df_mes_top['Peso'].sum() != 0:
            
                mes_top.add_trace(go.Scatter(
                                x=df_mes_top['Mes'],
                                y=df_mes_top['Peso'],
                                name="Kilogramos",
                                yaxis="y4",
                                text=df_mes_top['Peso'],
                                #marker_color="#1f1587",
                                textposition='bottom right',
                                texttemplate='{text:.2s}'
                            ))
                
                mes_top.update_layout(
                            
                            yaxis4=dict(
                                    
                                    title="Kilogramos",
                                    titlefont=dict(
                                        #color="#1f1587"
                                    ),
                                    tickfont=dict(
                                        #color="#1f1587"
                                    ),
                                    anchor="x",
                                    overlaying="y",
                                    side="right",
                                    titlefont_size=12,
                                    tickfont_size=12,
                                    #tickprefix="Peso (kg)",
                                    #showtickprefix="last",
                                ),
                        )

                
 
            mes_top.update_layout(
                        showlegend=True,
                        legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1

                        )

                    )
                    
            mes_top.add_trace(go.Scatter(
                x=df_mes_top['Mes'],
                y=df_mes_top['Promedio'],
                name="Promedio",
                mode='lines',
                #yaxis="y4",
                #text=df_mes_top['PESONETO_PRODUCTO'],
                #marker_color="#1f1587",
                textposition='bottom right',
                texttemplate='{text:.2s}'
            ))
            mes_top.update_layout(xaxis_title="",yaxis_title=radio,legend_title="")
            mes_top.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
            #df_year_cultivo=options.groupby(['Año','Cultivo'])[[importe]].sum().reset_index()
            #df_year_cultivo=df_year_cultivo[(df_year_cultivo[importe]!=0)]
            #year_group = px.bar(df_year_cultivo, x="Año", y=importe, 
            #         color="Cultivo", barmode="group",height=280,title='Importe de Cultivos por Año',template='none')
            #year_group.update_layout#(update_layout(height=280,)
            cantidad_productos=len(options['Producto'])
            cantidad_peso=(options['Peso'].sum()/1000)
            cantidad_clientes=len(options['Cliente'].unique())

            graph4=options.groupby(['Pais'])[[importe,'Peso']].sum().reset_index().sort_values(importe,ascending=True)
            pais_importe_peso = go.Figure()
            pais_importe_peso.add_trace(go.Bar(x=graph4['Pais'],y=graph4[importe],text=graph4[importe],orientation='v',textposition='outside',texttemplate='%{text:.2s}',name=importe,marker_color="#145f82"))#,marker_color="#01B8AA"
            pais_importe_peso.update_layout(
                                        title={
                                                'text':'Ventas por País/Kilogramos',
                                                    #'y': 0.93,
                                                    #'x': 0.5,
                                                    #'xanchor': 'center',
                                                    #'yanchor': 'top',
                                        },
                                        titlefont={'size': 15},
                                        uniformtext_minsize=8,# uniformtext_mode='hide',
                                        template='none')
            pais_importe_peso.update_layout(
                        autosize=True,
                        #width=100,
                        height=350,
                        margin=dict(
                            l=50,
                            r=50,
                            b=100,
                            t=80,

                        ),

                        xaxis=dict(
                            
                            showticklabels=True,

                            tickfont=dict(
                                    #family='Arial',
                                    #color='black',
                                    size=11
                                    )
                        ),
                        yaxis=dict(
                            #gridcolor='#F2F2F2',
                            #showline=True,
                            #showgrid=True,
                            #ticks='outside',
                            tickfont=dict(
                                    #family='Arial',
                                    #color='black',
                                    size=11
                                    )
                        )
                        
                        ) 
            pais_importe_peso.add_trace(go.Scatter(
                        x=graph4['Pais'],
                        y=graph4['Peso'],
                        name="Kilogramos",
                        mode='lines',
                        yaxis="y4",
                        text=graph4['Peso'],
                        #marker_color="#1f1587",
                        textposition='bottom right',
                        texttemplate='{text:.2s}'
                    ))
            pais_importe_peso.update_layout(
                    
                    yaxis4=dict(
                            
                            title="Kilogramos",
                            titlefont=dict(
                                #color="#1f1587"
                            ),
                            tickfont=dict(
                                #color="#1f1587"
                            ),
                            anchor="x",
                            overlaying="y",
                            side="right",
                            titlefont_size=12,
                            tickfont_size=12,
                            #tickprefix="Peso (kg)",
                            #showtickprefix="last",
                        ),
                )
            pais_importe_peso.update_layout(
                    showlegend=True,
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1

                    )

                )
            pais_importe_peso.update_layout(xaxis_title="PAIS",yaxis_title=radio,legend_title="")
            pais_importe_peso.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
            df_table=options.groupby(['Pais','Cultivo'])[[importe,'Peso']].sum().reset_index().sort_values(importe,ascending=True)
            df_table=df_table.rename(columns={'Peso':'Kg',importe:'Importe'})
            table=TableDtScrolling_no_color(df_table,'10px')
            #col=[{"name": c, "id": c,"type": "numeric", "format": Format(group=",", precision=2,scheme="f")} for c in df_table],
            #if download_type == "csv":
            #    files= dcc.send_data_frame(df_table.to_csv, "table.csv")
            #else:
            #    files= dcc.send_data_frame(df_table.to_excel, "table.xlsx")
            return top_productos,card_ventas(cantidad_productos,None,"N° de Ventas"),card_ventas(cantidad_peso,None,"Toneladas Vendidas"),card_ventas(cantidad_clientes,None,"N° de Clientes"),mes_top,pais_importe_peso,table#,col#,files
   # @app.callback(
   # Output("download", "data"),
   # Input("btn_excel", "n_clicks"),
   # prevent_initial_call=True,
   # )
   # def func(n_clicks):
        #if download_type == "csv":
            #    files= dcc.send_data_frame(df_table.to_csv, "table.csv")
            #else:
            #    files= dcc.send_data_frame(df_table.to_excel, "table.xlsx")
   #     df=df_ventas.groupby(['Producto'])[['Importe en Soles']].sum().reset_index()
   #     return dcc.send_data_frame( df.to_excel, "test.xlsx", sheet_name="Sheet_name_1")
def ventas2(empresa,staff_comment):
    
    df_ventas_expo=dataVentasEmpresa(empresa)
    df_ventas=changeVentasCol(df_ventas_expo)
    df_ventas_d=df_ventas.groupby(['Año','Cliente','Cultivo','Variedad'])[['Importe en Soles']].sum().reset_index()

    app = DjangoDash('dashventas2', external_stylesheets=[url_theme1, dbc.icons.BOOTSTRAP, dbc_css])#
    app.layout = html.Div([
            dbc.Row([
                        dbc.Col([
                            btnFilter(),
                            offcanvas(componentes=[
                                select(ids="year",texto="Año",value=sorted(df_ventas_d['Año'].unique())[-1]),
                                select(ids="cliente",texto="Cliente"),
                                select(ids="cultivo",texto="Cultivo"),
                                select(ids="variedad",texto="Variedad"),
                                radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                          children=[dmc.Radio(label='S/', value='Soles'),
                                                    dmc.Radio(label='$', value='Dolares'),
                                          ]),
                            ]),
                            
                            
                        ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([
                            html.H3(id='title', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                            html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})

                        ],width=10,className="col-xl-10 col-md-10 col-sm-12 col-12 mb-3")
                    ]),
            dbc.Row([
                
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-2'),className="shadow-sm"))],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
            ]),
            #type="default"
            dbc.Row([
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-3'),className="shadow-sm"))],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-1'),className="shadow-sm"))],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                #dbc.Col([dcc.Loading(children=dbc.Card(dcc.Graph(id='graph-4')))],width=5,className="col-xl-5 col-md-12 col-sm-12 col-12 mb-3")
            ]),
            html.Div(id='comentario')
        ])
    offcanvasAction(app)

    @app.callback(
        Output("year","data"),
        Output("cultivo","data"),
        Output("variedad","data"),
        Output("cliente","data"),
        #Output('filter-data', 'data'),
        Input("year","value"),
        Input("cultivo","value"),
        Input("variedad","value"),
        #Input("cultivo","value"),
        Input("cliente","value"),
            
            )
    def filter_ventas(year,cultivo,variedad,cliente):
            

            if year==None and cultivo == None and variedad== None and cliente==None:
                options=df_ventas_d

            elif year!=None and cultivo == None and variedad== None and cliente==None:    
                options=df_ventas_d[df_ventas_d['Año']==year]
            elif year==None and cultivo != None and variedad== None and cliente==None:    
                options=df_ventas_d[df_ventas_d['Cultivo']==cultivo]
            
            elif year==None and cultivo == None and variedad!= None and cliente==None:    
                options=df_ventas_d[df_ventas_d['Variedad']==variedad]
            
            elif year==None and cultivo == None and variedad== None and cliente!=None:    
                options=df_ventas_d[df_ventas_d['Cliente']==cliente]
            
            elif year!=None and cultivo != None and variedad== None and cliente==None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Cultivo']==cultivo)]
            
            elif year!=None and cultivo == None and variedad!= None and cliente==None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Variedad']==variedad)]
            
            elif year!=None and cultivo == None and variedad== None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Cliente']==cliente)]

            
            elif year==None and cultivo != None and variedad== None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Cliente']==cliente)]
            
            elif year==None and cultivo != None and variedad!= None and cliente==None:
                options=df_ventas_d[(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Variedad']==variedad)]
            
            elif year==None and cultivo == None and variedad!= None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Variedad']==variedad)&(df_ventas_d['Cliente']==cliente)]
            
            elif year!=None and cultivo != None and variedad!= None and cliente==None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Variedad']==variedad)]

            elif year!=None and cultivo != None and variedad== None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Cliente']==cliente)]
            
            elif year!=None and cultivo == None and variedad!= None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Año']==year)&(df_ventas_d['Variedad']==variedad)&(df_ventas_d['Cliente']==cliente)]

            elif year==None and cultivo != None and variedad!= None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Variedad']==variedad)&(df_ventas_d['Cliente']==cliente)]
            
            elif year!=None and cultivo != None and variedad!= None and cliente!=None:
                options=df_ventas_d[(df_ventas_d['Cultivo']==cultivo)&(df_ventas_d['Variedad']==variedad)&(df_ventas_d['Cliente']==cliente)&(df_ventas_d['Año']==year)]


            option_year=[{'label': i, 'value': i} for i in options['Año'].unique()] 
            option_cultivo=[{'label': i, 'value': i} for i in options['Cultivo'].unique()] 
            option_variedad=[{'label': i, 'value': i} for i in options['Variedad'].unique()] 
            option_cliente=[{'label': i, 'value': i} for i in options['Cliente'].unique()] 
            return option_year,option_cultivo,option_variedad,option_cliente
    
    @app.callback(
        Output("comentario","children"),
        Input("year","value"),)
    def staff(year):
        if staff_comment == 1 or staff_comment == True:
            trash=dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.Div('Esto es una prueba')
                ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            ])
        else :
            trash=html.Div('-')
        return trash

    @app.callback(
            
            Output("title","children"),
            Output("subtitle","children"),
            Input("year","value"),
            Input("cultivo","value"),
            Input("cliente","value"),
            Input("radio-moneda","value"),
            
            )
    def title_ventas(year,cultivo,cliente,moneda):
        general='Ventas'+' '+str(moneda)
        if year == None:
            title=general
        else:
            title=general+' '+str(year)
        if cliente == None and cultivo == None:
            subtitle=''
        elif cliente != None and cultivo == None:
            subtitle=str(cliente)
        elif cliente != None and cultivo != None:
            subtitle=str(cliente)+' '+str(cultivo)
            
        return title,subtitle


    @app.callback(
            Output("graph-1","figure"),
            Output("graph-2","figure"),
            Output("graph-3","figure"),
            #Output("graph-4","figure"),
            #Output("graph-st","figure"),
            #Output("1","figure"),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            Input("cliente","value"),
            Input("radio-moneda","value"),
            #Input(ThemeSwitchAIO.ids.switch("theme"), "value"),

            )
    def ventas(year,cultivo,variedad,cliente,radio):
            if year==None and cultivo == None and variedad== None and cliente==None:
                options=df_ventas

            elif year!=None and cultivo == None and variedad== None and cliente==None:    
                options=df_ventas[df_ventas['Año']==year]
            elif year==None and cultivo != None and variedad== None and cliente==None:    
                options=df_ventas[df_ventas['Cultivo']==cultivo]
            
            elif year==None and cultivo == None and variedad!= None and cliente==None:    
                options=df_ventas[df_ventas['Variedad']==variedad]
            
            elif year==None and cultivo == None and variedad== None and cliente!=None:    
                options=df_ventas[df_ventas['Cliente']==cliente]
            
            elif year!=None and cultivo != None and variedad== None and cliente==None:
                options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)]
            
            elif year!=None and cultivo == None and variedad!= None and cliente==None:
                options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)]
            
            elif year!=None and cultivo == None and variedad== None and cliente!=None:
                options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cliente']==cliente)]

            
            elif year==None and cultivo != None and variedad== None and cliente!=None:
                options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
            
            elif year==None and cultivo != None and variedad!= None and cliente==None:
                options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]
            
            elif year==None and cultivo == None and variedad!= None and cliente!=None:
                options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
            
            elif year!=None and cultivo != None and variedad!= None and cliente==None:
                options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

            elif year!=None and cultivo != None and variedad== None and cliente!=None:
                options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
            
            elif year!=None and cultivo == None and variedad!= None and cliente!=None:
                options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]

            elif year==None and cultivo != None and variedad!= None and cliente!=None:
                options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
            
            elif year!=None and cultivo != None and variedad!= None and cliente!=None:
                options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)]

                
            if radio=='Soles':
                importe='Importe en Soles'
            else:
                importe='Importe en Dolares'

            graph2=options.groupby(['Sucursal'])[[importe]].sum().reset_index()
            graph1=options.groupby(['Año','Mes','MONTH'])[[importe]].sum().reset_index().sort_values('MONTH',ascending=True)
            #df_ventas_detalle.groupby(['YEAR','MES_TEXT','MONTH'])[['IMPORTEMOF']].sum().reset_index().sort_values('MONTH',ascending=True)
            #graph 1
            fig = px.bar(graph1, x="Mes", y=importe, facet_row="Año",template="none",title="Importe Mensual por Año")#, facet_col="sex"#, color="smoker"
            fig.update_yaxes(matches=None)
            fig.update_layout(autosize=True,height=330,margin=dict(l=60,r=40,b=40,t=50))
            fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
            #graph 2
            fig2 = px.pie(graph2, values=importe, names='Sucursal',template="none",
                title='Ventas por Sucursal',hole=.5
                #hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'}
                )
            fig2.update_traces(textposition='inside', textinfo='percent+label')

            fig2.update_layout(height=340,margin=dict(l=10,r=10,b=20,t=50),showlegend=False)
            fig2.update_layout(paper_bgcolor='#f7f7f7')

            #legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,traceorder="reversed",
            #                    title_font_family="Arial",font=dict(family="Arial",size=8,color="black"),
            #                    bgcolor="white"
            #                    ))  
            
            #graph 3
            graph3=options.groupby(['Cliente'])[[importe,'Peso']].sum().reset_index().sort_values(importe,ascending=True).tail(15)
            cliente_importe_peso = go.Figure()
            cliente_importe_peso.add_trace(go.Bar(x=graph3['Cliente'],y=graph3[importe],text=graph3[importe],orientation='v',textposition='inside',texttemplate='%{text:.2s}',name=importe,marker_color="#145f82"))#,marker_color="#01B8AA"
            cliente_importe_peso.update_layout(
                                        title={
                                                'text':'Ventas por Cliente',
                                                    #'y': 0.93,
                                                    #'x': 0.5,
                                                    #'xanchor': 'center',
                                                    #'yanchor': 'top',
                                        },
                                        titlefont={'size': 15},
                                        uniformtext_minsize=8,# uniformtext_mode='hide',
                                        template='none')
            cliente_importe_peso.update_layout(
                        autosize=True,
                        #width=100,
                        height=350,
                        margin=dict(
                            l=70,
                            r=70,
                            b=100,
                            t=80,

                        ),

                        xaxis=dict(
                            
                            showticklabels=True,

                            tickfont=dict(
                                    #family='Arial',
                                    #color='black',
                                    size=11
                                    )
                        ),
                        yaxis=dict(
                            #gridcolor='#F2F2F2',
                            #showline=True,
                            #showgrid=True,
                            #ticks='outside',
                            tickfont=dict(
                                    #family='Arial',
                                    #color='black',
                                    size=11
                                    )
                        )
                        
                        ) 
            cliente_importe_peso.add_trace(go.Scatter(
                        x=graph3['Cliente'],
                        y=graph3['Peso'],
                        name="Kilogramos",
                        mode='lines',
                        yaxis="y4",
                        text=graph3['Peso'],
                        #marker_color="#1f1587",
                        textposition='bottom right',
                        texttemplate='{text:.2s}'
                    ))
            cliente_importe_peso.update_layout(
                    
                    yaxis4=dict(
                            
                            title="Kilogramos",
                            titlefont=dict(
                                #color="#1f1587"
                            ),
                            tickfont=dict(
                                #color="#1f1587"
                            ),
                            anchor="x",
                            overlaying="y",
                            side="right",
                            titlefont_size=12,
                            tickfont_size=12,
                            #tickprefix="Peso (kg)",
                            #showtickprefix="last",
                        ),
                )
            cliente_importe_peso.update_layout(
                    showlegend=True,
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1

                    )

                )
            cliente_importe_peso.update_layout(xaxis_title="Cliente",yaxis_title=radio,legend_title="")
            cliente_importe_peso.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')

            graph4=options.groupby(['Cultivo'])[[importe,'Peso']].sum().reset_index().sort_values(importe,ascending=True)
            cultivo_importe_peso = go.Figure()
            cultivo_importe_peso.add_trace(go.Bar(x=graph4['Cultivo'],y=graph4[importe],text=graph4[importe],orientation='v',textposition='inside',texttemplate='%{text:.2s}',name=importe,marker_color="#125745"))#
            cultivo_importe_peso.update_layout(
                                        title={
                                                'text':'Ventas y Kilogramos por Cultivo',
                                                    #'y': 0.93,
                                                    #'x': 0.5,
                                                    #'xanchor': 'center',
                                                    #'yanchor': 'top',
                                        },
                                        titlefont={'size': 15},
                                        uniformtext_minsize=8,# uniformtext_mode='hide',
                                        template='none')
            cultivo_importe_peso.update_layout(
                        autosize=True,
                        #width=100,
                        height=350,
                        margin=dict(
                            l=60,
                            r=50,
                            b=50,
                            t=80,

                        ),

                        xaxis=dict(
                            
                            showticklabels=True,

                            tickfont=dict(
                                    #family='Arial',
                                    #color='black',
                                    size=11
                                    )
                        ),
                        yaxis=dict(
                            #gridcolor='#F2F2F2',
                            #showline=True,
                            #showgrid=True,
                            #ticks='outside',
                            tickfont=dict(
                                    #family='Arial',
                                    #color='black',
                                    size=11
                                    )
                        )
                        
                        ) 
            cultivo_importe_peso.add_trace(go.Scatter(
                        x=graph4['Cultivo'],
                        y=graph4['Peso'],
                        name="Kilogramos",
                        mode='lines',
                        yaxis="y4",
                        text=graph4['Peso'],
                        #marker_color="#1f1587",
                        textposition='bottom right',
                        texttemplate='{text:.2s}'
                    ))
            cultivo_importe_peso.update_layout(
                    
                    yaxis4=dict(
                            
                            title="Kilogramos",
                            titlefont=dict(
                                #color="#1f1587"
                            ),
                            tickfont=dict(
                                #color="#1f1587"
                            ),
                            anchor="x",
                            overlaying="y",
                            side="right",
                            titlefont_size=12,
                            tickfont_size=12,
                            #tickprefix="Peso (kg)",
                            #showtickprefix="last",
                        ),
                )
            cultivo_importe_peso.update_layout(
                    showlegend=True,
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1

                    )

                )
            cultivo_importe_peso.update_layout(xaxis_title="Cultivo",yaxis_title=radio,legend_title="")
            cultivo_importe_peso.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
            return fig2,cliente_importe_peso,cultivo_importe_peso#,fig

def contenedoresExportados1(empresa,staff_comment):
    df_expo=dataContenedoresEmpresa(empresa)
    

    app = DjangoDash('contenedores_exportados_1', external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([
        dbc.Row([
            dbc.Col([
                #html.H3(id='title-cont-export'),
                title(ids='title-cont-export',order=2)
            ],width=9,className="col-xl-9 col-md-9 col-sm-12 col-12 mb-3"),
            dbc.Col([
                select(ids='year',texto='Año',data=[{'label': i, 'value': i} for i in df_expo['YEAR'].unique()],value=df_expo['YEAR'].unique()[-1])
                
                      
            ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
        ]),
        
        dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-1'),className="shadow-sm"))
                
            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-2'),className="shadow-sm")  )
                          
            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-3'),className="shadow-sm"))
                
            ],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-4'),className="shadow-sm"))
                         
            ],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-5'),className="shadow-sm"))
                
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
        ]),
        html.Div(id='comentario')
    ])

    @app.callback(
        Output("comentario","children"),
        Input("year","value"),)
    def staff(year):
        if staff_comment == 1 or staff_comment == True:
            trash=dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.Div('Esto es una prueba')
                ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            ])
        else :
            trash=html.Div('-')
        return trash

    @app.callback(
            Output("graph-1","figure"),
            Output("graph-2","figure"),
            Output("graph-3","figure"),
            Output("graph-4","figure"),
            Output("graph-5","figure"),
            Output('title-cont-export','children'),
            Input("year","value"),
            
        )
    def ctrl(year):
        if year == None:
            df_control_expo=df_expo
            total_cont=df_control_expo['YEAR'].count()
            title=f"INDICADORES CAMPAÑA - CONTENEDORES EXPORTADOS A LA FECHA {total_cont}"
        elif year != None:
            df_control_expo=df_expo[df_expo['YEAR']==year]
            total_cont=df_control_expo['YEAR'].count()
            title=f"INDICADORES CAMPAÑA {year}- CONTENEDORES EXPORTADOS A LA FECHA {total_cont}"
           

        
        #NUMERO DE CONTENEDORES POR VARIEDAD      
        df_n_cont_var=df_control_expo.groupby(['VARIEDAD'])[['NRO_CONTENEDOR']].count().sort_values('NRO_CONTENEDOR',ascending=False).reset_index()
        graph1=bar_ctrl(df_n_cont_var,'VARIEDAD','NRO_CONTENEDOR','NRO_CONTENEDOR','VARIEDAD','# Contenedores por Variedad','relative',False,None)

        #NUMERO DE CONTENEDORES POR CONTINENTE 
        df_n_cont_conti=df_control_expo.groupby(['CONTINENTE'])[['NRO_CONTENEDOR']].count().sort_values('NRO_CONTENEDOR',ascending=False).reset_index()
        graph2=bar_ctrl(df_n_cont_conti,'CONTINENTE','NRO_CONTENEDOR','NRO_CONTENEDOR','CONTINENTE','# Contenedores por Continente','relative',False,None)

        #NUMERO DE CONTENEDORES POR CONTIENENTE POR VARIEDAD
        df_n_cont_conti_var=df_control_expo.groupby(['CONTINENTE','VARIEDAD'])[['NRO_CONTENEDOR']].count().sort_values('NRO_CONTENEDOR',ascending=False).reset_index()
        graph3=bar_ctrl(df_n_cont_conti_var,'CONTINENTE','NRO_CONTENEDOR','NRO_CONTENEDOR','VARIEDAD','# Contenedores por Continente por Variedad','group',True,None)

        #NUMERO DE CONTENEDORES POR PAIS
        df_n_cont_pais=df_control_expo.groupby(['PAIS'])[['NRO_CONTENEDOR']].count().sort_values('NRO_CONTENEDOR',ascending=False).reset_index()
        graph4=bar_ctrl(df_n_cont_pais,'NRO_CONTENEDOR','PAIS','NRO_CONTENEDOR','PAIS','# Contenedores por Países','relative',False,None,'h')

        #NUMERO DE CONTENEDORES POR PAISES POR VARIEDAD
        df_n_cont_pais_var=df_control_expo.groupby(['PAIS','VARIEDAD'])[['NRO_CONTENEDOR']].count().sort_values('NRO_CONTENEDOR',ascending=True).reset_index()
        graph5=bar_ctrl(df_n_cont_pais_var,'PAIS','NRO_CONTENEDOR','NRO_CONTENEDOR','VARIEDAD','# Contenedores por Países por Variedad','group',True,None)
        
        return graph1,graph2,graph3,graph4,graph5,title

def contenedoresExportados2(empresa,staff_comment):
    df_expo=dataContenedoresEmpresa(empresa)

    app = DjangoDash('contenedores_exportados_2', external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([
        dbc.Row([
            dbc.Col([
                #html.H3(id='title-cont-export'),
                title(ids='title-cont-export',order=2)
            ],width=9,className="col-xl-9 col-md-9 col-sm-12 col-12 mb-3"),
            dbc.Col([
                select(ids='year',texto='Año',data=[{'label': i, 'value': i} for i in df_expo['YEAR'].unique()],value=df_expo['YEAR'].unique()[-1])
                
                      
            ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
        ]),
        
        dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-1'),className="shadow-sm"))
                
            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-2'),className="shadow-sm") )
                           
            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-3'),className="shadow-sm"))
                
            ],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-4'),className="shadow-sm") )
                           
            ],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-5'),className="shadow-sm"))
                
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
        ]),
        html.Div(id='comentario')

    ])
    @app.callback(
        Output("comentario","children"),
        Input("year","value"),)
    def staff(year):
        if staff_comment == 1 or staff_comment == True:
            trash=dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.Div('Esto es una prueba')
                ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            ])
        else :
            trash=html.Div('-')
        return trash
    @app.callback(
            Output("graph-1","figure"),
            Output("graph-2","figure"),
            Output("graph-3","figure"),
            Output("graph-4","figure"),
            Output("graph-5","figure"),
            Output('title-cont-export','children'),
            Input("year","value"),
            
        )
    def ctrl(year):
        if year == None:
            df_control_expo=df_expo
            total_kg=df_control_expo['CANTIDAD_KG'].sum()
            title=f"INDICADORES CAMPAÑA - KG EXPORTADOS: {total_kg}"
        elif year != None:
            df_control_expo=df_expo[df_expo['YEAR']==year]
            total_kg=df_control_expo['CANTIDAD_KG'].sum()
            title=f"INDICADORES CAMPAÑA {year}- KG EXPORTADOS: {total_kg}"
        #NUMERO DE CONTENEDORES POR VARIEDAD      
        #df_n_cont_var=df_control_expo.groupby(['VARIEDAD'])[['NRO_CONTENEDOR']].count().sort_values('NRO_CONTENEDOR',ascending=False).reset_index()
        #graph1=bar_ctrl(df_n_cont_var,'VARIEDAD','NRO_CONTENEDOR','NRO_CONTENEDOR','VARIEDAD','# Contenedores por Variedad','relative',False)
        df_kg_var=df_control_expo.groupby(['VARIEDAD'])[['CANTIDAD_KG']].sum().sort_values('CANTIDAD_KG',ascending=False).reset_index()
        graph1=bar_ctrl(df_kg_var,'VARIEDAD','CANTIDAD_KG','CANTIDAD_KG','VARIEDAD','Kg por Variedad','relative',False,'%{text:,}')

        df_kg_conti=df_control_expo.groupby(['CONTINENTE'])[['CANTIDAD_KG']].sum().sort_values('CANTIDAD_KG',ascending=False).reset_index()
        graph2=bar_ctrl(df_kg_conti,'CONTINENTE','CANTIDAD_KG','CANTIDAD_KG','CONTINENTE','# Kg Exportados por Continente','relative',False,'%{text:,}')

        df_kg_pais=df_control_expo.groupby(['PAIS'])[['CANTIDAD_KG']].sum().sort_values('CANTIDAD_KG',ascending=False).reset_index()
        graph3=bar_ctrl(df_kg_pais,'CANTIDAD_KG','PAIS','CANTIDAD_KG','PAIS','# Kg Exportados por País','relative',False,'%{text:,}','h')

        df_kg_conti_var=df_control_expo.groupby(['CONTINENTE','VARIEDAD'])[['CANTIDAD_KG']].sum().sort_values('CANTIDAD_KG',ascending=False).reset_index()
        graph4=bar_ctrl(df_kg_conti_var,'CONTINENTE','CANTIDAD_KG','CANTIDAD_KG','VARIEDAD','# Kg por Continente/Variedad','group',True,'%{text:,}')

        df_kg_pais_var=df_control_expo.groupby(['PAIS','VARIEDAD'])[['CANTIDAD_KG']].sum().sort_values('CANTIDAD_KG',ascending=True).reset_index()
        graph5=bar_ctrl(df_kg_pais_var,'PAIS','CANTIDAD_KG','CANTIDAD_KG','VARIEDAD','# Kg por Paises por Variedad','group',True,'%{text:,}')
        return graph1,graph2,graph3,graph4,graph5,title