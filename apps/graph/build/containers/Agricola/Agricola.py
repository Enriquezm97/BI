from turtle import color
from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import plotly.express as px
from dash_iconify import DashIconify
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
from apps.graph.data.data import *
from apps.graph.build.utils.controls_utils import *
from apps.graph.build.utils.dict_colors import *
from datetime import datetime, date

from apps.graph.build.components.mantine_react_components.loaders import loadingOverlay
from apps.graph.build.components.mantine_react_components.selects import select,multiSelect
from apps.graph.build.components.mantine_react_components.radio import radioGroup
from apps.graph.build.components.mantine_react_components.checkbox import checkboxGroup,checkboxChild,checkList
from apps.graph.build.components.mantine_react_components.actionIcon import btnFilter
#from apps.graph.build.components.mantine_react_components.drawer import drawer
from apps.graph.build.components.bootstrap_components.offcanvas import offcanvas
from apps.graph.build.components.mantine_react_components.accordion import accordion
from apps.graph.utils.callback import *
from apps.graph.utils.utils import colArea
from apps.graph.build.components.mantine_react_components.actionIcon import btnFilter,btnCollapse
from apps.graph.data.transform_produccion import cleanVariablesAgricolas,variablesAgricolasPivot,costosAgricolas
from apps.graph.build.components.draw.card import cardGF,calculateCard
import dash_ag_grid as dag

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




df_consumidores = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
df_var_agricolas_default=cleanVariablesAgricolas(df_consumidores,
                                                  df_variedad,
                                                  df_cultivos,
                                                  df_fertilizacion)
df_costos_agricola_default=costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad)
df_var_agricolas_pivot_default=variablesAgricolasPivot(df_var_agricolas_default)

#import dash_ag_grid as dag

#df2 = pd.read_csv(
#    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
#)
###SCRIPTS PARA EL DATAPICKER EN ESPAÑOL
scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/es.min.js",
]

columnDefs = [
    {
        "field": "country",
        "checkboxSelection": True,
        "headerCheckboxSelection": True,
    },
    {"headerName": "Continent", "field": "continent"},
    {
        "headerName": "Life Expectancy",
        "field": "lifeExp",
        "type": "rightAligned",
        "valueFormatter": {"function": "d3.format('.1f')(params.value)"},
    },
    {
        "headerName": "Population",
        "field": "pop",
        "type": "rightAligned",
        "valueFormatter": {"function": "d3.format(',.0f')(params.value)"},
    },
    {
        "headerName": "GDP per Capita",
        "field": "gdpPercap",
        "type": "rightAligned",
        "valueFormatter": {"function": "d3.format('$,.1f')(params.value)"},
    },
]

def TableDtScrolling_no_color(dff):
    
    
    fig = dash_table.DataTable(#id=idd, 
                                    columns=[{"name": c, "id": c,
                                     "type": "numeric", "format": Format(group=",", precision=0,scheme="f")} for c in dff
                                     ],
                                    
                                    style_cell={
                                            'padding': '12px',
                                            'font-family': 'sans-serif',
                                            'font-size': '14px',
                                            'text_align': 'left',
                                        },
                                        style_header={
                                            'backgroundColor': 'white',
                                            'fontWeight': 'bold',
                                            'text_align': 'left',
                                            'font-size': '14px',
                                        },
                                    style_data_conditional=[
                                        {
                                            "if": {"row_index": "even"},
                                            "backgroundColor": "#f5f6f7",
                                        },
                                        {
                                            "if": {"row_index": "odd"},
                                            "backgroundColor": "#ffffff",
                                        },
                                        
                   
                                        {
                                            'if': {
                                                'filter_query': '{CULTIVO} = "TOTAL"',
                                            },
                                            'backgroundColor': '#0074D9',
                                            'color': 'white'
                                        },
                                    ],
                                    data=dff.to_dict('records'),
                                    page_action='none',
                                    sort_action="native",
                                    style_table={#'height': '310px',
                                                'maxHidth': '310px',
                                                'overflowY': 'auto'
                                    },
                                    fixed_rows={'headers': True},
                                 )
    #return dbc.Card(dbc.CardHeader("Card header"),dbc.CardBody([fig]),color="primary", outline=True),
    return fig


        
def line_agricola_card(df,x,y,color,heig,x_title,y_title,title_legend,orders={},title='',):
    #tipo=df['TIPO'].unique()[0]
    if x=='week':
        ejex='SEMANA'
    else:
        ejex='Fecha'
    #if tipo=='Riego':
    #    simbol=''
    fig=px.line(df, x=x, y=y, color=color,template='plotly_white',
                color_discrete_map=dict_recursos_agricola,
                category_orders=orders,
                title=title,
                hover_name=color,
                custom_data=['CANTXHA'],
                
                #text='CANTXHA'
                #hover_data=[]
                
                #hover_data={x:True,y:True},
                #hovertemplate ='<br><b>{ejex}</b>:%{x}'+
                #               '<br><b>Cantidad</b>: %{y}<br>'+
                #               '<br> %{color}',
                               )
    #fig.update_traces(hovertemplate="<br>".join([
    #                                            "ColX: %{x}",
    #                                            "ColY: %{y}",
    ##                                            "Col1: %{customdata[0]}",
    #                                            
    #                                        ])
    #)
    fig.update_layout(margin=dict(l=20,r=20,b=20,t=60,pad=0,autoexpand=True),#height=heig,
        xaxis_title=ejex,
        yaxis_title=y_title,
        legend_title_text=title_legend,
        height=280,
        
        )
    if title_legend=='Fertilizantes':
        hover='<br><b>Cantidad</b>: %{y:.1f} Kg<br> <b>Unidad/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=9
    elif title_legend=='Horas Máquina':
        hover='<br><b>Cantidad</b>: %{y:.1f} h<br> <b>Hm/Ha</b>: %{customdata[0]:.1f} <br>'
        size_text=9
    elif title_legend=='Mano de Obra':
        hover='<br><b>Cantidad</b>: %{y:.1f} jr<br> <b>Jr/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=9
    elif title_legend=='Riego':
        hover='<br><b>Cantidad</b>: %{y:.1f} m3<br> <b>m3/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=9
    else: 
        hover='<br><b>Cantidad</b>: %{y:.1f}<br>{text} <b>-/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=8
    fig.update_traces(hovertemplate =hover)
    fig.update_xaxes(tickfont=dict(size=9)) 
    fig.update_yaxes(tickfont=dict(size=9))
    fig.update_layout(hovermode="x unified",hoverlabel=dict(font_size=size_text,font_family="sans-serif"))

    #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    
    
        
    return fig

from apps.graph.data.transform_produccion import *

def plandeSiembra(empresa):
    """"""
    #df_consumidores = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    #df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
    #df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    #df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
    #df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
    #df_var_agricolas_default=cleanVariablesAgricolas(df_consumidores,
    #                                              df_variedad,
    #                                              df_cultivos,
    #                                              df_fertilizacion)
    #df_var_agricolas_pivot_default=variablesAgricolasPivot(df_var_agricolas_default)
    #df_costos_agricola_default=costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad)
    """"""
    """
    data=dataAgricolaEmpresa(empresa)
    df_general=data[0]
    df_general_pivot=data[1]
    """
    df_general=df_var_agricolas_default
    df_general_pivot=df_var_agricolas_pivot_default


    #data=dataAgricolaEmpresa(empresa)
    #df_general=data[0]
    #df_general_pivot=data[1]
    #DATAFRAME FOR FILTRO AND VALUE YEAR
    df_produccion=df_general.groupby(['AÑO_CAMPAÑA','FECHAINICIO_CAMPAÑA','FECHAFIN_CAMPAÑA','CULTIVO','AÑO_CULTIVO','VARIEDAD','DSCVARIABLE','FECHA','CONSUMIDOR'])[['CANTIDAD']].sum().reset_index()
    external_stylesheets = [dbc.themes.LITERA]#
    app = DjangoDash('vagricola',external_stylesheets=external_stylesheets,external_scripts=scripts)
    app.layout = html.Div([
            dbc.Modal(
                            id="modal",
                            fullscreen=True,
                            #size="xl",
                            #style={"max-width": "none", "width": "90%", "max-height":"none", "height":"90%"}

                            ),
        dbc.Row([
            dbc.Col([
                    html.Div(id='title'),
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([btnFilter()],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
            dbc.Col([select(ids="drop_anio",texto="Campaña-Cultivo",value=sorted(df_produccion['AÑO_CULTIVO'].unique())[-1])],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([select(ids="drop_variedad",texto="Variedad")],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([select(ids="drop_lote",texto="Lote")],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
            dbc.Col([
                html.Div(
                        [
                            dmc.DateRangePicker(
                                id="date-range-picker",
                                label="Fecha inicio y fin - Campaña",
                                locale="es",
                                disabled=True
                                #minDate=date(2020, 8, 5),
                                #value=[datetime.now().date(), datetime.now().date() + timedelta(days=5)],
                                #style={"width": 330},
                            ),
                            dmc.Space(h=10),
                            dmc.Text(id="selected-date-date-range-picker"),
                        ]
                    )
            ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
            #dbc.Col([select(ids="drop_anio",texto="Campaña",value=sorted(df_produccion['AÑO_CAMPAÑA'].unique())[-1])],width=2,className="col-xl-2 col-md-3 col-sm-12 col-12 mb-3"),
            #dbc.Col([multiSelect(ids="drop_cultivo",texto="Cultivos")],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
            
            
            dbc.Col([btnCollapse(),],width=1,className="col-xl-1 col-md-1 col-sm-12 col-12 mb-3"),
            
            
        ]),
        
        offcanvas(componentes=[
            radioGroup(ids="radio-st",
                                texto="Serie de Tiempo",
                                children=[dmc.Radio(label='Fecha', value='FECHA'),
                                       dmc.Radio(label='Semana', value='week')],
                                value='week'),
            radioGroup(ids="recursos",
                                texto="Serie de Tiempo",
                               children=[dmc.Radio(label='Por Cantidad', value='cantidad'),
                                       dmc.Radio(label='Por Hectárea', value='hectarea')],
                                value='cantidad'),
            #checkboxGroup(orientacion="vertical"),
            dbc.Checklist(  
                                    id="check-agricola",
                                    #options=options,
                                    #value=value,
                                    inline=False,
                                    #label_checked_style={"color": "red"},
                                    input_checked_style={
                                        "backgroundColor": "rgb(34, 139, 230)",
                                        "borderColor": "rgb(34, 139, 230)",
                                    },     
                                    label_style={'font-size': '12px'} 
                            ),
            
            #checkList(ids="check-agricola",texto="Recursos Agricolas")
        ]),
    #dbc.Collapse(
                #dbc.Row([
            
                    #dbc.Col([html.Div(children=loadingOverlay(dbc.Card(dcc.Graph(id='graph-1'),className="shadow-sm")),style={'max-height': '490px','overflow': "auto"})],width=5,className="col-xl-5 col-md-5 col-sm-12 col-12 mb-3"),
    #                dbc.Col([
    #                    html.Div(id='badge-lotes')
    #                ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
    #           ]),
    #        id="collapse",is_open=True),
    dbc.Row([
                dbc.Col([
                    loadingOverlay(html.Div(id='tabs')),
                ],width=8,className="col-xl-8 col-md-8 col-sm-12 col-12 mb-3"),
                dbc.Col([
                    loadingOverlay(html.Div(id='table-grid-lotes')),
                ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
                #dbc.Col([
                #    dmc.ActionIcon(
                #                        DashIconify(icon='feather:maximize'), 
                #                        color="blue", 
                #                        variant="default",
                #                        id="btn-modal",
                #                        n_clicks=0,
                #                        mb=10,
                #                    ),
                    
                
                #],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
                
            ]),
        
        dbc.Row([   
                dbc.Col([
                
                     #html.Label("Cultivos",
                     #       style={'font-size': 24,
                     #               'text-align': 'left',
                     #               },
                    #),
        accordion(children=[
            loadingOverlay(
                dash_table.DataTable(
                    id='table-cultivo',
                    #columns=[{"name": c, "id": c,
                    #         "type": "numeric", "format": Format(group=",", precision=0,scheme="f")} for c in d.dff_t_end],
                    #active_cell={"row": 0, "column": 0, "column_id": 0, "row_id": 0},
                    #active_cell={},
                    sort_action="native",
                    page_action='none',
                    style_table={
                                  'minHeight': '100px',
                                  'maxHeight': '310px',
                                 'overflowY': 'auto'},
                    fixed_rows={'headers': True},
                    style_as_list_view=True,
                    style_cell={'padding': '12px',
                                 'font-family': 'sans-serif',
                                  'font-size': '14px',
                                  'text_align': 'left',
                                },
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'text_align': 'left',
                        'font-size': '14px',
                    },
                    style_data_conditional=[
                        {'if': {'filter_query': '{CULTIVO} = "TOTAL"',},
                                    'backgroundColor': '#0074D9',
                                    'color': 'white',
                                    'fontWeight': 'bold',
                        },
                    ]
                    #page_size= 10,
                    #style_table={'overflowY': 'auto','height': '250px',},
                    #style_table={'overflowY': 'auto'},
                    

                ),)
            ],texto='Tabla Cultivo',value='cultivo')
                    
                
                
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            
            
        ]),
        
        
        dbc.Row([
                dbc.Col([
                    #html.Label("Lotes",style={'font-size': 24,'text-align': 'left'}),
                accordion(children=[
                        loadingOverlay(html.Div(id='table-lote')),html.Div(id='cultivo_cell'),
                ],texto='Tabla Lotes',value='lote'),
                
                ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            ]),
        dbc.Row([
            dbc.Col([
                #dag.AgGrid(
                #    id="datatable-interactivity",
                #    columnDefs=columnDefs,
                #    rowData=df2.to_dict("records"),
                #    dashGridOptions={"rowSelection": "multiple"},
                #    columnSize="sizeToFit",
                #    defaultColDef={"resizable": True, "sortable": True, "filter": True},
                #),
                #html.Div(id="datatable-interactivity-container"),
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
        ]),
        
        
        
    ])#, style={'backgroundColor':'blue'}
   
    offcanvasAction(app)
    @app.callback(Output('drop_anio','data'),
                #Output('drop_cultivo', 'data'),
                Output('drop_variedad', 'data'),
                Output('check-agricola','options'),
                Output('check-agricola','value'),  
                #Output('subtitle','children'), 
                Output('drop_lote','data'),
                #Output('badge-lotes','children'),
                Output("date-range-picker",'value'),#minDate=date(2020, 8, 5),
                Output("date-range-picker",'minDate'),
                Output("date-range-picker",'maxDate'),
                #Output("selected-date-date-range-picker","children"),
                #Output('estado-ha','children'),
                
                  #Output('drop_variedad', 'options'),
              [Input('drop_anio','value'),
               #Input('drop_cultivo','value'), 
               Input('drop_variedad','value'),
               Input('drop_lote','value'),
               #Input("date-range-picker", "value"),
               #Input('recursos','value'),
               #drop_lote
              ])
    def update_drop_cultivo(year_cultivo,variedad,lote):#,cultivo#,recurso#
        #print(date[0])
        #print(date[1])
        #df_produccion = df_produccion[df_produccion["FECHA"].isin(pd.date_range(date[0], date[1]))]
        #if recurso =='hectarea':
        #      estado='x Ha'
        #else:
        #      estado='x Cantidad'
        #df=DataAgricola.data_general(ip)
        #if year==None and (cultivo==None or len(cultivo)==0) and variedad==None:
        #    options=df_produccion
        #elif year!=None and (cultivo==None or len(cultivo)==0)and variedad==None:
        #    options=df_produccion[df_produccion['AÑO_CAMPAÑA']==year]
        #elif year==None and (cultivo!=None or len(cultivo)>0)and variedad==None:
        #    options=df_produccion[df_produccion['CULTIVO'].isin(cultivo)]
        #elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad==None:# or len(cultivo)>0
        #    options=df_produccion[(df_produccion['CULTIVO'].isin(cultivo))&(df_produccion['AÑO_CAMPAÑA']==year)]

        #elif year==None and (cultivo==None or len(cultivo)==0) and variedad!=None:
        #    options=df_produccion[df_produccion['VARIEDAD']==variedad]
        #elif year!=None and (cultivo==None or len(cultivo)==0) and variedad!=None:
        #    options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['AÑO_CAMPAÑA']==year)]
        #elif year==None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
        #    options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['CULTIVO'].isin(cultivo))]
        #elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
        #    options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['AÑO_CAMPAÑA']==year)&(df_produccion['CULTIVO'].isin(cultivo))]
        if year_cultivo==None and variedad==None and lote==None:
            options=df_produccion
        elif year_cultivo!=None and variedad==None and lote==None:
            options=df_produccion[df_produccion['AÑO_CULTIVO']==year_cultivo]
        elif year_cultivo!=None and variedad!=None and lote==None:
            options=df_produccion[(df_produccion['AÑO_CULTIVO']==year_cultivo)&(df_produccion['VARIEDAD']==variedad)]
        elif year_cultivo!=None and variedad!=None and lote!=None:
            options=df_produccion[(df_produccion['AÑO_CULTIVO']==year_cultivo)&(df_produccion['VARIEDAD']==variedad)&(df_produccion['CONSUMIDOR']==lote)] 
        elif year_cultivo!=None and variedad==None and lote!=None:
            options=df_produccion[(df_produccion['AÑO_CULTIVO']==year_cultivo)&(df_produccion['CONSUMIDOR']==lote)] 
        
        elif year_cultivo==None and variedad!=None and lote!=None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['CONSUMIDOR']==lote)]
        
        elif year_cultivo==None and variedad!=None and lote==None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)]
        elif year_cultivo==None and variedad==None and lote!=None:
            options=df_produccion[(df_produccion['CONSUMIDOR']==lote)]
        

        anio=[{'label': i, 'value': i} for i in options['AÑO_CULTIVO'].unique()]
        #cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()]
        variedad=[{'label': i, 'value': i} for i in options['VARIEDAD'].unique()]
        #check=checkboxChild(options['DSCVARIABLE'].unique())
        check=[{'label': i, 'value': i} for i in options['DSCVARIABLE'].unique()]

        lotes=[{'label': i, 'value': i} for i in options['CONSUMIDOR'].unique()]
        
        minimo=str(options['FECHAINICIO_CAMPAÑA'].min())#
        print(minimo)
        maximo=str(options['FECHAFIN_CAMPAÑA'].max())#.str[0:10]
        print(maximo)
        #inicio_fin=str(minimo)+' - '+str(maximo)
        #badges=html.Div([
        #      dmc.Stack(
        #            spacing="xs",
        #            children=[
        #                dmc.Group(
        #                    [dmc.Badge(lote, variant='dot', color='black',size='lg') for lote in options['CONSUMIDOR'].unique()],
        #                    position="center",
        #                )
        #                
        #            ],
        #        )
        #])
        #datepicker=[date(int(minimo[:4]),int(minimo[-5:-3]),int(minimo[-2:])), date(int(maximo[:4]),int(maximo[-5:-3]),int(maximo[-2:]))],
        datepicker=[options['FECHAINICIO_CAMPAÑA'].min(),options['FECHAFIN_CAMPAÑA'].max()]
        return anio,variedad,check,options['DSCVARIABLE'].unique(),lotes,datepicker,date(int(minimo[:4]),int(minimo[-5:-3]),int(minimo[-2:])),date(int(maximo[:4]),int(maximo[-5:-3]),int(maximo[-2:]))#,estado
    
    
    """
    @app.callback(
    Output("title","children"),
    #Output('estado-ha','children'),
    Input("drop_anio","value"),
    Input("recursos","value"),
    Input('cultivo_cell', 'value'),

    )
    def update_title(anio,recursos,cultivo):
        if cultivo == None:
            text="Ejecución de Campaña "
        else: 
            text="Ejecución de Campaña "+' '+str(cultivo)
        if recursos =='cantidad':
            
            if anio == None:
                title=text
            else:
                title=text+' '+str(anio)
            return title   
        elif recursos == 'hectarea': 
            #text="Plan de Siembra por Héctarea"
            if anio == None:
                title=text
            else:
                title=text+' '+str(anio)
            return title 
    """
    @app.callback(
    Output("title","children"),
    #Output("estado-variedad","children"),
    #Output("estado-ha","children"),
    #Output('estado-ha','children'),
    Input("drop_anio","value"),
    Input('drop_variedad','value'),
    Input("recursos","value"),
   #Input('cultivo_cell', 'value'),

    )
    def update_title(campania,variedad,recursos):
        

        if recursos =='hectarea':
              estado=dmc.Badge('x Ha',variant='filled',color='blue', size='lg')
        elif recursos == 'cantidad':
              estado=dmc.Badge('x Cantidad',variant='filled',color='blue', size='lg')

        if campania == None and variedad == None :
              badge=dmc.Title(id='title',children=['Ejecución de Campaña ',dmc.Badge('ALL',variant='filled',color='gray', size='lg'),estado], order=2,align='center')
        elif campania != None and variedad == None :
              badge=dmc.Title(id='title',children=['Ejecución de Campaña ',dmc.Badge(campania,variant='filled',color='gray', size='lg'),estado], order=2,align='center')
        elif campania != None and variedad != None :
              badge=dmc.Title(id='title',children=['Ejecución de Campaña ',dmc.Badge(campania,variant='filled',color='gray', size='lg'),dmc.Badge(variedad,variant='filled',color='indigo', size='lg'),estado], order=2,align='center')
        elif campania == None and variedad != None :
              badge=dmc.Title(id='title',children=['Ejecución de Campaña ',dmc.Badge(variedad,variant='filled',color='indigo', size='lg'),estado], order=2,align='center')
        return badge
          

    @app.callback(
        Output("collapse", "is_open"),
        [Input("btn-collapse", "n_clicks")],
        [State("collapse", "is_open")],
        )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
    


       

    
    

    


        #return 
        #return fig_fertilizantes,fig_agua,fig_horas

    @app.callback(
        Output('table-cultivo', 'data'),
        Output('cultivo_cell', 'value'),
        Output('table-cultivo','columns'),
        Output('table-lote', 'children'),
        
        #Output('tabs','children'),
        #Output('owo', 'children'),
        [Input('drop_anio','value'),
         #Input('drop_cultivo','value'),
         Input('drop_variedad','value'),
         Input('check-agricola','value'),
         Input('recursos','value'),
         #Input('radio-st','value'), 
         Input('table-cultivo', 'active_cell'),
         Input('drop_lote','value'),
         #Input('cultivo','active_cell'),

         ]
    )   
    def table_cultivo_plansiembra(year_cultivo,variedad,check,recursos,active_cell,lote):#,cultivo
        print(check)
        print(year_cultivo)
        df_produccion=df_general_pivot.copy()
        #if year==None and (cultivo==None or len(cultivo)==0) and variedad==None:
        #    dff=df
        #elif year!=None and (cultivo==None or len(cultivo)==0)and variedad==None:
        #        dff=df[df['AÑO_CAMPAÑA']==year]
        #elif year==None and (cultivo!=None or len(cultivo)>0)and variedad==None:
        #        dff=df[df['CULTIVO'].isin(cultivo)]
        #elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad==None:# or len(cultivo)>0
        #        dff=df[(df['CULTIVO'].isin(cultivo))&(df['AÑO_CAMPAÑA']==year)]

        #elif year==None and (cultivo==None or len(cultivo)==0) and variedad!=None:
        #        dff=df[df['VARIEDAD']==variedad]
        #elif year!=None and (cultivo==None or len(cultivo)==0) and variedad!=None:
        #        dff=df[(df['VARIEDAD']==variedad)&(df['AÑO_CAMPAÑA']==year)]
        #elif year==None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
        #        dff=df[(df['VARIEDAD']==variedad)&(df['CULTIVO'].isin(cultivo))]
        #elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
        #        dff=df[(df['VARIEDAD']==variedad)&(df['AÑO_CAMPAÑA']==year)&(df['CULTIVO'].isin(cultivo))]
        print(df_produccion['AÑO_CULTIVO'].unique())
        if year_cultivo==None and variedad==None and lote==None:
            options=df_produccion
        elif year_cultivo!=None and variedad==None and lote==None:
            options=df_produccion[df_produccion['AÑO_CULTIVO']==year_cultivo]
        elif year_cultivo!=None and variedad!=None and lote==None:
            options=df_produccion[(df_produccion['AÑO_CULTIVO']==year_cultivo)&(df_produccion['VARIEDAD']==variedad)]
        elif year_cultivo!=None and variedad!=None and lote!=None:
            options=df_produccion[(df_produccion['AÑO_CULTIVO']==year_cultivo)&(df_produccion['VARIEDAD']==variedad)&(df_produccion['CONSUMIDOR']==lote)] 
        elif year_cultivo!=None and variedad==None and lote!=None:
            options=df_produccion[(df_produccion['AÑO_CULTIVO']==year_cultivo)&(df_produccion['CONSUMIDOR']==lote)] 
        
        elif year_cultivo==None and variedad!=None and lote!=None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['CONSUMIDOR']==lote)]
        
        elif year_cultivo==None and variedad!=None and lote==None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)]
        elif year_cultivo==None and variedad==None and lote!=None:
            options=df_produccion[(df_produccion['CONSUMIDOR']==lote)]

        

        
        #df_general_pivot['AÑO_CAMPAÑA']=df_general_pivot['AÑO_CAMPAÑA'].astype(object)
        dff_area=colArea(options)
        
        dff_pt=dff_area.groupby(['CULTIVO']).sum().reset_index()
        dff_pt=dff_pt.rename(columns={
                                        'Nitrógeno':'Nitrogeno',
                                        'Fósforo':'Fosforo',

                                       })
        dff_pt=dff_pt[['CULTIVO','AREA_CAMPAÑA']+check]
        ### CONSUMIDORES
        dff_lotes=dff_area.groupby(['CONSUMIDOR','CULTIVO']).sum().reset_index()
        dff_lotes=dff_lotes.rename(columns={
                                        'Nitrógeno':'Nitrogeno',
                                        'Fósforo':'Fosforo',

                                       })
        
        ###################
        if active_cell is None:
                cultivo_cell=None
                
        elif active_cell != None:
                row = active_cell["row"]
                cultivo_cell = dff_pt.iloc[row,0]
                dff_lotes=dff_lotes[dff_lotes['CULTIVO']==cultivo_cell]
                #dff=dff[dff['CULTIVO']==cultivo_cell]
        ##CONSUMIDORES SIN LA COLUMNA CULTIVO
        dff_lotes=dff_lotes[['CONSUMIDOR','AREA_CAMPAÑA']+check]
        ## DF GRAPH
        #df_graph=dff.groupby(['DSCVARIABLE','TIPO',radio_st])[['CANTIDAD']].sum().reset_index()

        if recursos == 'hectarea':
            columns=dff_pt.columns
            columns_lote=dff_lotes.columns
            dff_pt['AREA_CAMPAÑA']=dff_pt['AREA_CAMPAÑA'].astype('float64')
            dff_lotes['AREA_CAMPAÑA']=dff_lotes['AREA_CAMPAÑA'].astype('float64')
            for recurso in columns[2:]:
                dff_pt[recurso]=dff_pt[recurso]/dff_pt['AREA_CAMPAÑA']
            for recurso2 in columns_lote[2:]:
                dff_lotes[recurso2]=dff_lotes[recurso2]/dff_lotes['AREA_CAMPAÑA']
        dff_lotes=dff_lotes.round(1)
        dff_pt.loc['TOTAL',:]= dff_pt.sum(numeric_only=True, axis=0)      
            #else:
        dff_pt=dff_pt.fillna('TOTAL')
        
        
        col=[{"name": c, "id": c,"type": "numeric", "format": Format(group=",", precision=0,scheme="f")} for c in dff_pt]
        #df_testeo=dff.groupby(['week','AÑO_FECHA','SEMANA'])[[check]].sum().reset_index()
        #fig = go.Figure()
        #for i in check:
        #    fig.add_trace(go.Scatter(x=df_testeo['week'], y=df_testeo[i],
        #                        mode='lines',
        #    
        #                    name='lines'))
        columnDefs = [{"field": i, "type": "rightAligned"} for i in dff_lotes.columns]
        table_grid=html.Div([
                dag.AgGrid(
                columnDefs=columnDefs,
                rowData=dff_lotes.to_dict("records"),
                columnSize="sizeToFit",
                defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":100},
                #columnDefs=columnDefs,
            ), 
        ])
                
                                 
        return dff_pt.to_dict('rows'),cultivo_cell,col,table_grid#TableDtScrolling_no_color(dff_lotes)#,fig  
    
    @app.callback(
        #Output('fertilizantes', 'figure'),
        #Output('agua', 'figure'),
        #Output('horas', 'figure'),
        Output('tabs','children'),
        Output("table-grid-lotes",'children'),
        [Input('drop_anio','value'),    
         #Input('drop_cultivo','value'),
         Input('drop_variedad','value'),
         Input('check-agricola','value'),
         Input('radio-st','value'),
         Input('recursos','value'),
        Input('drop_lote','value'),
         #Input('drop_lote','value')
         ]
         #Input('cultivo_cell', 'value'),
    )  

    def LineMultivar(year_cultivo,variedad,check,radio_st,recursos,lote):#,cultivo_cell#,cultivo
        #if cultivo_cell == None:
        #lote=None
        #    df_produccion=df_general
        #else:
        #    df_produccion=df_general[df_general['CULTIVO']==cultivo_cell]
        
        df_produccion=df_general.copy()
        #if year==None and (cultivo==None or len(cultivo)==0) and variedad==None:
        #    dff=df_produccion
        #elif year!=None and (cultivo==None or len(cultivo)==0)and variedad==None:
        #    dff=df_produccion[df_produccion['AÑO_CAMPAÑA']==year]
        #elif year==None and (cultivo!=None or len(cultivo)>0)and variedad==None:
        #    dff=df_produccion[df_produccion['CULTIVO'].isin(cultivo)]
        #elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad==None:# or len(cultivo)>0
        #    dff=df_produccion[(df_produccion['CULTIVO'].isin(cultivo))&(df_produccion['AÑO_CAMPAÑA']==year)]

        #elif year==None and (cultivo==None or len(cultivo)==0) and variedad!=None:
        #    dff=df_produccion[df_produccion['VARIEDAD']==variedad]
        #elif year!=None and (cultivo==None or len(cultivo)==0) and variedad!=None:
        #    dff=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['AÑO_CAMPAÑA']==year)]
        #elif year==None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
        #    dff=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['CULTIVO'].isin(cultivo))]
        #elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
        #    dff=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['AÑO_CAMPAÑA']==year)&(df_produccion['CULTIVO'].isin(cultivo))]
        if year_cultivo==None and variedad==None and lote==None:
            options=df_produccion
        elif year_cultivo!=None and variedad==None and lote==None:
            options=df_produccion[df_produccion['AÑO_CULTIVO']==year_cultivo]
        elif year_cultivo!=None and variedad!=None and lote==None:
            options=df_produccion[(df_produccion['AÑO_CULTIVO']==year_cultivo)&(df_produccion['VARIEDAD']==variedad)]
        elif year_cultivo!=None and variedad!=None and lote!=None:
            options=df_produccion[(df_produccion['AÑO_CULTIVO']==year_cultivo)&(df_produccion['VARIEDAD']==variedad)&(df_produccion['CONSUMIDOR']==lote)] 
        elif year_cultivo!=None and variedad==None and lote!=None:
            options=df_produccion[(df_produccion['AÑO_CULTIVO']==year_cultivo)&(df_produccion['CONSUMIDOR']==lote)] 
        
        elif year_cultivo==None and variedad!=None and lote!=None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['CONSUMIDOR']==lote)]
        
        elif year_cultivo==None and variedad!=None and lote==None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)]
        elif year_cultivo==None and variedad==None and lote!=None:
            options=df_produccion[(df_produccion['CONSUMIDOR']==lote)]

        
        df_ha_sembrado=options.groupby(['CONSUMIDOR',radio_st,'SEMANA','CULTIVO','VARIEDAD','AÑO_FECHA','AÑO_CAMPAÑA','AREA_CAMPAÑA','AÑO_CULTIVO'])[['CANTIDAD']].sum().reset_index()
        df_ha_total=df_ha_sembrado.groupby(['CONSUMIDOR',radio_st,'SEMANA','VARIEDAD','AÑO_FECHA','AÑO_CAMPAÑA','AÑO_CULTIVO'])[['AREA_CAMPAÑA']].sum().reset_index()
        df_ha_st=df_ha_total.groupby([radio_st,'SEMANA','AÑO_FECHA','AÑO_CAMPAÑA','AÑO_CULTIVO'])[['AREA_CAMPAÑA']].sum().reset_index()
        df_ha_st=df_ha_st[[radio_st,'AREA_CAMPAÑA']]
        
        
            #if drop_anio==None:

            #    x='week'
            #    df_test2=dff.groupby(['DSCVARIABLE','week'])[['CANTIDAD']].sum().sort_values('week',ascending=True).reset_index()
        
            #elif drop_anio!=None:
            #    x='SEMANA'
            #    df_test2=dff.groupby(['DSCVARIABLE','SEMANA'])[['CANTIDAD']].sum().sort_values('SEMANA',ascending=True).reset_index()
        df_graph=options.groupby(['DSCVARIABLE','TIPO',radio_st,'AÑO_FECHA','SEMANA'])[['CANTIDAD']].sum().reset_index()
        df_graph=df_graph.merge(df_ha_st, how='inner', left_on=[radio_st], right_on=[radio_st])

        df_graph.loc[df_graph.DSCVARIABLE == 'Nitrógeno','DSCVARIABLE'] =  'Nitrogeno'  
        df_graph.loc[df_graph.DSCVARIABLE == 'Fósforo','DSCVARIABLE'] =  'Fosforo'  
        df_graph=df_graph[df_graph['DSCVARIABLE'].isin(check)]
        df_graph['CANTXHA']=df_graph['CANTIDAD']/df_graph['AREA_CAMPAÑA']
        if recursos == 'hectarea':
              df_graph['CANTIDAD']=df_graph['CANTIDAD']/df_graph['AREA_CAMPAÑA']
              #df_graph['CANTXHA']=df_graph['CANTIDAD']/df_graph['AREA_CAMPAÑA']
        list_tipo=df_graph['TIPO'].unique()

        df_fer=df_graph[df_graph['TIPO']=='Insumos']
        df_fer=df_fer[df_fer['DSCVARIABLE'].isin(check)]
        df_fer=df_fer.sort_values(by=[radio_st,'AÑO_FECHA','SEMANA'],ascending=True)

        df_agua=df_graph[df_graph['TIPO']=='Riego']
        df_agua=df_agua[df_agua['DSCVARIABLE'].isin(check)]
        df_agua=df_agua.sort_values(by=[radio_st,'AÑO_FECHA','SEMANA'],ascending=True)

        df_horas=df_graph[df_graph['TIPO']=='Mano de obra']
        df_horas=df_horas[df_horas['DSCVARIABLE'].isin(check)]
        df_horas=df_horas.sort_values(by=[radio_st,'AÑO_FECHA','SEMANA'],ascending=True)

        df_horas_maquina=df_graph[df_graph['TIPO']=='Maquinaria']
        df_horas_maquina=df_horas_maquina[df_horas_maquina['DSCVARIABLE'].isin(check)]
        df_horas_maquina=df_horas_maquina.sort_values(by=[radio_st,'AÑO_FECHA','SEMANA'],ascending=True)

        #fig_fertilizantes=px.line(df_fer, x=x, y="CANTIDAD", color='DSCVARIABLE',template='plotly_white',height=280,margin=dict(l=60,r=40,b=40,t=70,pad=0,autoexpand=True))
        #fig.update_layout(height=380,margin=dict(l=60,r=40,b=40,t=70,pad=0,autoexpand=True),
        def orderX(x,df):
            if x == 'week':
                order={'week':sorted(df['week'].unique()),'DSCVARIABLE': sorted(df['DSCVARIABLE'].unique())}
            else: 
                order={}
            return order

        def titleConcat(title,cultivo,variedad):
            if variedad == None and (len(cultivo)==0 or cultivo==None):
                titulo=title
            elif variedad == None and (len(cultivo)>0 or cultivo!=None):
                titulo=f"{title} "+", ".join(cultivo)
            elif variedad != None and (len(cultivo)>0 or cultivo!=None):
                titulo=f"{title} "+", ".join(cultivo)+" -{}".format(variedad)
            return titulo

        fig_fertilizantes=line_agricola_card(df_fer,radio_st,"CANTIDAD",'DSCVARIABLE',330,radio_st,'Unidades','Fertilizantes',orders=orderX(radio_st,df_fer),title='Fertilizantes')
        fig_agua=line_agricola_card(df_agua,radio_st,"CANTIDAD",'DSCVARIABLE',330,radio_st,'Metros Cúbicos','Riego',orders=orderX(radio_st,df_agua),title='Riego')
        #fig_horas=px.line(df_horas, x=x, y="CANTIDAD", color='DSCVARIABLE',template='plotly_white',height=280,margin=dict(l=60,r=40,b=40,t=70,pad=0,autoexpand=True))
        fig_horas=line_agricola_card(df_horas,radio_st,"CANTIDAD",'DSCVARIABLE',330,radio_st,"Cantidad",'Mano de Obra',orders=orderX(radio_st,df_horas),title='Mano de Obra')
        fig_horas_maquinaria=line_agricola_card(df_horas_maquina,radio_st,"CANTIDAD",'DSCVARIABLE',330,radio_st,"Horas",'Horas Máquina',orders=orderX(radio_st,df_horas_maquina),title='Horas Máquina')

        child=html.Div(
            
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab(i, value=i)for i in list_tipo
                        ]
                    ),
                    #dbc.Card(dcc.Graph(id='graph-partida-pronostico'),className="shadow-sm")
                    dmc.TabsPanel(dbc.Card(dcc.Graph(figure=fig_agua),className="shadow-sm"), value='Riego'),
                    dmc.TabsPanel(dbc.Card(dcc.Graph(figure=fig_horas_maquinaria),className="shadow-sm"), value='Maquinaria'),
                    dmc.TabsPanel(dbc.Card(dcc.Graph(figure=fig_horas),className="shadow-sm"), value='Mano de obra'),
                    dmc.TabsPanel(dbc.Card(dcc.Graph(figure=fig_fertilizantes),className="shadow-sm"), value='Insumos'),
                ],
                value=list_tipo[0],
              ),
        ) 
        df_tablew=df_ha_total.groupby(['CONSUMIDOR',radio_st,'VARIEDAD','AÑO_FECHA','AÑO_CAMPAÑA'])[['AREA_CAMPAÑA']].sum().reset_index()
        
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
                                                'font-size': '10px',
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
                                        'font-size': '11px',    
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
        
        return child,table_Dash_plotly
    @app.callback(
    Output("modal", "is_open"),
    Output("modal", "children"),
    Input("btn-modal", "n_clicks"),
    State('tabs','children'),
    )
    def flames_x_modal(n_clicks,tabs):
        
        children=html.Div(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Pantalla Completa"), close_button=True
                ),
                dbc.ModalBody(
                    [
                        tabs
                    ]
                ),
            ],
        )

        if n_clicks:
            return True, children
        return False, no_update

"""   
    @app.callback(
        Output('multiejes', 'figure'),
        [Input('drop_anio','value'),    
         Input('drop_cultivo','value'),
         #Input('check-agricola','value'),
         Input('radio-st','value')]
    )  

    def Line_vagricola_ST_multieje(drop_anio,drop_cultivo,radio_st):
        if radio_st == 'fecha':
            title="Serie de Tiempo Multiejes"
            x="FECHA"
            
            #x=[df['AÑO_CAMPAÑA'],df['SEMANA']]

        elif radio_st == 'semana':
            title="Serie de Tiempo Multiejes x Semana"
            x="SEMANA"
            

        #dfg=DataAgricola.data_general(ip)
        dfg=df_general
        

        if drop_anio== None and (drop_cultivo == None or len(drop_cultivo) == 0):

            dff=dfg

        elif drop_anio !=None and (drop_cultivo == None or len(drop_cultivo) == 0):
            dff = dfg[(dfg['AÑO_CAMPAÑA']==drop_anio)]

        elif drop_anio != None and drop_cultivo != None:
                
                
            dff = dfg[(dfg['AÑO_CAMPAÑA']==drop_anio) & (dfg['CULTIVO'].isin(drop_cultivo))]
            
        #print(dff)    
        dff_end= dff.groupby([x,'CODVARIABLE',])[['CANTIDAD']].sum().reset_index()
        dff_end_pivot2=dff_end.pivot_table(index=(x),values=('CANTIDAD'),columns=('CODVARIABLE'))
        dff_end_pivot2.reset_index()
        dff_end_pivot2=pd.DataFrame(dff_end_pivot2.to_records())
        
            
        return LineGraph_vagricolas(dff_end_pivot2,title,x)
"""   
def OffcanvasAgricolaCostos(idd_costos,r,check):

    return dbc.Offcanvas(
                            [
                             #dbc.Label('Recursos'),
                             
                            dbc.Badge("Tipo de Costo", pill=True, color="dark"), 
                            #rbtn.Radibtn_2_costosHa(idd_costos),


                            dbc.Badge("Moneda", pill=True, color="dark"), 
                            #rbtn.Radibtn_2(r,"Soles","Dolares","sol","dolar"),
                            
                            dbc.Badge("Recursos", pill=True, color="dark"), 
                            
                                #Checklist.Checklist_var_agricola_recursos(check),
                            ],
                            
                            scrollable=True,
                            id="offcanvas-placement",
                            title="Filtros",
                            is_open=False,
                            #placement="end",
                            backdrop=False,
                            style={"width":250}#,"background-color": "S"
                        )
def Table_LOTE_COSTOS(dff):
    #df = get_data()
    fig = dash_table.DataTable(#id=idd, 
                                    columns=[{"name": c, "id": c,
                                     "type": "numeric", "format": Format(group=",", precision=0,scheme="f")} for c in dff
                                     ],
                                     #data=df.to_dict('records'),
                                     style_header={
                                        'backgroundColor': 'white',
                                        'fontWeight': 'bold',
                                        'text_align': 'left',
                                        'font-size': '14px',
                                    },
                                    #sort_action='native',
                                    style_cell={'padding': '12px',
                                        'font-family': 'sans-serif',
                                        'font-size': '14px',
                                        'text_align': 'left',
                                    },
                                    style_data_conditional=[
                                        {
                                            "if": {"row_index": "even"},
                                            "backgroundColor": "#f5f6f7",
                                        },
                                        {
                                            "if": {"row_index": "odd"},
                                            "backgroundColor": "#ffffff",
                                        },
                                    ],
                                    data=dff.to_dict('records'),

                                    style_table={
                                        'minHeight': '100px',
                                        'maxHeight': '310px',
                                        'overflowY': 'auto'},
                                    page_action='none',
                                    sort_action="native",
                                    fixed_rows={'headers': True},   
                                    #page_size=10,
                                    #style_table={'overflowY': 'auto'},
                                    #selected_rows=[],
                                    #row_selectable="single",
                                    #fixed_rows={'headers': True},
                                 )
    return fig
def BarGOV_SX(x, y,title,prueba,dinero,x_title,y_title,promedio,y2,eyey2=True,basex=True):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=y,y=x,name=title,text=x,orientation='v',textposition='outside',texttemplate='%{text:.2s}',marker={'color':[dict_cultivos[i]for i in prueba]}))#,marker={'color':[diccionario[i]for i in prueba]}
    #
    fig.update_layout(title={
                                        'text':title,
                                        #'y': 0.93,
                                        #'x': 0.5,
                                        #'xanchor': 'right',
                                        #'yanchor': 'top',
                                    },
                        titlefont={'color': 'black','size': 15},
                        uniformtext_minsize=8, #uniformtext_mode='hide',
                        template='none',
                        bargap=0.15,)
    fig.update_layout(
        autosize=True,
        #width=100,
        height=300,
        margin=dict(
            l=60,
            r=40,
            b=30,
            t=70,
            #pad=0,
            #autoexpand=True
        ),

        hovermode='closest',
        hoverlabel=dict(

        ),
        #paper_bgcolor='white',
        #plot_bgcolor='white',
        
        #showgrid=False,
        #modeclic='event+select'
        
        #yaxis=dict(
        #    gridcolor='#F2F2F2',
        #    showline=True,
        #    showgrid=True,
        #    ticks='outside',
        #    tickfont=dict(
        #            family='Arial',
        #            color='black',
        #            size=12
        #               )
        #)
    
        )
    fig.update_layout(
    
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend_title="",
        
        )
    
    if eyey2==True : 
        #[1.5, 1, 1.3, 0.7, 0.8, 0.9]
        fig.update_layout(showlegend=False,legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1

                        ))
        fig.add_trace(go.Scatter(
                            x=y,
                            y=y2,
                            name="Hectáreas",
                            yaxis="y4",
                            text=y2,
                            #marker_color="#1f1587",
                            textposition='bottom right',
                            texttemplate='{text:.2s}'
                        ))
        fig.update_layout(
                        yaxis4=dict(title="Hectáreas",anchor="x",overlaying="y",side="right",titlefont_size=12,tickfont_size=12)
                        )
    elif len(prueba.unique())==1:
        fig.add_trace( go.Scatter( x=y, y=promedio,name='Promedio',mode='lines' ))
    #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    if basex == True:#CONSUMIDOR    
        fig.update_xaxes(showticklabels=False)
        fig.update_layout(xaxis=dict(tickfont=dict(color='black',size=11)))
    
    return fig
def TableDtScrolling_no_format(dff):
    #df = get_data()
    fig = dash_table.DataTable(#id=idd, 
                                    columns=[{"name": c, "id": c,
                                     "type": "numeric", "format": Format(group=",", precision=0,scheme="f")} for c in dff
                                     ],
                                     #data=df.to_dict('records'),
                                     style_header={
                                        'textAlign': 'center',
                                        "textTransform": "Uppercase",
                                        "fontWeight": "bold",
                                        "backgroundColor": "#ffffff",
                                        "padding": "10px 0px",
                                    },
                                    sort_action="native",
                                    #sort_action='native',
                                    style_cell={'textAlign': 'left','fontSize':16,"textTransform": "Uppercase"},

                                    data=dff.to_dict('records'),
                                    style_data_conditional=[
                                        {
                                            'if': {
                                                'filter_query': '{RECURSO} = "TOTAL"',
                                            },
                                            'backgroundColor': '#0074D9',
                                            'color': 'white'
                                        },
                                    ]

                                    
                                 )
    return fig
def costosAgricola(empresa):
    """"""
    df_consumidores = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
    df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
    df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
    df_var_agricolas_default=cleanVariablesAgricolas(df_consumidores,
                                                  df_variedad,
                                                  df_cultivos,
                                                  df_fertilizacion)
    df_var_agricolas_pivot_default=variablesAgricolasPivot(df_var_agricolas_default)
    df_costos_agricola_default=costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad)
    """"""
    """
    data=dataAgricolaEmpresa(empresa)
    df_general=data[0]
    df_costos_agricolas=data[2]
    """
    df_general=df_var_agricolas_default
    df_costos_agricolas=df_costos_agricola_default


    #df_general_pivot=data[1]
    #df_general_costos=data[2]
    cultivo_columns=['CULTIVO','AREA_CAMPAÑA','INSUMOS','MANO DE OBRA','MAQUINARIA','RIEGO','OTROS','TOTAL','AH']
    lote_columns=['CONSUMIDOR','AREA_CAMPAÑA','INSUMOS','MANO DE OBRA','MAQUINARIA','RIEGO','OTROS','TOTAL','AH']

    external_stylesheets = [dbc.themes.BOOTSTRAP]#
    #df_costos_agricolas=DataAgricola.costos_campaña(ip)
    
    try:
        df_produc_costos=df_costos_agricolas.groupby(['AÑO_CAMPAÑA','CULTIVO','VARIEDAD','TIPO','FECHAINICIO_CAMPAÑA','FECHAFIN_CAMPAÑA'])[['SALDO_MOF']].sum().reset_index()
    except:
        df_produc_costos = pd.DataFrame(columns=['AÑO_CAMPAÑA','CULTIVO','VARIEDAD','TIPO','FECHAINICIO_CAMPAÑA','FECHAFIN_CAMPAÑA'],index=range(3))
        df_produc_costos=df_produc_costos.fillna(0)      
    app = DjangoDash(
        'vcostos',
        external_stylesheets=external_stylesheets,
    )

    #app.scripts.append_script({"external_url": "/static/assets/resizing_script.js"})

    app.layout = html.Div([
        dbc.Row([
            #dbc.Col([
            #    dmc.Text(id='if',weight=500),

            #],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([
                dmc.Title(id='title', order=3, style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                dmc.Title(id='subtitle', order=4, style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                
                #html.H3(id='title'),
                #html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
        ]),
        dbc.Row([
            
            dbc.Col([btnFilter()],width=1,className="col-xl-1 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([select(ids="drop_anio",texto="Campaña",value=sorted(df_produc_costos['AÑO_CAMPAÑA'].unique())[-1])],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([multiSelect(ids="drop_cultivo",texto="Cultivos")],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([select(ids="drop_variedad",texto="Variedad")],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),
            
            offcanvas(componentes=[
                    radioGroup(ids="radio-costos",
                               texto="Tipo de Costo",
                               children=[dmc.Radio(label='Totales', value='CT'),dmc.Radio(label='Por Hectárea', value='CH')],
                               value="CT",
                    ),
                    radioGroup(ids="rbtn_dinero",
                               texto="Moneda",
                               children=[dmc.Radio(label='Soles', value='SALDO_MOF'),dmc.Radio(label='Dolares', value='SALDO_MEX')],
                               value="SALDO_MEX",
                    ),
                    dbc.Checklist(
                                    id="check-recursos",
                                    inline=False,
                                    input_checked_style={
                                        "backgroundColor": "rgb(34, 139, 230)",
                                        "borderColor": "rgb(34, 139, 230)",
                                    },     
                                    label_style={'font-size': '12px'} )

            ]),
        ]), 
        dbc.Row([
            
            dbc.Col([
                #dbc.Card(dcc.Graph(id='costos-bar-consumidor'),className="shadow-sm")
            
                dmc.Tabs(
                        [
                            dmc.TabsList(
                                [
                                    dmc.Tab("CULTIVOS", value="1"),
                                    dmc.Tab("VARIEDADES", value="2"),
                                    dmc.Tab("LOTES", value="3"),
                                ]
                            ),
                        dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(id='costos-bar-consumidor'),className="shadow-sm")), value="3"),
                            dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(id='costos-bar-variedad'),className="shadow-sm")), value="2"),
                            dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(id='costos-bar-cultivo'),className="shadow-sm")), value="1"),
                            #dmc.TabsPanel(create_graph(), value="2"),
                            #dmc.TabsPanel(create_graph(), value="3"),
                        ],
                        value="1",
                    )
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            #dbc.Col([
            #    html.H5("Tabla Detalle Recursos por Cultivo (%)", className="text-dark p-2"),
            #    html.Div(id='table-percent'),
            #],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([
                accordion(children=[
                loadingOverlay(
                    dash_table.DataTable(
                        id='table-cultivo',
                        #columns=[{"name": c, "id": c,
                        #        "type": "numeric", "format": Format(group=",", precision=0,scheme="f")} for c in d.dff_cols_cultivo],
                        active_cell={"row": 0, "column": 0, "column_id": 0, "row_id": 0},
                        sort_action="native",
                        #page_size= 10,
                        style_table={
                                  'minHeight': '100px',
                                  'maxHeight': '310px',
                                 'overflowY': 'auto'},
                        style_cell={'padding': '12px',
                                 'font-family': 'sans-serif',
                                  'font-size': '14px',
                                  'text_align': 'left',
                                },
                        style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'text_align': 'left',
                        'font-size': '14px',
                    },
                        fixed_rows={'headers': True},
                        style_as_list_view=True,
                        style_data_conditional=[
                                            {
                                                "if": {"row_index": "even"},
                                                "backgroundColor": "#f5f6f7",
                                            },
                                            {
                                                "if": {"row_index": "odd"},
                                                "backgroundColor": "#ffffff",
                                            },
                                            {
                                                'if': {
                                                    'filter_query': '{CULTIVO} = "TOTAL"',
                                                },
                                                'backgroundColor': '#0074D9',
                                                'color': 'white'
                                            },
                                        ],
                                        

                    )),
                ],texto='Costos Cultivo',value='cultivo'),
                
                    
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
        
        ]),  
        dbc.Row([
            dbc.Col([
                accordion(children=[
                  loadingOverlay(html.Div(id='table-lote'),html.Div(id='cultivo_cell')),
                  dmc.Text(id='if',weight=500),
                ],texto='Detalle de Costos por Lote',value='lote'),
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
        ]), 
        #dbc.Row([
        #    dbc.Col([
        #        dbc.Card(dcc.Graph(id='area-cultivo'),className="shadow-sm")
        #    ],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
        #    dbc.Col([
        #        dbc.Card(dcc.Graph(id='area-campania'),className="shadow-sm")
        #    ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
            
        #]),    
                
    ])
    offcanvasAction(app)



   


    @app.callback(Output('drop_anio','data'),
                Output('drop_cultivo', 'data'),
                Output('drop_variedad', 'data'),
                Output('check-recursos', 'options'),
                Output('check-recursos', 'value'),
                Output('if', 'children'),
                
                  
                  #Output('drop_variedad', 'options'),
              [Input('drop_anio','value'),
               Input('drop_cultivo','value'), 
               Input('drop_variedad','value'),
               #Input('cultivo_cell','value'),
              ])
    def update_drop_cultivo(year,cultivo,variedad):#,cultivo_cell
        
        #df=DataAgricola.data_general(ip)
        #if cultivo_cell == None and (cultivo==None or len(cultivo)==0):
        #    df_produccion=df_produc_costos.copy()
        #elif cultivo_cell == None and (cultivo!=None or len(cultivo)>0):
        #    df_produccion=df_produc_costos[df_produc_costos['CULTIVO'].isin(cultivo)]
        
        #elif cultivo_cell != None and cultivo_cell !='TOTAL':
        #    df_produccion=df_produc_costos[df_produc_costos['CULTIVO']==cultivo_cell]
        df_produccion=df_produc_costos.copy()
        if year==None and (cultivo==None or len(cultivo)==0) and variedad==None:
            options=df_produccion
        elif year!=None and (cultivo==None or len(cultivo)==0)and variedad==None:
            options=df_produccion[df_produccion['AÑO_CAMPAÑA']==year]
        elif year==None and (cultivo!=None or len(cultivo)>0)and variedad==None:
            options=df_produccion[df_produccion['CULTIVO'].isin(cultivo)]

        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad==None:# or len(cultivo)>0
            options=df_produccion[(df_produccion['CULTIVO'].isin(cultivo))&(df_produccion['AÑO_CAMPAÑA']==year)]

        elif year==None and (cultivo==None or len(cultivo)==0) and variedad!=None:
            options=df_produccion[df_produccion['VARIEDAD']==variedad]
        elif year!=None and (cultivo==None or len(cultivo)==0) and variedad!=None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['AÑO_CAMPAÑA']==year)]
        elif year==None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['CULTIVO'].isin(cultivo))]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['AÑO_CAMPAÑA']==year)&(df_produccion['CULTIVO'].isin(cultivo))]

        anio=[{'label': i, 'value': i} for i in options['AÑO_CAMPAÑA'].unique()]
        cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()]
        variedad=[{'label': i, 'value': i} for i in options['VARIEDAD'].unique()]
        check=[{'label': i, 'value': i} for i in options['TIPO'].unique()]
        minimo=str(options['FECHAINICIO_CAMPAÑA'].min())#
        print(minimo)
        maximo=str(options['FECHAFIN_CAMPAÑA'].max())#.str[0:10]
        print(maximo)
        inicio_fin=str(minimo)+' - '+str(maximo)
        print(inicio_fin)
        return anio,cultivo,variedad,check,options['TIPO'].unique(),inicio_fin

    @app.callback(
    Output("title","children"),
    Output("subtitle","children"),
    Input("drop_anio","value"),
    #Input('cultivo_cell','value'),
    Input('rbtn_dinero','value'),
    Input('radio-costos','value')
    )
    def update_title(anio,radio,radio_costos):#,cultivo
        if radio_costos == 'CT':
            
            text="COSTOS POR CULTIVO EN"
            
            #"Costos por Cultivo en"
            if radio == 'SALDO_MOF':
                dinero="SOLES"
                if anio == None:
                    title=text+' '+dinero
                    title2=''
                    
                else:
                    title=text+' '+dinero
                    title2='Campaña '+str(anio)
                return title,title2
            elif radio == 'SALDO_MEX':
                dinero="DOLARES"
                if anio == None:
                    title=text+' '+dinero
                    title2=''
                else:
                    title=text+' '+dinero
                    title2='Campaña '+str(anio)
                return title,title2
        elif radio_costos == 'CH':
            text="COSTOS POR HECTÁREA EN"
            if radio == 'SALDO_MOF':
                dinero="SOLES"
                if anio == None:
                    
                    title=text+' '+dinero
                    title2=''
                else:
                    title=text+' '+dinero
                    title2='Campaña '+str(anio)
                return title,title2
            elif radio == 'SALDO_MEX':
                dinero="DOLARES"
                if anio == None:
                    title=text+' '+dinero
                    title2=''
                else:
                    title=text+' '+dinero
                    title2='Campaña '+str(anio)
                return title    ,title2
    @app.callback(
        Output('table-cultivo', 'data'),#children
        #Output('cultivo_cell', 'value'),
        Output('table-cultivo', 'columns'),
        Input('drop_anio','value'),
         Input('drop_cultivo','value'),
         Input('drop_variedad','value'),
         Input('rbtn_dinero','value'),
         #Input('check-recursos','value'),
         Input('radio-costos','value'),#rbtn_dinero
         #Input('table-cultivo', 'active_cell'),
         Input('check-recursos','value'),
    )   
    def actualizar_table_cultivo(year,cultivo,variedad,radio,radio_costos,check):#,active_cell,check#,active_cell
        df_campaña_ccc=df_costos_agricolas[df_costos_agricolas['TIPO'].isin(check)]
        #df_campaña_ccc=df_campaña_ccc[df_campaña_ccc['TIPO'].isin(check)]
       
        #dff=func.filter_dataframe_cultivo(d.table_cultivo,anio,cultivo)
        dff_end_pivot= df_campaña_ccc.pivot(index=('CODCULTIVO','CULTIVO','VARIEDAD','AREA_CAMPAÑA','IDCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA'),values=(radio),columns=('TIPO'))
        dff_end_pivot.reset_index()
        dff_pivot=pd.DataFrame(dff_end_pivot.to_records())
        
        if year==None and (cultivo==None or len(cultivo)==0) and variedad==None:
            dff=dff_pivot
        elif year!=None and (cultivo==None or len(cultivo)==0)and variedad==None:
                dff=dff_pivot[dff_pivot['AÑO_CAMPAÑA']==year]
        elif year==None and (cultivo!=None or len(cultivo)>0)and variedad==None:
                dff=dff_pivot[dff_pivot['CULTIVO'].isin(cultivo)]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad==None:# or len(cultivo)>0
                dff=dff_pivot[(dff_pivot['CULTIVO'].isin(cultivo))&(dff_pivot['AÑO_CAMPAÑA']==year)]

        elif year==None and (cultivo==None or len(cultivo)==0) and variedad!=None:
                dff=dff_pivot[dff_pivot['VARIEDAD']==variedad]
        elif year!=None and (cultivo==None or len(cultivo)==0) and variedad!=None:
                dff=dff_pivot[(dff_pivot['VARIEDAD']==variedad)&(dff_pivot['AÑO_CAMPAÑA']==year)]
        elif year==None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
                dff=dff_pivot[(dff_pivot['VARIEDAD']==variedad)&(dff_pivot['CULTIVO'].isin(cultivo))]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
                dff=dff_pivot[(dff_pivot['VARIEDAD']==variedad)&(dff_pivot['AÑO_CAMPAÑA']==year)&(dff_pivot['CULTIVO'].isin(cultivo))]


        dff_cultivo=dff.groupby(['CODCULTIVO','CULTIVO']).sum().reset_index()
        if radio_costos == 'CH':
            columns=dff_cultivo.columns
            for recurso in columns[4:]:
                dff_cultivo[recurso]=dff_cultivo[recurso]/dff_cultivo['AREA_CAMPAÑA']

        dff_cultivo=dff_cultivo.drop(['CODCULTIVO','AÑO_CAMPAÑA'], axis=1)
        dff_cultivo['AREA_CAMPAÑA']=dff_cultivo['AREA_CAMPAÑA'].astype('object')

        dff_cultivo.loc[:,'TOTAL']= dff_cultivo.sum(numeric_only=True, axis=1)
        dff_cultivo['AREA_CAMPAÑA']=dff_cultivo['AREA_CAMPAÑA'].astype('float64')
        dff_cultivo=dff_cultivo.sort_values('TOTAL',ascending=False)#
        dff_cultivo.loc['TOTAL',:]= dff_cultivo.sum(numeric_only=True, axis=0)
        dff_cultivo=dff_cultivo.fillna('TOTAL')
        try:        
            dff_cultivo=dff_cultivo.drop(['CODSIEMBRA','CODCAMPAÑA'], axis=1)
        except:
            pass
        #if active_cell is None:
        #        return no_update
        #row = active_cell["row"]
        #cultivo = dff_cultivo.iloc[row,0] 
        #print(cultivo)
                
        col=[{"name": c, "id": c,"type": "numeric", "format": Format(group=",", precision=0,scheme="f")} for c in dff_cultivo]
        return dff_cultivo.to_dict('rows'),col#,cultivo
        
    @app.callback(
        Output('table-lote', 'children'),
        #Output('table-lote', 'columns'),
         Input('drop_anio','value'),
         Input('drop_cultivo','value'),
         Input('drop_variedad','value'),
         Input('rbtn_dinero','value'),
         Input('check-recursos','value'),
         Input('radio-costos','value'),
         #Input('cultivo_cell','value'),
    )   
    def actualizar_table_lote(year,cultivo,variedad,radio,check,radio_costos):#,cultivo_cell
        
        df_campaña_ccc=df_costos_agricolas[df_costos_agricolas['TIPO'].isin(check)]
        #if cultivo !='TOTAL':
        #    df_campaña_ccc=df_campaña_ccc[df_campaña_ccc['CULTIVO']==cultivo]


        #if cultivo_cell == None and (cultivo==None or len(cultivo)==0):
        #    df_campaña=df_campaña_ccc.copy()
        #elif cultivo_cell == None and (cultivo!=None or len(cultivo)>0):
        #    df_campaña=df_campaña_ccc[df_campaña_ccc['CULTIVO'].isin(cultivo)]
        
        #elif cultivo_cell != None and cultivo_cell !='TOTAL':
        #    df_campaña=df_campaña_ccc[df_campaña_ccc['CULTIVO']==cultivo_cell]

        dff_end_pivot= df_campaña_ccc.pivot(index=('CODCULTIVO','CULTIVO','VARIEDAD','AREA_CAMPAÑA','IDCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA'),values=(radio),columns=('TIPO'))
        dff_pivot=pd.DataFrame(dff_end_pivot.to_records())
        if year==None and (cultivo==None or len(cultivo)==0) and variedad==None:
            dff=dff_pivot
        elif year!=None and (cultivo==None or len(cultivo)==0)and variedad==None:
                dff=dff_pivot[dff_pivot['AÑO_CAMPAÑA']==year]
        elif year==None and (cultivo!=None or len(cultivo)>0)and variedad==None:
                dff=dff_pivot[dff_pivot['CULTIVO'].isin(cultivo)]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad==None:# or len(cultivo)>0
                dff=dff_pivot[(dff_pivot['CULTIVO'].isin(cultivo))&(dff_pivot['AÑO_CAMPAÑA']==year)]

        elif year==None and (cultivo==None or len(cultivo)==0) and variedad!=None:
                dff=dff_pivot[dff_pivot['VARIEDAD']==variedad]
        elif year!=None and (cultivo==None or len(cultivo)==0) and variedad!=None:
                dff=dff_pivot[(dff_pivot['VARIEDAD']==variedad)&(dff_pivot['AÑO_CAMPAÑA']==year)]
        elif year==None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
                dff=dff_pivot[(dff_pivot['VARIEDAD']==variedad)&(dff_pivot['CULTIVO'].isin(cultivo))]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
                dff=dff_pivot[(dff_pivot['VARIEDAD']==variedad)&(dff_pivot['AÑO_CAMPAÑA']==year)&(dff_pivot['CULTIVO'].isin(cultivo))]



        dff_lote=dff.groupby(['IDCONSUMIDOR','CONSUMIDOR']).sum().reset_index()
        if radio_costos == 'CH':
            for cultivo in check:
                dff_lote[cultivo]=dff_lote[cultivo]/dff_lote['AREA_CAMPAÑA']
        dff_lote=dff_lote.drop(['IDCONSUMIDOR','AÑO_CAMPAÑA'], axis=1)
        dff_lote['AREA_CAMPAÑA']=dff_lote['AREA_CAMPAÑA'].astype('object')

        dff_lote.loc[:,'TOTAL']= dff_lote.sum(numeric_only=True, axis=1)
        dff_lote['AREA_CAMPAÑA']=dff_lote['AREA_CAMPAÑA'].astype('float64')

        dff_lote=dff_lote.sort_values('TOTAL',ascending=False)
        try:        
            dff_lote=dff_lote.drop(['CODSIEMBRA','CODCAMPAÑA'], axis=1)
        except:
            pass

        return Table_LOTE_COSTOS(dff_lote)    
        
    @app.callback(
        Output('costos-bar-consumidor', 'figure'),
        Output('costos-bar-variedad', 'figure'),
        Output('costos-bar-cultivo', 'figure'),
        [Input('drop_anio','value'),
         #Input('drop_cultivo','value'),
         Input('drop_cultivo','value'),
         Input('drop_variedad','value'),
         Input('rbtn_dinero','value'),
         Input('check-recursos','value'),
         Input('radio-costos','value'),
         #Input('cultivo_cell','value')
         ]#rbtn_dinero
    )   
    def costos_bar_consumidor(year,cultivo,variedad,radio,check,radio_costos):#,cultivo_cell
        if radio == 'SALDO_MOF':
            simbolo='S/'
        elif radio == 'SALDO_MEX':
            simbolo='$'
        df_campaña_ccc=df_costos_agricolas[df_costos_agricolas['TIPO'].isin(check)]
        #if cultivo_cell == None and (cultivo==None or len(cultivo)==0):
        #    df_campaña=df_campaña_ccc.copy()
        #elif cultivo_cell == None and (cultivo!=None or len(cultivo)>0):
        #    df_campaña=df_campaña_ccc[df_campaña_ccc['CULTIVO'].isin(cultivo)]
        
        #elif cultivo_cell != None and cultivo_cell !='TOTAL':
         #   df_campaña=df_campaña_ccc[df_campaña_ccc['CULTIVO']==cultivo_cell]

        
        dff_pivot= df_campaña_ccc.pivot(index=('CODCULTIVO','VARIEDAD','CULTIVO','AREA_CAMPAÑA','IDCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA'),values=(radio),columns=('TIPO'))
        dff_pivot=pd.DataFrame(dff_pivot.to_records())
        #df_ha=dff_pivot.groupby(['CONSUMIDOR','AREA_CAMPAÑA']).sum().reset_index()
        #dff_pivot['AREA_CAMPAÑA']=df_ha['AREA_CAMPAÑA']
        if year==None and (cultivo==None or len(cultivo)==0) and variedad==None:
            dff=dff_pivot
        elif year!=None and (cultivo==None or len(cultivo)==0)and variedad==None:
                dff=dff_pivot[dff_pivot['AÑO_CAMPAÑA']==year]
        elif year==None and (cultivo!=None or len(cultivo)>0)and variedad==None:
                dff=dff_pivot[dff_pivot['CULTIVO'].isin(cultivo)]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad==None:# or len(cultivo)>0
                dff=dff_pivot[(dff_pivot['CULTIVO'].isin(cultivo))&(dff_pivot['AÑO_CAMPAÑA']==year)]

        elif year==None and (cultivo==None or len(cultivo)==0) and variedad!=None:
                dff=dff_pivot[dff_pivot['VARIEDAD']==variedad]
        elif year!=None and (cultivo==None or len(cultivo)==0) and variedad!=None:
                dff=dff_pivot[(dff_pivot['VARIEDAD']==variedad)&(dff_pivot['AÑO_CAMPAÑA']==year)]
        elif year==None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
                dff=dff_pivot[(dff_pivot['VARIEDAD']==variedad)&(dff_pivot['CULTIVO'].isin(cultivo))]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
                dff=dff_pivot[(dff_pivot['VARIEDAD']==variedad)&(dff_pivot['AÑO_CAMPAÑA']==year)&(dff_pivot['CULTIVO'].isin(cultivo))]
        #['NCONSUMIDOR','CULTIVO']
        def tabs_cvl(dff,cols,radio_costos,ejey,tickedx):
            dff_lote=dff.groupby(cols).sum().reset_index()
            dff_lote['AREA_CAMPAÑA']=dff_lote['AREA_CAMPAÑA'].astype('object')
            dff_lote.loc[:,'TOTAL']= dff_lote.sum(numeric_only=True, axis=1)
            dff_lote['AREA_CAMPAÑA']=dff_lote['AREA_CAMPAÑA'].astype('float64')

            if ejey =='Lote':
                  df_ha=dff.groupby(['CONSUMIDOR','AREA_CAMPAÑA']).sum().reset_index()
            elif ejey =='Variedad':
                  df_ha=dff.groupby(['VARIEDAD','CONSUMIDOR','AREA_CAMPAÑA']).sum().reset_index()
            elif ejey =='Cultivo':
                  df_ha=dff.groupby(['CULTIVO','CONSUMIDOR','AREA_CAMPAÑA']).sum().reset_index()
            
            if radio_costos == 'CT':
                
                dff_lote=dff_lote.sort_values('TOTAL',ascending=False)
                #x=dff_lote['NCONSUMIDOR']
                x=dff_lote[cols[0]]
                y=dff_lote['TOTAL']
                color=dff_lote['CULTIVO']
                print(color)
                print(type)
                owo=dff_lote['TOTAL'].max()
                if owo>999999:
                    dff_lote['TOTAL_y']=dff_lote['TOTAL']/1000000   
                    promedio=(dff_lote['TOTAL_y'].sum())/len(dff_lote[cols[0]].unique()) 
                    title=f'Costos {simbolo}. / {ejey} (Millón)'
                elif owo<999999:
                    dff_lote['TOTAL_y']=dff_lote['TOTAL']/1000
                    promedio=(dff_lote['TOTAL_y'].sum())/len(dff_lote[cols[0]].unique())    
                    title=f'Costos {simbolo}. / {ejey} (Mil)'
                elif owo <1000:
                    dff_lote['TOTAL_y']=dff_lote['TOTAL']/1
                    promedio=(dff_lote['TOTAL_y'].sum())/len(dff_lote[cols[0]].unique())      
                    title=f'Costos {simbolo} / {ejey}'
                dff_lote['PROMEDIO']=promedio
                ejetotal='TOTAL_y'
           
            #return BarGOV_SX(dff_lote['TOTAL_y'],x,title,color,None,'Lotes',simbolo,dff_lote['PROMEDIO'],dff_lote['AREA_CAMPAÑA'])

            elif radio_costos == 'CH':

                #dff_lote['AH']=dff_lote['TOTAL']/dff_lote['AREA_CAMPAÑA']
                dff_lote['AH']=dff_lote['TOTAL']/df_ha['AREA_CAMPAÑA']
                dff_lote=dff_lote.sort_values('AH',ascending=False)
                x=dff_lote[cols[0]]
                y=dff_lote['AH']
                color=dff_lote['CULTIVO']
                print(color)
                print(type)
                owo=dff_lote['AH'].max()
                if owo>999999:
                    dff_lote['AH_y']=dff_lote['AH']/1000000 
                    promedio=(dff_lote['AH_y'].sum())/len(dff_lote[cols[0]].unique())   
                    title=f'Costos {simbolo} / Ha x {ejey} (Millón)'
                elif owo<999999:
                    dff_lote['AH_y']=dff_lote['AH']/1000
                    promedio=(dff_lote['AH_y'].sum())/len(dff_lote[cols[0]].unique())  
                    title=f'Costos {simbolo} / Ha x {ejey} (Mil)'
                elif owo <1000:
                    dff_lote['AH_y']=dff_lote['AH']/1
                    promedio=(dff_lote['AH_y'].sum())/len(dff_lote[cols[0]].unique())  
                    title=f'Costos {simbolo} / Ha x {ejey}'
                dff_lote['PROMEDIO']=promedio
                ejetotal='AH_y'
            print(cols[0])
            return BarGOV_SX(dff_lote[ejetotal],x,title,color,None,ejey,simbolo, dff_lote['PROMEDIO'],dff_lote['AREA_CAMPAÑA'],False,tickedx)       
                #scatter=dff_lote_mof['AH']
                #return dff_lote_mof.to_dict("records")
        lotes=tabs_cvl(dff,['CONSUMIDOR','CULTIVO'],radio_costos,'Lote',True)
        variedad=tabs_cvl(dff,['VARIEDAD','CULTIVO'],radio_costos,'Variedad',True)
        cultivo=tabs_cvl(dff,['CULTIVO'],radio_costos,'Cultivo',False)
        return lotes,variedad,cultivo
        
    @app.callback(
        Output('table-percent', 'children'),
        #Output('pie-costos','figure'),
        [Input('drop_anio','value'),
         #Input('drop_cultivo','value'),
          Input('drop_cultivo','value'),
         Input('drop_variedad','value'),
         Input('rbtn_dinero','value'),
         Input('check-recursos','value'),
         Input('radio-costos','value'),
         Input('cultivo_cell','value'),]#rbtn_dinero
    )   
    def actualizar_table_CostosPorcentajes(year,cultivo,variedad,radio,check,radio_costos,cultivo_cell):
        if radio == 'SALDO_MOF':
            simbolo='S/'
        elif radio == 'SALDO_MEX':
            simbolo='$'
        
        df_campaña_ccc=df_costos_agricolas[df_costos_agricolas['TIPO'].isin(check)]

        if cultivo_cell == None and (cultivo==None or len(cultivo)==0):
            df_campaña=df_campaña_ccc
        elif cultivo_cell == None and (cultivo!=None or len(cultivo)>0):
            df_campaña=df_campaña_ccc[df_campaña_ccc['CULTIVO'].isin(cultivo)]
        
        elif cultivo_cell != None and cultivo_cell !='TOTAL':
            df_campaña=df_campaña_ccc[df_campaña_ccc['CULTIVO']==cultivo_cell]

        if year==None and (cultivo==None or len(cultivo)==0) and variedad==None:
            dff=df_campaña
        elif year!=None and (cultivo==None or len(cultivo)==0)and variedad==None:
                dff=df_campaña[df_campaña['AÑO_CAMPAÑA']==year]
        elif year==None and (cultivo!=None or len(cultivo)>0)and variedad==None:
                dff=df_campaña[df_campaña['CULTIVO'].isin(cultivo)]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad==None:# or len(cultivo)>0
                dff=df_campaña[(df_campaña['CULTIVO'].isin(cultivo))&(df_campaña['AÑO_CAMPAÑA']==year)]

        elif year==None and (cultivo==None or len(cultivo)==0) and variedad!=None:
                dff=df_campaña[df_campaña['VARIEDAD']==variedad]
        elif year!=None and (cultivo==None or len(cultivo)==0) and variedad!=None:
                dff=df_campaña[(df_campaña['VARIEDAD']==variedad)&(df_campaña['AÑO_CAMPAÑA']==year)]
        elif year==None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
                dff=df_campaña[(df_campaña['VARIEDAD']==variedad)&(df_campaña['CULTIVO'].isin(cultivo))]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
                dff=df_campaña[(df_campaña['VARIEDAD']==variedad)&(df_campaña['AÑO_CAMPAÑA']==year)&(df_campaña['CULTIVO'].isin(cultivo))]
            
        if radio_costos == 'CT':
            df_costos=dff.groupby(['TIPO'])[[radio]].sum().reset_index()
            df_tipo_costos=df_costos
            df_tipo_costos['%']=(df_tipo_costos[radio]/df_tipo_costos[radio].sum())*100
            df_tipo_costos.loc['TOTAL',:]= df_tipo_costos.sum(numeric_only=True, axis=0)
            df_tipo_costos=df_tipo_costos.fillna('TOTAL')
            df_tipo_costos.rename(columns={'TIPO':'RECURSO',radio :'COSTOS ({simbolo})'},inplace=True)

            return TableDtScrolling_no_format(df_tipo_costos)
        elif radio_costos == 'CH':
            dff_end_pivot= dff.pivot(index=('CODCULTIVO','CULTIVO','AREA_CAMPAÑA','IDCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA'),values=(radio),columns=('TIPO'))
            dff_pivot=pd.DataFrame(dff_end_pivot.to_records())
            df_tipo_costos=dff.groupby(['TIPO'])[[radio]].sum().reset_index()
            df_tipo_costos['COSTOS POR HAS']=(df_tipo_costos[radio]/dff_pivot['AREA_CAMPAÑA'].sum())
            df_tipo_costos['%']=(df_tipo_costos[radio]/df_tipo_costos[radio].sum())*100
            df_tipo_costos.loc['TOTAL',:]= df_tipo_costos.sum(numeric_only=True, axis=0)
            df_tipo_costos=df_tipo_costos.fillna('TOTAL')
            df_tipo_costos.rename(columns={'TIPO':'RECURSO',radio :'COSTOS ({simbolo})'},inplace=True)

            return TableDtScrolling_no_format(df_tipo_costos) 
                


    

"""

    @app.callback(
    Output("title","children"),
    Output("subtitle","children"),
    Input("drop_anio","value"),
    Input('cultivo_cell','value'),
    Input('rbtn_dinero','value'),
    Input('radio-costos','value')
    )
    def update_title(anio,cultivo,radio,radio_costos):
        if radio_costos == 'CT':
            
            text="COSTOS POR CULTIVO EN"
            
            #"Costos por Cultivo en"
            if radio == 'sol':
                dinero="SOLES"
                if anio == None:
                    title=text+' '+dinero
                    title2=''
                    
                else:
                    title=text+' '+dinero
                    title2='Campaña '+str(anio)
                return title,title2
            elif radio == 'dolar':
                dinero="DOLARES"
                if anio == None:
                    title=text+' '+dinero
                    title2=''
                else:
                    title=text+' '+dinero
                    title2='Campaña '+str(anio)
                return title,title2
        elif radio_costos == 'CH':
            text="COSTOS POR HECTÁREA EN"
            if radio == 'sol':
                dinero="SOLES"
                if anio == None:
                    
                    title=text+' '+dinero
                    title2=''
                else:
                    title=text+' '+dinero
                    title2='Campaña '+str(anio)
                return title,title2
            elif radio == 'dolar':
                dinero="DOLARES"
                if anio == None:
                    title=text+' '+dinero
                    title2=''
                else:
                    title=text+' '+dinero
                    title2='Campaña '+str(anio)
                return title,title2


    @app.callback(Output('drop_anio','options'),
                Output('drop_cultivo', 'options'),
                  
                  #Output('drop_variedad', 'options'),
              [Input('drop_anio','value')])
    def update_drop_cultivo(anio):
        df_costos_campania=d.dff_end_pivot
        options_anio=[{'label': i, 'value': i} for i in df_costos_campania['AÑO_CAMPAÑA'].unique()]
        df_filtro= df_costos_campania[df_costos_campania['AÑO_CAMPAÑA']==anio]
        options_cultivo=[{'label': i, 'value': i} for i in df_filtro['CULTIVO'].unique()]
        return options_anio,options_cultivo
"""
template_theme1 = "pulse"
template_theme2 = "vapor"
url_theme1 = dbc.themes.PULSE
url_theme2 = dbc.themes.VAPOR
#df_ventas=DataframeVentasEjes()
color_variado=px.colors.qualitative.Dark2+px.colors.qualitative.Prism
#df_agricola=df_general
def card_agricola1(valor,prefijo,title):
    card = go.Figure(
            go.Indicator(
            mode = "number+delta",
            #mode = "number",
            #number_font_color="black",
            number_font_size=20,
            value =valor,#d.total_if,
            #delta = {"reference": 0, "valueformat": ".0f"},
            title = {"text": title,"font": {'size': 12}},#"font": {'size': 15,'family': "Arial"}
            number = {'prefix':prefijo },
            #position="top",
            #domain = {'y': [0, 1], 'x': [0.25, 0.75]}
        ))
        

    card.update_layout(
            showlegend=False,
            #plot_bgcolor="white",
            margin=dict(t=35,l=0,b=0,r=0),
            height=80,
            template="none",
        )
    card.update_xaxes(visible=False, fixedrange=True)
    card.update_yaxes(visible=False, fixedrange=True)
    return card

def graph_lines_agricola2(df,titulo,name_ejex,name_ejey):
    fig = go.Figure()
    x=[df['AÑO_CAMPAÑA'],df['SEMANA']]
    for variable in df.columns[3:]:
        fig.add_trace(go.Scatter(x=x, y=df[variable],
                            mode='lines',
                            name=variable))
        
    fig.update_layout(template='none',title=titulo,xaxis_title=name_ejex,yaxis_title=name_ejey)
    fig.update_layout(autosize=True,height=280,margin=dict(l=60,r=30,b=80,t=40))
    
    
    return fig
def graph_bar_agricola2(df,titulo,name_ejex,name_ejey):
    fig = px.bar(df, x="AÑO_FECHA", y="CANTIDAD",
             color='DSCVARIABLE', barmode='group',color_discrete_map=dict_recursos_agricola)
        
    fig.update_layout(template='none',title=titulo,xaxis_title=name_ejex,yaxis_title=name_ejey)
    fig.update_layout(autosize=True,height=280,margin=dict(l=60,r=30,b=30,t=80),legend_title_text='')
    fig.update_layout(
        legend=dict(x=1, y=1.02,orientation="h",
                    yanchor="bottom",
                    xanchor="right"),)
    
    return fig

def variablesAgricolas(empresa):
    """"""
    df_consumidores = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
    df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
    df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
    df_var_agricolas_default=cleanVariablesAgricolas(df_consumidores,
                                                  df_variedad,
                                                  df_cultivos,
                                                  df_fertilizacion)
    df_var_agricolas_pivot_default=variablesAgricolasPivot(df_var_agricolas_default)
    df_costos_agricola_default=costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad)
    """"""
    #data=dataAgricolaEmpresa(empresa)
    """
    df_agricola=data[0]
    """
    df_agricola=df_var_agricolas_default.copy()
    
    df_agricola_1=df_agricola.groupby(['AÑO_FECHA','CULTIVO','VARIEDAD','CONSUMIDOR'])[['CANTIDAD']].sum().reset_index()
    year_min=sorted(df_agricola_1['AÑO_FECHA'].unique())[0]
    year_max=sorted(df_agricola_1['AÑO_FECHA'].unique())[-1]
    value_1=sorted(df_agricola_1['AÑO_FECHA'].unique())[-2]
    value_2=sorted(df_agricola_1['AÑO_FECHA'].unique())[-1]
    year_list=sorted(df_agricola_1['AÑO_FECHA'].unique())
    lista_year=[str(x) for x in year_list]
    app = DjangoDash('variables_agricolas', external_stylesheets=[dbc.themes.BOOTSTRAP])#

    app.layout = html.Div([
            dbc.Row([
                    dbc.Col([
                            html.H3(id='title', style={'margin-bottom': '0px', 'color': 'black'}),#,'textAlign': 'center'
                            html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black'})
                        ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                        
                    dbc.Col([  
                        
                            dcc.RangeSlider(
                                        id="slider-year",
                                        min=year_min,
                                        max=year_max,
                                        value=[value_1,value_2 ],
                                        step=None,
                                        className="p-0",
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        marks=dict(zip(lista_year, lista_year))
                                        #mb=35,
                                    ),
                      

                    ],width=5,className="col-xl-5 col-md-5 col-sm-11 col-11 mb-3"), 
                    dbc.Col([btnFilter()],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
                    offcanvas(componentes=[
                        select(ids="cultivo",texto="Cultivo"),
                        select(ids="variedad",texto="Variedad"),
                        select(ids="consumidor",texto="Consumidor"),
                    ]),
                       
                        
                ]),
        dbc.Row([
            dbc.Row([#
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='card1'),className="shadow-sm"))],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),#dbc.Card(dcc.Graph(id='card1'),className="shadow-sm")
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='card2'),className="shadow-sm"))],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='card3'),className="shadow-sm"))],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='card4'),className="shadow-sm"))],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3"),
                
            ]),
            #dbc.Row([dbc.Col([dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")]),
            #dbc.Row([dbc.Col([dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")]),
            #dbc.Row([dbc.Col([dbc.Card(dcc.Graph(id='graph3'),className="shadow-sm")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")]),
            #dbc.Row([dbc.Col([dbc.Card(dcc.Graph(id='graph4'),className="shadow-sm")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")]),

            #dbc.Row([dbc.Col([dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")]),
         
         ]),
         dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
         ]),
         dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph3'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph4'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
         ]),

            
        ])
    offcanvasAction(app)

    @app.callback(
            Output("title","children"),
            Output("subtitle","children"),
            
            Input("cultivo","value"),
            Input("consumidor","value"),
            Input("slider-year","value"),
            
            )
    def title(cultivo,consumidor,slider):
        general='Recursos Agrícolas'
        
        if slider == None:
            title=general
        else:
            title=general+' del año '+str(slider[0])+' al '+str(slider[1])
        
        if cultivo == None and consumidor == None:
            subtitle=''
        elif cultivo != None and consumidor == None: 
            subtitle=cultivo
        elif cultivo == None and consumidor != None: 
            subtitle=consumidor
        elif cultivo != None and consumidor != None: 
            subtitle=cultivo+' '+consumidor
        
        return title, subtitle


    @app.callback(
            Output("cultivo","data"),
            Output("variedad","data"),
            Output("consumidor","data"),
            #Output("range-slider","marks"),
            
            Input("cultivo","value"),
            #Input("cultivo","value"),
            Input("variedad","value"),
            Input("consumidor","value"),
            Input("slider-year","value"),
            
            )
    def filtrar_agricola1(cultivo,variedad,consumidor,slider):
            

            if not slider:
                return no_update
            df_agricola_lastyears = df_agricola_1[df_agricola_1.AÑO_FECHA.between(slider[0], slider[1])]

            if cultivo==None and consumidor==None and variedad==None:
                    options=df_agricola_lastyears

            elif cultivo!=None  and consumidor==None and variedad==None:    
                    options=df_agricola_lastyears[df_agricola_lastyears['CULTIVO']==cultivo]
            elif cultivo==None  and consumidor!=None and variedad==None:    
                    options=df_agricola_lastyears[df_agricola_lastyears['CONSUMIDOR']==consumidor]
            
            elif cultivo==None  and consumidor==None and variedad!=None:    
                    options=df_agricola_lastyears[df_agricola_lastyears['VARIEDAD']==variedad]

            elif cultivo!=None  and consumidor!=None and variedad!=None:
                    options=df_agricola_lastyears[(df_agricola_lastyears['CULTIVO']==cultivo)&(df_agricola_lastyears['CONSUMIDOR']==consumidor)&(df_agricola_lastyears['VARIEDAD']==variedad)]

            elif cultivo!=None  and consumidor!=None and variedad==None:
                    options=df_agricola_lastyears[(df_agricola_lastyears['CULTIVO']==cultivo)&(df_agricola_lastyears['CONSUMIDOR']==consumidor)]

            elif cultivo!=None  and consumidor==None and variedad!=None:
                    options=df_agricola_lastyears[(df_agricola_lastyears['CULTIVO']==cultivo)&(df_agricola_lastyears['VARIEDAD']==variedad)]        

            elif cultivo==None  and consumidor!=None and variedad!=None:
                    options=df_agricola_lastyears[(df_agricola_lastyears['CONSUMIDOR']==consumidor)&(df_agricola_lastyears['VARIEDAD']==variedad)]  
                    
            
            

        

            option_cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()] 
            option_variedad=[{'label': i, 'value': i} for i in options['VARIEDAD'].unique()] 
            option_consumidor=[{'label': i, 'value': i} for i in options['CONSUMIDOR'].unique()] 
            #list_years=sorted(options['AÑO_FECHA'].unique())
            #lista_anios=[str(x) for x in list_years]
            #marks=dict(zip(lista_anios, lista_anios))
            
            
            return option_cultivo,option_variedad,option_consumidor#,marks

    @app.callback(
            Output("card1","figure"),
            Output("card2","figure"),
            Output("card3","figure"),
            Output("card4","figure"),
            Output("graph1","figure"),
            Output("graph2","figure"),
            Output("graph3","figure"),
            Output("graph4","figure"),
            
            Input("cultivo","value"),
            Input("variedad","value"),
            Input("consumidor","value"),
            Input("slider-year","value"),
            
            #Input(ThemeSwitchAIO.ids.switch("theme"), "value"),

            )
    def filtro(cultivo,variedad,consumidor,slider):

            if not slider:
                return no_update
            df_agricola_lastyears = df_agricola[df_agricola.AÑO_FECHA.between(slider[0], slider[1])]

            
            
            if cultivo==None and consumidor==None and variedad==None:
                    options=df_agricola_lastyears

            elif cultivo!=None  and consumidor==None and variedad==None:    
                    options=df_agricola_lastyears[df_agricola_lastyears['CULTIVO']==cultivo]
            elif cultivo==None  and consumidor!=None and variedad==None:    
                    options=df_agricola_lastyears[df_agricola_lastyears['CONSUMIDOR']==consumidor]
            
            elif cultivo==None  and consumidor==None and variedad!=None:    
                    options=df_agricola_lastyears[df_agricola_lastyears['VARIEDAD']==variedad]

            elif cultivo!=None  and consumidor!=None and variedad!=None:
                    options=df_agricola_lastyears[(df_agricola['CULTIVO']==cultivo)&(df_agricola_lastyears['CONSUMIDOR']==consumidor)&(df_agricola_lastyears['VARIEDAD']==variedad)]

            elif cultivo!=None  and consumidor!=None and variedad==None:
                    options=df_agricola_lastyears[(df_agricola['CULTIVO']==cultivo)&(df_agricola_lastyears['CONSUMIDOR']==consumidor)]

            elif cultivo!=None  and consumidor==None and variedad!=None:
                    options=df_agricola_lastyears[(df_agricola['CULTIVO']==cultivo)&(df_agricola_lastyears['VARIEDAD']==variedad)]        

            elif cultivo==None  and consumidor!=None and variedad!=None:
                    options=df_agricola_lastyears[(df_agricola['CONSUMIDOR']==consumidor)&(df_agricola_lastyears['VARIEDAD']==variedad)]  
                    
            #graph_bar_agricola2
            df_recursos=options.groupby(['AÑO_FECHA','TIPO','DSCVARIABLE',])[['CANTIDAD']].sum().reset_index()
            df_recursos['AÑO_FECHA']=df_recursos['AÑO_FECHA'].astype('string')
            df_recursos['AÑO_FECHA']=df_recursos['AÑO_FECHA']+'-'
            #options=options.sort_values(['AÑO_CAMPAÑA','SEMANA'],ascending=True)
            #df_variables_agricolas=options.groupby(['AÑO_CAMPAÑA','SEMANA','TIPO','DSCVARIABLE',])[['CANTIDAD']].sum().reset_index()

            df_riego=df_recursos[df_recursos['TIPO']=='Riego']
            df_maquinaria=df_recursos[df_recursos['TIPO']=='Maquinaria']
            df_manodeobra=df_recursos[df_recursos['TIPO']=='Mano de obra']
            df_insumos=df_recursos[df_recursos['TIPO']=='Insumos']  

            total_riego=df_riego['CANTIDAD'].sum()
            total_maquinaria=df_maquinaria['CANTIDAD'].sum()
            total_mano=df_manodeobra['CANTIDAD'].sum()
            total_insumos=df_insumos['CANTIDAD'].sum()

            card1=card_agricola1(total_riego,None,'Total de Riego en Metros Cúbicos')
            #card1=cardMantine('Total de Riego en Metros Cúbicos',total_riego,df_riego,'FECHA','CANTIDAD')
            card2=card_agricola1(total_maquinaria,None,'Total de Horas Máquina')
            card3=card_agricola1(total_mano,None,'Total de Jornales trabajados')
            card4=card_agricola1(total_insumos,None,'Total de Insumos en Kilogramos')
    #card_agricola1(total_riego,None,'Total de Riego en Metros Cúbicos')
            #SERIES DE TIEMPO CARDS


            

            ##GRAPH
            #----insumos
             #df_insumos_pivot=df_insumos.pivot_table(index=('AÑO_CAMPAÑA','SEMANA','TIPO'),values=('CANTIDAD'),columns=('DSCVARIABLE'))
             #df_insumos_pivot.reset_index()
             #df_insumos_pivot=pd.DataFrame(df_insumos_pivot.to_records())
             #df_insumos_pivot=df_insumos_pivot.sort_values(['AÑO_CAMPAÑA','SEMANA'],ascending=True)
            #----Mano de Obra
             #df_manodeobra_pivot=df_manodeobra.pivot_table(index=('AÑO_CAMPAÑA','SEMANA','TIPO'),values=('CANTIDAD'),columns=('DSCVARIABLE'))
             #df_manodeobra_pivot.reset_index()
             #df_manodeobra_pivot=pd.DataFrame(df_manodeobra_pivot.to_records())
             #df_manodeobra_pivot=df_manodeobra_pivot.sort_values(['AÑO_CAMPAÑA','SEMANA'],ascending=True)
            #----Maquinaria
             #df_maquinaria_pivot=df_maquinaria.pivot_table(index=('AÑO_CAMPAÑA','SEMANA','TIPO'),values=('CANTIDAD'),columns=('DSCVARIABLE'))
             #df_maquinaria_pivot.reset_index()
             #df_maquinaria_pivot=pd.DataFrame(df_maquinaria_pivot.to_records())
             #df_maquinaria_pivot=df_maquinaria_pivot.sort_values(['AÑO_CAMPAÑA','SEMANA'],ascending=True)
            #----Riego
             #df_riego_pivot=df_riego.pivot_table(index=('AÑO_CAMPAÑA','SEMANA','TIPO'),values=('CANTIDAD'),columns=('DSCVARIABLE'))
             #df_riego_pivot.reset_index()
             #df_riego_pivot=pd.DataFrame(df_riego_pivot.to_records())
             #df_riego_pivot=df_riego_pivot.sort_values(['AÑO_CAMPAÑA','SEMANA'],ascending=True)

            ##dibujar lines df,titulo,name_ejex,name_ejey
            graph1=graph_bar_agricola2(df_insumos,'Tipos Insumos(Kilogramos)','AÑO','Kilogramos')
            graph2=graph_bar_agricola2(df_manodeobra,'Jornales','AÑO','Jornales')
            graph3=graph_bar_agricola2(df_maquinaria,'Horas Máquina','AÑO','Horas Máquina')
            graph4=graph_bar_agricola2(df_riego,'Metros Cúbicos','AÑO','Metros Cúbicos')
            return card1,card2,card3,card4,graph1,graph2,graph3,graph4

def card_agricola1(valor,prefijo,title):
    card = go.Figure(
            go.Indicator(
            mode = "number+delta",
            #mode = "number",
            #number_font_color="black",
            number_font_size=25,
            value =valor,#d.total_if,
            #delta = {"reference": 0, "valueformat": ".0f"},
            title = {"text": title,"font": {'size': 12}},#"font": {'size': 15,'family': "Arial"}
            number = {'prefix':prefijo },
            #position="top",
            #domain = {'y': [0, 1], 'x': [0.25, 0.75]}
        ))
        

    card.update_layout(
            showlegend=False,
            #plot_bgcolor="white",
            margin=dict(t=35,l=0,b=0,r=0),
            height=80,
            template="none",
        )
    card.update_xaxes(visible=False, fixedrange=True)
    card.update_yaxes(visible=False, fixedrange=True)
    return card

def cardMantine(title,value,df,x,y):
    fig = px.area(
        df,
        x=x, y=y,
        template='simple_white',
        log_y=True
    )

    fig.update_yaxes(visible=False),
    fig.update_xaxes(visible=False),
    fig.update_traces(
        line={'color': 'rgba(31, 119, 180, 0.2)'},
        fillcolor='rgba(31, 119, 180, 0.2)'
    ),
    fig.update_layout(
        margin={'t': 0, 'l': 0, 'b': 0, 'r': 0}
    )
    return html.Div([dmc.Paper([
            dcc.Location(id='url', refresh=False),
                dmc.Group([
                    html.Div([
                        dmc.Title(title, order=5),
                        dmc.Title(value, order=3)
                    ], style={'position': 'relative', 'z-index': '999'}),
                    dcc.Graph(
                        figure=fig,
                        config={
                            'displayModeBar': False,
                            'staticPlot': True
                        },
                        responsive=True,
                        style={'height': 60, 'margin': '-1rem'})
                ], grow=True)
            ], shadow="xl", p="md", withBorder=True, style={'margin-bottom': "1rem"})
    ])

def graph_lines_agricola1(df,titulo):
    fig = go.Figure()
    x=[df['AÑO_CAMPAÑA'],df['SEMANA']]
    for variable in df.columns[3:]:
        fig.add_trace(go.Scatter(x=x, y=df[variable],
                            mode='lines',
                            name=variable))
        
    fig.update_layout(template='none',title=titulo)
    fig.update_layout(autosize=True,height=280,margin=dict(l=40,r=70,b=80,t=40))
    fig.update_layout(xaxis_title="",yaxis_title="Hectáreas",legend_title="")
    return fig

def hectareaSembrada(empresa):
    """"""
    df_consumidores = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
    df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
    df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
    df_var_agricolas_default=cleanVariablesAgricolas(df_consumidores,
                                                  df_variedad,
                                                  df_cultivos,
                                                  df_fertilizacion)
    df_var_agricolas_pivot_default=variablesAgricolasPivot(df_var_agricolas_default)
    df_costos_agricola_default=costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad)
    """"""
    """
    data=dataAgricolaEmpresa(empresa)
    df_agricola=data[0]
    """
    df_agricola=df_var_agricolas_default.copy()

    df_agricola_1=df_agricola.groupby(['AÑO_CAMPAÑA','CULTIVO','VARIEDAD','CONSUMIDOR'])[['CANTIDAD']].sum().reset_index()
    app = DjangoDash('hectarea_sembrada', external_stylesheets=[dbc.themes.BOOTSTRAP])#

    app.layout = html.Div([
            dbc.Row([
                        dbc.Col([
                            btnFilter(),
                            offcanvas(componentes=[
                                select(ids="year",texto="Año",value=sorted(df_agricola_1['AÑO_CAMPAÑA'].unique())[-1]),
                                select(ids="cultivo",texto="Cultivo"),
                                select(ids="variedad",texto="Variedad"),
                                select(ids="consumidor",texto="Consumidor"),
                                radioGroup(ids="rbtn_dinero",
                                           texto="Moneda",
                                           children=[dmc.Radio(label='Soles', value='Soles'),dmc.Radio(label='Dolares', value='Dolares')],
                                           value="Dolares",
                                ),

                             ]),
                            

                        ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([
                            html.H3(id='title', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                            html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})

                        ],width=10,className="col-xl-10 col-md-10 col-sm-12 col-12 mb-3")
                    ]),
            dbc.Row([
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm"))],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm"))],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3")

            ]),
            dbc.Row([
                dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph3'),className="shadow-sm"))],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
               

            ]),

            
        ])
    offcanvasAction(app)

    @app.callback(
                
                Output("title","children"),
                Output("subtitle","children"),
                Input("cultivo","value"),
                Input("consumidor","value"),
                Input("year","value"),
                
                
                )
    def filtrar_agricola2(cultivo,consumidor,year):
            general='Hectáreas Sembradas'
            
            if cultivo == None:
                title=general
            else:
                title=general+' en el año '+str(year)
            
            if cultivo == None and consumidor == None:
                subtitle=''
            elif cultivo != None and consumidor == None: 
                subtitle=cultivo
            elif cultivo == None and consumidor != None: 
                subtitle=consumidor
            elif cultivo != None and consumidor != None: 
                subtitle=cultivo+' - '+consumidor
            
            return title, subtitle

    @app.callback(
                Output("cultivo","data"),
                Output("variedad","data"),
                Output("consumidor","data"),
                Output("year","data"),
                #Output("year","value"),
                Input("cultivo","value"),
                Input("variedad","value"),
                Input("consumidor","value"),

                Input("year","value"),
                
                
                )
    def filtrar_agricola2(cultivo,variedad,consumidor,year):
                
                
                if cultivo==None and consumidor==None and variedad==None and year==None:
                    options=df_agricola_1

                elif cultivo!=None  and consumidor==None and variedad==None and year==None:    
                        options=df_agricola_1[df_agricola_1['CULTIVO']==cultivo]
                elif cultivo==None  and consumidor!=None and variedad==None and year==None:    
                        options=df_agricola_1[df_agricola_1['CONSUMIDOR']==consumidor]
                
                elif cultivo==None  and consumidor==None and variedad!=None and year==None:    
                        options=df_agricola_1[df_agricola_1['VARIEDAD']==variedad]

                elif cultivo==None  and consumidor==None and variedad==None and year!=None:
                        options=df_agricola_1[(df_agricola_1['AÑO_CAMPAÑA']==year)]  

                elif cultivo!=None  and consumidor!=None and variedad==None and year==None:
                        options=df_agricola_1[(df_agricola_1['CULTIVO']==cultivo)&(df_agricola_1['CONSUMIDOR']==consumidor)]

                elif cultivo!=None  and consumidor==None and variedad!=None and year==None:
                        options=df_agricola_1[(df_agricola_1['CULTIVO']==cultivo)&(df_agricola_1['VARIEDAD']==variedad)]     

                elif cultivo!=None  and consumidor==None and variedad==None and year!=None:
                        options=df_agricola_1[(df_agricola_1['CULTIVO']==cultivo)&(df_agricola_1['AÑO_CAMPAÑA']==year)]


                elif cultivo==None  and consumidor!=None and variedad!=None and year==None:
                        options=df_agricola_1[(df_agricola_1['CONSUMIDOR']==consumidor)&(df_agricola_1['VARIEDAD']==variedad)]  

                elif cultivo==None  and consumidor!=None and variedad==None and year!=None:
                        options=df_agricola_1[(df_agricola_1['CONSUMIDOR']==consumidor)&(df_agricola_1['AÑO_CAMPAÑA']==year)]  
                
                elif cultivo==None  and consumidor==None and variedad!=None and year!=None:
                        options=df_agricola_1[(df_agricola_1['VARIEDAD']==variedad)&(df_agricola_1['AÑO_CAMPAÑA']==year)]  


                elif cultivo!=None  and consumidor!=None and variedad!=None and year==None:
                        options=df_agricola_1[(df_agricola_1['CULTIVO']==cultivo)&(df_agricola_1['CONSUMIDOR']==consumidor)&(df_agricola_1['VARIEDAD']==variedad)]
                
                elif cultivo==None  and consumidor!=None and variedad!=None and year!=None:
                        options=df_agricola_1[(df_agricola_1['AÑO_CAMPAÑA']==year)&(df_agricola_1['CONSUMIDOR']==consumidor)&(df_agricola_1['VARIEDAD']==variedad)]
                
                elif cultivo!=None  and consumidor!=None and variedad==None and year!=None:
                        options=df_agricola_1[(df_agricola_1['AÑO_CAMPAÑA']==year)&(df_agricola_1['CONSUMIDOR']==consumidor)&(df_agricola_1['CULTIVO']==cultivo)]
                
                elif cultivo!=None  and consumidor==None and variedad!=None and year!=None:
                        options=df_agricola_1[(df_agricola_1['AÑO_CAMPAÑA']==year)&(df_agricola_1['CULTIVO']==cultivo)&(df_agricola_1['VARIEDAD']==variedad)]
                
                elif cultivo!=None  and consumidor!=None and variedad!=None and year!=None:
                        options=df_agricola_1[(df_agricola_1['AÑO_CAMPAÑA']==year)&(df_agricola_1['CULTIVO']==cultivo)&(df_agricola_1['VARIEDAD']==variedad)&(df_agricola_1['CONSUMIDOR']==consumidor)]


                option_cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()] 
                option_variedad=[{'label': i, 'value': i} for i in options['VARIEDAD'].unique()] 
                option_consumidor=[{'label': i, 'value': i} for i in options['CONSUMIDOR'].unique()] 
                option_year=[{'label': i, 'value': i} for i in sorted(options['AÑO_CAMPAÑA'].unique())] 
                
                
                return option_cultivo,option_variedad,option_consumidor,option_year

    @app.callback(
                
                Output("graph1","figure"),
                Output("graph2","figure"),
                Output("graph3","figure"),
                
                
                Input("cultivo","value"),
                Input("variedad","value"),
                Input("consumidor","value"),
                Input("year","value"),
        )
    def filtrar_agricola2(cultivo,variedad,consumidor,year):
            if cultivo==None and consumidor==None and variedad==None and year==None:
                    options=df_agricola

            elif cultivo!=None  and consumidor==None and variedad==None and year==None:    
                        options=df_agricola[df_agricola['CULTIVO']==cultivo]
            elif cultivo==None  and consumidor!=None and variedad==None and year==None:    
                        options=df_agricola[df_agricola['CONSUMIDOR']==consumidor]
                
            elif cultivo==None  and consumidor==None and variedad!=None and year==None:    
                        options=df_agricola[df_agricola['VARIEDAD']==variedad]

            elif cultivo==None  and consumidor==None and variedad==None and year!=None:
                        options=df_agricola[(df_agricola['AÑO_CAMPAÑA']==year)]  

            elif cultivo!=None  and consumidor!=None and variedad==None and year==None:
                        options=df_agricola[(df_agricola['CULTIVO']==cultivo)&(df_agricola['CONSUMIDOR']==consumidor)]

            elif cultivo!=None  and consumidor==None and variedad!=None and year==None:
                        options=df_agricola[(df_agricola['CULTIVO']==cultivo)&(df_agricola['VARIEDAD']==variedad)]     

            elif cultivo!=None  and consumidor==None and variedad==None and year!=None:
                        options=df_agricola[(df_agricola['CULTIVO']==cultivo)&(df_agricola['AÑO_CAMPAÑA']==year)]


            elif cultivo==None  and consumidor!=None and variedad!=None and year==None:
                        options=df_agricola[(df_agricola['CONSUMIDOR']==consumidor)&(df_agricola['VARIEDAD']==variedad)]  

            elif cultivo==None  and consumidor!=None and variedad==None and year!=None:
                        options=df_agricola[(df_agricola['CONSUMIDOR']==consumidor)&(df_agricola['AÑO_CAMPAÑA']==year)]  
                
            elif cultivo==None  and consumidor==None and variedad!=None and year!=None:
                        options=df_agricola[(df_agricola['VARIEDAD']==variedad)&(df_agricola['AÑO_CAMPAÑA']==year)]  


            elif cultivo!=None  and consumidor!=None and variedad!=None and year==None:
                        options=df_agricola[(df_agricola['CULTIVO']==cultivo)&(df_agricola['CONSUMIDOR']==consumidor)&(df_agricola['VARIEDAD']==variedad)]
                
            elif cultivo==None  and consumidor!=None and variedad!=None and year!=None:
                        options=df_agricola[(df_agricola['AÑO_CAMPAÑA']==year)&(df_agricola['CONSUMIDOR']==consumidor)&(df_agricola['VARIEDAD']==variedad)]
            
            elif cultivo!=None  and consumidor!=None and variedad==None and year!=None:
                        options=df_agricola[(df_agricola['AÑO_CAMPAÑA']==year)&(df_agricola['CULTIVO']==cultivo)&(df_agricola['VARIEDAD']==variedad)]
                
            elif cultivo!=None  and consumidor==None and variedad!=None and year!=None:
                        options=df_agricola[(df_agricola['AÑO_CAMPAÑA']==year)&(df_agricola['CULTIVO']==cultivo)&(df_agricola['CONSUMIDOR']==consumidor)]
                
            elif cultivo!=None  and consumidor!=None and variedad!=None and year!=None:
                        options=df_agricola[(df_agricola['AÑO_CAMPAÑA']==year)&(df_agricola['CULTIVO']==cultivo)&(df_agricola['VARIEDAD']==variedad)&(df_agricola['CONSUMIDOR']==consumidor)]

            
            #print(options['AÑO_CAMPAÑA'].unique())
            df_area_agricola=pd.DataFrame()
            years=sorted(options['AÑO_CAMPAÑA'].unique())
            for year in years:
                df_year=options[options['AÑO_CAMPAÑA']==year]
                df_year=df_year.groupby(['CODCONSUMIDOR','CONSUMIDOR','CULTIVO','VARIEDAD','AREA_CAMPAÑA','AÑO_CAMPAÑA'])[['CANTIDAD']].sum().reset_index()
                df_area_agricola=pd.concat([df_area_agricola,df_year])  
            
            df_area_agricola_total=df_area_agricola.groupby(['CULTIVO','VARIEDAD'])[['AREA_CAMPAÑA']].sum().reset_index()

            fig2 = px.pie(df_area_agricola_total, values='AREA_CAMPAÑA', names='CULTIVO',template="none",
                    title='Hectáreas sembradas por Cultivo',hole=.7
                    #hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'}
                    )
            fig2.update_traces(textposition='outside', textinfo='percent+label',textfont_size=16)

            fig2.update_layout(showlegend=False)

            df_area_agricola_total=df_area_agricola_total.sort_values('AREA_CAMPAÑA',ascending=False)
            df_area_agricola_total['PROMEDIO']=df_area_agricola_total['AREA_CAMPAÑA'].mean()
            fig5 = go.Figure([go.Bar(x=df_area_agricola_total['VARIEDAD'], y=df_area_agricola_total['AREA_CAMPAÑA'],name='Variedad')])
            fig5.update_layout(
                            title='Hectáreas por Variedad',
                            template='none',
                            showlegend=True,
                            legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            
                            )

                        )
            fig5.update_layout(xaxis_title='Variedad',yaxis_title='Hectáreas',legend_title="")
            fig5.add_trace(go.Scatter(
                        x=df_area_agricola_total['VARIEDAD'],
                        y=df_area_agricola_total['PROMEDIO'],
                        name="Promedio",
                        #yaxis="y4",
                        #text=df_mes_top['PESONETO_PRODUCTO'],
                        #marker_color="#1f1587",
                        textposition='bottom right',
                        texttemplate='{text:.2s}'
                    ))
            fig5.update_layout(autosize=True,margin=dict(l=40,r=70,b=90,t=40),
                             xaxis=dict(showticklabels=True,tickfont=dict(size=11)),
                             yaxis=dict(tickfont=dict(size=11)))
            
            df_area_consumidor=df_area_agricola.groupby(['CONSUMIDOR'])[['AREA_CAMPAÑA']].sum().reset_index().sort_values('AREA_CAMPAÑA',ascending=False)
            df_area_consumidor['PROMEDIO']=df_area_consumidor['AREA_CAMPAÑA'].mean()
            fig6 = go.Figure([go.Bar(x=df_area_consumidor['CONSUMIDOR'], y=df_area_consumidor['AREA_CAMPAÑA'],name='Consumidor')])
            fig6.update_layout(
                            title='Hectáreas por Consumidor',
                            template='none',
                            showlegend=True,
                            legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            
                            )

                        )
            fig6.update_layout(xaxis_title='Consumidor',yaxis_title='Hectáreas',legend_title="")
            fig6.add_trace(go.Scatter(
                        x=df_area_consumidor['CONSUMIDOR'],
                        y=df_area_consumidor['PROMEDIO'],
                        name="Promedio",
                        #yaxis="y4",
                        #text=df_mes_top['PESONETO_PRODUCTO'],
                        #marker_color="#1f1587",
                        textposition='bottom right',
                        texttemplate='{text:.2s}'
                    ))
            fig6.update_layout(autosize=True,margin=dict(l=40,r=40,b=160,t=40),
                            xaxis=dict(showticklabels=True,tickfont=dict(size=11)),
                             yaxis=dict(tickfont=dict(size=11)))

            return fig2,fig5,fig6

def barline(df,title):
    fig1 = go.Figure()
    for insumo in df.columns[3:]:
        fig1.add_trace(go.Bar(x=df['CULTIVO'],y=df[insumo],text=df[insumo],orientation='v',textposition='inside',texttemplate='%{text:.2s}',name=insumo))

    fig1.update_layout(
                    title={'text':title},
                    titlefont={'size': 13},
                    uniformtext_minsize=8,# uniformtext_mode='hide',
                    template='none')
    fig1.update_layout(
                        autosize=True,
                        #width=100,
                        height=360,
                        margin=dict(l=40,r=70,b=20,t=80),
                        xaxis=dict(showticklabels=True,tickfont=dict(size=11)),
                        yaxis=dict(tickfont=dict(size=11)) ) 
    fig1.add_trace(go.Scatter(
                        x=df['CULTIVO'],
                        y=df['AREA_CAMPAÑA'],
                        name="Hectáreas",
                        yaxis="y4",
                        text=df['AREA_CAMPAÑA'],
                        #marker_color="#1f1587",
                        textposition='bottom right',
                        texttemplate='{text:.2s}'
                    ))
    fig1.update_layout(
                    yaxis4=dict(title="Hectáreas",anchor="x",overlaying="y",side="right",titlefont_size=12,tickfont_size=12)
                    )
    fig1.update_layout(showlegend=True,legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    return fig1

def costosCultivo(empresa):
    """"""
    df_consumidores = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
    df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
    df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
    df_var_agricolas_default=cleanVariablesAgricolas(df_consumidores,
                                                  df_variedad,
                                                  df_cultivos,
                                                  df_fertilizacion)
    df_var_agricolas_pivot_default=variablesAgricolasPivot(df_var_agricolas_default)
    df_costos_agricola_default=costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad)
    """"""
    """
    data=dataAgricolaEmpresa(empresa)
    df_costos_agricolas=data[2]
    """
    df_costos_agricolas=df_costos_agricola_default.copy()
    dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )
    app = DjangoDash('costos_cultivo', external_stylesheets=[url_theme1, dbc.icons.BOOTSTRAP, dbc_css])#

    app.layout = html.Div([
            dbc.Row([
                        dbc.Col([
                            dbc.Button("Filtrar", id="open-offcanvas-placement", n_clicks=0),
                            dbc.Offcanvas(
                            [
                                html.Div([
                                        dbc.Label('Año'),
                                        dcc.Dropdown(
                                        id='year',
                                        multi=False,
                                        searchable= True,
                                        #placeholder= pholder,
                                        options=[],
                                        #clearable=False,
                                        style={
                                            
                                            'font-size': "90%",
                                            #'min-height': '2px',
                                            },
                                        ),

                                ]) ,  
                                
                                html.Div([
                                        dbc.Label('Cultivo'),
                                        dcc.Dropdown(
                                            id='cultivo',
                                            multi=False,
                                            searchable= True,
                                            placeholder= 'All',
                                            options=[],
                                            style={
                                                
                                                'font-size': "80%",
                                                #'min-height': '2px',
                                                },
                                            )
                                ]) ,
                                html.Div([
                                        dbc.Label('Consumidor'),
                                        dcc.Dropdown(
                                        id='consumidor',
                                        multi=False,
                                        searchable= True,
                                        placeholder= 'All',
                                        options=[],
                                        style={
                                            
                                            'font-size': "80%",
                                            #'min-height': '2px',
                                            },
                                        )

                                ]),
                                html.Div([
                                        dbc.Label('Moneda'),
                                        dbc.RadioItems(  id='radio-moneda',
                                            options=[
                                                {'label': 'Soles', 'value': 'Soles'},
                                                {'label': 'Dolares', 'value':'Dolares'},
                                                
                                            ],
                                            value='Soles',
                                            inline=True
                                        )

                                ])
                            
                                ],
                                
                                scrollable=True,
                                id="offcanvas-placement",
                                title="Filtros",
                                is_open=False,

                                backdrop=False,
                                style={"width":250}
                        )
                        ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([#id='title'
                            html.H3(id='title', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                            html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                            
                        ],width=10,className="col-xl-10 col-md-10 col-sm-12 col-12 mb-3")
                    ]),
            dbc.Row([dbc.Col([dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")]),
            dbc.Row([dbc.Col([dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")])
            
        ])
    @app.callback(
    Output("offcanvas-placement", "is_open"),
    Input("open-offcanvas-placement", "n_clicks"),
    [State("offcanvas-placement", "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
            if n1:
                return not is_open
            return is_open

    @app.callback(
            
            Output("title","children"),
            Output("subtitle","children"),
            Input("cultivo","value"),
            Input("consumidor","value"),
            Input("year","value"),
            Input("radio-moneda","value")
            
            
            )
    def filtrar_agricola2(cultivo,consumidor,year,moneda):
        general='Costos por Cultivo'+' '+str(moneda)
        
        if cultivo == None:
            title=general
        else:
            title=general+' '+str(year)
        
        if cultivo == None and consumidor == None:
            subtitle=''
        elif cultivo != None and consumidor == None: 
            subtitle=cultivo
        elif cultivo == None and consumidor != None: 
            subtitle=consumidor
        elif cultivo != None and consumidor != None: 
            subtitle=cultivo+' - '+consumidor
        
        return title, subtitle

    @app.callback(
            Output("cultivo","options"),
            Output("consumidor","options"),
            Output("year","options"),
            Output("year","value"),
            
            Input("cultivo","value"),
            #Input("cultivo","value"),
            Input("consumidor","value"),
            
            Input("year","value"),
            
            
            )
    def filtrar_agricola2(cultivo,consumidor,year):
            
            if cultivo==None and consumidor==None and year==None:
                options=df_costos_agricolas
            elif cultivo!=None  and consumidor==None and year==None:    
                options=df_costos_agricolas[df_costos_agricolas['CULTIVO']==cultivo]
            elif cultivo!=None  and consumidor!=None and year==None:
                options=df_costos_agricolas[(df_costos_agricolas['CULTIVO']==cultivo)&(df_costos_agricolas['CONSUMIDOR']==consumidor)]
            elif cultivo==None  and consumidor!=None and year==None:
                options=df_costos_agricolas[(df_costos_agricolas['CONSUMIDOR']==consumidor)]

            elif cultivo==None  and consumidor==None and year!=None:
                options=df_costos_agricolas[(df_costos_agricolas['AÑO_CAMPAÑA']==year)]
            
            elif cultivo==None  and consumidor!=None and year!=None:
                options=df_costos_agricolas[(df_costos_agricolas['AÑO_CAMPAÑA']==year)&(df_costos_agricolas['CONSUMIDOR']==consumidor)]

            elif cultivo!=None  and consumidor!=None and year!=None:
                options=df_costos_agricolas[(df_costos_agricolas['AÑO_CAMPAÑA']==year)&(df_costos_agricolas['CONSUMIDOR']==consumidor)&(df_costos_agricolas['CULTIVO']==cultivo)]

            elif cultivo!=None  and consumidor==None and year!=None:
                options=df_costos_agricolas[(df_costos_agricolas['AÑO_CAMPAÑA']==year)&(df_costos_agricolas['CULTIVO']==cultivo)]
        

            option_cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()] 
            option_consumidor=[{'label': i, 'value': i} for i in options['CONSUMIDOR'].unique()] 
            option_year=[{'label': i, 'value': i} for i in sorted(options['AÑO_CAMPAÑA'].unique())] 
            last_year=sorted(options['AÑO_CAMPAÑA'].unique())[-1:]
            last_year=int(last_year[0])
        
            return option_cultivo,option_consumidor,option_year,last_year

    @app.callback(
            
            Output("graph1","figure"),
            Output("graph2","figure"),
            
            
            
            Input("cultivo","value"),
            Input("consumidor","value"),
            Input("year","value"),
            Input("radio-moneda","value")
    )
    def filtrar_agricola2(cultivo,consumidor,year,moneda):
        if moneda=='Soles':
                saldo='SALDO_MOF'
        else:
                saldo='SALDO_MEX'

        if cultivo==None and consumidor==None and year==None:
                options=df_costos_agricolas
        elif cultivo!=None  and consumidor==None and year==None:    
                options=df_costos_agricolas[df_costos_agricolas['CULTIVO']==cultivo]
        elif cultivo!=None  and consumidor!=None and year==None:
                options=df_costos_agricolas[(df_costos_agricolas['CULTIVO']==cultivo)&(df_costos_agricolas['CONSUMIDOR']==consumidor)]
        elif cultivo==None  and consumidor!=None and year==None:
                options=df_costos_agricolas[(df_costos_agricolas['CONSUMIDOR']==consumidor)]

        elif cultivo==None  and consumidor==None and year!=None:
                options=df_costos_agricolas[(df_costos_agricolas['AÑO_CAMPAÑA']==year)]
            
        elif cultivo==None  and consumidor!=None and year!=None:
                options=df_costos_agricolas[(df_costos_agricolas['AÑO_CAMPAÑA']==year)&(df_costos_agricolas['CONSUMIDOR']==consumidor)]

        elif cultivo!=None  and consumidor!=None and year!=None:
                options=df_costos_agricolas[(df_costos_agricolas['AÑO_CAMPAÑA']==year)&(df_costos_agricolas['CONSUMIDOR']==consumidor)&(df_costos_agricolas['CULTIVO']==cultivo)]

        elif cultivo!=None  and consumidor==None and year!=None:
                options=df_costos_agricolas[(df_costos_agricolas['AÑO_CAMPAÑA']==year)&(df_costos_agricolas['CULTIVO']==cultivo)]
        
        df_costos_agricolas_pivot=options.pivot(index=('CODCULTIVO','CULTIVO','AREA_CAMPAÑA','IDCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA'),values=(saldo),columns=('TIPO'))
        df_costos_agricolas_pivot.reset_index()
        df_costos_agricolas_pivot=pd.DataFrame(df_costos_agricolas_pivot.to_records())
        df_costos_insumos=df_costos_agricolas_pivot.drop(['CODCULTIVO','CODSIEMBRA','CODCAMPAÑA'], axis=1)
        df_costos_insumos=df_costos_insumos.groupby(['CULTIVO','AÑO_CAMPAÑA','CONSUMIDOR','AREA_CAMPAÑA']).sum().reset_index()
        df_costos_insumos_cultivo=df_costos_insumos.groupby(['CULTIVO']).sum().reset_index()
        #########################
        df_costos_hectarea=df_costos_insumos_cultivo.copy()
        for recurso in df_costos_hectarea.columns[3:]:
            df_costos_hectarea[recurso]=df_costos_hectarea[recurso]/df_costos_hectarea['AREA_CAMPAÑA']

        return barline(df_costos_insumos_cultivo,'Costos Totales por Cultivo'),barline(df_costos_hectarea,'Costos por Hectárea')

def comparativoRecursos(empresa):
    """"""
    df_consumidores = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
    df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
    df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
    df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
    df_var_agricolas_default=cleanVariablesAgricolas(df_consumidores,
                                                  df_variedad,
                                                  df_cultivos,
                                                  df_fertilizacion)
    df_var_agricolas_pivot_default=variablesAgricolasPivot(df_var_agricolas_default)
    df_costos_agricola_default=costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad)
    """"""
    """
    data=dataAgricolaEmpresa(empresa)
    df_agricola=data[0] 
    """     
    df_agricola=df_var_agricolas_default.copy()

    df_produccion=df_agricola.groupby(['AÑO_CAMPAÑA','FECHAINICIO_CAMPAÑA','FECHAFIN_CAMPAÑA','CULTIVO','AÑO_CULTIVO','VARIEDAD','DSCVARIABLE','FECHA','CONSUMIDOR'])[['CANTIDAD']].sum().reset_index()
    app = DjangoDash('variables_agricolas', external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div([
            dbc.Row([
                    dbc.Col([btnFilter()],width=1,className="col-xl-1 col-md-1 col-sm-1 col-1 mb-3"),
                    dbc.Col([
                            html.H3(id='title', style={'margin-bottom': '0px', 'color': 'black'}),#,'textAlign': 'center'
                            html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black'})
                        ],width=11,className="col-xl-11 col-md-11 col-sm-11 col-11 mb-3"),
                    
                    ]),
                    offcanvas(componentes=[
                        select(ids="cultivo",texto="Cultivo"),
                        select(ids="variedad",texto="Variedad"),
                        select(ids="consumidor",texto="Consumidor"),
                    ]),
        dbc.Row([multiSelect(ids="camp-cultivo",texto="Seleccione Campaña - Cultivo"),]),

    
         dbc.Row([
            dbc.Col([loadingOverlay(html.Div(id='tabs')),],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            #dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
         ]),
         #dbc.Row([
         #   dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph3'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
         #   dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph4'),className="shadow-sm"))],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
         #]),

            
    ])
    offcanvasAction(app)
    @app.callback(
            Output("title","children"),
            Output("subtitle","children"),
            
            Input("cultivo","value"),
            Input("consumidor","value"),
            #Input("slider-year","value"),
            
            )
    def title(cultivo,consumidor):
        general='Recursos Agrícolas'
        
        #if slider == None:
        #    title=general
        #else:
        #    title=general+' del año '+str(slider[0])+' al '+str(slider[1])
        title=general
        if cultivo == None and consumidor == None:
            subtitle=''
        elif cultivo != None and consumidor == None: 
            subtitle=cultivo
        elif cultivo == None and consumidor != None: 
            subtitle=consumidor
        elif cultivo != None and consumidor != None: 
            subtitle=cultivo+' '+consumidor
        
        return title, subtitle
    
    @app.callback(
            Output("cultivo","data"),
            Output("variedad","data"),
            Output("consumidor","data"),
            Output("camp-cultivo","data"),
            #Output("range-slider","marks"),
            
            Input("cultivo","value"),
            #Input("cultivo","value"),
            Input("variedad","value"),
            Input("consumidor","value"),
            
            
            )
    def filtrar_agricola1(cultivo,variedad,consumidor):

            if cultivo==None and consumidor==None and variedad==None:
                    options=df_produccion

            elif cultivo!=None  and consumidor==None and variedad==None:    
                    options=df_produccion[df_produccion['CULTIVO']==cultivo]
            elif cultivo==None  and consumidor!=None and variedad==None:    
                    options=df_produccion[df_produccion['CONSUMIDOR']==consumidor]
            
            elif cultivo==None  and consumidor==None and variedad!=None:    
                    options=df_produccion[df_produccion['VARIEDAD']==variedad]

            elif cultivo!=None  and consumidor!=None and variedad!=None:
                    options=df_produccion[(df_produccion['CULTIVO']==cultivo)&(df_produccion['CONSUMIDOR']==consumidor)&(df_produccion['VARIEDAD']==variedad)]

            elif cultivo!=None  and consumidor!=None and variedad==None:
                    options=df_produccion[(df_produccion['CULTIVO']==cultivo)&(df_produccion['CONSUMIDOR']==consumidor)]

            elif cultivo!=None  and consumidor==None and variedad!=None:
                    options=df_produccion[(df_produccion['CULTIVO']==cultivo)&(df_produccion['VARIEDAD']==variedad)]        

            elif cultivo==None  and consumidor!=None and variedad!=None:
                    options=df_produccion[(df_produccion['CONSUMIDOR']==consumidor)&(df_produccion['VARIEDAD']==variedad)]  
                    
            option_cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()] 
            option_variedad=[{'label': i, 'value': i} for i in options['VARIEDAD'].unique()] 
            option_consumidor=[{'label': i, 'value': i} for i in options['CONSUMIDOR'].unique()]
            option_camp_cultivo=[{'label': i, 'value': i} for i in options['AÑO_CULTIVO'].unique()] 
            #list_years=sorted(options['AÑO_FECHA'].unique())
            #lista_anios=[str(x) for x in list_years]
            #marks=dict(zip(lista_anios, lista_anios))
            
            
            return option_cultivo,option_variedad,option_consumidor,option_camp_cultivo#,marks
    
    @app.callback(
            Output("tabs","children"),
            
            
            #Output("range-slider","marks"),
            
            Input("cultivo","value"),
            #Input("cultivo","value"),
            Input("variedad","value"),
            Input("consumidor","value"),
            Input("camp-cultivo","value"),
            
            
            )
    def filtrar_agricola1(cultivo,variedad,consumidor,campaña_cultivo):
            df_produccion=df_agricola
            def orderX(x,df):
                if x == 'week':
                    order={'week':sorted(df['week'].unique()),'DSCVARIABLE': sorted(df['DSCVARIABLE'].unique())}
                else: 
                    order={}
                return order
            if cultivo==None and consumidor==None and variedad==None:
                    options=df_produccion

            elif cultivo!=None  and consumidor==None and variedad==None:    
                    options=df_produccion[df_produccion['CULTIVO']==cultivo]
            elif cultivo==None  and consumidor!=None and variedad==None:    
                    options=df_produccion[df_produccion['CONSUMIDOR']==consumidor]
            
            elif cultivo==None  and consumidor==None and variedad!=None:    
                    options=df_produccion[df_produccion['VARIEDAD']==variedad]

            elif cultivo!=None  and consumidor!=None and variedad!=None:
                    options=df_produccion[(df_produccion['CULTIVO']==cultivo)&(df_produccion['CONSUMIDOR']==consumidor)&(df_produccion['VARIEDAD']==variedad)]

            elif cultivo!=None  and consumidor!=None and variedad==None:
                    options=df_produccion[(df_produccion['CULTIVO']==cultivo)&(df_produccion['CONSUMIDOR']==consumidor)]

            elif cultivo!=None  and consumidor==None and variedad!=None:
                    options=df_produccion[(df_produccion['CULTIVO']==cultivo)&(df_produccion['VARIEDAD']==variedad)]        

            elif cultivo==None  and consumidor!=None and variedad!=None:
                    options=df_produccion[(df_produccion['CONSUMIDOR']==consumidor)&(df_produccion['VARIEDAD']==variedad)]  

            if campaña_cultivo == None or len(campaña_cultivo) == 0:
                  options=options.copy()
            else :
                  options=options[options['AÑO_CULTIVO'].isin(campaña_cultivo)]

            options.loc[options.DSCVARIABLE == 'Nitrógeno','DSCVARIABLE'] =  'Nitrogeno'  
            options.loc[options.DSCVARIABLE == 'Fósforo','DSCVARIABLE'] =  'Fosforo'  
            list_tipo=options['TIPO'].unique()
            df_fertilizantes=options[options['TIPO']=='Insumos']
            df_fer=df_fertilizantes.groupby(['AÑO_CULTIVO','DSCVARIABLE'])[['CANTIDAD']].sum().reset_index()
            #FACE_ROW
            test=df_fertilizantes.groupby(['AÑO_CULTIVO','DSCVARIABLE','week'])[['CANTIDAD']].sum().reset_index()
            for campcul in test['AÑO_CULTIVO'].unique():
                
                fig2 = px.line(test[test['AÑO_CULTIVO']==campcul]  , x="week", y="CANTIDAD", color='DSCVARIABLE',category_orders=orderX('week',test[test['AÑO_CULTIVO']==campcul]  ),template='none')#, facet_row="AÑO_CULTIVO"
            #fig2.update_yaxes(matches=None)
            #df_fer=df_fer.sort_values(by=[radio_st,'AÑO_FECHA','SEMANA'],ascending=True)

            df_agua=options[options['TIPO']=='Riego']
            df_agua=df_agua.groupby(['AÑO_CULTIVO'])[['CANTIDAD']].sum().reset_index()
            #df_agua=df_agua.sort_values(by=[radio_st,'AÑO_FECHA','SEMANA'],ascending=True)

            df_horas=options[options['TIPO']=='Mano de obra']
            df_horas=df_horas.groupby(['AÑO_CULTIVO'])[['CANTIDAD']].sum().reset_index()
            #df_horas=df_horas.sort_values(by=[radio_st,'AÑO_FECHA','SEMANA'],ascending=True)

            df_horas_maquina=options[options['TIPO']=='Maquinaria']
            df_horas_maquina=df_horas_maquina.groupby(['AÑO_CULTIVO'])[['CANTIDAD']].sum().reset_index()
            #df_horas_maquina=df_horas_maquina.sort_values(by=[radio_st,'AÑO_FECHA','SEMANA'],ascending=True)
                
            #df_bar_comparativo=options.groupby(['AÑO_CULTIVO'])[['CANTIDAD']].sum().reset_index()
            def barComparativoAR(df,title='',x='x',y='y',color=None):
                fig_b = px.bar(df, x=x, y=y,template="none",title=title,color=color)#, facet_row="Año",facet_row_spacing=0.1
                fig_b.update_layout(autosize=True,margin=dict(l=60,r=40,b=90,t=50),height=350,bargap=0.15)
                fig_b.update_xaxes(type='category')
                return fig_b
            fig_fertilizantes=barComparativoAR(df_fer,title='Fertilizantes',x='AÑO_CULTIVO',y='CANTIDAD',color='DSCVARIABLE')
            fig_agua=barComparativoAR(df_agua,title='Riego',x='AÑO_CULTIVO',y='CANTIDAD')
            #fig_horas=px.line(df_horas, x=x, y="CANTIDAD", color='DSCVARIABLE',template='plotly_white',height=280,margin=dict(l=60,r=40,b=40,t=70,pad=0,autoexpand=True))
            fig_horas=barComparativoAR(df_horas,title='Mano de Obra',x='AÑO_CULTIVO',y='CANTIDAD')
            fig_horas_maquinaria=barComparativoAR(df_horas_maquina,title='Horas Máquina',x='AÑO_CULTIVO',y='CANTIDAD')

            child=html.Div([
            
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab(i, value=i)for i in list_tipo
                        ]
                    ),
                    dmc.TabsPanel(dcc.Graph(figure=fig_agua),value='Riego'),
                    dmc.TabsPanel(dcc.Graph(figure=fig_horas_maquinaria), value='Maquinaria'),
                    dmc.TabsPanel(dcc.Graph(figure=fig_horas), value='Mano de obra'),
                    dmc.TabsPanel(dcc.Graph(figure=fig_fertilizantes), value='Insumos'),
                ],
                value=list_tipo[0],
                ),
            html.Div([dcc.Graph(figure=fig2)])
            
            ]),

            
            return child




















"""
 dbc.Row([
            dbc.Col([
                dbc.Button("Mas Filtros",id="open-offcanvas-placement",n_clicks=0, className="me-1",outline=True, color="primary"),
                #canvas()
                dbc.Offcanvas([
                            dbc.Badge("Recursos", pill=True, color="dark"),
                            dcc.RadioItems(id="recursos",
                                options=[
                                    {'label': 'Por Cantidad', 'value': 'cantidad'},
                                    {'label': 'Por Héctarea', 'value': 'hectarea'}, 
                                ],
                                value='cantidad',
                                #labelStyle={'display': 'inline-block'}
                            ),

                            dbc.Badge("Eje X", pill=True, color="dark"), 
                            dcc.RadioItems(id="radio-st",
                                options=[
                                    {'label': 'Fecha', 'value': 'fecha'},
                                    {'label': 'Semana', 'value': 'semana'},
                                ],
                                value='fecha',
                                labelStyle={'display': 'inline-block'}
                            ),
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
                            ],
                            scrollable=True,
                            id="offcanvas-placement",
                            title="Filtros",
                            is_open=False,
                            #placement="end",
                            backdrop=False,
                            style={"width":250}#,"background-color": "S"
                        ), 
            ],width=3,className="col-xl-3 col-md-4 col-sm-12 col-12 mb-3"),
            dbc.Col([
                html.Div("Seleccione Año Campaña"),
                dcc.Dropdown(
                    id="drop_anio",
                    multi=False,
                    searchable= True,
                    placeholder= 'All',
                    options=[],
                    style={
                        
                        'font-size': "80%",
                        #'min-height': '2px',
                        },
                ),

            ],width=3,className="col-xl-3 col-md-4 col-sm-12 col-12 mb-3"),
            dbc.Col([
                html.Div('Seleccione Cultivos'),
                dcc.Dropdown(
                    id="drop_cultivo",
                    multi=True,
                    searchable= True,
                    placeholder= '',
                    options=[],
                
                ),
            ],width=3,className="col-xl-3 col-md-4 col-sm-12 col-12 mb-3"),
            dbc.Col([
                
            ],width=3,className="col-xl-3 col-md-4 col-sm-12 col-12 mb-3"),
        ]),
 """ 
external_stylesheets = [dbc.themes.BOOTSTRAP]#
def Column(content=[],size=12):
      return dbc.Col(content,width=size,className=f"col-xl-{size} col-md-{size} col-sm-12 col-12 mb-3")

def dashCostosProduccionAgricola():
      
    df_general=df_var_agricolas_default.copy()
    df_general_pivot=df_var_agricolas_pivot_default.copy()
    df_costos_agricolas=df_costos_agricola_default.copy()

    app = DjangoDash('vcostos',external_stylesheets=external_stylesheets,external_scripts=scripts)
    app.layout = html.Div([
        dbc.Row([
            Column(content=[
                  btnFilter()
            ],size=1),
            Column(content=[
                  html.Div(id='title')
            ],size=5),
            Column(content=[
                  select(
                         ids="drop_anio",
                         texto="Campaña",
                         value=sorted(df_costos_agricolas['AÑO_CAMPAÑA'].unique())[-1],
                         data=[{'label': i, 'value': i} for i in df_costos_agricolas['AÑO_CAMPAÑA'].unique()],
                         size='xs',
                        )
            ],size=2),
            Column(content=[
                  multiSelect(ids="drop_cultivo",
                              texto="Cultivos",
                              size='xs'
                            )
            ],size=2),
            Column(content=[
                  select(
                         ids="drop_variedad",
                         texto="Variedad",
                         size='xs'
                        )
                         

            ],size=2),
            ######################################################################################
            offcanvas(componentes=[
                    radioGroup(ids="radio-costos",
                               texto="Tipo de Costo",
                               children=[dmc.Radio(label='Totales', value='CT'),dmc.Radio(label='Por Hectárea', value='CH')],
                               value="CT",
                    ),
                    radioGroup(ids="rbtn_dinero",
                               texto="Moneda",
                               children=[dmc.Radio(label='Soles', value='SALDO_MOF'),dmc.Radio(label='Dolares', value='SALDO_MEX')],
                               value="SALDO_MEX",
                    ),
                    dbc.Checklist(
                                    id="check-recursos",
                                    inline=False,
                                    input_checked_style={
                                        "backgroundColor": "rgb(34, 139, 230)",
                                        "borderColor": "rgb(34, 139, 230)",
                                    },     
                                    label_style={'font-size': '12px'} )

            ]),
        ]),
        dbc.Row([
            Column(content=[
                html.Div(id='card-total-costos')#tipo de gasto     
            ],size=4),
            Column(content=[
               html.Div(id='card-total-ha')#por cultivo
            ],size=4),
            Column(content=[
               html.Div(id='card-cultivo-costos')#
            ],size=4),
        ]),
        dbc.Row([
            Column(content=[
                  dmc.Card(children=[
                                    dmc.CardSection([dcc.Graph(id='bar-cultivo-costosp')])
                            ],
                            withBorder=True,
                            shadow="lg",
                            radius="xs"
                        )
            ],size=5),
            Column(content=[
                  dmc.Card(children=[
                                    dmc.CardSection([dcc.Graph(id='bar-lote-costosp')])
                            ],
                            withBorder=True,
                            shadow="lg",
                            radius="xs"
                        )
            ],size=7),
        ]),
        dbc.Row([
            
            Column(content=[
                  dmc.Card(children=[
                                    dmc.CardSection([dcc.Graph(id='bar-variedad-costosp')])
                            ],
                            withBorder=True,
                            shadow="lg",
                            radius="xs"
                        )
            ],size=4),
            Column(content=[
                  dmc.Card(children=[
                                    dmc.CardSection([dcc.Graph(id='pie-tipo-costosp')])
                            ],
                            withBorder=True,
                            shadow="lg",
                            radius="xs"
                        )
            ],size=4),
            Column(content=[
                  dmc.Card(children=[
                                    dmc.CardSection([dcc.Graph(id='mapa-costosp')])
                            ],
                            withBorder=True,
                            shadow="lg",
                            radius="xs"
                        )
            ],size=4),
        ]),
        

    dcc.Store(id='data-values')     
    ])
    offcanvasAction(app)
    @app.callback(
                Output('drop_anio','data'),
                Output('drop_cultivo', 'data'),
                Output('drop_variedad', 'data'),
                Output('check-recursos', 'options'),
                Output('check-recursos', 'value'),
                Output("data-values","data"),
              [Input('drop_anio','value'),
               Input('drop_cultivo','value'), 
               Input('drop_variedad','value'),
               #Input('cultivo_cell','value'),
              ])
    def update_drop_cultivo(year,cultivo,variedad):#,cultivo_cell
        df_produccion=df_costos_agricola_default.copy()
        if year==None and (cultivo==None or len(cultivo)==0) and variedad==None:
            options=df_produccion
        elif year!=None and (cultivo==None or len(cultivo)==0)and variedad==None:
            options=df_produccion[df_produccion['AÑO_CAMPAÑA']==year]
        elif year==None and (cultivo!=None or len(cultivo)>0)and variedad==None:
            options=df_produccion[df_produccion['CULTIVO'].isin(cultivo)]

        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad==None:# or len(cultivo)>0
            options=df_produccion[(df_produccion['CULTIVO'].isin(cultivo))&(df_produccion['AÑO_CAMPAÑA']==year)]

        elif year==None and (cultivo==None or len(cultivo)==0) and variedad!=None:
            options=df_produccion[df_produccion['VARIEDAD']==variedad]
        elif year!=None and (cultivo==None or len(cultivo)==0) and variedad!=None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['AÑO_CAMPAÑA']==year)]
        elif year==None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['CULTIVO'].isin(cultivo))]
        elif year!=None and (cultivo!=None or len(cultivo)>0) and variedad!=None:
            options=df_produccion[(df_produccion['VARIEDAD']==variedad)&(df_produccion['AÑO_CAMPAÑA']==year)&(df_produccion['CULTIVO'].isin(cultivo))]

        anio=[{'label': i, 'value': i} for i in options['AÑO_CAMPAÑA'].unique()]
        cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()]
        variedad=[{'label': i, 'value': i} for i in options['VARIEDAD'].unique()]
        check=[{'label': i, 'value': i} for i in options['TIPO'].unique()]
        #minimo=str(options['FECHAINICIO_CAMPAÑA'].min())#
        
        #maximo=str(options['FECHAFIN_CAMPAÑA'].max())#.str[0:10]
        
        #inicio_fin=str(minimo)+' - '+str(maximo)

        return anio,cultivo,variedad,check,options['TIPO'].unique(),options.to_json(date_format='iso', orient='split')#,inicio_fin

    @app.callback(
         Output('card-total-costos','children'),
         Output('card-total-ha','children'),
         Output('card-cultivo-costos','children'),

         Output('bar-lote-costosp','figure'),
         Output('bar-variedad-costosp','figure'),
         Output('bar-cultivo-costosp','figure'),
         Output('pie-tipo-costosp','figure'),
         Output("mapa-costosp","figure"),
        
         Input('data-values','data'),
         Input('rbtn_dinero','value'),
         Input('radio-costos','value'),#rbtn_dinero
         Input('check-recursos','value'),
    )   
    def actualizar_table_cultivo(data,radio,radio_costos,check):
        options=pd.read_json(data, orient='split')
        df_campaña_ccc=options[options['TIPO'].isin(check)]
        dff_end_pivot= df_campaña_ccc.pivot(index=('CODCULTIVO','CULTIVO','VARIEDAD','AREA_CAMPAÑA','IDCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA'),values=(radio),columns=('TIPO'))
        dff_end_pivot.reset_index()
        dff_pivot=pd.DataFrame(dff_end_pivot.to_records())
        if radio == 'SALDO_MOF':
            simbolo='S/'
        elif radio == 'SALDO_MEX':
            simbolo='$'
        """
        dff_cultivo=dff_pivot.groupby(['CODCULTIVO','CULTIVO']).sum().reset_index()
        if radio_costos == 'CH':
            columns=dff_cultivo.columns
            for recurso in columns[4:]:
                dff_cultivo[recurso]=dff_cultivo[recurso]/dff_cultivo['AREA_CAMPAÑA']
                
        dff_cultivo=dff_cultivo.drop(['CODCULTIVO','AÑO_CAMPAÑA'], axis=1)
        dff_cultivo['AREA_CAMPAÑA']=dff_cultivo['AREA_CAMPAÑA'].astype('object')

        dff_cultivo.loc[:,'TOTAL']= dff_cultivo.sum(numeric_only=True, axis=1)
        dff_cultivo['AREA_CAMPAÑA']=dff_cultivo['AREA_CAMPAÑA'].astype('float64')
        dff_cultivo=dff_cultivo.sort_values('TOTAL',ascending=False)#
        dff_cultivo.loc['TOTAL',:]= dff_cultivo.sum(numeric_only=True, axis=0)
        dff_cultivo=dff_cultivo.fillna('TOTAL')
        try:        
            dff_cultivo=dff_cultivo.drop(['CODSIEMBRA','CODCAMPAÑA'], axis=1)
        except:
            pass
        #col=[{"name": c, "id": c,"type": "numeric", "format": Format(group=",", precision=0,scheme="f")} for c in dff_cultivo]
        """
        def tabs_cvl(dff,cols,radio_costos,ejey,tickedx):
            dff_lote=dff.groupby(cols).sum().reset_index()
            dff_lote['AREA_CAMPAÑA']=dff_lote['AREA_CAMPAÑA'].astype('object')
            dff_lote.loc[:,'TOTAL']= dff_lote.sum(numeric_only=True, axis=1)
            dff_lote['AREA_CAMPAÑA']=dff_lote['AREA_CAMPAÑA'].astype('float64')

            if ejey =='Lote':
                  df_ha=dff.groupby(['CONSUMIDOR','AREA_CAMPAÑA']).sum().reset_index()
            elif ejey =='Variedad':
                  df_ha=dff.groupby(['VARIEDAD','CONSUMIDOR','AREA_CAMPAÑA']).sum().reset_index()
            elif ejey =='Cultivo':
                  df_ha=dff.groupby(['CULTIVO','CONSUMIDOR','AREA_CAMPAÑA']).sum().reset_index()
            
            if radio_costos == 'CT':
                
                dff_lote=dff_lote.sort_values('TOTAL',ascending=False)
                #x=dff_lote['NCONSUMIDOR']
                x=dff_lote[cols[0]]
                y=dff_lote['TOTAL']
                color=dff_lote['CULTIVO']
                dff_lote['PROMEDIO']=(dff_lote['TOTAL'].sum())/len(dff_lote[cols[0]].unique()) 
                title=f'Costos {simbolo}. / {ejey}'
                ejetotal='TOTAL'

            #return BarGOV_SX(dff_lote['TOTAL_y'],x,title,color,None,'Lotes',simbolo,dff_lote['PROMEDIO'],dff_lote['AREA_CAMPAÑA'])

            elif radio_costos == 'CH':

                #dff_lote['AH']=dff_lote['TOTAL']/dff_lote['AREA_CAMPAÑA']
                dff_lote['AH']=dff_lote['TOTAL']/df_ha['AREA_CAMPAÑA']
                dff_lote=dff_lote.sort_values('AH',ascending=False)
                x=dff_lote[cols[0]]
                y=dff_lote['AH']
                color=dff_lote['CULTIVO']
                dff_lote['PROMEDIO']=(dff_lote['AH'].sum())/len(dff_lote[cols[0]].unique())   
                title=f'Costos {simbolo} / Ha x {ejey}'
                ejetotal='AH'
            return BarGOV_SX(dff_lote[ejetotal],x,title,color,None,ejey,simbolo, dff_lote['PROMEDIO'],dff_lote['AREA_CAMPAÑA'],False,tickedx)       
                #scatter=dff_lote_mof['AH']
        lotes=tabs_cvl(dff_pivot,['CONSUMIDOR','CULTIVO'],radio_costos,'Lote',True)
        variedad=tabs_cvl(dff_pivot,['VARIEDAD','CULTIVO'],radio_costos,'Variedad',True)
        cultivo=tabs_cvl(dff_pivot,['CULTIVO'],radio_costos,'Cultivo',False)

        pie_tipo_gasto=df_campaña_ccc.groupby('TIPO')[[radio]].sum().reset_index()
        fig_pie = go.Figure(data=[go.Pie(labels=pie_tipo_gasto['TIPO'],#,title_text=f"Tipo Gasto",
                             values=pie_tipo_gasto[radio])])
        fig_pie.update_layout(title_text="Tipo de Costo",template='none')
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_traces(hoverinfo='label+percent+value', textfont_size=10)
                        #marker=dict(colors=colors))#line=dict(color='#000000', width=2)
        fig_pie.update_layout(height=300,margin = dict(t=30, b=50, l=10, r=10))
        fig_pie.update_layout(showlegend=False)
        fig_pie.update_layout(title_font_color="black")

        ######################
        df_loader=df_campaña_ccc.groupby(['CULTIVO'])[[radio]].sum().reset_index()
        total_card_1=df_loader[radio].sum()
        lista_cultivo=df_loader['CULTIVO'].unique()
        total_costos_dict=calculateCard(df_loader,col=radio,color=px.colors.qualitative.G10[:len(lista_cultivo)],list_partidas=lista_cultivo,pivot=False,col_='CULTIVO')
        ###########################
        df_ha=dff_pivot.groupby(['CULTIVO'])[['AREA_CAMPAÑA']].sum().reset_index()
        total_card_2=df_ha['AREA_CAMPAÑA'].sum()
        lista_cultivo_ha=df_ha['CULTIVO'].unique()
        total_ha_dict=calculateCard(df_ha,col='AREA_CAMPAÑA',color=px.colors.qualitative.G10[:len(lista_cultivo_ha)],list_partidas=lista_cultivo_ha,pivot=False,col_='CULTIVO')
        #######################################################
        costo_x_ha=total_card_1/total_card_2
        ####maps
        df_map=df_campaña_ccc[df_campaña_ccc['POLYGON'].notnull()]
        df_map_polygon=df_map.groupby(['CONSUMIDOR','POLYGON'])[['AREA_CAMPAÑA']].sum().reset_index()

        def createPolygonMap(df):
            fig = go.Figure()
            for lista_string,lote in zip(df['POLYGON'].unique(),df['CONSUMIDOR'].unique()):
                lista_coord=eval(lista_string)
                fig.add_trace(go.Scattermapbox(
                    mode="lines",
                    lon=[coord[0] for coord in lista_coord],
                    lat=[coord[1] for coord in lista_coord],
                    fill='toself',
                    fillcolor='rgba(0, 0, 100, 0.3)',
                    line=dict(color='rgba(0, 0, 100, 0.3)', width=2),
                    hovertext=lote,
                    name=lote,
                ))

                # Configurar el diseño del mapa
                fig.update_layout(
                    mapbox=dict(
                        center=dict(lon=-79.53234131,lat=-7.03284940),#,-79.53234131
                        style="carto-positron",
                        zoom=12
                    ),
                    showlegend=False
                )
                fig.update_layout(height=300,margin = dict(t=0, b=0, l=0, r=0))
            return fig


        
         
        return [
                cardGF(value_total=f"{simbolo} {round(total_card_1,0)}",text='Costos Totales',list_element=total_costos_dict),
                cardGF(value_total=f"{round(total_card_2,1)} ha",text='Hectáreas Sembradas',list_element=total_ha_dict),
                cardGF(value_total=f"{simbolo} {round(costo_x_ha,1)}",text='Costo por Hectárea',list_element=[{'value': 100, 'color': "rgb(51, 102, 204)", 'label': '100%', "tooltip": "Costo por Hectárea"}]),
                lotes,
                variedad,
                cultivo,
                fig_pie,
                createPolygonMap(df_map_polygon)
            ]