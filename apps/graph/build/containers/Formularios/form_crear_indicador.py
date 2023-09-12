from dash.dash_table.Format import Format, Group, Scheme, Symbol
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from apps.graph.data.data import *
from apps.graph.data.transform_finanzas import *
from apps.graph.build.components.bootstrap_components.layout import Column
from apps.graph.build.containers.Created.created import EvaluarFormula,figure__line
from apps.graph.save import RegistrarIndicador

from dash import html,dcc

from apps.graph.build.components.mantine_react_components.title import *
from apps.graph.models import Indicador,TipoIndicador

from apps.graph.build.components.mantine_react_components.selects import *
from apps.graph.build.components.mantine_react_components.textbox import *
from apps.graph.build.components.mantine_react_components.checkbox import *
from apps.graph.build.components.mantine_react_components.button import *
from apps.graph.build.components.mantine_react_components.alert import *
from apps.graph.build.components.mantine_react_components.spoiler import *
from apps.graph.build.components.mantine_react_components.loaders import loadingOverlay


from apps.graph.data.transform_finanzas import *
from apps.graph.data.gets import getApi


#api_nisira_finanzas='http://69.64.92.160:3005/api/consulta/nsp_eeff_json'
#finanzas_lista_nisira=getApi(api_nisira_finanzas,token_nisira)
#df_owo=pd.DataFrame(finanzas_lista_nisira)
df_bc_nisira=pd.read_parquet('finanzas.parquet', engine='pyarrow')
#df_bc_nisira=pd.read_parquet('bc_paraiso.parquet', engine='pyarrow')
def figure__line2(x,y,y2,name,namex,namey,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3):#,esperado,permitido,limite
    fig = go.Figure()

    #fig.update_layout(yaxis_tickformat = '.0%')
    fig.add_trace(go.Scatter(x=x, y=y,text=y,textposition="bottom center",
                        mode='lines+markers',
                        name=namex,line=dict( width=3)))
    fig.add_trace(go.Scatter(x=x, y=y2,
                        mode='lines',
                        name=namey,line=dict( width=2)))
    fig.update_layout(
        autosize=True,
        #width=,
        height=390,
        margin=dict(
            l=60,
            r=40,
            b=60,
            t=70,
            #pad=4,
            autoexpand=True

        ),
        legend=dict(orientation= 'h',yanchor="bottom",xanchor='center', x= 0.5, y= 1,font=dict(size=10,color="black"),),#family="Courier",
    )
    
    fig.update_layout(template='none', title=name)
    #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    fig.add_hrect(y0=rango_desde_1,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.2)
    fig.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.2)
    fig.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.2)
    fig.add_layout_image(
        dict(
            source="https://www.nisira.com.pe/images/logo.png",
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=2,
            sizey=2,
            sizing="stretch",
            opacity=0.5,
            layer="below")
        )
    #fig.add_hrect(y0=limite,y1=maximo, line_width=0, fillcolor="#fc2100", opacity=0.2)

    
    return fig
def formIndicador(empresa,usuario):#empresa,usuario
    """"""
    
    """"""
    #df_bcomprobacion=dataBcEmpresa(empresa)
    df_bcomprobacion=df_bc_nisira.copy()

    idind_list=list(TipoIndicador.objects.all().values_list('id',flat=True))
    tipoind_list=list(TipoIndicador.objects.all().values_list('name_tipo_indicador',flat=True))
    list_dicts=[]
    for (i,j) in zip(tipoind_list,idind_list):
        list_dicts.append({'label': i, 'value': j})

    app = DjangoDash('form_indicador', external_stylesheets=[dbc.themes.BOOTSTRAP])#
    app.layout = html.Div([
    dbc.Row([
            Column(content=[title(text="Crear Indicador Financiero")],size=12),
             
    ]),
    dbc.Row([
        dbc.Col([ 
                 
                        dbc.Row([
                            dbc.Col([
                                select(ids="tipo-indicador",texto="Tipo de Indicador",place="Seleccione Tipo",data=list_dicts,size='sm'),
                            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-1"),
                            dbc.Col([
                                textInput(label="Nombre de Indicador",ids="nombre-indicador"),
                                

                            ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-1"),


                        ]),
                        dbc.Row([
                            dbc.Col([
                                select(ids="partidas-indicador",texto="Partidas",size='sm'),
                                
                            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-1"),
                            dbc.Col([
                                textInput(label="Ingrese Fórmula",ids="formula-indicador"),
                                

                            ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-1"),


                        ]),
                        dbc.Row([
                            dbc.Col([
                                dmc.Card(
                                children=[
                                    
                                    dmc.CardSection(
                                        dmc.Center(
                                            style={"width": "100%"},
                                            children=[
                                                #
                                                dbc.Row([
                                                    dbc.Col([
                                                        dmc.Center(
                                                                style={"height":"100%", "width": "100%"},#
                                                                children=[
                                                                    dmc.Text("Rango Negativo :", weight=450),
                                                                ],
                                                            ),
                                                                                                                                
                                                            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                                    numberInput(label="Desde",ids="desde1"),
                                                                ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                                    numberInput(label="Hasta",ids="hasta1"),
                                                                ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                                    dbc.Label(""),
                                                                    dbc.Input(
                                                                        type="color",
                                                                        id="color1",
                                                                        value="#F70808",
                                                                        style={"width": 45, "height": 40},
                                                                    ),

                                                                ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                                                ]),
                                            ],
                                        ),
                                        
                                    ),
                                    
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                py="xs"
                                #style={"width": 350},
                            ),
                                

                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-1"),
                        ]),
                            
                        dbc.Row([
                            dbc.Col([
                                dmc.Card(
                                children=[
                                    
                                    dmc.CardSection(
                                        dmc.Center(
                                            style={"width": "100%"},
                                            children=[
                                                dbc.Row([
                            
                                                    dbc.Col([
                                                        dmc.Center(
                                                            style={"height":"100%", "width": "100%"},#
                                                            children=[dmc.Text("Rango Medio :", weight=450),],
                                                        ),
                                                        
                                                        

                                                    ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                        numberInput(label="Desde",ids="desde2"),

                                                    ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                        numberInput(label="Hasta",ids="hasta2"),

                                                    ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                        dbc.Label(""),
                                                        dbc.Input(
                                                            type="color",
                                                            id="color2",
                                                            value="#FFF817",
                                                            style={"width": 45, "height": 40},
                                                        ),

                                                    ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),


                                                ]),
                                            ]),
                                        

                                    ),
                                    
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                py="xs"
                                #style={"width": 350},
                            ),
                                

                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-1"),
                        ]),    
                            
                        dbc.Row([
                            dbc.Col([
                                dmc.Card(
                                children=[
                                    
                                    dmc.CardSection(
                                        dmc.Center(
                                            style={"width": "100%"},
                                            children=[
                                                dbc.Row([
                                                    dbc.Col([
                                                        dmc.Center(
                                                                style={"height":"100%", "width": "100%"},#
                                                                children=[
                                                                    dmc.Text("Rango Positivo :", weight=450),
                                                                ],
                                                            ),
                                                                                                                                
                                                            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-1"),
                                                    dbc.Col([
                                                        numberInput(label="Desde",ids="desde3"),
                                                        

                                                    ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-1"),
                                                    dbc.Col([
                                                        numberInput(label="Hasta",ids="hasta3"),
                                                        
                                                    ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-1"),
                                                    dbc.Col([
                                                        dbc.Label(""),
                                                        dbc.Input(
                                                            type="color",
                                                            id="color3",
                                                            value="#66FF2E",
                                                            style={"width": 45, "height": 40},
                                                        ),

                                                    ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-1"),


                                                ]),
                                            ]),
                                        

                                    ),
                                    
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                py="xs"
                                #style={"width": 350},
                            ),
                                

                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-1"),
                        ]),

                        
                        
                        
                        dbc.Row([
                            
                            dbc.Col([
                                #dbc.Label("Desde"),
                                #dbc.Input(type="number", min=0.0, max=10000.0, step=0.1),
                                dcc.Checklist(
                                                id='favorito',
                                                options=[
                                                    {'label': 'Indicador Favorito', 'value': True},
                                                    
                                                ],
                                                value=False,

                                            ),
                                
                                #html.P(),
                                textAreaInput(ids="comentario",label="Comentarios")
                               
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                            


                        ]),
                        dbc.Row([
                            
                            dbc.Col([
                                button(text="Guardar",ids="guardar"),
                                #dbc.Button("Guardar", color="dark", className="me-1",id="guardar", n_clicks=0),
                            ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                            dbc.Col([
                                button(text="Mostrar",ids="mostrar"),
                                #dbc.Button("Mostrar", color="dark", className="me-1",id="mostrar", n_clicks=0),
                            ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),


                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Div(id="respuesta") 
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                        ])

                                    
         ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
         dbc.Col([
            loadingOverlay(dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm")),
                #html.P(),
                #dbc.Alert(children='owo', color="light"), 
            html.Div(id="alert-comentario") 
                 #html.H2(["Example heading", dbc.Badge("New", className="ms-1")]),
                # html.Hr(),
         ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
    ]),

    dbc.Row([
        dbc.Col([
            #dmc.Anchor(z
            #    "Todos los Indicadores",
            #    href="/indicadores/",
            #)
            html.A("Todos los Indicadores Financieros", href="../indicadores", className="alert-link"),
           # html.A("Todos los Indicadores", href="/indicadores", className="alert-link"),
        ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
    ])
    ])
    #partidas-indicador
    @app.callback(
        Output("partidas-indicador", "data"),
        Input("partidas-indicador", "values"),
    )
    def load_partidas(partidas):
        df=balancePivot('Trimestre','soles',df_bcomprobacion)
        print(df.columns)
        print(df)
        #df_general.drop(['NCULTIVO', 'FECHAINICIO_CAMPAÑA', 'FECHAFIN_CAMPAÑA','NCULTIVO'], axis=1)
        df=df.drop(['Año_x','trimestre_x','TRIM','Año_y','trimestre_y','Año','trimestre','PATRIMONIO_y'],axis=1)
        #distinct_consumidores.rename(columns={'AREA_CAMPAÑA':'AREA'
        df=df.rename(columns={'PATRIMONIO_x':'PATRIMONIO'})
        if partidas == None:
             return [{'label': i, 'value': i} for i in df.columns]

    #@app.callback(
    #    Output("formula-indicador", "value"),
    #    Input("partidas-indicador", "value"),
    #    Input("formula-indicador","value"),
    #)
    #def load_formula(partidas,formula):
    #    if formula == None:
    #        return PreventUpdate
    #    else:
    #        return formula + partidas
        #elif partidas != None:
            #calculo=formula + partidas
            #verificar si el texbox solo tiene el nombre de la partida seleccionada
            #if len(calculo) == partidas:
            #    return calculo 
            #elif len(calculo) == formula:
            #    return PreventUpdate

            #return calculo

    @app.callback(
 
    Output("graph1", "figure"),
    Output("alert-comentario", "children"),

    Input("mostrar","n_clicks"),
    State("tipo-indicador","value"),
    State("nombre-indicador","value"),

    State("formula-indicador","value"),
    State("desde1", "value"),
    State("hasta1", "value"),
    State("color1", "value"),
    State("desde2", "value"),
    State("hasta2", "value"),
    State("color2", "value"),
    State("desde3", "value"),
    State("hasta3", "value"),
    State("color3", "value"),
    
    State("comentario", "value"),
    State("favorito","value"),

    )
    def update_graph(n_clicks,tipo,nombre,formula,desde1,hasta1,color1,desde2,hasta2,color2,desde3,hasta3,color3,comentario,favorito):
        if n_clicks:
            name=nombre.upper()
            formula=formula.upper()
            df_ratios=balancePivot("Trimestre","soles",df_bcomprobacion)
            print(df_ratios)
            print(df_ratios.columns)
            column='TRIM'
            df = pd.DataFrame()
            df['Agrupado']=df_ratios[column]
            df['valor']=EvaluarFormula(formula,df_ratios)
            promedio=df['valor'].sum()/len(df['Agrupado'].unique())
            df['promedio']=promedio
            print(color1)
            fig=figure__line2(df['Agrupado'],df['valor'],df['promedio'],name,'Valor','Promedio',desde1,hasta1,color1,desde2,hasta2,color2,desde3,hasta3,color3)
            #owo=dbc.Alert(children=comentario, color="primary"),  
        #RegistrarIndicador
            comentario_alert=html.Div([dmc.Alert(comentario,title="Comentario :",color="blue")]),    
        return fig,comentario_alert
        #df_stack=df_ratios[group]
        #df_stack['valor']=EvaluarFormula(formula,df_ratios)#df_ratios
        #df_stack['Año']=df_stack['year']
  
    @app.callback(
 
    #Output("graph1", "figure"),
    
    Output("respuesta", "children"),
    Output("tipo-indicador","value"),
    Output("nombre-indicador","value"),
    Output("formula-indicador","value"),
    Output("desde1", "value"),
    Output("hasta1", "value"),
    Output("desde2", "value"),
    Output("hasta2", "value"),
    Output("desde3", "value"),
    Output("hasta3", "value"),
    Output("comentario", "value"),

    Input("guardar","n_clicks"),
    #Input("mostrar","n_clicks"),
    State("tipo-indicador","value"),
    State("nombre-indicador","value"),
    #State("partidas-indicador","value"),
    State("formula-indicador","value"),
    State("desde1", "value"),
    State("hasta1", "value"),
    State("color1", "value"),
    State("desde2", "value"),
    State("hasta2", "value"),
    State("color2", "value"),
    State("desde3", "value"),
    State("hasta3", "value"),
    State("color3", "value"),
    
    State("comentario", "value"),
    State("favorito","value"),

    )
    def update_graph(guardar,tipo,nombre,formula,desde1,hasta1,color1,desde2,hasta2,color2,desde3,hasta3,color3,comentario,favorito):
        nombre=nombre.upper()
        formula=formula.upper()
        print(tipo)
        if guardar:
           RegistrarIndicador(tipo,nombre,formula,desde1,hasta1,color1,desde2,hasta2,color2,desde3,hasta3,color3,comentario,favorito,empresa,usuario)
           
           return  html.Div([dmc.Alert("Se guardó correctamente",title="Exitoso :",color="green",duration=5000)]),"","","","","","","","","",""
        else:
           return  html.Div([dmc.Alert("Error al intentar guardar",title="Error :",color="red",duration=5000)])
