#from pydoc import classname
from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from apps.graph.data.data import *
                               
from apps.graph.build.components.mantine_react_components.loaders import loadingOverlay

def table_dash(df):
    return dash_table.DataTable(
                    id='table-gastos',
                    columns=[{"name": c, "id": c,"type": "numeric", "format": Format(group=",", precision=2,scheme="f")} for c in df],# "type": "numeric", "format": Format(group=",", precision=2,scheme="f")
                    #active_cell={},
                    style_table={'overflowY': 'auto','height': '380px'},
                    #style_table={'minWidth': '100%'},
                    #sort_action="native",
                    data=df.to_dict('records'),
                    sort_action="native",
                    fixed_rows = {'headers': True},
                    style_cell={
                                            'width': '80px',
                                            'minWidth': '80px',
                                            'maxWidth': '350px',
                                            'overflow': 'hidden',
                                            'textOverflow': 'ellipsis',
                                            'text_align': 'left',
                                            'font-family': 'sans-serif',
                                            'font-size': '14px',
                                        },
                    style_header={
                                            'backgroundColor': 'white',
                                            'fontWeight': 'bold',
                                            'text-align': 'left',
                                            'font-family': 'sans-serif',
                                            'font-size': '14px',
                                        },
                    
                    
    ),

def cargasdePersonalFinanzas(empresa):
    
    df=dataBcEmpresa(empresa)

    app = DjangoDash('cargas_personal', external_stylesheets=[dbc.themes.BOOTSTRAP])#

    app.layout = html.Div([
                        dbc.Row([
                                dbc.Col([
                                    html.H3('CARGAS DE PERSONAL', style={'margin-bottom': '0px', 'color': 'black'}),#id='title''textAlign': 'center'
                                    #html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                                    
                                    ],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='years',
                                            multi=False,
                                            searchable= True,
                                            placeholder= '',
                                            options=[],
                                            style={
                                                
                                                'font-size': "90%",
                                                #'min-height': '2px',
                                                },
                                            )    

                                    ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                                    dbc.Col([
                                        dcc.RadioItems( 
                                        id='moneda',
                                        options=[
                                            {'label': 'S/', 'value': 'saldo_cargo_mof'},
                                            {'label': '$', 'value': 'saldo_cargo_mex'},
                                            
                                        ],
                                        value='saldo_cargo_mex',
                                        #labelStyle={'display': 'inline-block'}
                                    ) 

                                    ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                            ]),
                    #rowGraphs.colsTwoGraphandTable(7,5,'graph1','graph2',table,'table-cell')
                    
                    dbc.Row([
                        
                        dbc.Col([

                            #dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm")
                            loadingOverlay(html.Div(html.Div(id='table')),html.Div(id='table-cell'))
                            
                            #dbc.Row([
                            #    html.Div(html.Div(id='table')),html.Div(id='table-cell')
                            #]),
                        ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")

                    ]),
                    dbc.Row([
                        dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm"))
                                
                        ],width=7,className="col-xl-7 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm"))
                            
                        ],width=5,className="col-xl-5 col-md-12 col-sm-12 col-12 mb-3"),
                    ]),
            ])
    #structuraFinanzas.dashCargasdePersonal(html.Div(id='table',style={"maxHeight": "1000px", "overflow": "scroll",'font_family': 'cursive',
    #            'font_size': '10px',}))
    @app.callback(
            Output("years","options"),
            #Output("drop_cultivo","options"),
            Input("years","value"),
            
        )
    def dropyear(year):
        if year==None:
            df_bcomprobacion=df
        else:
            df_bcomprobacion=df[df['year']==year]

        option_year=[{'label': i, 'value': i} for i in sorted(df_bcomprobacion['year'].unique())]
        return option_year
    
    @app.callback(
            Output("graph1","figure"),
            Output("graph2","figure"),
            #Output("graph3","figure"),
            Output("table","children"),
            #Output("drop_cultivo","options"),
            Input("years","value"),
            Input("moneda","value"),
            
        )
    def output_dash(year,moneda):
        
        if year==None:
            df_bcomprobacion=df
        else:
            df_bcomprobacion=df[df['year']==year]
        #TABLE
        df_cargas_personal=df_bcomprobacion[df_bcomprobacion['grupo_naturaleza']=='Cargas de Personal']
        df_cargas_personal=df_cargas_personal.fillna(0)
        df_cargas_personal_mes= df_cargas_personal.pivot_table(index='descripcion',values=moneda,columns='Mes').reset_index()
        df_cargas_personal_mes=df_cargas_personal_mes.fillna(0)
        df_cargas_personal_mes.loc[:,'TOTAL']=df_cargas_personal_mes.sum(numeric_only=True, axis=1)
        df_cargas_personal_mes.loc['TOTAL',:]=df_cargas_personal_mes.sum(numeric_only=True, axis=0)
        df_cargas_personal_mes['descripcion']=df_cargas_personal_mes['descripcion'].fillna('TOTAL')
        #table=dbc.Table.from_dataframe(df_cargas_personal_mes, bordered=True)
        try:
            df_cargas_personal_mes=df_cargas_personal_mes[['descripcion','Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre','TOTAL']]
        except:
            df_cargas_personal_mes=df_cargas_personal_mes

        df_cargas_personal_anual=df_cargas_personal.groupby(['year'])[[moneda]].sum().reset_index()
        cp_anual = go.Figure([go.Bar(x=df_cargas_personal_anual['year'], y=df_cargas_personal_anual[moneda],text=df_cargas_personal_anual[moneda])])
        cp_anual.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        cp_anual.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',title_text="Carga de Personal Anual",template='none',margin=dict(t=35,b=85,r=10),height=400)
        df_descripcion=df_cargas_personal.groupby(['descripcion'])[[moneda]].sum().sort_values(moneda,ascending=True).reset_index()
        #fig = px.bar(df_descripcion, x=moneda, y="descripcion",title="Top de Cargas de Personal")#,height=700
        fig = go.Figure([go.Bar(x=df_descripcion[moneda], y=df_descripcion['descripcion'],orientation='h',)])
        fig.update_layout(margin=dict(t=35,b=35,l=250),height=400,xaxis_title='Importe',yaxis_title='Partidas',template='none',title_text='Top de Cargas de Personal')
        table=table_dash(df_cargas_personal_mes)
        #print(df_cargas_personal_mes)
        return cp_anual,fig,table

def estadodeResultadosFinanzas(empresa):
    df=dataBcEmpresa(empresa)                             
    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )
    app = DjangoDash('estado_resultados', external_stylesheets=[dbc.icons.BOOTSTRAP, dbc_css])#

    app.layout = html.Div([
                        dbc.Row([
                                dbc.Col([
                                    html.H3('ESTADO DE RESULTADOS', style={'margin-bottom': '0px', 'color': 'black'}),#id='title''textAlign': 'center'
                                    #html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                                    
                                    ],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='years',
                                            multi=False,
                                            searchable= True,
                                            placeholder= '',
                                            options=[],
                                            style={
                                                
                                                'font-size': "90%",
                                                #'min-height': '2px',
                                                },
                                            )    

                                    ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                                    dbc.Col([
                                        dcc.RadioItems( 
                                        id='moneda',
                                        options=[
                                            {'label': 'S/', 'value': 'saldo_cargo_mof'},
                                            {'label': '$', 'value': 'saldo_cargo_mex'},
                                            
                                        ],
                                        value='saldo_cargo_mex',
                                        #labelStyle={'display': 'inline-block'}
                                    ) 

                                    ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                            ]),
                    #rowGraphs.colsTwoGraphandTable2(6,6,'graph1','graph2','graph3',table),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([html.Div(html.Div(id='table')),],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                            ]),
                            dbc.Row([
                                dbc.Col([dbc.Card(dcc.Graph(id='graph3'),className="shadow-sm")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                            ]),
                            
                        ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([
                            dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm")
                        ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")
                        ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                    ]),
            ])
    #structuraFinanzas.dashEstadodeResultados(
        #html.Div(id='table',style={"maxHeight": "1000px", "overflow": "scroll",'font_family': 'cursive',
        #        'font_size': '10px',}))

                
    @app.callback(
            Output("years","options"),
            #Output("drop_cultivo","options"),
            Input("years","value"),
            
        )
    def dropyear(year):
        if year==None:
            df_bcomprobacion=df
        else:
            df_bcomprobacion=df[df['year']==year]

        option_year=[{'label': i, 'value': i} for i in sorted(df_bcomprobacion['year'].unique())]
        return option_year
    
    @app.callback(
            Output("graph1","figure"),
            Output("graph2","figure"),
            Output("graph3","figure"),
            Output("table","children"),
            #Output("drop_cultivo","options"),
            Input("years","value"),
            Input("moneda","value"),
            
        )
    def output_dash(year,moneda):
        df_bcomprobacion_123=balancePivotRename(moneda,df)#dfCompuesto(moneda)
        df_bc_uti_pivot=createBc_uti(moneda,df)
        if year==None:
            df_bcomprobacion=df
            df_bc_uti=df_bc_uti_pivot
            df_grupo1=df_bcomprobacion_123
        else:
            df_bcomprobacion=df[df['year']==year]
            df_bc_uti=df_bc_uti_pivot[df_bc_uti_pivot['year']==year]
            df_grupo1=df_bcomprobacion_123[df_bcomprobacion_123['year']==year]

        df_gf_year=df_bcomprobacion.groupby(['grupo_funcion','year'])[[moneda]].sum().reset_index()
        #graph1
        df_ingresosvscostos=df_gf_year[df_gf_year['grupo_funcion'].isin(['VENTAS','COSTO DE VENTAS'])]
        ingresos_costos = px.bar(df_ingresosvscostos, x="year", y=moneda,
             color='grupo_funcion', barmode='group',text=moneda,
             height=400,width=1000)
        ingresos_costos.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        ingresos_costos.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        #graph2
        df_year_grupo_funcion=df_gf_year.groupby(['year'])[[moneda]].sum().reset_index()
        total_grupo_funcion = go.Figure([go.Bar(x=df_year_grupo_funcion['year'], y=df_year_grupo_funcion[moneda],text=df_year_grupo_funcion[moneda])])
        total_grupo_funcion.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        total_grupo_funcion.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        #graph3
        df_bc=df_bc_uti.merge(df_grupo1,how='inner',left_on='al_periodo',right_on='al_periodo')
        df_bc['CAPITAL EMPLEADO']=df_bc['ACTIVO']-df_bc['PASIVO CORRIENTE']
        df_bc['ROCE']=(df_bc['EBIT']/df_bc['CAPITAL EMPLEADO'])*100
        df_bc['ROA']=(df_bc['UTILIDAD NETA']/df_bc['ACTIVO'])*100
        df_bc['ROE']=(df_bc['UTILIDAD NETA']/df_bc['PATRIMONIO'])*100
        df_roes=df_bc.groupby(['year_x'])[['ROA','ROCE','ROE']].sum().reset_index()
        fig = go.Figure(data=[
            go.Bar(name='ROA', x=df_roes['year_x'], y=df_roes['ROA']),
            go.Bar(name='ROCE', x=df_roes['year_x'], y=df_roes['ROCE']),
            go.Bar(name='ROE', x=df_roes['year_x'], y=df_roes['ROE'])
        ])
        # Change the bar mode
        fig.update_layout(barmode='group',template='none')
        table=table_dash(df_roes)
        #table=dbc.Table.from_dataframe(df_roes, bordered=True)

        return ingresos_costos,total_grupo_funcion,fig,table

def treemap(df,moneda):
    fig = px.treemap(df,
    path = [px.Constant(""),'grupo1'],
    values = moneda,template='none'
    )
    fig.update_traces(root_color="aliceblue")
    fig.update_layout(uniformtext=dict(minsize=14, mode='hide'),margin = dict(t=0, l=0, r=0, b=0),)#
    return fig
def pie_chart_2(df,moneda):
    fig2 = px.pie(df, values=moneda, names='grupo1',template="none",
             title='',hole=.6
             #hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'}
             )
    fig2.update_traces(textposition='inside', textinfo='percent+label')

    #fig2.update_layout(height=330,margin=dict(l=60,r=40,b=20,t=50))#,legend=dict(y=-0.7,xanchor="center",x=0.5)
    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    ))
    fig2.update_traces(textposition='outside', textinfo='percent+label',textfont_size=14)
    return fig2

def estadodeSituacionFinanzas(empresa):
    df=dataBcEmpresa(empresa)
                                
    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )
    app = DjangoDash('estado_situacion', external_stylesheets=[dbc.icons.BOOTSTRAP, dbc_css])#

    app.layout = html.Div([
                        dbc.Row([
                                dbc.Col([
                                    html.H3('ESTADO DE SITUACION', style={'margin-bottom': '0px', 'color': 'black'}),#id='title''textAlign': 'center'
                                    #html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                                    
                                    ],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='years',
                                            multi=False,
                                            searchable= True,
                                            placeholder= '',
                                            options=[],
                                            style={
                                                
                                                'font-size': "90%",
                                                #'min-height': '2px',
                                                },
                                            )    

                                    ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                                    dbc.Col([
                                        dcc.RadioItems( 
                                        id='moneda',
                                        options=[
                                            {'label': 'S/', 'value': 'saldo_cargo_mof'},
                                            {'label': '$', 'value': 'saldo_cargo_mex'},
                                            
                                        ],
                                        value='saldo_cargo_mex',
                                        #labelStyle={'display': 'inline-block'}
                                    ) 

                                    ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                            ]),
                    #rowGraphs.colsTwoGraphandTable(7,5,'graph1','graph2',table,'table-cell')
                    
                    
                    dbc.Row([
                        dbc.Col([html.Div(html.Div(id='table')),html.Div(id='table-cell')],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                        
                    ]),
                    dbc.Row([
                        dbc.Col([dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm")],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                    ]),
    ])
    @app.callback(
            Output("years","options"),
            #Output("drop_cultivo","options"),
            Input("years","value"),
            
        )
    def dropyear(year):
        if year==None:
            df_bcomprobacion=df
        else:
            df_bcomprobacion=df[df['year']==year]

        option_year=[{'label': i, 'value': i} for i in sorted(df_bcomprobacion['year'].unique())]
        return option_year
    
    @app.callback(
            Output("graph1","figure"),
            Output("graph2","figure"),
            #Output("graph3","figure"),
            Output("table","children"),
            #Output("drop_cultivo","options"),
            Input("years","value"),
            Input("moneda","value"),
            
        )
    def output_dash(year,moneda):
        if year==None:
            df_bcomprobacion=df[df['year']==sorted(df['year'].unique())[-1]]
        else:
            df_bcomprobacion=df[df['year'].isin([str(year),str(year-1)])]
        #TABLE
        df_bcomprobacion_year=df_bcomprobacion.groupby(['grupo1','grupo2','grupo3','year'])[[moneda]].sum().sort_values('year',ascending=False).reset_index()
        last_years=sorted(df_bcomprobacion_year['year'].unique(), reverse=True)[:2]

        df_bcomprobacion_year_pivot=df_bcomprobacion_year.pivot_table(index=('grupo1','grupo2','grupo3'),values=moneda,columns='year')
        df_bcomprobacion_year_pivot.reset_index()
        df_bcomprobacion_year_pivot=pd.DataFrame(df_bcomprobacion_year_pivot.to_records())
        df_bcomprobacion_year_pivot2=df_bcomprobacion_year_pivot[['grupo1','grupo2','grupo3']+last_years]#
        df_bcomprobacion_year_pivot2=df_bcomprobacion_year_pivot2.rename(columns={last_years[0]:'AÑO ACTUAL',last_years[1]:'AÑO ANTERIOR'})
        df_bcomprobacion_year_pivot2['VAR_ESF']=df_bcomprobacion_year_pivot2['AÑO ACTUAL']-df_bcomprobacion_year_pivot2['AÑO ANTERIOR']

        #TREEMAP AND PIE
        df_bc_group1=df_bcomprobacion.groupby(['grupo1'])[[moneda]].sum().reset_index()
        treechart=treemap(df_bc_group1,moneda)
        pie= pie_chart_2(df_bc_group1,moneda)
        table=table_dash(df_bcomprobacion_year_pivot2)
        #table=dbc.Table.from_dataframe(df_bcomprobacion_year_pivot2, bordered=True)
        return treechart,pie,table

def pie_chart(df,moneda):
    fig5 = px.pie(df, values=moneda, names='grupo_funcion',template="none",
             title='',hole=.6
             #hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'}
             )
    fig5.update_traces(textposition='inside', textinfo='percent+label',textfont_size=10)

    #fig2.update_layout(height=330,margin=dict(l=60,r=40,b=20,t=50))#,legend=dict(y=-0.7,xanchor="center",x=0.5)
    fig5.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5,
        #title_font_family="Times New Roman",
        font=dict(
            #family="Courier",
            size=8,
            color="black"
        ),
    ))
    fig5.update_traces(textposition='outside', textinfo='percent+label',textfont_size=10)
    fig5.update_layout(margin = dict(t=0, b=60, l=10, r=10),height=300)
    return fig5

def line_chart(df,moneda):
    fig6 = px.line(df, x="Mes", y=moneda, color='grupo_funcion',template="none",title='')
    fig6.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5,
       #title_font_family="Times New Roman",
        font=dict(
            #family="Courier",
            size=8,
            color="black"
        ),
    ))
    fig6.update_layout(
        
        xaxis_title='',
        yaxis_title='',
        legend_title='',
        
    )
    fig6.update_layout(margin = dict(t=0, b=30, l=40, r=30),height=300)
    return fig6

def bar_ori(df,moneda):
    fig8 = px.bar(df, x=moneda, y="year", 
                 color="grupo_funcion", barmode="group",orientation='h',template='none',text=moneda,title='')
    fig8.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5,
        #title_font_family="Times New Roman",
        font=dict(
        #    family="Courier",
            size=8,
            color="black"
        ),
    ))
    fig8.update_layout(
        
        xaxis_title='',
        yaxis_title='',
        legend_title="",
        
        )
    fig8.update_traces(textposition='outside')
    fig8.update_layout(margin = dict(t=0, b=60, l=40, r=30),height=350)
    return fig8

def GraphwithHeader(idd,title):
    #df = get_data()
    
    return dbc.Card([
        dbc.CardHeader(html.H6(title, style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),style={"background": "white"}),
        dbc.CardBody([
        dcc.Graph(id=idd)#,style={"maxHeight": "800px", "overflow": "scroll",'font_family': 'cursive','font_size': '10px'}
        ])
        #dcc.Graph(id=idd),className="shadow-sm")
        ], color="light", outline=True,className='shadow-sm')


def gastosOperativosFinanzas(empresa):
    
    df = dataBcEmpresa(empresa)
    
    
    app = DjangoDash('gastos_operativos', external_stylesheets=[dbc.themes.BOOTSTRAP])#url_theme1, dbc.icons.BOOTSTRAP, dbc_css,

    app.layout = html.Div([#
                dbc.Row([
                        
                            dbc.Col([
                                html.H3('GASTOS OPERATIVOS',className=" py-3 text-5xl font-bold text-gray-800"),#id='title''textAlign': 'center'# style={'margin-bottom': '0px', 'color': 'black'},
                                #html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                                
                            ],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-1"),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='years',
                                    multi=False,
                                    searchable= True,
                                    placeholder= '',
                                    options=[],
                                    style={
                                        
                                        'font-size': "90%",
                                        #'min-height': '2px',
                                        },
                                    )    

                            ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-1"),
                            dbc.Col([
                                dcc.RadioItems( 
                                id='moneda',
                                options=[
                                    {'label': 'S/', 'value': 'saldo_cargo_mof'},
                                    {'label': '$', 'value': 'saldo_cargo_mex'},
                                    
                                ],
                                value='saldo_cargo_mex',
                            ) 

                            ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-1"),
                        ]),
        dcc.Loading(children=dbc.Row([
                    dbc.Col([GraphwithHeader('graph1','Composición de Gastos Operativos')],width=5,className="col-xl-5 col-md-12 col-sm-12 col-12 mb-1"),
                    dbc.Col([GraphwithHeader('graph2','Composición Mensual de Gastos Operativos')],width=7,className="col-xl-7 col-md-12 col-sm-12 col-12 mb-1"),
                    #dbc.Col([GraphwithHeader('graph3','Comparación de Gastos Anual')],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                ])),
                #rowGraphs.colsGraphThree('graph1','graph2','graph3'),
        dcc.Loading(children=dbc.Row([
                    dbc.Col([html.Div(
                        #html.Div(id='table-gastos'),
                        dash_table.DataTable(
                                    id='table-gastos',
                                    
                                    #active_cell={},
                                    style_table={'overflowY': 'auto','height': '380px'},
                                    active_cell={"row": 0, "column": 0, "column_id": 0, "row_id": 0},
                                    #style_table={'minWidth': '100%'},
                                    #sort_action="native",
                                    #data=df.to_dict('records'),
                                    sort_action="native",
                                    fixed_rows = {'headers': True},
                                    style_cell={
                                                            'width': '80px',
                                                            'minWidth': '80px',
                                                            'maxWidth': '350px',
                                                            'overflow': 'hidden',
                                                            'textOverflow': 'ellipsis',
                                                            'text_align': 'left',
                                                            'font-family': 'sans-serif',
                                                            'font-size': '14px',
                                                        },
                                    style_header={
                                                            'backgroundColor': 'white',
                                                            'fontWeight': 'bold',
                                                            'text-align': 'left',
                                                            'font-family': 'sans-serif',
                                                            'font-size': '14px',
                                                        },
                                    
                                    
                        ),
                    )],width=7,className="col-xl-7 col-md-12 col-sm-12 col-12 mb-1"),#,style={"maxHeight": "1000px", "overflow": "scroll",'font_family': 'cursive','font_size': '10px',}
                    dbc.Col([GraphwithHeader('graph3','Comparación de Gastos Anual')],width=5,className="col-xl-5 col-md-12 col-sm-12 col-12 mb-3")
                    ]))
                    
            ])
            

    @app.callback(
                Output("years","options"),
                #Output("drop_cultivo","options"),
                Input("years","value"),
                
            )
    def dropyear(year):
            if year==None:
                df_bcomprobacion=df
            else:
                df_bcomprobacion=df[df['year']==year]

            option_year=[{'label': i, 'value': i} for i in sorted(df_bcomprobacion['year'].unique())]
            return option_year
        
    @app.callback(
                Output("graph1","figure"),
                Output("graph2","figure"),
                Output("graph3","figure"),
                Output("table-gastos","data"),
                Output("table-gastos","columns"),
                #Output("table-gastos","columns"),
                #Output("table-gastos","columns"),
                #Output("drop_cultivo","options"),
                Input("years","value"),
                Input("moneda","value"),
                
            )
    def filtrar_agricola2(year,moneda):
            if year==None:
                df_bcomprobacion=df
            else:
                df_bcomprobacion=df[df['year']==year]
            #pie_chart
            df_gastos=df_bcomprobacion[df_bcomprobacion['grupo_funcion'].isin(['GASTOS FINANCIEROS, NETO','GASTOS DE ADMINISTRACION','GASTOS DE VENTA'])]#,'GASTOS - CONTRATO DE COLABORACION'
            df_gastos_operativos=df_gastos.groupby(['grupo_funcion','year','Mes','month','descripcion'])[[moneda]].sum().reset_index()
            df_gastos_operativos_total=df_gastos_operativos.groupby(['grupo_funcion'])[[moneda]].sum().round(2).reset_index()
            #line_chart
            df_go_month=df_gastos_operativos.groupby(['grupo_funcion','Mes','month'])[[moneda]].sum().round(2).sort_values('month',ascending=True).reset_index()
            #bar_chart
            df_go_year=df_gastos_operativos.groupby(['grupo_funcion','year'])[[moneda]].sum().round(2).reset_index()
            #table
            df_go_descripcion=df_gastos_operativos.groupby(['descripcion','month','Mes'])[[moneda]].sum().sort_values('month',ascending=True).reset_index()
            df_descripcion_mes=df_go_descripcion.pivot_table(index=('descripcion'),values=moneda,columns='Mes')
            df_descripcion_mes.reset_index()
            df_descripcion_mes=pd.DataFrame(df_descripcion_mes.to_records())
            df_descripcion_mes=df_descripcion_mes.rename(columns={'descripcion':'Gastos_Operativos'})
        
            df_descripcion_mes=df_descripcion_mes.fillna(0)
            df_descripcion_mes.loc[:,'TOTAL']= df_descripcion_mes.sum(numeric_only=True, axis=1)
            df_descripcion_mes.loc['TOTAL',:]= df_descripcion_mes.sum(numeric_only=True, axis=0)
            df_descripcion_mes=df_descripcion_mes.fillna('TOTAL').round(2)
            try:
                df_descripcion_mes=df_descripcion_mes[['Gastos_Operativos','Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre','TOTAL']]
            except:
                df_descripcion_mes=df_descripcion_mes
            print(df_descripcion_mes)
            pie=pie_chart(df_gastos_operativos_total,moneda)
            line= line_chart(df_go_month,moneda)
            bar=bar_ori(df_go_year,moneda)
            col=[{"name": c, "id": c,"type": "numeric" }for c in df_descripcion_mes]
            #tabla=table_dash(df_descripcion_mes)
            return pie,line,bar,df_descripcion_mes.to_dict('rows'),col