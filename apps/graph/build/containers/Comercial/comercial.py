from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
from datetime import datetime, date, timedelta
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
from apps.graph.build.components.mantine_react_components.actionIcon import btnFilter,btnCollapse
from apps.graph.build.components.bootstrap_components.offcanvas import offcanvas
from apps.graph.build.components.mantine_react_components.title import title
from apps.graph.build.components.mantine_react_components.cards import cardGraph
from apps.graph.utils.callback import *
from apps.graph.build.containers.Comercial.callbacks.callback_comercial import *
from apps.graph.build.components.mantine_react_components.datepicker import datepickerRange
from apps.graph.data.gets import getApi
from apps.graph.build.components.draw.table import tableDMC
import dash_ag_grid as dag
from apps.graph.build.components.bootstrap_components.layout import Column




from apps.graph.data.transform_comercial import *
meses_list={'Mes': ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre']}

def tabVentaDfGraph(df,tipo,tab,varnum,top_data):
        if tab == 'Serie de Tiempo':
            #AQUI NO LE QUITE LOS VALORES NEGATIVOS POR SER UN ST 
            df_mes_top=df.groupby(['Año','Mes',tipo,'MONTH'])[[varnum]].sum().sort_values(varnum,ascending=True).reset_index()
            df_mes_top=df_mes_top.sort_values(varnum,ascending=True)#.tail(15).reset_index()
            df_mes_top=df_mes_top.sort_values('MONTH',ascending=True)
            if top_data=='Top 20':
                df_mes_top=df_mes_top.sort_values(varnum,ascending=False).head(20)
                df_mes_top=df_mes_top.sort_values('MONTH',ascending=True)

            #elif top_data=='pareto':
                
            #elif top_data=='Top low 20':
            #    df_mes_top=df_mes_top.sort_values(varnum,ascending=True)#.tail(15).reset_index()
            #    df_mes_top=df_mes_top.sort_values('MONTH',ascending=True)
            fig = px.line(df_mes_top, x='Mes', y=varnum,template="none",title=f"Ventas por Mes",color=tipo,markers=True,category_orders=meses_list,color_discrete_sequence=px.colors.qualitative.Dark24)#, facet_row="Año",facet_row_spacing=0.1
            fig.update_layout(autosize=True,margin=dict(l=60,r=40,b=40,t=50))
            fig.update_layout(legend=dict(font=dict(size= 8)))
        else:
            #df_v=df.groupby([tipo])[[varnum]].sum().reset_index()
            #df_v=df_v[df_v[varnum]>0]  
            df_v=df.groupby([tipo,tab])[[varnum]].sum().reset_index()   
            df_v=df_v[df_v[varnum]>0]
            
            
            if top_data=='Top 20':
                #df=df_v.groupby([tipo,tab])[[varnum]].sum().sort_values(varnum,ascending=True).reset_index()
                df=df_v.groupby([tipo,tab])[[varnum]].sum().sort_values(varnum,ascending=True).reset_index().tail(20)
            elif top_data=='pareto':
                df=df_v.groupby([tipo,tab])[[varnum]].sum().sort_values(varnum,ascending=False).reset_index()
                list_20_percent=df[tipo].unique()[:(int(len(df[tipo].unique())*0.2))] 
                df=df[df[tipo].isin(list_20_percent)]
            elif top_data=='All':
                 df=df_v.groupby([tipo,tab])[[varnum]].sum().sort_values(varnum,ascending=True).reset_index()
            elif top_data=='Top low 20':
                print(df_v)
                df=df_v.groupby([tipo,tab])[[varnum]].sum().sort_values(varnum,ascending=True).reset_index()
                print(df)
                list_20_percent=df[tipo].unique()[:(int(len(df[tipo].unique())*0.2))] 
                df=df[df[tipo].isin(list_20_percent)]

            fig = px.bar(df, x= tipo , y=varnum, color= tab,# text_auto=True,
                                    title=f'Ventas {tipo} por {tab}',template="none")
            fig.update_layout(autosize=True,margin=dict(l=60,r=40,b=120,t=50))
            fig.update_layout(legend=dict(font=dict(size= 8)))
        return fig





###test mdata


token_nisira='0Q10D10N10D10O10Z1lpu0N10O10H10Q10D10N10D10O10Z1mkidfgsgk0Q10D10N10D10O10Z1lpu0Q10d10n10d10o10z1lpu0Q1ert45g0d10o123d45gqwsmkiqwsqwspoi0I1asd0o10A1lpumkimkiertlpuertsdfasdasdlpuertbhgnjhsdfqwsasdnjhdfgdfgrtgertrtgqws'
api_nisira_ventas='http://69.64.92.160:3005/api/consulta/nsp_rpt_ventas_detallado'
    
ventas_lista_nisira=getApi(api_nisira_ventas,token_nisira)
df_ventas_nisira=pd.DataFrame(ventas_lista_nisira)
df_ventas_detalle=cleanVentas(df_ventas_nisira)
df_ventas_expo=df_ventas_detalle.copy()
##










#.update_layout(bargap=0.15)

template_theme1 = "zephyr"
template_theme2 = "slate"
url_theme1 = dbc.themes.BOOTSTRAP
url_theme2 = dbc.themes.SLATE
color_variado=px.colors.qualitative.Dark2+px.colors.qualitative.Prism

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)
external_stylesheets=[dbc.themes.BOOTSTRAP]
scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/es.min.js",
]


def informeVentas(empresa,rubro_empresa,staff_comment):
    """"""
    #df_ventas_default= pd.read_json(f"http://68.168.108.184:3000/api/consulta/NSP_RPT_VENTAS_DETALLADO_nisira")
    #df_ventas_detalle=cleanVentas(df_ventas_default)
    """"""
    """
    df_informe_ventas=dataVentasEmpresa(empresa)
    """
    df_informe_ventas=df_ventas_detalle.copy()


    fecha=df_informe_ventas.groupby(['FECHA','DAY','MONTH','YEAR'])[['IMPORTEMEX']].sum().reset_index().sort_values('FECHA',ascending=True)
    print(df_informe_ventas.columns)
    print(rubro_empresa)
    last_year=sorted(df_informe_ventas['YEAR'].unique())[-1]
    if rubro_empresa == 'Agricola' or rubro_empresa == 'Agroindustrial':
        ticked_1='Cultivo'
        ticked_2='Variedad'
    else:
        ticked_1='Tipo de Venta'
        ticked_2='Grupo de Venta'
        


    #df_informe_ventas=df_ventas_detalle
    app = DjangoDash('ventas1', external_stylesheets=[external_stylesheets,scripts])

    app.layout = html.Div([

            dbc.Row([
                #dbc.Col([ThemeSwitchAIO(aio_id="theme",icons={"left": "bi bi-moon", "right": "bi bi-sun"},themes=[url_theme1, url_theme2])],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([
                    html.Div(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                    html.Div(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                    ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
            ]),
            dbc.Row([
                            dbc.Col([
                                select(ids="year",texto="Año",value=last_year)
                    
                            ],
                            
                            width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                            dbc.Col([
                                select(ids="month",texto="Mes")
                    
                            ],
                            
                            width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                            
                            dbc.Col([
                                select("cliente","Cliente")
                                
                            ],
                            width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"), 
                            dbc.Col([
                                select("cultivo-tipo",ticked_1)
                                
                            ],
                            width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                            dbc.Col([
                                select("variedad-grupo",ticked_2)
                                
                            ],
                            width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                            dbc.Col([
                                radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                        children=[dmc.Radio(label='S/', value='Soles'),dmc.Radio(label='$', value='Dolares'),
                                #datepickerRange(first=date(int(fecha['YEAR'][:1]), int(fecha['MONTH'][:1]), int(fecha['DAY'][:1])),last=date(int(fecha['YEAR'][-1:]), int(fecha['MONTH'][-1:]), int(fecha['DAY'][-1:]))),
                                ]),
                                
                            ],
                            width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                            

            ]),
            dbc.Row([
                dbc.Col([
                    loadingOverlay(dbc.Card(dcc.Graph(id='card'),className="shadow-sm")),
                    html.P(),
                    loadingOverlay(dbc.Card(dcc.Graph(id='bar-naviera'),className="shadow-sm"))
                    
                ],width=5,className="col-xl-5 col-md-5 col-sm-12 col-12 mb-3"),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            loadingOverlay(dbc.Card(dcc.Graph(id='pais_top_facturado'),className="shadow-sm"))
                    ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),

                        dbc.Col([
                            loadingOverlay(dbc.Card(dcc.Graph(id='cultivo_top_facturado'),className="shadow-sm"))
                            
                        ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                        loadingOverlay(dbc.Card(dcc.Graph(id='mes_top'),className="shadow-sm")),
                        
                    ]),
                    #dbc.Card(dcc.Graph(id='pais_top_facturado'),className="shadow-sm"),
                ],width=7,className="col-xl-7 col-md-7 col-sm-12 col-12 mb-3"),
            
            #dbc.Col([
            #    dbc.Card(dcc.Graph(id='bar_top_cultivo'),className="shadow-sm")
            #],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3")
            ]),
            #dbc.Row([
            #    dbc.Col([
            #        loadingOverlay(dbc.Card(dcc.Graph(id='graph-last'),className="shadow-sm"))
            #    ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            #]),
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
    ##CALLBACK FILTROS SELECTS
    #filtroInformeVentas(app,rubro_empresa,df_informe_ventas)
    filtroInformeVentas2(app,rubro_empresa,df_informe_ventas)
    titleInformeVentas(app,rubro_empresa,'Informe de Ventas ')
    drawGraphInformeVentas(app,rubro_empresa,df_informe_ventas)

def ventasExportacion(empresa,rubro_empresa,staff_comment):
    """"""
    #df_ventas_default= pd.read_json(f"http://68.168.108.184:3000/api/consulta/NSP_RPT_VENTAS_DETALLADO_nisira")
    #df_ventas_detalle=cleanVentas(df_ventas_default)
    """"""
    """
    df_ventas_expo_1=dataVentasEmpresa(empresa)
    """
    df_ventas_expo_1=df_ventas_detalle.copy()

    df_ventas_expo=df_ventas_expo_1[df_ventas_expo_1['PAIS']!='PERÚ']
    last_year=sorted(df_ventas_expo['YEAR'].unique())[0]#[-1]
    if rubro_empresa == 'Agricola' or rubro_empresa == 'Agroindustrial':
        ticked_1='Cultivo'
        ticked_2='Variedad'
    else:
        ticked_1='Tipo de Venta'
        ticked_2='Grupo de Venta'
        
    #df_ventas_expo=df_ventas_detalle
    app = DjangoDash(
        'ventas_exportacion',
        external_stylesheets=external_stylesheets,
    )
    app.layout = html.Div([
        dbc.Row([
                #dbc.Col([ThemeSwitchAIO(aio_id="theme",icons={"left": "bi bi-moon", "right": "bi bi-sun"},themes=[url_theme1, url_theme2])],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([
                    html.Div(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                    html.Div(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                    ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
            ]),
        dbc.Row([
                    dbc.Col([
                        #value=sorted(df_ventas_expo['YEAR'].unique())[-1],
                        #select("year","Año"),
                        select(ids="year",texto="Año",place="",value=last_year)
                        
                    ],
                    width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                                select(ids="month",texto="Mes")
                    
                            ],
                            
                            width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),  
                     
                    dbc.Col([
                        select(ids="cliente",texto="Cliente",place="")
                       
                                    ],
                    width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"), 
                    dbc.Col([
                        select("cultivo-tipo",ticked_1)
                        
                        
                    ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                        select("variedad-grupo",ticked_2)
                        
                    ],
                    width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                         radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                   children=[dmc.Radio(label='S/', value='Soles'),dmc.Radio(label='$', value='Dolares'),

                        ]),
                    ],
                    width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                    
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
    filtroInformeVentas2(app,rubro_empresa,df_ventas_expo)
    

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
    titleInformeVentas(app,rubro_empresa,'Ventas de Exportación ')
    drawGraphExportacionVentas(app,rubro_empresa,df_ventas_expo)




        
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
from dash_iconify import DashIconify

        
   # @app.callback(
   # Output("download", "data"),
   # Input("btn_excel", "n_clicks"),
   # prevent_initial_call=True,<s
   # )
   # def func(n_clicks):
        #if download_type == "csv":
            #    files= dcc.send_data_frame(df_table.to_csv, "table.csv")
            #else:
            #    files= dcc.send_data_frame(df_table.to_excel, "table.xlsx")
   #     df=df_ventas.groupby(['Producto'])[['Importe en Soles']].sum().reset_index()
   #     return dcc.send_data_frame( df.to_excel, "test.xlsx", sheet_name="Sheet_name_1")
def ventas2(empresa,staff_comment):
    """"""
    df_ventas_default= pd.read_json(f"http://68.168.108.184:3000/api/consulta/NSP_RPT_VENTAS_DETALLADO_nisira")
    df_ventas_detalle=cleanVentas(df_ventas_default)
    """"""
    """
    df_ventas_expo=dataVentasEmpresa(empresa)
    """
    df_ventas_expo=df_ventas_detalle.copy()
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
    


def ventasProductos(empresa,staff_comment):
    """"""
    df_ventas_default= pd.read_json(f"http://68.168.108.184:3000/api/consulta/NSP_RPT_VENTAS_DETALLADO_nisira")
    df_ventas_detalle=cleanVentas(df_ventas_default)
    """"""
    """
    df_ventas_expo=dataVentasEmpresa(empresa)
    """
    df_ventas_expo=df_ventas_detalle.copy()

    app = DjangoDash('ventasProductos', external_stylesheets=[url_theme1, dbc.icons.BOOTSTRAP, dbc_css])#
    
    df_ventas_d=changeVentasCol(df_ventas_expo)
    app.layout = html.Div([
            dbc.Row([   
                        
                        dbc.Col([
                            btnFilter(),

                            offcanvas(componentes=[
                                select(ids="year",texto="Año",value=sorted(df_ventas_d['Año'].unique())[-1]),
                                select(ids="cliente",texto="Cliente"),
                                select(ids="cultivo",texto="Cultivo"),
                                select(ids="variedad",texto="Variedad"),
                                select(ids="month",texto="Mes"),
                                radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                          children=[dmc.Radio(label='S/', value='Soles'),
                                                    dmc.Radio(label='$', value='Dolares'),
                                          ]),
                                dbc.Checklist(  
                                    id="check-igv",
                                    options=[{'label':'CON IGV','value':'IGV'}],
                                    #value=value,
                                    inline=False,
                                    #label_checked_style={"color": "red"},
                                    input_checked_style={
                                        "backgroundColor": "rgb(34, 139, 230)",
                                        "borderColor": "rgb(34, 139, 230)",
                                    },     
                                    label_style={'font-size': '12px'} ,
                                    value="IGV"
                                ),
                            ]),
                        ],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
                        dbc.Col([
                            html.Div(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                            html.Div(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})

                           ],width=10,className="col-xl-10 col-md-10 col-sm-10 col-10 mb-3"),
                        dbc.Col([btnCollapse(),],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
                        
                        
                        
                    ]),
              

            dbc.Collapse(
                dbc.Row([#,style={'max-height': '3490px','overflow': "auto"}
            
                    dbc.Col([html.Div(children=loadingOverlay(dbc.Card(dcc.Graph(id='graph-1'),className="shadow-sm")),style={'max-height': '490px','overflow': "auto"})],width=5,className="col-xl-5 col-md-5 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                        dbc.Row([
                        dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2_1'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2_2'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                        #dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2_3'),className="shadow-sm"))],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                        #dbc.Col([Graph_notshadow(graph2_4)],width=3,className="col-xl-3 col-md-6 col-sm-12 col-12 mb-3")
                        ]),
                        dbc.Row([
                        dbc.Col([loadingOverlay(html.Div(id='graph-5',style={'max-height': '360px','overflow': "auto"}),)],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ])
                    ],width=7,className="col-xl-7 col-md-7 col-sm-12 col-12 mb-3")
                ]),
            id="collapse",is_open=True),

            dbc.Row(
                        [
                            
                            dbc.Col([
                                dbc.Card(
                                dbc.CardBody([
                                    
                                        dmc.MultiSelect(
                                            id='filter-tab',            
                                            label="Todos los Productos",
                                            #data=["React", "Angular", "Svelte", "Vue"],
                                            searchable=True,
                                            nothingFound="No options found",
                                            style={'font-size': "70%"},
                                            #value=options['Cliente'].unique()[:10]
                                            
                                        ),
                                    
                                    
                                    
                                    
                                        dmc.Tabs(
                                                [
                                                    dmc.TabsList(
                                                        [
                                                            dmc.Tab('Serie de Tiempo (Meses)', value='ST'),
                                                            dmc.Tab('Sucursal', value='S'),
                                                            dmc.Tab('País', value='P'),
                                                            dmc.Tab('Tipo de Venta', value='G'),

                                                            dmc.Tab('Cultivo', value='C'),
                                                            #dmc.Tab('Productos', value='Pro'),
                                                            dmc.Tab('Clientes', value='Cli'),


                                                        ]
                                                    ),
                                                    

                                                    dmc.TabsPanel(html.Div(id='tab-ST'), value='ST'),
                                                    dmc.TabsPanel(html.Div(id='tab-S'), value='S'),
                                                    dmc.TabsPanel(html.Div(id='tab-P'), value='P'),
                                                    dmc.TabsPanel(html.Div(id='tab-G'), value='G'),

                                                    dmc.TabsPanel(html.Div(id='tab-Cultivo'), value='C'),
                                                    dmc.TabsPanel(html.Div(id='tab-Cliente'), value='Cli'),
                                                ],
                                                value='ST',
                                                id='tabs-data',
                                            ),
                                    
                                ]),className="shadow-sm",
                            ),
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                ]
            ),



            html.Div(id='comentario'),
            dcc.Store(id='data-values')  
        ])
    offcanvasAction(app)
    @app.callback(
        Output("collapse", "is_open"),
        [Input("btn-collapse", "n_clicks")],
        [State("collapse", "is_open")],
        )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
    

    @app.callback(
            Output("year","data"),
            Output("cultivo","data"),
            Output("variedad","data"),
            Output("cliente","data"),
            Output("month","data"),
            #Output('filter-data', 'data'),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            #Input("cultivo","value"),
            Input("cliente","value"),
            Input("month","value"),
            
            )
    def filter_ventas(year,cultivo,variedad,cliente,month):
        df_ventas=df_ventas_d.groupby(['Año','Cliente','Cultivo','Variedad','Mes'])[['Importe en Soles']].sum().reset_index()

        if year==None and cultivo == None and variedad== None and cliente==None and month==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Año']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Cultivo']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Variedad']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month==None:    
            options=df_ventas[df_ventas['Cliente']==cliente]
        
        elif year==None and cultivo == None and variedad== None and cliente==None and month !=None:    
            options=df_ventas[df_ventas['Mes']==cliente]





        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year==None and cultivo != None and variedad == None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]

        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Mes']==month)]



        
        elif year!=None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]



        elif year==None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        





        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        option_year=[{'label': i, 'value': i} for i in options['Año'].unique()] 
        option_cultivo=[{'label': i, 'value': i} for i in options['Cultivo'].unique()] 
        option_variedad=[{'label': i, 'value': i} for i in options['Variedad'].unique()] 
        option_cliente=[{'label': i, 'value': i} for i in options['Cliente'].unique()] 
        option_mes=[{'label': i, 'value': i} for i in options['Mes'].unique()] 
        return option_year,option_cultivo,option_variedad,option_cliente,option_mes
    #####################################################################################################################################
    @app.callback(
            Output("data-values","data"),
            #Output('filter-data', 'data'),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            #Input("cultivo","value"),
            Input("cliente","value"),
            Input("month","value"),
            
            )
    def filter_ventas(year,cultivo,variedad,cliente,month):
        df_ventas=df_ventas_d
        if year==None and cultivo == None and variedad== None and cliente==None and month==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Año']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Cultivo']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Variedad']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month==None:    
            options=df_ventas[df_ventas['Cliente']==cliente]
        
        elif year==None and cultivo == None and variedad== None and cliente==None and month !=None:    
            options=df_ventas[df_ventas['Mes']==cliente]





        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year==None and cultivo != None and variedad == None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]

        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Mes']==month)]



        
        elif year!=None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]



        elif year==None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        





        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)&(df_ventas['Mes']==month)]
        
        return options.to_json(date_format='iso', orient='split')
    ####################################################################################################################################    
    
    
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
        #general='Ventas por Productos '+' '+str(moneda)
            if moneda =='Soles':
                importe=dmc.Badge(moneda,variant='filled',color='blue', size='lg')
            elif moneda == 'Dolares':
                importe=dmc.Badge(moneda,variant='filled',color='blue', size='lg')



            
                #general=str(titulo)+' '+str(moneda)
            if year == None:
                    title=dmc.Title(children=['Ventas por Productos ',dmc.Badge('ALL',variant='filled',color='gray', size='lg'),importe], order=2,align='center')
            else:
                    title=dmc.Title(children=['Ventas por Productos ',dmc.Badge(year,variant='filled',color='gray', size='lg'),importe], order=2,align='center')


            if cliente == None and cultivo == None:
                    subtitle=dmc.Title(children=[], order=3,align='center')
            elif cliente != None and cultivo == None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg')], order=3,align='center')
                    #subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(variedad,variant='filled',color='indigo', size='lg'),estado], order=2,align='center')
            elif cliente != None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(cultivo,variant='filled',color='indigo', size='lg')], order=3,align='center')
            elif cliente == None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cultivo,variant='filled',color='indigo', size='lg')], order=3,align='center')
                    
            return title,subtitle
    
    @app.callback(
            Output("graph-1","figure"),
            Output("graph2_1","figure"),
            Output("graph2_2","figure"),
            Output("graph-5","children"),
            Input("data-values","data"),
            Input("radio-moneda","value"),
            Input("check-igv","value"),
            
            #Input("filter-tab","value"),

            )
    def ventas(data, radio,igv ):#year,cultivo,variedad,cliente,
            options=pd.read_json(data, orient='split')
            

            
            if igv == 'IGV' or igv[-1] == 'IGV' :
                if radio=='Soles':
                    importe='Importe en Soles'
                else:
                    importe='Importe en Dolares'
                #options[importe]=options[importe]
                
            else:
                if radio=='Soles':
                    
                    options['Importe en Soles-']=options['Importe en Soles']-(options['Importe en Soles']*0.18)
                    importe='Importe en Soles-'
                else:
                    options['Importe en Dolares-']=options['Importe en Dolares']-(options['Importe en Dolares']*0.18)
                    importe='Importe en Dolares-'
            
            df_productos_top15=options.groupby(['Producto'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()#.tail(15)
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

            top_productos.update_layout(title={'text':'Productos con mas Ventas'},titlefont={'size': 15},template='none')
            top_productos.update_layout(autosize=True,height=490,margin=dict(l=300,r=40,b=40,t=40),yaxis=dict(titlefont_size=9,tickfont_size=9))#l=400,
            top_productos.update_layout(xaxis_title=radio,yaxis_title="",legend_title="")
            #top_productos.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')

            cantidad_productos=len(options['Producto'])
           
            cantidad_productos_unique=len(options['Producto'].unique())
            df_table=options.groupby(['Pais','Producto'])[[importe]].sum().reset_index().sort_values(importe,ascending=False).round(0)
            df_table[importe] = df_table.apply(lambda x: "{:,}".format(x[importe]), axis=1)
            def create_table(df):
                columns, values = df.columns, df.values
                header = [html.Tr([html.Th(col) for col in columns])]
                rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
                table = [html.Thead(header), html.Tbody(rows)]
                return table
            table=dmc.Table(
                striped=True,
                highlightOnHover=True,
                withBorder=True,
                withColumnBorders=True,
                children=create_table(df_table),
                #style={'backgroundColor': '#f7f7f7'}

            )

            return top_productos,card_ventas(cantidad_productos,None,"N° de Ventas"),card_ventas(cantidad_productos_unique,None,"N° de Productos"),table
#################################################################### OLD CODE
    @app.callback(
            Output("tab-ST","children"),
            Output("tab-S","children"),
            Output("tab-P","children"),
            Output("tab-G","children"),
            Output("tab-Cultivo","children"),
            Output("tab-Cliente","children"),
            Output("filter-tab","data"),
            
            Input("data-values","data"),
            Input("radio-moneda","value"),
            Input("filter-tab","value"),
            Input("check-igv","value"),

            )
    def ventas(data, radio  ,filtro ,igv):
            options=pd.read_json(data, orient='split')
            print(igv)

            if igv == 'IGV' or igv[-1] == 'IGV':
                if radio=='Soles':
                    importe='Importe en Soles'
                else:
                    importe='Importe en Dolares'
                #options[importe]=options[importe]
                
            else:
                if radio=='Soles':
                
                    options['Importe en Soles-']=options['Importe en Soles']-(options['Importe en Soles']*0.18)
                    importe='Importe en Soles-'
                else:
                    options['Importe en Dolares-']=options['Importe en Dolares']-(options['Importe en Dolares']*0.18)
                    importe='Importe en Dolares-'

            data_filtro=options['Producto'].unique()

            if filtro == None or len(filtro) == 0:

                df_15=options.groupby(['Producto'])[[importe]].sum().sort_values(importe,ascending=False).reset_index().head(20)
                df=options[options['Producto'].isin(df_15['Producto'].unique())]
            else:
            #if tab == 'ST':
                df=options[options['Producto'].isin(filtro)]
            
            df_mes_top=df.groupby(['Año','Mes','Producto','MONTH'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()#.sort_values('MONTH',ascending=True)#.tail(15)
            #df_mes_top=df_mes_top.sort_values(importe,ascending=True).tail(15).reset_index()
            df_mes_top=df_mes_top.sort_values(importe,ascending=True)#.tail(15).reset_index()
            df_mes_top=df_mes_top.sort_values('MONTH',ascending=True)
            #df_mes_top['Año']=df_mes_top['Año'].astype(object)
            #df_mes_top['Año']=df_mes_top['Año'].astype(object)
            #df_mes_top['Promedio']=df_mes_top[importe].mean()
            #df_mes_top=df_mes_top[(df_mes_top[importe]!=0) & (df_mes_top['Peso']!=0)]
            df_mes_producto = px.line(df_mes_top, x='Mes', y=importe,template="none",title=f"Ventas por Productos por Mes",color='Producto',markers=True,category_orders=meses_list,color_discrete_sequence=px.colors.qualitative.Dark24)#, facet_row="Año",facet_row_spacing=0.1
            df_mes_producto.update_layout(autosize=True,margin=dict(l=60,r=40,b=40,t=50))
            df_mes_producto.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))

            tab_st=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=df_mes_producto),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ###########################################################
            df_sucursal=df.groupby(['Producto','Sucursal'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            fig_sucursal = px.bar(df_sucursal, x="Producto", y=importe, color="Sucursal",# text_auto=True,
                                  title='Ventas Producto por Sucursal',template="none")
            fig_sucursal.update_layout(autosize=True,margin=dict(l=60,r=40,b=100,t=50),)
            fig_sucursal.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))

            tab_s=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_sucursal),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ###########################################################
            df_pais=df.groupby(['Producto','Pais'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            fig_pais = px.bar(df_pais, x="Producto", y=importe, color="Pais",# text_auto=True,
                                  title='Ventas Producto por País',template="none")
            fig_pais.update_layout(autosize=True,margin=dict(l=60,r=40,b=100,t=50))
            fig_pais.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            tab_p=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_pais),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ###########################################################
            df_grupo=df.groupby(['Producto','Tipo de Venta'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            fig_grupo = px.bar(df_grupo, x="Producto", y=importe, color="Tipo de Venta",# text_auto=True,
                                  title='Ventas Producto por Tipo',template="none")
            fig_grupo.update_layout(autosize=True,margin=dict(l=60,r=40,b=100,t=50))
            fig_grupo.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            tab_g=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_grupo),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ############################################################
            df_cultivo=df.groupby(['Producto','Cultivo'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            fig_cultivo = px.bar(df_cultivo, x="Producto", y=importe, color="Cultivo",# text_auto=True,
                                  title='Ventas Producto por Cultivo',template="none")
            fig_cultivo.update_layout(autosize=True,margin=dict(l=60,r=40,b=100,t=50))
            fig_cultivo.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            tab_c=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_cultivo),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ############################################################
            df_cliente=df.groupby(['Producto','Cliente'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            df_cliente['Cliente']=df_cliente['Cliente'].str[:45]
            fig_cliente = px.bar(df_cliente, x="Producto", y=importe, color="Cliente",# text_auto=True,
                                  title='Ventas Producto por Cliente',template="none")
            fig_cliente.update_layout(autosize=True,margin=dict(l=60,r=40,b=120,t=50))
            fig_cliente.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            tab_cli=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_cliente),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            return tab_st,tab_s,tab_p,tab_g,tab_c,tab_cli,data_filtro

         
    
    
def tipoVenta(empresa,staff_comment):
    """"""
    df_ventas_default= pd.read_json(f"http://68.168.108.184:3000/api/consulta/NSP_RPT_VENTAS_DETALLADO_nisira")
    df_ventas_detalle=cleanVentas(df_ventas_default)
    """"""
    """
    df_ventas_expo=dataVentasEmpresa(empresa)
    """
    df_ventas_expo=df_ventas_detalle.copy()
    


    app = DjangoDash('tipoVenta', external_stylesheets=[url_theme1, dbc.icons.BOOTSTRAP, dbc_css])#
    
    df_ventas_d=changeVentasCol(df_ventas_expo)
    df_ventas_d['Tipo de Venta']=df_ventas_d['Tipo de Venta'].str[4:]

    app.layout = html.Div([
            dbc.Row([   
                        dbc.Col([
                            btnFilter(),
                            offcanvas(componentes=[
                                select(ids="year",texto="Año",value=sorted(df_ventas_d['Año'].unique())[-1]),
                                select(ids="cliente",texto="Cliente"),
                                select(ids="cultivo",texto="Cultivo"),
                                select(ids="variedad",texto="Variedad"),
                                select(ids="month",texto="Mes"),
                                radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                          children=[dmc.Radio(label='S/', value='Soles'),
                                                    dmc.Radio(label='$', value='Dolares'),
                                          ]),
                                dbc.Checklist(  
                                    id="check-igv",
                                    options=[{'label':'CON IGV','value':'IGV'}],
                                    #value=value,
                                    inline=False,
                                    #label_checked_style={"color": "red"},
                                    input_checked_style={
                                        "backgroundColor": "rgb(34, 139, 230)",
                                        "borderColor": "rgb(34, 139, 230)",
                                    },     
                                    label_style={'font-size': '12px'} ,
                                    value="IGV"
                                ),
                            ]),
                        ],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
                        dbc.Col([
                            html.Div(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                            html.Div(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})

                           ],width=10,className="col-xl-10 col-md-10 col-sm-10 col-10 mb-3"),
                        dbc.Col([btnCollapse(),],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
                        
                        
                        
                    ]),
              

            dbc.Collapse(
                dbc.Row([#,style={'max-height': '3490px','overflow': "auto"}
            
                    dbc.Col([html.Div(children=loadingOverlay(dbc.Card(dcc.Graph(id='graph-1'),className="shadow-sm")),style={'max-height': '490px','overflow': "auto"})],width=5,className="col-xl-5 col-md-5 col-sm-12 col-12 mb-3"),
                    dbc.Col([
                        dbc.Row([
                        dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2_1'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2_2'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                        #dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2_3'),className="shadow-sm"))],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                        #dbc.Col([Graph_notshadow(graph2_4)],width=3,className="col-xl-3 col-md-6 col-sm-12 col-12 mb-3")
                        ]),
                        dbc.Row([
                        dbc.Col([loadingOverlay(html.Div(id='graph-5',style={'max-height': '360px','overflow': "auto"}),)],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ])
                    ],width=7,className="col-xl-7 col-md-7 col-sm-12 col-12 mb-3")
                ]),
            id="collapse",is_open=True),

            dbc.Row(
                        [
                            
                            dbc.Col([
                                dbc.Card(
                                dbc.CardBody([
                                    
                                        dmc.MultiSelect(
                                            id='filter-tab',            
                                            label="Todos los Tipos de Venta",
                                            #data=["React", "Angular", "Svelte", "Vue"],
                                            searchable=True,
                                            nothingFound="No options found",
                                            style={'font-size': "70%"},
                                            #value=options['Cliente'].unique()[:10]
                                            
                                        ),
                                    dmc.Tabs(
                                        [
                                            dmc.TabsList(
                                                [
                                                    dmc.Tab('Serie de Tiempo (Meses)', value='ST'),
                                                    dmc.Tab('Sucursal', value='S'),
                                                    dmc.Tab('País', value='P'),
                                                    dmc.Tab('Grupo de Venta', value='G'),

                                                    dmc.Tab('Cultivo', value='C'),
                                                    dmc.Tab('Productos', value='Pro'),
                                                    dmc.Tab('Clientes', value='Cli'),


                                                ]
                                            ),
                                            dmc.TabsPanel(html.Div(id='tab-ST'), value='ST'),
                                            dmc.TabsPanel(html.Div(id='tab-S'), value='S'),
                                            dmc.TabsPanel(html.Div(id='tab-P'), value='P'),
                                            dmc.TabsPanel(html.Div(id='tab-G'), value='G'),

                                            dmc.TabsPanel(html.Div(id='tab-Cultivo'), value='C'),
                                            dmc.TabsPanel(html.Div(id='tab-Producto'), value='Pro'),
                                            dmc.TabsPanel(html.Div(id='tab-Cliente'), value='Cli'),
                                        ],
                                        value='ST',
                                        id='tabs-data',
                                    ),
                                    
                                ]),className="shadow-sm",
                            ),
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                ]
            ),


            html.Div(id='comentario'),
                 
        ])
    offcanvasAction(app)
    @app.callback(
        Output("collapse", "is_open"),
        [Input("btn-collapse", "n_clicks")],
        [State("collapse", "is_open")],
        )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
    

    @app.callback(
            Output("year","data"),
            Output("cultivo","data"),
            Output("variedad","data"),
            Output("cliente","data"),
            Output("month","data"),
            #Output('filter-data', 'data'),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            #Input("cultivo","value"),
            Input("cliente","value"),
            Input("month","value"),
            
            )
    def filter_ventas(year,cultivo,variedad,cliente,month):
        df_ventas=df_ventas_d.groupby(['Año','Cliente','Cultivo','Variedad','Mes'])[['Importe en Soles']].sum().reset_index()

        if year==None and cultivo == None and variedad== None and cliente==None and month==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Año']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Cultivo']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Variedad']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month==None:    
            options=df_ventas[df_ventas['Cliente']==cliente]
        
        elif year==None and cultivo == None and variedad== None and cliente==None and month !=None:    
            options=df_ventas[df_ventas['Mes']==cliente]





        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year==None and cultivo != None and variedad == None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]

        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Mes']==month)]



        
        elif year!=None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]



        elif year==None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        





        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        option_year=[{'label': i, 'value': i} for i in options['Año'].unique()] 
        option_cultivo=[{'label': i, 'value': i} for i in options['Cultivo'].unique()] 
        option_variedad=[{'label': i, 'value': i} for i in options['Variedad'].unique()] 
        option_cliente=[{'label': i, 'value': i} for i in options['Cliente'].unique()] 
        option_mes=[{'label': i, 'value': i} for i in options['Mes'].unique()] 
        return option_year,option_cultivo,option_variedad,option_cliente,option_mes

    @app.callback(
            Output("data-values","data"),
            #Output('filter-data', 'data'),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            #Input("cultivo","value"),
            Input("cliente","value"),
            Input("month","value"),
            
            
            )
    def filter_ventas(year,cultivo,variedad,cliente,month):
        df_ventas=df_ventas_d
        if year==None and cultivo == None and variedad== None and cliente==None and month==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Año']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Cultivo']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Variedad']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month==None:    
            options=df_ventas[df_ventas['Cliente']==cliente]
        
        elif year==None and cultivo == None and variedad== None and cliente==None and month !=None:    
            options=df_ventas[df_ventas['Mes']==cliente]





        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year==None and cultivo != None and variedad == None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]

        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Mes']==month)]



        
        elif year!=None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]



        elif year==None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        





        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)&(df_ventas['Mes']==month)]
        return options.to_json(date_format='iso', orient='split')
    
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
        #general='Ventas por Tipo '+' '+str(moneda)
            if moneda =='Soles':
                importe=dmc.Badge(moneda,variant='filled',color='blue', size='lg')
            elif moneda == 'Dolares':
                importe=dmc.Badge(moneda,variant='filled',color='blue', size='lg')



            
                #general=str(titulo)+' '+str(moneda)
            if year == None:
                    title=dmc.Title(children=['Ventas por Tipo ',dmc.Badge('ALL',variant='filled',color='gray', size='lg'),importe], order=2,align='center')
            else:
                    title=dmc.Title(children=['Ventas por Tipo ',dmc.Badge(year,variant='filled',color='gray', size='lg'),importe], order=2,align='center')


            if cliente == None and cultivo == None:
                    subtitle=dmc.Title(children=[], order=3,align='center')
            elif cliente != None and cultivo == None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg')], order=3,align='center')
                    #subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(variedad,variant='filled',color='indigo', size='lg'),estado], order=2,align='center')
            elif cliente != None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(cultivo,variant='filled',color='indigo', size='lg')], order=3,align='center')
            elif cliente == None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cultivo,variant='filled',color='indigo', size='lg')], order=3,align='center')
                    
            return title,subtitle
############################################################
    @app.callback(
            Output("graph-1","figure"),
            Output("graph2_1","figure"),
            Output("graph2_2","figure"),
            Output("graph-5","children"),
            Input("data-values","data"),
            Input("radio-moneda","value"),
            Input("check-igv","value"),
            
            #Input("filter-tab","value"),

            )
    def ventas(data, radio,igv ):#year,cultivo,variedad,cliente,

        options=pd.read_json(data, orient='split')
        if igv == 'IGV' or igv[-1] == 'IGV' :
            if radio=='Soles':
                importe='Importe en Soles'
            else:
                importe='Importe en Dolares'
            #options[importe]=options[importe]
            
        else:
            if radio=='Soles':
                
                options['Importe en Soles-']=options['Importe en Soles']-(options['Importe en Soles']*0.18)
                importe='Importe en Soles-'
            else:
                options['Importe en Dolares-']=options['Importe en Dolares']-(options['Importe en Dolares']*0.18)
                importe='Importe en Dolares-'
        
        df_tipo_venta=options.groupby(['Tipo de Venta'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
        top_productos = go.Figure()
        top_productos.add_trace(go.Bar(x=df_tipo_venta[importe],y=df_tipo_venta['Tipo de Venta'],text=df_tipo_venta[importe],orientation='h',
                                                textposition='outside',texttemplate='%{text:.2s}',#,marker_color=px.colors.qualitative.Dark24,#marker_color=colors,
                                                hovertemplate =
                                                    '<br><b>Tipo de Venta</b>:%{y}'+
                                                    '<br><b>Importe($)</b>: %{x}<br>',
                                                marker_color="#145f82",
                                                hoverlabel=dict(
                                                font_size=10,
                                                ),
                                                name=''
                                            ))#.2s

        top_productos.update_layout(title={'text':'Tipo de Venta'},titlefont={'size': 15},template='none')
        top_productos.update_layout(autosize=True,height=490,margin=dict(l=300,r=40,b=40,t=40),yaxis=dict(titlefont_size=9,tickfont_size=9))#l=400,
        top_productos.update_layout(xaxis_title=radio,yaxis_title="",legend_title="")
        #top_productos.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')

        cantidad_productos=len(options['Producto'])
           
        cantidad_productos_unique=len(options['Tipo de Venta'].unique())
        df_table=options.groupby(['Pais','Tipo de Venta'])[[importe]].sum().reset_index().sort_values(importe,ascending=False).round(0)
        df_table[importe] = df_table.apply(lambda x: "{:,}".format(x[importe]), axis=1)
        def create_table(df):
                columns, values = df.columns, df.values
                header = [html.Tr([html.Th(col) for col in columns])]
                rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
                table = [html.Thead(header), html.Tbody(rows)]
                return table
        table=dmc.Table(
                striped=True,
                highlightOnHover=True,
                withBorder=True,
                withColumnBorders=True,
                children=create_table(df_table),
                #style={'backgroundColor': '#f7f7f7'}

            )
        return top_productos,card_ventas(cantidad_productos,None,"N° de Ventas"),card_ventas(cantidad_productos_unique,None,"N° de Tipos de Venta"),table

    @app.callback(
            Output("tab-ST","children"),
            Output("tab-S","children"),
            Output("tab-P","children"),
            Output("tab-G","children"),
            Output("tab-Cultivo","children"),
            Output("tab-Producto","children"),
            Output("tab-Cliente","children"),
            Output("filter-tab","data"),

            Input("data-values","data"),
            Input("radio-moneda","value"),
            Input("filter-tab","value"),
            Input("check-igv","value"),

            )
    def ventas(data, radio  ,filtro ,igv):#year,cultivo,variedad,cliente,
            options=pd.read_json(data, orient='split')
            print(igv)

            if igv == 'IGV' or igv[-1] == 'IGV':
                if radio=='Soles':
                    importe='Importe en Soles'
                else:
                    importe='Importe en Dolares'
                #options[importe]=options[importe]
                
            else:
                if radio=='Soles':
                
                    options['Importe en Soles-']=options['Importe en Soles']-(options['Importe en Soles']*0.18)
                    importe='Importe en Soles-'
                else:
                    options['Importe en Dolares-']=options['Importe en Dolares']-(options['Importe en Dolares']*0.18)
                    importe='Importe en Dolares-'
            
            data_filtro=options['Tipo de Venta'].unique()
            
            
            ### ST
            if filtro == None or len(filtro) == 0:
                df=options
            else:
                df=options[options['Tipo de Venta'].isin(filtro)]
            
            ###########################################
            df_mes_top=df.groupby(['Año','Mes','Tipo de Venta','MONTH'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
           
            df_mes_top=df_mes_top.sort_values(importe,ascending=True)#.tail(15).reset_index()
            df_mes_top=df_mes_top.sort_values('MONTH',ascending=True)
            #(dff_lote['TOTAL_y'].sum())/len(dff_lote[cols[0]].unique()) 
            pronm=(df[importe].sum())/len(df['Tipo de Venta'].unique())
            print(df[importe].sum())
            print(df['Tipo de Venta'].unique())
            print(len(df['Tipo de Venta'].unique()))
            df_mes_top['avg']=pronm

            print(pronm)
          
            df_mes_tipov = px.line(df_mes_top, x='Mes', y=importe,template="none",title=f"Tipo de Ventas por Mes",color='Tipo de Venta',markers=True,category_orders=meses_list,color_discrete_sequence=px.colors.qualitative.Dark24)#, facet_row="Año",facet_row_spacing=0.1
            df_mes_tipov.update_layout(autosize=True,margin=dict(l=60,r=40,b=40,t=50))
            #df_mes_tipov.add_hline(y=pronm, line_dash="dot")
            
            df_mes_tipov.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            
            
            #df_mes_tipov.add_trace(go.Scatter(
            #                    x=df_mes_top['Mes'],
            #                    y=df_mes_top['avg'],
            #                    name="avg",
            #                    yaxis="y2",
            #                    text=df_mes_top['avg'],
            #                    #marker_color="#1f1587",
            #                    textposition='bottom right',
            #                    texttemplate='{text:.2s}'
            #                ))
            #df_mes_tipov.update_layout(
            #    
            #    yaxis2=dict(
            #        title="yaxis3 title",
            #        titlefont=dict(
            #            color="#2741d6"
            #        ),
            #        tickfont=dict(
            #            color="#2741d6"
            #        ),
            #        anchor="x",
            #        overlaying="y",
            #        side="right"
            #    ),)
            tab_st=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=df_mes_tipov),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ###########################################################
            df_sucursal=df.groupby(['Tipo de Venta','Sucursal'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            fig_sucursal = px.bar(df_sucursal, x="Tipo de Venta", y=importe, color="Sucursal",# text_auto=True,
                                  title='Tipo de Venta por Sucursal',template="none")
            fig_sucursal.update_layout(autosize=True,margin=dict(l=60,r=40,b=100,t=50),)
            fig_sucursal.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            tab_s=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_sucursal),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ###########################################################
            df_pais=df.groupby(['Tipo de Venta','Pais'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            fig_pais = px.bar(df_pais, x="Tipo de Venta", y=importe, color="Pais",# text_auto=True,
                                  title='Tipo de Venta por País',template="none")
            fig_pais.update_layout(autosize=True,margin=dict(l=60,r=40,b=100,t=50))
            fig_pais.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            tab_p=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_pais),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ###########################################################
            df_grupo=df.groupby(['Tipo de Venta','Grupo de Venta'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            fig_grupo = px.bar(df_grupo, x="Tipo de Venta", y=importe, color="Grupo de Venta",# text_auto=True,
                                  title='Tipo de Venta por Grupo',template="none")
            fig_grupo.update_layout(autosize=True,margin=dict(l=60,r=40,b=100,t=50))
            fig_grupo.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            tab_g=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_grupo),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ############################################################
            df_cultivo=df.groupby(['Tipo de Venta','Cultivo'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            fig_cultivo = px.bar(df_cultivo, x="Tipo de Venta", y=importe, color="Cultivo",# text_auto=True,
                                  title='Tipo de Venta por Cultivo',template="none")
            fig_cultivo.update_layout(autosize=True,margin=dict(l=60,r=40,b=100,t=50))
            fig_cultivo.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            tab_c=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_cultivo),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ############################################################
            df_producto=df.groupby(['Tipo de Venta','Producto'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            df_producto['Producto']=df_producto['Producto'].str[:45]
            fig_producto = px.bar(df_producto, x="Tipo de Venta", y=importe, color="Producto",# text_auto=True,
                                  title='Tipo de Venta por Producto',template="none")
            fig_producto.update_layout(autosize=True,margin=dict(l=60,r=40,b=120,t=50))
            fig_producto.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            tab_pro=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_producto),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            ############################################################
            df_cliente=df.groupby(['Tipo de Venta','Cliente'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            df_cliente['Cliente']=df_cliente['Cliente'].str[:45]
            fig_cliente = px.bar(df_cliente, x="Tipo de Venta", y=importe, color="Cliente",# text_auto=True,
                                  title='Tipo de Venta por Cliente',template="none")
            fig_cliente.update_layout(autosize=True,margin=dict(l=60,r=40,b=120,t=50))
            fig_cliente.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',legend=dict(font=dict(size= 8)))
            #fig_cliente = px.scatter(df_cliente, x="Cliente", y=importe, facet_row="Tipo de Venta")#, color='sex'
            tab_cli=html.Div([
                    
                    dbc.Row(
                        [
                            dbc.Col([
                                loadingOverlay(dbc.Card(dcc.Graph(figure=fig_cliente),className="shadow-sm"))
                                
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
                        ]
                    )
            ])
            return tab_st,tab_s,tab_p,tab_g,tab_c,tab_pro,tab_cli,data_filtro


def contenedoresExportados1(empresa,staff_comment):
    """"""
    df_control_expo_arona = pd.read_csv("https://raw.githubusercontent.com/Enriquezm97/file/main/exportacion_arona.csv")
    df_control_contenedores_default=cleanContenedores(df_control_expo_arona)
    """"""
    #df_expo=dataContenedoresEmpresa(empresa)
    df_expo=df_control_contenedores_default.copy()

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
    """"""
    df_control_expo_arona = pd.read_csv("https://raw.githubusercontent.com/Enriquezm97/file/main/exportacion_arona.csv")
    df_control_contenedores_default=cleanContenedores(df_control_expo_arona)
    """"""
    #df_expo=dataContenedoresEmpresa(empresa)
    df_expo=df_control_contenedores_default.copy()

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





"""
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
"""


def ventasComparativo(empresa,staff_comment):

    #df_ventas_default= pd.read_json(f"http://68.168.108.184:3000/api/consulta/NSP_RPT_VENTAS_DETALLADO_nisira")
    #df_ventas_detalle=cleanVentas(df_ventas_default)


    df_ventas_expo=df_ventas_detalle.copy()

    app = DjangoDash('VentaComparativo', external_stylesheets=[url_theme1, dbc.icons.BOOTSTRAP, dbc_css])#
    
    df_ventas_d=changeVentasCol(df_ventas_expo)
    df_ventas_d['Tipo de Venta']=df_ventas_d['Tipo de Venta'].str[4:]
    df_ventas_2=changeVentasCol(df_ventas_expo)
    year_min=sorted(df_ventas_d['Año'].unique())[0]
    year_max=sorted(df_ventas_d['Año'].unique())[-1]
    value_1=sorted(df_ventas_d['Año'].unique())[-2]
    value_2=sorted(df_ventas_d['Año'].unique())[-1]
    year_list=sorted(df_ventas_d['Año'].unique())
    lista_year=[str(x) for x in year_list]
    app.layout = html.Div([
            dbc.Row([   
                        dbc.Col([
                            html.H3(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                            html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})

                           ],width=5,className="col-xl-5 col-md-5 col-sm-11 col-11 mb-3"),
                        dbc.Col([
                            
                            dcc.RangeSlider(
                                        id="slider-year",
                                        min=year_min,
                                        max=year_max,
                                        value=[value_1,value_2 ],
                                        step=None,
                                        #className="p-0",
                                        #tooltip={"placement": "bottom", "always_visible": True},
                                        marks=dict(zip(lista_year, lista_year))
                                        #mb=35,
                                    ),
                           ],width=6,className="col-xl-6 col-md-6 col-sm-11 col-11 mb-3"),
                        dbc.Col([
                            btnFilter(),
                            offcanvas(componentes=[
                                select(ids="year",texto="Año"),#,value=sorted(df_ventas_d['Año'].unique())[-1]
                                select(ids="cliente",texto="Cliente"),
                                select(ids="cultivo",texto="Cultivo"),
                                select(ids="variedad",texto="Variedad"),
                                radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                          children=[dmc.Radio(label='S/', value='Soles'),
                                                    dmc.Radio(label='$', value='Dolares'),
                                          ]),
                            ]),
                        ],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
                        
                        
                    ]),
              

            dbc.Row([
                dbc.Col([
                loadingOverlay(dbc.Card(dcc.Graph(id='comparativo'),className="shadow-sm"))
                    

                ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            
                        ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            loadingOverlay(dbc.Card(dcc.Graph(id='st-year'),className="shadow-sm"))
                        ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                    ]),
                    
                    

                ],width=8,className="col-xl-8 col-md-8 col-sm-12 col-12 mb-3"),
                
            ]),


            dbc.Row([
                select(ids="select-graph",texto="Tipo de Gráfico",data=[{"value": "bar-stack", "label": "Bar Stack"},{"value": "bar-group", "label": "Bar Group"},{"value": "line", "label": "Line chart"}]),
                loadingOverlay(dbc.Card(dcc.Graph(id='bar-stack'),className="shadow-sm"))
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
            Input("slider-year","value"),
            
            )
    def title_ventas(year,cultivo,cliente,moneda,slider):
        general='Ventas Comparativo por Año '+' '+str(moneda)
        if year == None:
            title=general
        else:
            title=general+' del año '+str(slider[0])+' al '+str(slider[1])
        if cliente == None and cultivo == None:
            subtitle=''
        elif cliente != None and cultivo == None:
            subtitle=str(cliente)
        elif cliente != None and cultivo != None:
            subtitle=str(cliente)+' '+str(cultivo)
            
        return title,subtitle

    @app.callback(
            Output("comparativo","figure"),
            Output("bar-stack","figure"),
            Output("st-year","figure"),
            #Output("graph2_1","figure"),
            #Output("graph2_2","figure"),
            #Output("graph2_3","figure"),
            #Output("graph-5","children"),
            #Output("tab-ST","figure"),

            #Output("tab-S","figure"),
            #Output("tab-P","figure"),
            #Output("tab-G","figure"),

            #Output("tab-Cultivo","figure"),
            #Output("tab-Producto","figure"),
            #Output("tab-Cliente","figure"),

            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            Input("cliente","value"),
            Input("radio-moneda","value"),
            Input("slider-year","value"),
            Input("select-graph","value")
            #Input('graph-1', 'clickData'),
            #Input("btn_csv", "n_clicks"),
            #State("dropdown", "value"),
            #prevent_initial_call=True,
            #Input(ThemeSwitchAIO.ids.switch("theme"), "value"),

            )
    def ventas(year,cultivo,variedad,cliente,radio,slider,tipe_graph):#,n_clicks_btn, download_type
            
            if not slider:
                return no_update
            df_ventas_d = df_ventas_2[df_ventas_2.Año.between(slider[0], slider[1])]



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
            #df_table[importe] = df_table.apply(lambda x: "{:,}".format(x[importe]), axis=1)
            #df_ventas_c=options.copy()
            #df_ventas_c[importe]=df_ventas_c.apply(lambda x: "{:,}".format(x[importe]), axis=1)
            df_year=options.groupby(['Año'])[[importe]].sum().reset_index().round(1)
            print(df_year)
            pie_years = go.Figure()

            pie_years.add_trace(go.Pie(labels=df_year['Año'], values=df_year[importe]))#,rotation=100
            pie_years.update_traces(hoverinfo="label+value+percent")#, hole=.4)#label+value+percent
                #fig.update_traces(textposition='inside', textinfo='percent+label')
            pie_years.update_traces(textposition='inside', textinfo='label+percent+value', marker=dict(colors=px.colors.qualitative.T10),textfont=dict(size=10),rotation=90)#line=dict(color='#000000', width=1)
            pie_years.update_layout(
                                        title={
                                        'text': 'Ventas por Año',
                                        #'y':0.9,
                                        #'x':0.5,
                                        },
                                        titlefont={'size': 15},
                                        showlegend=False,
                                        template="none"
                                        )
            pie_years.update_layout(margin = dict(t=40, b=10, l=10, r=30),height=300)#,height=330
            pie_years.update_layout(paper_bgcolor='#f7f7f7')
            df_mes_year=options.groupby(['Año','Mes','MONTH'])[[importe]].sum().reset_index().round(1).sort_values('MONTH',ascending=True)
            df_mes_year['Año']=df_mes_year['Año'].astype('string')
            if tipe_graph == None or tipe_graph == 'bar-stack':
            
                fig_comparative = px.bar(df_mes_year, x='Mes', y=importe,color='Año',height=400,template='none',text=importe,title="Comparativo por Año (Bar)",category_orders=meses_list)#
                fig_comparative.update_traces(textposition='outside',texttemplate='%{text:.3f}')
                fig_comparative.update_layout(margin=dict(l=50,r=30,b=30,t=50,pad=0,autoexpand=True))  
                fig_comparative.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
            elif tipe_graph == 'bar-group': 
                fig_comparative = px.bar(df_mes_year, x='Mes', y=importe,color='Año',height=400,template='none',text=importe,title="Comparativo por Año (Bar)",category_orders=meses_list,barmode='group')#
                fig_comparative.update_traces(textposition='outside',texttemplate='%{text:.3f}')
                fig_comparative.update_layout(margin=dict(l=50,r=30,b=30,t=50,pad=0,autoexpand=True))  
                fig_comparative.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
            elif tipe_graph == 'line': 
                fig_comparative = px.line(df_mes_year, x='Mes', y=importe,template="none",title=f"Ventas Anuales por Meses",color='Año',markers=True,category_orders=meses_list,color_discrete_sequence=px.colors.qualitative.T10)#, facet_row="Año",facet_row_spacing=0.1
                fig_comparative.update_layout(autosize=True,margin=dict(l=60,r=40,b=40,t=50))
                #df_mes_cliente.update_traces(textposition="bottom center",texttemplate='%{text:.3f}',textfont_size=12)#,texttemplate='%{text:.2s}'
                #df_mes_cliente.update_layout(showlegend=False)
                fig_comparative.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')

            df_year['Año']=df_year['Año'].astype('string')
            
            fig_st = px.bar(df_year, x='Año', y=importe,template="none",title=f"Ventas Anuales")#, facet_row="Año",facet_row_spacing=0.1
            fig_st.update_layout(autosize=True,margin=dict(l=60,r=40,b=40,t=50),height=290,bargap=0.15)
            #fig_st.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7',xaxis = dict(
            #    tickmode = 'array',
            #))  
            fig_st.update_xaxes(type='category')
            fig_st.update_traces(marker_color='#3049AD', marker_line_color='#070809',
                  marker_line_width=1.5, opacity=0.8)
                #df_mes_cliente.update_traces(textposition="bottom center",texttemplate='%{text:.3f}',textfont_size=12)#,texttemplate='%{text:.2s}'
                #df_mes_cliente.update_layout(showlegend=False)
            #fig_st.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')

            return pie_years,fig_comparative,fig_st
colors=[
        "#15CAB6",
        "#007FFF",
        "#F6B53D",
        "#EF8A5A",
        "#E85E76",
        "#696CB5",
        "#0F488C",
        "#323447",
        "#3599B8",
        "#DFBFBF",
        "#4AC5BB",
        "#5F6B6D",
        "#FB8281",
        "#F4D25A",
        "#7F898A",
        "#A4DDEE",
        "#FDAB89",
        "#B687AC",
        "#28738A",
        "#A78F8F",
        "#168980",
        "#293537",
        "#BB4A4A",
        "#B59525",
        "#475052",
        "#6A9FB0",
        "#BD7150",
        "#7B4F71",
        "#1B4D5C",
        "#706060",
        "#0F5C55",
        "#1C2325",
    "#1C2325",
    ]
def dashVentasCore():
   
    app = DjangoDash('ventasProductos', external_stylesheets=[url_theme1, dbc.icons.BOOTSTRAP, dbc_css])#
    df_ventas_d=changeVentasCol(df_ventas_expo)
    df_ventas_d['Año']=df_ventas_d['Año'].astype('string')
    df_ventas_d['year-month']=df_ventas_d['Año']+'-'+df_ventas_d['Mes']
    df_ventas_d['Tipo de Venta']=df_ventas_d['Tipo de Venta'].str[4:]
    df_ventas_d['VENDEDOR']=df_ventas_d['VENDEDOR'].str[4:]
    color1 = 'rgb(71, 214, 171)'
    color2 = 'rgb(3, 20, 26)'
    color3 = 'rgb(79, 205, 247)'
    fontweight = 700



    app.layout = html.Div([
        dbc.Row([
            dbc.Col([
                            btnFilter(),
                            
                            offcanvas(componentes=[
                                select(ids="year",texto="Año",value=sorted(df_ventas_d['Año'].unique())[-1],data=[{'label': i, 'value': i} for i in df_ventas_d['Año'].unique()]),
                                select(ids="cliente",texto="Cliente"),
                                select(ids="cultivo",texto="Cultivo"),
                                select(ids="variedad",texto="Variedad"),
                                select(ids="month",texto="Mes"),
                                radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                          children=[dmc.Radio(label='S/', value='Soles'),
                                                    dmc.Radio(label='$', value='Dolares'),
                                          ]),
                                radioGroup(ids='radio-top-data',texto='Filtro Data Bar',value='pareto',
                                          children=[
                                                    #dmc.Radio(label='Top 20', value='Top 20'),
                                                    dmc.Radio(label='Pareto', value='pareto'),
                                                    dmc.Radio(label='Pareto Negativo', value='Top low 20'),
                                          ]),
                                
                            ]),
                    ],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
            dbc.Col([
                        html.Div(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                        html.Div(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})

                    ],width=5,className="col-xl-5 col-md-5 col-sm-10 col-10 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([
                dmc.Card(
                            children=[
                                
                                
                            dmc.CardSection([
                                   dmc.SegmentedControl(
                                    id='select-st',
                                    value="year-month",
                                    data=[{'label': 'Mensual', 'value': 'year-month'},
                                          {'label': 'Trimestral', 'value': 'Trimestre'},
                                          {'label': 'FECHA', 'value': 'FECHA'}],
                                    #mt=10,
                                    fullWidth=True,
                                    color='rgb(34, 184, 207)'
                                ),
                                    
                                dcc.Graph(id='st-comercial') 
                                
                            ]),
                                
                            ],
                            withBorder=True,
                            shadow="lg",
                            radius="xs",
                           
            )
                
                
            ],width=7,className="col-xl-7 col-md-7 col-sm-12 col-12 mb-3"),
            dbc.Col([
                     dmc.Card(
                            children=[
                                
                                
                                dmc.CardSection([
                                    dmc.SegmentedControl(
                                    id='segmented-pie',
                                    value="VENDEDOR",
                                    data=[
                                        {"value": "VENDEDOR", "label": "Vendedor"},
                                        {"value": "Pais", "label": "País"},
                                        {"value": "Sucursal", "label": "Sucursal"},
                                        {"value": "Mes", "label": "Mes"},
                                        
                                    ],
                                    
                                    fullWidth=True,
                                    color='rgb(34, 184, 207)'
                                ),
                                dcc.Graph(id='pie-comercial')
                            ]),
                                
                            ],
                            withBorder=True,
                            shadow="lg",
                            radius="xs",
                           
                        )
                     ],width=5,className="col-xl-5 col-md-5 col-sm-12 col-12 mb-3"),
        ]), 
        dbc.Row([
            dbc.Col([
                dmc.Card(
                            children=[
                                
                                
                                dmc.CardSection([
                                    dmc.SegmentedControl(
                                    id='segmented-bar',
                                    #id="segmented",
                                    value="Tipo de Venta",
                                    data=[
                                        {"value": "Tipo de Venta", "label": "Tipo de Venta"},
                                        {"value": "Producto", "label": "Producto"},
                                        {"value": "Cliente", "label": "Cliente"},
                                        #{"value": "Tipo de Movimiento", "label": "Tipo de Movimiento"},
                                    ],
                                    fullWidth=True,
                                    color='rgb(34, 184, 207)'
                                    #mt=10,
                                ),
                                dmc.Grid(
                                    children=[
                                        dmc.Col(dcc.Graph(id='bar-tventa-comercial'), span=7),
                                        dmc.Col(html.Div(id='table-comercial'), span=5),
                                        
                                    ],
                                    gutter="xs",
                                )
                                
                            ]),
                                
                            ],
                            withBorder=True,
                            shadow="lg",
                            radius="xs",
                           
                        )
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                
                
                
            
            #dbc.Col([dbc.Card(dcc.Graph(id='table-comercial'),className="shadow-sm")],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
        ]),
    dcc.Store(id='data-values') 

    ])

    @app.callback(
        Output("offcanvas-placement", "is_open"),
        Input("btn-filter", "n_clicks"),
        State("offcanvas-placement", "is_open"),
    )
    def toggle_offcanvas_scrollable(n1, is_open):
        if n1:
            return not is_open
        return is_open
    
    @app.callback(
            #Output("year","data"),
            Output("cultivo","data"),
            Output("variedad","data"),
            Output("cliente","data"),
            Output("month","data"),
            Output("data-values","data"),
            #Output('filter-data', 'data'),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            #Input("cultivo","value"),
            Input("cliente","value"),
            Input("month","value"),
            
            )
    def filter_ventas(year,cultivo,variedad,cliente,month):
        #df_ventas=df_ventas_d.groupby(['Año','Cliente','Cultivo','Variedad'])[['Importe en Soles']].sum().reset_index()
        df_ventas=df_ventas_d.copy()
        if year==None and cultivo == None and variedad== None and cliente==None and month==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Año']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Cultivo']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Variedad']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month==None:    
            options=df_ventas[df_ventas['Cliente']==cliente]
        
        elif year==None and cultivo == None and variedad== None and cliente==None and month !=None:    
            options=df_ventas[df_ventas['Mes']==cliente]





        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year==None and cultivo != None and variedad == None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]

        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Mes']==month)]



        
        elif year!=None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]



        elif year==None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        





        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)&(df_ventas['Mes']==month)]



        option_year=[{'label': i, 'value': i} for i in options['Año'].unique()] 
        option_cultivo=[{'label': i, 'value': i} for i in options['Cultivo'].unique()] 
        option_variedad=[{'label': i, 'value': i} for i in options['Variedad'].unique()] 
        option_cliente=[{'label': i, 'value': i} for i in options['Cliente'].unique()] 
        option_mes=[{'label': i, 'value': i} for i in options['Mes'].unique()] 
        return option_cultivo,option_variedad,option_cliente,option_mes,options.to_json(date_format='iso', orient='split')#option_year,

    @app.callback(
            
            Output("title","children"),
            Output("subtitle","children"),
            Input("year","value"),
            Input("cultivo","value"),
            Input("cliente","value"),
            Input("radio-moneda","value"),
            Input("month","value"),
            
            )
    def title_ventas(year,cultivo,cliente,moneda,month):
        #general='Ventas por Tipo '+' '+str(moneda)
            if moneda =='Soles':
                importe=dmc.Badge(moneda,variant='outline',color='blue', size='lg')
            elif moneda == 'Dolares':
                importe=dmc.Badge(moneda,variant='outline',color='blue', size='lg')



            
                #general=str(titulo)+' '+str(moneda)
            if year == None and month == None:
                    title=dmc.Title(children=['Informe de Ventas',dmc.Badge('ALL',variant='outline',color='gray', size='lg'),importe], order=2,align='center')
            elif year != None and month == None:
                    title=dmc.Title(children=['Informe de Ventas',dmc.Badge(year,variant='outline',color='gray', size='lg'),importe], order=2,align='center')
            elif year != None and month != None:
                    title=dmc.Title(children=['Informe de Ventas',dmc.Badge(year,variant='outline',color='gray', size='lg'),importe,dmc.Badge(month,variant='outline',color='blue', size='lg')], order=2,align='center')


            if cliente == None and cultivo == None:
                    subtitle=dmc.Title(children=[], order=3,align='center')
            elif cliente != None and cultivo == None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='outline',color='gray', size='lg')], order=3,align='center')
                    #subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(variedad,variant='filled',color='indigo', size='lg'),estado], order=2,align='center')
            elif cliente != None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='outline',color='gray', size='lg'),dmc.Badge(cultivo,variant='filled',color='indigo', size='lg')], order=3,align='center')
            elif cliente == None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cultivo,variant='outline',color='indigo', size='lg')], order=3,align='center')
                    
            return title,subtitle
    
    @app.callback(Output('st-comercial','figure'),
                  Output('pie-comercial','figure'),
                  Output('bar-tventa-comercial','figure'),
                  Output('table-comercial','children'),
                  Input("data-values","data"),
                  Input("select-st",'value'),
                  Input("radio-moneda","value"),
                  Input("segmented-pie",'value'),
                  Input("segmented-bar",'value'),
                  Input('radio-top-data','value')
    
    )
    def update_data_components(data,st,moneda,segmented_pie,segmented_bar,top_data ):
        options=pd.read_json(data, orient='split')
        if moneda=='Soles':
                importe='Importe en Soles'
        else:
                importe='Importe en Dolares'
        if st == 'year-month':
            st_ventas=options.groupby([st,'MONTH'])[[importe]].sum().reset_index().sort_values('MONTH',ascending=True)
        else:
            st_ventas=options.groupby([st])[[importe]].sum().reset_index()
        fig = px.line(st_ventas, x=st, y=importe, title=f'Serie de Tiempo - {st}',template='none')
        fig.update_layout(margin = dict(t=50, b=60, l=60, r=50),height=300,)
        df_vendedor=options.groupby([segmented_pie])[[importe]].sum().reset_index().sort_values(importe,ascending=False)
        
        fig_pie = go.Figure(data=[go.Pie(labels=df_vendedor[segmented_pie],title=f"{segmented_pie}",
                             values=df_vendedor[importe])])
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_traces(hoverinfo='label+percent', textfont_size=10,
                        marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig_pie.update_layout(height=300,margin = dict(t=30, b=50, l=10, r=10))
        fig_pie.update_layout(showlegend=False)
        fig_pie.update_layout(
            #font_family="Courier New",
            #font_color="black",
            #title_font_family="Times New Roman",
            title_font_color="black",
            #legend_title_font_color="green"
        )
        if top_data == 'pareto':
            df_tipo_venta_f=options.groupby([segmented_bar])[[importe]].sum().reset_index().sort_values(importe,ascending=False)
        elif top_data == 'Top low 20':
            df_tipo_venta_f=options.groupby([segmented_bar])[[importe]].sum().reset_index().sort_values(importe,ascending=True)
        df_tipo_venta_cl=df_tipo_venta_f[df_tipo_venta_f[importe]>0]
        list_pareto_segmented=df_tipo_venta_cl[segmented_bar].unique()[:(int(len(df_tipo_venta_cl[segmented_bar].unique())*0.2))] 
        df_tipo_venta=df_tipo_venta_cl[df_tipo_venta_cl[segmented_bar].isin(list_pareto_segmented)]
        
        if top_data == 'pareto':
            df_tipo_venta_f=df_tipo_venta.groupby([segmented_bar])[[importe]].sum().reset_index().sort_values(importe,ascending=False)
        elif top_data == 'Top low 20':
            df_tipo_venta_f=df_tipo_venta.groupby([segmented_bar])[[importe]].sum().reset_index().sort_values(importe,ascending=True)

        #df_tipo_venta=df_tipo_venta.groupby([segmented_bar])[[importe]].sum().reset_index().sort_values(importe,ascending=False)#
        fig_tventa = px.bar(df_tipo_venta, x=segmented_bar, y=importe,template='none',title=f"Pareto - {segmented_bar}")
        fig_tventa.update_layout(height=380,margin = dict(t=40, b=80, l=60, r=30))
        fig_tventa.update_traces(marker_color='#1F77B4', marker_line_color='#070809',
                  marker_line_width=1, opacity=0.9)
        fig_tventa.update_xaxes(tickfont=dict(size=9)) 
        

            
        df_tablew=df_tipo_venta_cl.groupby([segmented_bar])[[importe]].sum().reset_index().sort_values(importe,ascending=False)
        df_tablew['%']=df_tablew[importe]/df_tablew[importe].sum()
        df_tablew['% acumulada']=df_tablew['%'].cumsum(axis = 0, skipna = True) 
        df_tablew['%']=df_tablew['%']*100
        df_tablew['% acumulada']=df_tablew['% acumulada']*100
        df_tablew=df_tablew.round(2)
        #.round(0)
        table_Dash_plotly=dash_table.DataTable(
                        data=df_tablew.to_dict('records'),
                        #columns=[
                        #    {'name': i, 'id': i}
                        #    if i != 'Date' else
                        #    {'name': 'Date', 'id': 'Date', 'type': 'datetime'}
                        #    for i in df_tablew.columns
                        #],
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        fixed_rows={'headers': True},
                        style_as_list_view=True,
                        style_cell={'padding': '12px',
                                                'font-family': 'sans-serif',
                                                'font-size': '12px',
                                                'text_align': 'left',

                                                'overflow': 'hidden',
                                                    'textOverflow': 'ellipsis',
                                                    'maxWidth': 0
                                                #'minWidth': 30, 'maxWidth': 70, #'width': 95
                                                },
                        
                        style_header={
                                        #'backgroundColor': 'white',
                                        'fontWeight': 'bold',
                                        'text_align': 'left',
                                        'font-size': '12px',    
                                        #'backgroundColor': 'rgb(30, 30, 30)',
                                        'color': 'Black'
                                    },
                        tooltip_data=[
                        {
                            column: {'value': str(value), 'type': 'markdown'}
                            for column, value in row.items()
                        } for row in df_tablew.to_dict('records')
                        ],
                        tooltip_duration=None,
                        )


        return fig,fig_pie,fig_tventa,table_Dash_plotly

def ventas1(empresa,staff_comment):
    """"""
    
    #df_ventas_default= pd.read_json(f"http://68.168.108.184:3000/api/consulta/NSP_RPT_VENTAS_DETALLADO_nisira")
    #df_ventas_detalle=cleanVentas(df_ventas_default)
    """"""
    """
    df_ventas_expo=dataVentasEmpresa(empresa)
    """
    
    #print(df_ventas_expo.columns)

    app = DjangoDash('dashventas1', external_stylesheets=[url_theme1, dbc.icons.BOOTSTRAP, dbc_css])#
    
    df_ventas_d=changeVentasCol(df_ventas_expo)
    df_ventas_d['Tipo de Venta']=df_ventas_d['Tipo de Venta'].str[4:]
    app.layout = html.Div([
        dbc.Modal(id="modal",size='xl',style={'position': 'absolute'}),

            dbc.Row([   
                Column(content=[
                  btnFilter(),
                            
                            offcanvas(componentes=[
                                select(ids="year",texto="Año",value=sorted(df_ventas_d['Año'].unique())[-1]),
                                select(ids="cliente",texto="Cliente"),
                                select(ids="cultivo",texto="Cultivo"),
                                select(ids="variedad",texto="Variedad"),
                                select(ids="month",texto="Mes"),
                                radioGroup(ids='radio-moneda',texto='Moneda',value='Dolares',
                                          children=[dmc.Radio(label='S/', value='Soles'),
                                                    dmc.Radio(label='$', value='Dolares'),
                                          ]),
                                radioGroup(ids='radio-top-data',texto='Data',value='pareto',
                                          children=[dmc.Radio(label='All', value='All'),
                                                    #dmc.Radio(label='Top 20', value='Top 20'),
                                                    dmc.Radio(label='Pareto', value='pareto'),
                                                    dmc.Radio(label='Pareto Negativo', value='Top low 20'),
                                          ]),
                                
                            
                            ]),
                ],size=1),
                Column(content=[
                    html.Div(id="title", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                            html.Div(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                ],size=5),    
                Column(content=[
                   dmc.SegmentedControl(
                                id="segmented",
                                value="Cliente",
                                data=['Cliente','Producto','Tipo de Venta'],
                                mt=10,
                                fullWidth=True,
                                radius='md',
                                color="blue"
                            ),
                ],size=5),       
                Column(content=[
                  btnCollapse()
                ],size=1),
                ]),
              
            dbc.Collapse(
                dbc.Row([#,style={'max-height': '3490px','overflow': "auto"}
                    Column(content=[
                        html.Div(
                            children=loadingOverlay(
                                cardGraph(id_graph='graph-1',id_maximize='btn-modal'),
                                
                            ))
                     ],size=7),
                     Column(content=[
                        dbc.Row([
                            Column(content=[
                                loadingOverlay(dbc.Card(dcc.Graph(id='graph2_1'),className="shadow-sm"))
                            
                            ],size=6),
                            Column(content=[
                        
                            loadingOverlay(dbc.Card(dcc.Graph(id='graph2_2'),className="shadow-sm"))
                            ],size=6),
                        ]),
                        dbc.Row([
                            Column(content=[
                                loadingOverlay(html.Div(id='graph-5',style={'max-height': '360px','overflow': "auto"}),)
                            
                            ],size=12),
                        ])
                     ],size=5),

                ]),
            id="collapse",is_open=True),
            dbc.Row([
                Column(content=[
                  dbc.Card(
                                dbc.CardBody([
                                    
                                        html.Div(id='tabs-g')
                                    
                                ]),className="shadow-sm",
                            ),
                ],size=12),
            ]),
            
            
            html.Div(id='comentario'),
            dcc.Store(id='data-values')  
        ])
    offcanvasAction(app)
    @app.callback(
        Output("collapse", "is_open"),
        [Input("btn-collapse", "n_clicks")],
        [State("collapse", "is_open")],
        )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
    


    @app.callback(
                Output("year","data"),
                Output("cultivo","data"),
                Output("variedad","data"),
                Output("cliente","data"),
                Output("month","data"),
            #Output('filter-data', 'data'),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            #Input("cultivo","value"),
            Input("cliente","value"),
            Input("month","value"),
            
            )
    def filter_ventas(year,cultivo,variedad,cliente,month):
        df_ventas=df_ventas_d.groupby(['Año','Cliente','Cultivo','Variedad','Mes'])[['Importe en Soles']].sum().reset_index()

        if year==None and cultivo == None and variedad== None and cliente==None and month==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Año']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Cultivo']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Variedad']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month==None:    
            options=df_ventas[df_ventas['Cliente']==cliente]
        
        elif year==None and cultivo == None and variedad== None and cliente==None and month !=None:    
            options=df_ventas[df_ventas['Mes']==cliente]





        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year==None and cultivo != None and variedad == None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]

        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Mes']==month)]



        
        elif year!=None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]



        elif year==None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        





        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        option_year=[{'label': i, 'value': i} for i in options['Año'].unique()] 
        option_cultivo=[{'label': i, 'value': i} for i in options['Cultivo'].unique()] 
        option_variedad=[{'label': i, 'value': i} for i in options['Variedad'].unique()] 
        option_cliente=[{'label': i, 'value': i} for i in options['Cliente'].unique()] 
        option_mes=[{'label': i, 'value': i} for i in options['Mes'].unique()] 
        return option_year,option_cultivo,option_variedad,option_cliente,option_mes
    
    #####################################################################################################################################
    @app.callback(
            Output("data-values","data"),
            #Output('filter-data', 'data'),
            Input("year","value"),
            Input("cultivo","value"),
            Input("variedad","value"),
            #Input("cultivo","value"),
            Input("cliente","value"),
            Input("month","value"),
            
            )
    def filter_ventas(year,cultivo,variedad,cliente,month):
        df_ventas=df_ventas_d
        if year==None and cultivo == None and variedad== None and cliente==None and month==None:
            options=df_ventas

        elif year!=None and cultivo == None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Año']==year]
        elif year==None and cultivo != None and variedad== None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Cultivo']==cultivo]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month==None:    
            options=df_ventas[df_ventas['Variedad']==variedad]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month==None:    
            options=df_ventas[df_ventas['Cliente']==cliente]
        
        elif year==None and cultivo == None and variedad== None and cliente==None and month !=None:    
            options=df_ventas[df_ventas['Mes']==cliente]





        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)]
        
        elif year!=None and cultivo == None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year==None and cultivo != None and variedad == None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]

        elif year==None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad== None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Mes']==month)]



        
        elif year!=None and cultivo != None and variedad!= None and cliente==None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)]

        elif year!=None and cultivo != None and variedad== None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo != None and variedad== None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Cultivo']==cultivo)&(df_ventas['Mes']==month)]


        
        elif year!=None and cultivo == None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year!=None and cultivo == None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Año']==year)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]



        elif year==None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)]
        
        elif year==None and cultivo != None and variedad!= None and cliente==None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        
        elif year==None and cultivo == None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cliente']==cliente)&(df_ventas['Variedad']==variedad)&(df_ventas['Mes']==month)]
        





        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month==None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)]
        
        elif year!=None and cultivo != None and variedad!= None and cliente!=None and month!=None:
            options=df_ventas[(df_ventas['Cultivo']==cultivo)&(df_ventas['Variedad']==variedad)&(df_ventas['Cliente']==cliente)&(df_ventas['Año']==year)&(df_ventas['Mes']==month)]

        return options.to_json(date_format='iso', orient='split')
    ####################################################################################################################################    
    
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
            Input("segmented","value")
            
            )
    def title_ventas(year,cultivo,cliente,moneda,segmented):
        #general='Ventas por Clientes '+' '+str(moneda)
            if moneda =='Soles':
                importe=dmc.Badge(moneda,variant='outline',color='blue', size='lg')
            elif moneda == 'Dolares':
                importe=dmc.Badge(moneda,variant='outline',color='blue', size='lg')



            
                #general=str(titulo)+' '+str(moneda)
            if year == None:
                    title=dmc.Title(children=[f'Venta Anual por {segmented} ',dmc.Badge('ALL',variant='outline',color='gray', size='lg'),importe], order=2,align='center')
            else:
                    title=dmc.Title(children=[f'Venta Anual por {segmented} ',dmc.Badge(year,variant='outline',color='gray', size='lg'),importe], order=2,align='center')


            if cliente == None and cultivo == None:
                    subtitle=dmc.Title(children=[], order=3,align='center')
            elif cliente != None and cultivo == None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='outline',color='gray', size='lg')], order=3,align='center')
                    #subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(variedad,variant='filled',color='indigo', size='lg'),estado], order=2,align='center')
            elif cliente != None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='outline',color='gray', size='lg'),dmc.Badge(cultivo,variant='outline',color='indigo', size='lg')], order=3,align='center')
            elif cliente == None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cultivo,variant='outline',color='indigo', size='lg')], order=3,align='center')
                    
            return title,subtitle
        
            
        

    @app.callback(
            Output("graph-1","figure"),
            Output("graph2_1","figure"),
            Output("graph2_2","figure"),
            Output("graph-5","children"),
            Input("data-values","data"),
            Input("radio-moneda","value"),
            Input("segmented","value"),
            Input('radio-top-data','value')
            #Input("check-igv","value"),
            
            #Input("filter-tab","value"),

            )
    def ventas(data, radio,segmented,radio_top ):#year,cultivo,variedad,cliente,

        options=pd.read_json(data, orient='split')
        

        
        #if igv == 'IGV' or igv[-1] == 'IGV' :
        if radio=='Soles':
                importe='Importe en Soles'
        else:
                importe='Importe en Dolares'
            #options[importe]=options[importe]
            
        #else:
        #    if radio=='Soles':
                
        #        options['Importe en Soles-']=options['Importe en Soles']-(options['Importe en Soles']*0.18)
        #        importe='Importe en Soles-'
        #    else:
        #        options['Importe en Dolares-']=options['Importe en Dolares']-(options['Importe en Dolares']*0.18)
        #        importe='Importe en Dolares-'
        """
        ###PARETO
        df_pareto=options.groupby([segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=False)
        #condiciono que todos los totales de los clientes sean mayores a 0
        df_pareto=df_pareto[df_pareto[importe]>0]
        df_pareto['percent']=df_pareto[importe]/df_pareto[importe].sum()
        df_pareto['percent_accu']=df_pareto['percent'].cumsum(axis = 0, skipna = True)
        #EL 0.2 CORRESPONDE AL 20% DE LOS SEGMENTED TOTALES 
        list_20_percent=df_pareto[segmented].unique()[:(int(len(df_pareto[segmented].unique())*0.2))] 
        df_pareto_agg=df_pareto[df_pareto[segmented].isin(list_20_percent)]
        """

            

            #df_filter=options.groupby([ejex])[[color]].sum().reset_index()#,color
        def barSegment(options_df,segmented,importe,radio,top_data):
            df_v=options_df.groupby([segmented])[[importe]].sum()   
            df_v=df_v[df_v[importe]>0]  
            if top_data == 'Top 20':
                
                df=df_v.groupby([segmented])[[importe]].sum().sort_values(importe,ascending=True).reset_index().tail(20)
                df['N°']=[i+1 for i in range(len(df))]
                df['N°']=df['N°'].astype("string")
                df[segmented]=df['N°']+'-'+df[segmented]
            elif top_data == 'All':
                df=df_v.groupby([segmented])[[importe]].sum().sort_values(importe,ascending=False).reset_index()
                df['N°']=[i+1 for i in range(len(df))]
                df['N°']=df['N°'].astype("string")
                df[segmented]=df['N°']+'-'+df[segmented]
                df=df.groupby([segmented])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            elif top_data == 'pareto':
                df=df_v.groupby([segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=False)
                #df['percent']=df[importe]/df[importe].sum()
                #df['percent_accu']=df['percent'].cumsum(axis = 0, skipna = True)
                list_20_percent=df[segmented].unique()[:(int(len(df[segmented].unique())*0.2))] 
                df=df[df[segmented].isin(list_20_percent)].sort_values(importe)
                #lista_enumerador=[i+1 for i in range(len(df))]
                #lista_enumerador=lista_enumerador.reverse()
                #df['N°']=lista_enumerador

                #df['N°']=[i+1 for i in range(len(df))]
                df['N°']=list(range(len(df),0,-1))
                df['N°']=df['N°'].astype("string")
                df[segmented]=df['N°']+'-'+df[segmented]
                
                df=df.groupby([segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=True)
                

            elif top_data == 'Top low 20':
                df=df_v.groupby([segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=True)
                #df['percent']=df[importe]/df[importe].sum()
                #df['percent_accu']=df['percent'].cumsum(axis = 0, skipna = True)
                list_20_percent=df[segmented].unique()[:(int(len(df[segmented].unique())*0.2))] 
                df=df[df[segmented].isin(list_20_percent)].sort_values(importe)

                
                
                df=df.groupby([segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=True)
                #lista_enumerador=[i+1 for i in range(len(df))]
                #lista_enumerador=lista_enumerador.reverse()
                #df['N°']=lista_enumerador
                df['N°']=list(range(len(df),0,-1))
                df['N°']=df['N°'].astype("string")
                df[segmented]=df['N°']+'-'+df[segmented]
                


            if segmented == 'Cliente':
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df[importe],y=df[segmented],text=df[importe],orientation='h',
                                                        textposition='outside',texttemplate='%{text:.2s}',#,marker_color=px.colors.qualitative.Dark24,#marker_color=colors,
                                                        hovertemplate =
                                                            '<br><b>Cliente</b>:%{y}'+
                                                            '<br><b>Importe($)</b>: %{x}<br>',
                                                        marker_color="#145f82",
                                                        hoverlabel=dict(
                                                        font_size=14,
                                                        ),
                                                        name=''
                                                    ))#.2s

                fig.update_layout(title={'text':f'{segmented} con mas Ventas','font': {'size': 15, 'color': 'black', 'family': 'Arial'},},template='none')
                fig.update_layout(autosize=True,height=490,margin=dict(l=300,r=40,b=40,t=40),yaxis=dict(titlefont_size=8,tickfont_size=10))#l=400,
                fig.update_layout(xaxis_title=radio,yaxis_title="",legend_title="")
            elif segmented == 'Tipo de Venta':
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df[importe],y=df[segmented],text=df[importe],orientation='h',
                                                        textposition='outside',texttemplate='%{text:.2s}',#,marker_color=px.colors.qualitative.Dark24,#marker_color=colors,
                                                        hovertemplate =
                                                            '<br><b>Tipo de Venta</b>:%{y}'+
                                                            '<br><b>Importe($)</b>: %{x}<br>',
                                                        marker_color="#145f82",
                                                        hoverlabel=dict(
                                                        font_size=14,
                                                        ),
                                                        name=''
                                                    ))#.2s

                fig.update_layout(title={'text':f'{segmented} con mas Ventas'},titlefont={'size': 15},template='none')
                fig.update_layout(autosize=True,height=490,margin=dict(l=300,r=40,b=40,t=40),yaxis=dict(titlefont_size=9,tickfont_size=10))#l=400,
                fig.update_layout(xaxis_title=radio,yaxis_title="",legend_title="")
            elif segmented == 'Producto':
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df[importe],y=df[segmented],text=df[importe],orientation='h',
                                                        textposition='outside',texttemplate='%{text:.2s}',#,marker_color=px.colors.qualitative.Dark24,#marker_color=colors,
                                                        hovertemplate =
                                                            '<br><b>Producto</b>:%{y}'+
                                                            '<br><b>Importe($)</b>: %{x}<br>',
                                                        marker_color="#145f82",
                                                        hoverlabel=dict(
                                                        font_size=14,
                                                        ),
                                                        name=''
                                                    ))#.2s

                fig.update_layout(title={'text':f'{segmented} con mas Ventas'},titlefont={'size': 15},template='none')
                fig.update_layout(autosize=True,height=490,margin=dict(l=300,r=40,b=40,t=40),yaxis=dict(titlefont_size=9,tickfont_size=10))#l=400,
                fig.update_layout(xaxis_title=radio,yaxis_title="",legend_title="")

            return fig


    
        
        #top_productos.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')

        cantidad_productos=options[importe].sum()#"{:,.0f}".format(
           
        cantidad_clientes=len(options[segmented].unique())

            #graph4=options.groupby(['Pais'])[[importe,'Peso']].sum().reset_index().sort_values(importe,ascending=True)
            
        if  radio_top == 'Top 20':  
            df_table=options.groupby(['Pais',segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=False).round(0).head(20)
            df_table[importe] = df_table.apply(lambda x: "{:,}".format(x[importe]), axis=1)
        elif radio_top =='All':
            df_table=options.groupby(['Pais',segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=False).round(0)
            df_table[importe] = df_table.apply(lambda x: "{:,}".format(x[importe]), axis=1)
        elif radio_top =='pareto':
            """
            ###PARETO
            df_pareto=options.groupby([segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=False)
            #condiciono que todos los totales de los clientes sean mayores a 0
            df_pareto=df_pareto[df_pareto[importe]>0]
            df_pareto['percent']=df_pareto[importe]/df_pareto[importe].sum()
            df_pareto['percent_accu']=df_pareto['percent'].cumsum(axis = 0, skipna = True)
            #EL 0.2 CORRESPONDE AL 20% DE LOS SEGMENTED TOTALES 
            list_20_percent=df_pareto[segmented].unique()[:(int(len(df_pareto[segmented].unique())*0.2))] 
            df_pareto_agg=df_pareto[df_pareto[segmented].isin(list_20_percent)]
            """
            df_table=options.groupby(['Pais',segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=False).round(0)
            list_20_percent=df_table[segmented].unique()[:(int(len(df_table[segmented].unique())*0.2))]
            df_table=df_table[df_table[segmented].isin(list_20_percent)]
            df_table=options.groupby(['Pais',segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=False).round(0)
            df_table[importe] = df_table.apply(lambda x: "{:,}".format(x[importe]), axis=1)
            
        elif radio_top =='Top low 20':
            df_table=options.groupby(['Pais',segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=True).round(0)
            list_20_percent=df_table[segmented].unique()[:(int(len(df_table[segmented].unique())*0.2))]
            df_table=df_table[df_table[segmented].isin(list_20_percent)]
            df_table=options.groupby(['Pais',segmented])[[importe]].sum().reset_index().sort_values(importe,ascending=True).round(0)
            df_table[importe] = df_table.apply(lambda x: "{:,}".format(x[importe]), axis=1)
        df_table['N°']=[i+1 for i in range(len(df_table))]
        df_table=df_table[['N°',segmented,'Pais',importe]]
        
        #df_table[importe]=df_table[importe].astype(int)
        def create_table(df):
                columns, values = df.columns, df.values
                header = [html.Tr([html.Th(col) for col in columns])]
                rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
                table = [html.Thead(header), html.Tbody(rows)]
                return table
        table=dmc.Table(
                striped=True,
                highlightOnHover=True,
                withBorder=True,
                withColumnBorders=True,
                children=create_table(df_table),
                #style={'backgroundColor': '#f7f7f7'}

            )
        return  barSegment(options,segmented,importe,radio,radio_top),card_ventas(cantidad_productos,None,f"Total Ventas ({radio})"),card_ventas(cantidad_clientes,None,f"Total de {segmented}"),table
    
    @app.callback(
            
            Output('tabs-g','children'),
            Input("data-values","data"),
            Input("radio-moneda","value"),
            #Input("filter-tab","value"),
            Input("segmented","value"),
            Input('radio-top-data','value')
            #Input("check-igv","value"),

            )
            #"""
            #Output("tab-ST","children"),
            #Output("tab-S","children"),
            #Output("tab-P","children"),
            #Output("tab-G","children"),
            #Output("tab-Cultivo","children"),
            #Output("tab-Producto","children"),
            #Output("filter-tab","data"),
            #"""
    def ventas(data, radio, segmented,radio_top):#year,cultivo,variedad,cliente,
            options=pd.read_json(data, orient='split')

            if radio=='Soles':
                    importe='Importe en Soles'
            else:
                    importe='Importe en Dolares'
            
            data_filtro=options['Cliente'].unique()
            
            
            """
            if filtro == None or len(filtro) == 0:

                df_15=options.groupby(['Cliente'])[[importe]].sum().sort_values(importe,ascending=False).reset_index().head(20)
                df=options[options['Cliente'].isin(df_15['Cliente'].unique())]
            else:
                df=options[options['Cliente'].isin(filtro)]
            """
            if segmented == 'Cliente':

                tabs_cliente=['Sucursal','Pais','Tipo de Venta','Cultivo','Producto']
                tabs=loadingOverlay(dmc.Tabs(
                    [
                        dmc.TabsList(
                            [
                            
                                dmc.Tab(children=tab,value=tab)for tab in tabs_cliente
                            ]
                        ),
                        
                            html.Div([dmc.TabsPanel(dbc.Card(dcc.Graph(figure=tabVentaDfGraph(options,segmented,tabs_cliente[i],importe,radio_top),className="shadow-sm")), value=tabs_cliente[i]) for i in range(len(tabs_cliente))]),

                    ],
                    value=tabs_cliente[0],
                )),


            elif segmented == 'Producto':
                tabs_producto=['Sucursal','Pais','Tipo de Venta','Cultivo','Cliente']
                tabs=dmc.Tabs(
                    [
                        dmc.TabsList(
                            [
                            
                                dmc.Tab(children=tab,value=tab)for tab in tabs_producto
                            ]
                        ),
                        
                            html.Div([dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(figure=tabVentaDfGraph(options,segmented,tabs_producto[i],importe,radio_top)),className="shadow-sm")), value=tabs_producto[i]) for i in range(len(tabs_producto))]),

                    ],
                    value=tabs_producto[0],
                ),
            elif segmented == 'Tipo de Venta':
                tabs_tipoventa=['Sucursal','Pais','Grupo de Venta','Cultivo','Cliente','Producto']
                tabs=dmc.Tabs(
                    [
                        dmc.TabsList(
                            [
                            
                                dmc.Tab(children=tab,value=tab)for tab in tabs_tipoventa
                            ]
                        ),
                        
                            html.Div([dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(figure=tabVentaDfGraph(options,segmented,tabs_tipoventa[i],importe,radio_top)),className="shadow-sm")), value=tabs_tipoventa[i]) for i in range(len(tabs_tipoventa))]),

                    ],
                    value=tabs_tipoventa[0],
                ),

            
            

            return tabs
    @app.callback(
    Output("modal", "is_open"),
    Output("modal", "children"),
    Input("btn-modal", "n_clicks"),

    Input('graph-1','figure'),
    #prevent_initial_call=True,
    )
    def flames_x_modal(n_clicks,bar):
        fig=go.Figure(bar)
        fig.update_layout(height=1500),
        fig.update_layout(yaxis=dict(titlefont_size=9,tickfont_size=13))
        children=html.Div(
            [
                dbc.ModalHeader(close_button=True),
                    #dbc.ModalTitle("Pantalla Completa"), close_button=True
                #),
                dbc.ModalBody(
                    [   
                        
                        #bar.update_layout(height=1500),
                        html.Div(dcc.Graph(figure=fig))
                    ]
                ),
            ],
        )

        if n_clicks:
            return True, children
        return False, no_update