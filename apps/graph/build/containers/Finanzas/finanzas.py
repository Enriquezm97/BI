from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
import pandas as pd
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
from apps.graph.build.components.draw.table import createTableDMC,tableSimpleDMC
from apps.graph.data.features.build_features import getApi,DataFinanzas
from apps.graph.build.components.mantine_react_components.actionIcon import btnCollapse
from apps.graph.build.components.mantine_react_components.selects import select
from apps.graph.build.components.mantine_react_components.loaders import loadingOverlay
from apps.graph.build.components.draw.treemap import treemapEstadoSituacion
from apps.graph.build.components.tables.table import table_dash,table_dash_gp,tableAgGrid
from apps.graph.build.components.draw.bar import barCharTrace
from apps.graph.build.components.draw.line import linesChartTrace
from apps.graph.build.components.draw.card import cardGF
import dash_ag_grid as dag
from apps.graph.build.components.bootstrap_components.layout import Column
from apps.graph.build.components.mantine_react_components.cards import cardGraph,cardTableDag,cardShowTotal,actionIcon,button_style
def bar_gp(dataframe,x='',y='',size=300,left=40):
     figure=px.bar(dataframe, x=x, y=y,title=f'<b>{y}</b>',color_discrete_sequence=['rgb(29, 105, 150)'],text=y)
     figure.update_traces(hovertemplate=
                           '<br><b>Periodo</b>:%{x}'+
                           '<br><b>Importe</b>: %{y:$,.2f}'#+
                           #'<br><b>Porcentaje</b>:%{customdata[0]}'
                           )
     figure.update_layout(margin = dict(t=50, b=40, r=10,l=left),height=size,template='none')# l=200
     figure.update_layout(
            title=dict(font=dict(size=11)),
            hoverlabel=dict(
                bgcolor="white",
                font_size=15,
            ),
            yaxis_title="",
            xaxis_title="",
            yaxis=dict(
            showgrid=True,
            tickfont=dict(size=9)#family='Arial',color='black',
            ),
            
        ),
     figure.update_xaxes(type='category')
     figure.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
     #figure.update_yaxes(showline=True, linewidth=2, linecolor='black')#, gridcolor='Red'
     
     
     return figure

def bar_es(dataframe,x='',y='',size=250,left=100):
     figure=px.bar(dataframe, x=x, y=y, orientation='h',title=f'<b>{y}</b>',hover_data=["%"],color_discrete_sequence=['rgb(29, 105, 150)'])
     figure.update_traces(hovertemplate=
                           '<br><b>Partida</b>:%{y}'+
                           '<br><b>Importe</b>: %{x:$,.2f}'#+
                           #'<br><b>Porcentaje</b>:%{customdata[0]}'
                           )
     figure.update_layout(margin = dict(t=50, b=30, r=10,l=left),height=size,template='none')# l=200
     figure.update_layout(
            title=dict(font=dict(size=11)),
            #title=dict(text="GDP-per-capita", font=dict(size=50), automargin=True, yref='paper'),
            hoverlabel=dict(
                bgcolor="white",
                font_size=17,
                #font_family="Rockwell"
            ),
            yaxis_title="",
            #xaxis=dict(showticklabels=False),
            yaxis=dict(
            #showticklabels=True,
            #gridcolor='#F2F2F2',
            #showline=True,
            showgrid=True,
            #ticks='outside',
            tickfont=dict(size=11)#family='Arial',color='black',
            ),
            
        ),
     figure.update_xaxes(showline=True, linewidth=2, linecolor='black')
     #figure.update_yaxes(showline=True, linewidth=2, linecolor='black')#, gridcolor='Red'
     
     
     return figure
df_23 = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)

# grouped column example
# If you want the columns to be grouped, you can include them as children like so:
columnDefs = [  
    {
        "headerName": "Clasificación",
        "children": [{"field": "Partidas"}, {"field": "Mes Seleccionado"}, {"field": "Diferencia"}],
    }
]



#TOKEN='0Q10D10N10D10O10Z1lpu0N10O10H10Q10D10N10D10O10Z1mkidfgsgk0Q10D10N10D10O10Z1lpu0Q10d10n10d10o10z1lpu0Q1ert45g0d10o123d45gqwsmkiqwsqwspoi0I1asd0o10A1lpumkimkiertlpuertsdfasdasdlpuertbhgnjhsdfqwsasdnjhdfgdfgrtgertrtgqws'
#API='http://69.64.92.160:3005/api/consulta/nsp_eeff_json'
#finanzas=getApi(API,TOKEN)
data_finanzas=pd.read_parquet('finanzas.parquet', engine='pyarrow')

all_partidas=list(data_finanzas['grupo1'].dropna().unique())+list(data_finanzas['grupo2'].dropna().unique())+list(data_finanzas['grupo3'].dropna().unique())+list(data_finanzas['grupo_funcion'].dropna().unique())
all_periodo=data_finanzas['al_periodo'].unique()
all_year=data_finanzas['Año'].unique()
data_finanzas['month']=data_finanzas['month'].astype("int")

external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP,dbc.icons.FONT_AWESOME]
#data_finanzas#=df_finanzas.copy()

def dashEstadoSituacion():
    #createTrimestre(df)
    all_partidas=list(data_finanzas['grupo1'].dropna().unique())+list(data_finanzas['grupo2'].dropna().unique())+list(data_finanzas['grupo3'].dropna().unique())+list(data_finanzas['grupo_funcion'].dropna().unique())
    all_periodo=data_finanzas['al_periodo'].unique()
    all_year=data_finanzas['Año'].unique()
    app = DjangoDash('estado_situacion', external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        dbc.Row([
            Column(
                content=[
                 #btnCollapse() 
            ],size=1), 
            Column(
                content=[
                  dmc.Title("Estado de Situción Financiera", align="center",order=3,color="black"),
                dmc.Title(id='subtitle-periodo', align="center",order=4,color="black"),
                dmc.Title(id='subtitle-moneda', align="center",order=6,color="black"),
            ],size=7), 
            Column(
                content=[
                  select('periodo-input',texto='Periodos',place="",value=all_periodo[-1],data=[{'label': i, 'value': i} for i in all_periodo]),
            ],size=2), 
            Column(
                content=[
                  select('tipo-moneda',texto='Moneda',place="",data=[{"value": "soles", "label": "PEN"},{"value": "dolares", "label": "USD"},],value='dolares'),
            ],size=2), 

        ]),
        
            dbc.Row([
                Column(
                    content=[
                        
                    loadingOverlay(cardGraph(id_graph='figure-treemap-sf',id_maximize='btn-modal'))
                ],size=12), 
                
            ]),
            #dbc.Collapse(
            dbc.Row([
                Column(
                    content=[
                        html.Div(id='card-estado-situacion-financiera'),
                ],size=12), 
                
                
            ]),
        #id="collapse",is_open=True),
        
    ])
    #@app.callback(
    #    Output("collapse", "is_open"),
    #    [Input("btn-collapse", "n_clicks")],
     #   [State("collapse", "is_open")],
     #   )
    #def toggle_collapse(n, is_open):
    #    if n:
    #        return not is_open
    #    return is_open
    
    @app.callback(
        Output("subtitle-periodo", "children"),
        Output("subtitle-moneda", "children"),
        [
         Input("periodo-input", "value"),
         Input("tipo-moneda", "value")
        ],

        )
    def update_subtitles(periodo, moneda):
        df=data_finanzas[data_finanzas['al_periodo']==periodo]
        moth_text=df['Mes'].unique()[0]
        year=df['Año'].unique()[0]
        text_subtitle_periodo=f'{moth_text} del {year}'
        text_subtitle_moneda=f'Expresado en {moneda}'
        return text_subtitle_periodo,text_subtitle_moneda


    @app.callback(
        Output("card-estado-situacion-financiera", "children"),
        Output("figure-treemap-sf", "figure"),
        [
         Input("periodo-input", "value"),
         Input("tipo-moneda", "value")
        ],

        )
    def update_situacion_financiera(periodo,moneda):
        if moneda == 'soles':
            value_moneda='saldo_cargo_mof'
        elif moneda == 'dolares':
            value_moneda='saldo_cargo_mex'    
        df=data_finanzas[data_finanzas['al_periodo']==periodo]
        df_bc=df.groupby(['grupo1','grupo2','grupo3'])[[value_moneda]].sum().reset_index()
        #totales filtrados
        total_activo="{:,.2f}".format(df_bc[df_bc['grupo1']=='ACTIVO'][value_moneda].sum())
        total_pasivo=df_bc[df_bc['grupo1']=='PASIVO'][value_moneda].sum()
        total_patrimonio=df_bc[df_bc['grupo1']=='PATRIMONIO'][value_moneda].sum()
        total_pasivo_patri="{:,.2f}".format(total_pasivo+total_patrimonio)


        df_activo_corriente=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='ACTIVO',importe=value_moneda,partida_grupo_2='ACTIVO CORRIENTE',label_total='Total Activo Corriente')
        df_activo_no_corriente=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='ACTIVO',importe=value_moneda,partida_grupo_2='ACTIVO NO CORRIENTE',label_total='Total Activo no Corriente')
        df_pasivo_corriente=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='PASIVO',importe=value_moneda,partida_grupo_2='PASIVO CORRIENTE',label_total='Total Pasivo Corriente')
        df_pasivo_no_corriente=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='PASIVO',importe=value_moneda,partida_grupo_2='PASIVO NO CORRIENTE',label_total='Total Pasivo no Corriente')
        df_patrimonio=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='PATRIMONIO',importe=value_moneda,partida_grupo_2='PATRIMONIO',label_total='Total Patrimonio')

        card_estado_situacion=html.Div([
                                    dmc.Card(
                                                    children=[
                                                        dbc.Row([
                                                            dbc.Col([
                                                                dmc.Text("ACTIVO", size="lg", weight=700,align="center"),
                                                                #dmc.Text("ACTIVO CORRIENTE", size="sm"),html.Div(),html.Div(),
                                                                table_dash(df_activo_corriente),
                                                                table_dash(df_activo_no_corriente),
                                                                dmc.Space(h=20),
                                                                dmc.Grid(
                                                                            children=[
                                                                                dmc.Col(dmc.Text("TOTAL ACTIVO", size="lg", weight=700), span=4),
                                                                                dmc.Col(html.Div(""), span=5),
                                                                                dmc.Col(dmc.Text(children=[total_activo], size="lg", weight=700), span=3),
                                                                            ],
                                                                            gutter="xl",
                                                                        ),
                                                                
                                                            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                                                            dbc.Col([
                                                                dmc.Text("PASIVO", size="lg", weight=700,align="center"),
                                                                table_dash(df_pasivo_corriente),
                                                                table_dash(df_pasivo_no_corriente),
                                                                table_dash(df_patrimonio),
                                                                dmc.Grid(
                                                                            children=[
                                                                                dmc.Col(dmc.Text("TOTAL PASIVO y PATRIMONIO", size="lg", weight=700), span=4),
                                                                                dmc.Col(html.Div(""), span=5),
                                                                                dmc.Col(dmc.Text(children=[total_pasivo_patri], size="lg", weight=700), span=3),
                                                                            ],
                                                                            gutter="xl",
                                                                        ),
                                                                
                                                            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                                                        ]),
                                                    ],
                                                    withBorder=True,
                                                    shadow="sm",
                                                    radius="md",
                                                    
                                                )
                                ])
        treemap_graph=treemapEstadoSituacion(df_bc,moneda=value_moneda,titulo='Partidas Financieras Treemap',list_path=['grupo1', 'grupo2', 'grupo3'])
        return card_estado_situacion,treemap_graph
    
def dashEstadoGananciasPerdidas():
    
    app = DjangoDash('estado_gp', external_stylesheets=external_stylesheets)
    
    app.layout = html.Div([
        dbc.Row([
            Column(content=[
                dmc.Title("Estado de Ganancias y Pérdidas por Función", align="center",order=3,color="black"),
                dmc.Title(id='subtitle-periodo', align="center",order=4,color="black"),
                dmc.Title(id='subtitle-moneda', align="center",order=6,color="black"),
            ],size=7),
            Column(content=[
                 select('periodo-input',texto='Periodos',place="",value=all_periodo[-1],data=[{'label': i, 'value': i} for i in all_periodo]),
            ],size=2),
            Column(content=[
                 select('tipo-moneda',texto='Moneda',place="",data=[{"value": "soles", "label": "PEN"},{"value": "dolares", "label": "USD"},],value='dolares'),
            ],size=2),
            
        ]),
        
        
        dbc.Row([
                Column(
                    content=[
                        
                    loadingOverlay(cardGraph(id_graph='graph-1',id_maximize='btn-modal-1'))
                ],size=4), 
                Column(
                    content=[
                        
                    loadingOverlay(cardGraph(id_graph='graph-2',id_maximize='btn-modal-2'))
                ],size=4), 
                Column(
                    content=[
                        
                    loadingOverlay(cardGraph(id_graph='graph-3',id_maximize='btn-modal-3'))
                ],size=4), 
                
            ]),
            dbc.Row([
                Column(content=[
                 loadingOverlay(html.Div(id='card-estado-gp-funcion'))
                ],size=12),
             
            ]),

    ])
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
        Output("subtitle-periodo", "children"),
        Output("subtitle-moneda", "children"),
        [
         Input("periodo-input", "value"),
         Input("tipo-moneda", "value")
        ],

        )
    def update_subtitles(periodo, moneda):
        year=periodo[:4]
        month=int(periodo[4:])
        
        df=data_finanzas[(data_finanzas['Año']==year)&(data_finanzas['month']>=1)&(data_finanzas['month']<=month)]
        
        month_inicio=df['Mes'].unique()[0]
        month_fin=df['Mes'].unique()[-1]
        year_text=df['Año'].unique()[0]
        text_subtitle_periodo=f'Desde {month_inicio}{year_text} Hasta {month_fin}{year_text}'
        text_subtitle_moneda=f'Expresado en {moneda}'
        return text_subtitle_periodo,text_subtitle_moneda
    
    @app.callback(
        Output("card-estado-gp-funcion", "children"),
        Output("graph-1", "figure"),
        Output("graph-2", "figure"),
        Output("graph-3", "figure"),
        [
         Input("periodo-input", "value"),
         Input("tipo-moneda", "value")
        ],

        )
    def update_tabla_gp(periodo, moneda):
        if moneda == 'soles':
            value_moneda='saldo_cargo_mof'
            value_moneda_funcion='importe_mof'
            sig='S/'
        elif moneda == 'dolares':
            value_moneda='saldo_cargo_mex'   
            value_moneda_funcion='importe_mex'
            sig='$' 
        year=periodo[:4]
        month=int(periodo[4:])
        df=data_finanzas[(data_finanzas['Año']==year)&(data_finanzas['month']>=1)&(data_finanzas['month']<=month)]
        
        #la moneda sera value_moneda_funcion
        def createTableGP(df,moneda):
            UTILIDAD_BRUTA=['VENTAS DE MERCADERIAS','COSTO DE VENTAS DE MERCADERIAS','COSTO DE PRODUCTOS MANUFACTURADOS','COSTO DEL SERVICIO']
            UTILIDAD_OPERATIVA=['GASTOS DE VENTAS','GASTOS ADMINISTRATIVOS','OTROS INGRESOS','GASTOS NO DEDUCIBLES']
            UTILIDAD_ANTES_DEL_IMPUESTO_RENTA=['GASTOS FINANCIEROS','INGRESOS FINANCIEROS','GANANCIA POR DIFERENCIA DE CAMBIO','PERDIDA POR DIFERENCIA DE CAMBIO']
            #selecciono solo las 12 partidas del gfurpo funcion
            df_=df[df['grupo_funcion'].isin(df['grupo_funcion'].unique()[1:])]
            #cambio el signo a los totales por partida funcion
            df_['importe_mex']=df_['importe_mex']*-1
            #agrupo
            df_pg=df_.groupby(['grupo_funcion','Año','Mes','al_periodo'])[[moneda]].sum().reset_index()
            #invierto la tabla por periodo = convierto los periodos en columnas
            df_pg_pivot=df_pg.pivot_table(index=('grupo_funcion'),values=moneda,columns='al_periodo').reset_index()

            #EMPIEZO CREANDO LA TABLA CON EL TOTAL DE LA UTILIDAD BRUTA
            df_utilidad_bruta=df_pg_pivot[df_pg_pivot['grupo_funcion'].isin(UTILIDAD_BRUTA)]
            #ORDENO POR VENTAS INICIAL
            df_utilidad_bruta=df_utilidad_bruta.sort_values('grupo_funcion',ascending=False)
            #CRETO EL TOTAL QUE SERIA LA UB
            df_utilidad_bruta.loc['UTILIDAD BRUTA',:]= df_utilidad_bruta.sum(numeric_only=True, axis=0)  
            df_utilidad_bruta=df_utilidad_bruta.fillna('UTILIDAD BRUTA')
            #CREO COLUMNA TOTAL
            df_utilidad_bruta.loc[:,'TOTAL']= df_utilidad_bruta.sum(numeric_only=True, axis=1)
            #lista de la fila utilidad bruta
            utilidad_bruta_list=df_utilidad_bruta.values[-1]
            #creto nuevo dataframe que almacenara la utilidad operativa
            df_ff=pd.DataFrame(columns=df_utilidad_bruta.columns)
            df_ff.loc[0]=utilidad_bruta_list
            ###############################UTILIDAD OPERATIVA
            df_utilidad_operativa=df_pg_pivot[df_pg_pivot['grupo_funcion'].isin(UTILIDAD_OPERATIVA)]
            df_utilidad_operativa.loc[:,'TOTAL']= df_utilidad_operativa.sum(numeric_only=True, axis=1)
            #CONCATENO EL DATAFRAME DONDE ESTA SOLO LA UTILIDAD BRUTA CON LAS PARTIDAS QUE ME AYUDARAN A CALCULAR LA UTILIDAD OPERATIVA
            df_utilidad_operativa_proc=pd.concat([df_ff, df_utilidad_operativa])
            #CAMBIO EL TIPO DE DATO A FLOAT
            for col in df_utilidad_operativa_proc.columns[1:]:
                df_utilidad_operativa_proc[col]=df_utilidad_operativa_proc[col].astype('float64')
            #CREO LA FILA TOTAL QUE SERIA LA UTILIDAD OPERATIVA
            df_utilidad_operativa_proc.loc['UTILIDAD OPERATIVA',:]= df_utilidad_operativa_proc.sum(numeric_only=True, axis=0)  
            df_utilidad_operativa_proc=df_utilidad_operativa_proc.fillna('UTILIDAD OPERATIVA')

            #ELIMINO LA PRIMERA FILA QUE ES LA UTILIDAD OPERATIVA QUE YA NO SE NECESITA
            df_utilidad_operativa_proc=df_utilidad_operativa_proc.drop([0],axis=0)
            df_utilidad_operativa_proc_list=df_utilidad_operativa_proc.values[-1]
            df_fff=pd.DataFrame(columns=df_utilidad_operativa_proc.columns)
            df_fff.loc[0]=df_utilidad_operativa_proc_list
            ##################################UTILIDAD NETA

            df_utilidad_neta=df_pg_pivot[df_pg_pivot['grupo_funcion'].isin(UTILIDAD_ANTES_DEL_IMPUESTO_RENTA)]
            df_utilidad_neta.loc[:,'TOTAL']= df_utilidad_neta.sum(numeric_only=True, axis=1)

            df_utilidad_neta_proc=pd.concat([df_fff, df_utilidad_neta])
            for col in df_utilidad_neta_proc.columns[1:]:
                df_utilidad_neta_proc[col]=df_utilidad_neta_proc[col].astype('float64')
            
            df_utilidad_neta_proc.loc['UTILIDAD NETA',:]= df_utilidad_neta_proc.sum(numeric_only=True, axis=0)  
            df_utilidad_neta_proc=df_utilidad_neta_proc.fillna('UTILIDAD NETA')
            df_utilidad_neta_proc=df_utilidad_neta_proc.drop([0],axis=0)
            #######################DATAFRAME CORE
            df_table_gp=pd.concat([df_utilidad_bruta, df_utilidad_operativa_proc,df_utilidad_neta_proc])
            for periodo_col in df_table_gp.columns[1:]:
                df_table_gp[periodo_col] = df_table_gp.apply(lambda x: "{:,.0f}".format(x[periodo_col]), axis=1)
            return df_table_gp

        df_utilidad=createTableGP(df,value_moneda_funcion)
        card_estado_gp=dag.AgGrid(
                                    id="datatable-result",
        #[{"field": i} for i in table_df.columns]
                                    columnDefs=[{"field": 'grupo_funcion','headerName': '', "maxWidth": 300,"type": "leftAligned"}]+[{"field": i,"maxWidth": 110,"type": "leftAligned"} for i in df_utilidad.columns[1:]],
                                    rowData=df_utilidad.to_dict("records"),
                                    #dashGridOptions={"rowSelection": "multiple"},
                                    #columnSize="sizeToFit",
                                    defaultColDef={"resizable": True},
                                    #style={'overflow': "auto"},#'max-height': f'{300}px',
                                    className="ag-theme-balham",
                                    #"['Flavia Mccloskey', 'Lilly Boaz'].includes(params.data.employee)"
                                    rowClassRules={"bg-primary fw-bold": "['UTILIDAD BRUTA', 'UTILIDAD OPERATIVA','UTILIDAD NETA'].includes(params.data.grupo_funcion)"},
                                    columnSize="sizeToFit",
                                    dashGridOptions={"domLayout": "autoHeight"},
                                ),    
                               
                               
        df_=df.copy()
        df_[value_moneda_funcion]=df_[value_moneda_funcion]*-1
        df_pivot_funcion=pd.pivot_table(df_,index=['Año','Mes','month','al_periodo'],columns='grupo_funcion',values=value_moneda_funcion,aggfunc='sum').reset_index().fillna(0)
        df_pivot_funcion['UTILIDAD BRUTA']=df_pivot_funcion['VENTAS DE MERCADERIAS']+df_pivot_funcion['COSTO DEL SERVICIO']+df_pivot_funcion['COSTO DE VENTAS DE MERCADERIAS']+df_pivot_funcion['COSTO DE PRODUCTOS MANUFACTURADOS']
        df_pivot_funcion['UTILIDAD OPERATIVA']=df_pivot_funcion['UTILIDAD BRUTA']+df_pivot_funcion['GASTOS ADMINISTRATIVOS']+df_pivot_funcion['GASTOS DE VENTAS']+df_pivot_funcion['GASTOS NO DEDUCIBLES']+df_pivot_funcion['OTROS INGRESOS']
        df_pivot_funcion['UTILIDAD NETA']=df_pivot_funcion['UTILIDAD OPERATIVA']+df_pivot_funcion['GASTOS FINANCIEROS']+df_pivot_funcion['INGRESOS FINANCIEROS']+df_pivot_funcion['GANANCIA POR DIFERENCIA DE CAMBIO']+df_pivot_funcion['PERDIDA POR DIFERENCIA DE CAMBIO']
        df_pivot_funcion=df_pivot_funcion.sort_values('month')
        
        return [card_estado_gp,
                bar_gp(df_pivot_funcion,x='al_periodo',y='UTILIDAD BRUTA',size=250,left=40),
                bar_gp(df_pivot_funcion,x='al_periodo',y='UTILIDAD OPERATIVA',size=250,left=40),
                bar_gp(df_pivot_funcion,x='al_periodo',y='UTILIDAD NETA',size=250,left=40)
                ]

def dashCostosGenerales():
    app = DjangoDash('costos_generales', external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        dmc.Title("Revisión Grupo Función", align="center"),
        #dbc.Row([
        #    dbc.Col([,] ,width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
        #]),
        dbc.Row([
            dbc.Col([
                select('year-input',texto='Desde el Año',place="",value=all_year[-3],data=[{'label': i, 'value': i} for i in all_year]),
            ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                select('tipo-moneda',texto='Moneda',place="",data=[{"value": "soles", "label": "PEN"},{"value": "dolares", "label": "USD"},],value='dolares'),
            ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                dmc.SegmentedControl(
                        id="segmented",
                        value="Costos",
                        data=['Costos','Gastos','Ingresos','Perdidas'],
                        mt=10,
                        fullWidth=True,
                        radius='md',
                        color="blue"
                    ),
            ],width=8,className="col-xl-8 col-md-8 col-sm-12 col-12 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card(dcc.Graph(id='graph-costos-generales'),className="shadow-sm")#id='graph-gatos-generales'
            ] ,width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id='graph-cg-comparative-bar')
                #dbc.Card(dcc.Graph(id='graph-gg-comparative-bar'),className="shadow-sm")#id='graph-gatos-generales'
            ] ,width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            #dbc.Col([
            #    html.Div(id='graph-cg-comparative-pie')
                #dbc.Card(dcc.Graph(id='graph-gg-comparative-bar'),className="shadow-sm")#id='graph-gatos-generales'
            #] ,width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
        ])
    ])
    @app.callback(
        Output("graph-costos-generales", "figure"),
        Output("graph-cg-comparative-bar", "children"), 
        #Output("graph-cg-comparative-pie", "children"),
        [Input("year-input", "value"),
         Input("segmented", "value"),
         Input("tipo-moneda", "value")],
        )
    def update_graph(year,segmented,moneda):
        if segmented == 'Costos':
            list=['COSTO DE VENTAS DE MERCADERIAS','COSTO DE PRODUCTOS MANUFACTURADOS','COSTO DEL SERVICIO']
        elif segmented == 'Gastos':
            list=['GASTOS DE VENTAS','GASTOS ADMINISTRATIVOS','GASTOS FINANCIEROS','GASTOS NO DEDUCIBLES']
        elif segmented == 'Ingresos':
            list=['INGRESOS FINANCIEROS','VENTAS DE MERCADERIAS','OTROS INGRESOS','GANANCIA POR DIFERENCIA DE CAMBIO']
        elif segmented == 'Perdidas':
            list=['PERDIDA POR DIFERENCIA DE CAMBIO']

        df_finanzas_pivot=DataFinanzas.separateItems(data_finanzas,ejex='Periodo Mensual',tipo_moneda=moneda,tipo_importe=['importe_mof','importe_mex'])
        if segmented == "Ingresos":
            for col_partida in ['INGRESOS FINANCIEROS','VENTAS DE MERCADERIAS','OTROS INGRESOS','GANANCIA POR DIFERENCIA DE CAMBIO']:
                df_finanzas_pivot[col_partida]=df_finanzas_pivot[col_partida]*-1
        df_finanzas_pivot['al_periodo']=df_finanzas_pivot['al_periodo']+'01'
        df_finanzas_pivot['al_periodo']=pd.to_datetime(df_finanzas_pivot['al_periodo'])
        df_finanzas_pivot=df_finanzas_pivot.sort_values('al_periodo')
        df_finanzas_pivot['Año']=df_finanzas_pivot['Año'].astype('int')
        df_data_finanzas=df_finanzas_pivot[df_finanzas_pivot['Año']>=int(year)]
        #
        df_year=df_data_finanzas.groupby(['Año'])[list].sum().reset_index()
        #df_year_pronostico=data_finanzas_pronostico.groupby(['Año'])[costos_list].sum().reset_index()
        #df_stack_pie=pd.concat([df_year, df_stack_pie])#, ignore_index=True, sort=True
        tabs=dmc.Tabs(
                    [
                        dmc.TabsList(
                            [
                            
                                dmc.Tab(children=gasto,value=gasto)for gasto in list
                            ]
                        ),
                        #for gasto in gastos_list:
                            
                            #[dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(figure=barCharTrace(df_year,list[i])),className="shadow-sm")), value=list[i]) for i in range(1) ],#range(len(list)-1)
                            html.Div([dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(figure=barCharTrace(df_year,list[i])),className="shadow-sm")), value=list[i]) for i in range(len(list))]),
                            #dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(figure=barCharTrace(df_year,list[0])),className="shadow-sm")), value=list[0]),
                            #dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(figure=barCharTrace(df_year,list[1])),className="shadow-sm")), value=list[1]),
                            #dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(figure=barCharTrace(df_year,list[2])),className="shadow-sm")), value=list[2]),
                            #dmc.TabsPanel(loadingOverlay(dbc.Card(dcc.Graph(figure=barCharTrace(df_year,list[3])),className="shadow-sm")), value=list[3]),
                    ],
                    value=list[0],
                ),

        
        #test=loadingOverlay(dbc.Card(dcc.Graph(figure=fig),className="shadow-sm"))
        return linesChartTrace(df_data_finanzas,list,'',moneda),tabs
    

import plotly.express as px

def dashER():
    app = DjangoDash('estado_resultados', external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        
        
        
        dbc.Row([
            dbc.Col([
                dmc.Title("Estado de Resultados", align="center"),
            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
            dbc.Col([
                select('year-input',texto='Año',place="",value=all_year[-3],data=[{'label': i, 'value': i} for i in all_year],clearable=False),
            ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                select('mes-input',texto='Mes',place=""),
            ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                select('tipo-moneda',texto='Moneda',place="",data=[{"value": "soles", "label": "PEN"},{"value": "dolares", "label": "USD"},],value='dolares'),
            ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            
        ]),
        dbc.Row([
            
            dbc.Col([
                html.Div(id='card-ingresos')
            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
            dbc.Col([
                html.Div(id='card-gastos')
            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
            dbc.Col([
                html.Div(id='card-costos')
            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
            
        ]),
        dbc.Row([
            
            dbc.Col([
                loadingOverlay(dbc.Card(dcc.Graph(id='graph-ingresos'),className="shadow-sm"))
            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
            dbc.Col([
                loadingOverlay(dbc.Card(dcc.Graph(id='graph-gastos'),className="shadow-sm"))
            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
            dbc.Col([
                loadingOverlay(dbc.Card(dcc.Graph(id='graph-costos'),className="shadow-sm"))
            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
            
        ]),
        #html.Div([
        #     dag.AgGrid(
        #    columnDefs=columnDefs,
        #    rowData=df_23.to_dict("records"),
        #    columnSize="sizeToFit",
        #    defaultColDef={"resizable": True, "sortable": True, "filter": True},
        #),
        #])
        dbc.Row([
            dbc.Col([
                dmc.Card(
                            children=[
                                
                                
                            dmc.CardSection([
                                   dmc.SegmentedControl(
                                    id='segment-igc',
                                    value="Ingresos",
                                    data=[{'label': 'Ingresos', 'value': 'Ingresos'},
                                          {'label': 'Gastos', 'value': 'Gastos'},
                                          {'label': 'Costos', 'value': 'Costos'}],
                                    #mt=10,
                                    fullWidth=True,
                                    color='rgb(34, 184, 207)'
                                ),
                                    
                                html.Div(id='table-igc') 
                                
                            ]),
                                
                            ],
                            withBorder=True,
                            shadow="lg",
                            radius="xs",
                           
            )   
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
        ])

    ])
    @app.callback(
        Output("mes-input", "data"),
        Input("year-input", "value"),
    )
    def update_input_mes(year):
        df=data_finanzas.copy()
        df=df[df['Año']==year]
        return [{'label': i, 'value': i} for i in df['Mes'].unique()] 
    
    @app.callback(
        Output("card-ingresos","children"),
        Output("card-gastos","children"),
        Output("card-costos","children"),
        Output("graph-ingresos","figure"),
        Output("graph-gastos","figure"),
        Output("graph-costos","figure"),

        Input("year-input", "value"),
        Input("mes-input", "value"),
        Input("tipo-moneda",'value'),

    )
    def update_input_mes(year,mes,moneda):
        df=data_finanzas.copy()
        if moneda == 'soles':
            value_moneda='saldo_cargo_mof'
            value_moneda_funcion='importe_mof'
            sig='S/'
        elif moneda == 'dolares':
            value_moneda='saldo_cargo_mex'   
            value_moneda_funcion='importe_mex'
            sig='$'
        
        if mes == None:
            df_=df[df['Año']==year]
        elif mes != None:
            df_=df[(df['Año']==year)&(df['Mes']==mes)]
        
        colors=['rgb(71, 214, 171)','rgb(3, 20, 26)','rgb(79, 205, 247)','cyan','blue']

        
        df_pivot_funcion=pd.pivot_table(df_,index=['Año','Mes','month','al_periodo'],columns='grupo_funcion',values=value_moneda_funcion)
        df_pivot_funcion=df_pivot_funcion.reset_index()
        df_pivot_funcion=df_pivot_funcion.fillna(0)
        for col_partida in ['INGRESOS FINANCIEROS','VENTAS DE MERCADERIAS','OTROS INGRESOS','GANANCIA POR DIFERENCIA DE CAMBIO']:
            df_pivot_funcion[col_partida]=df_pivot_funcion[col_partida]*-1

        df_pivot_funcion['Ingresos_Generales']=df_pivot_funcion['INGRESOS FINANCIEROS']+df_pivot_funcion['VENTAS DE MERCADERIAS']+df_pivot_funcion['OTROS INGRESOS']+df_pivot_funcion['GANANCIA POR DIFERENCIA DE CAMBIO']#INBHGRESOS CUENTA 70
        df_pivot_funcion['Gastos_Generales']=df_pivot_funcion['GASTOS DE VENTAS']+df_pivot_funcion['GASTOS ADMINISTRATIVOS']+df_pivot_funcion['GASTOS FINANCIEROS']+df_pivot_funcion['GASTOS NO DEDUCIBLES']+df_pivot_funcion['PERDIDA POR DIFERENCIA DE CAMBIO']
        df_pivot_funcion['Costos_Generales']=df_pivot_funcion['COSTO DE VENTAS DE MERCADERIAS']+df_pivot_funcion['COSTO DE PRODUCTOS MANUFACTURADOS']+df_pivot_funcion['COSTO DEL SERVICIO']
        
        def calculateCard(df,col='Ingresos_Generales',color=[],list_partidas=[]):
            total=df[col].sum()
            lista_diccionario=[]
            for element,color in zip(list_partidas,color):
                percent_value=round((df[element].sum()/total)*100)
                dicts={'value': percent_value, 'color': color, 'label': f'{percent_value}%', "tooltip": element}
                #print(f"UNA ITERACION:{(df[element].sum()/total)*100}")
                lista_diccionario.append(dicts)
            return lista_diccionario


        dict_ingresos=calculateCard(df_pivot_funcion,col='Ingresos_Generales',color=colors[:4],list_partidas=['INGRESOS FINANCIEROS','VENTAS DE MERCADERIAS','OTROS INGRESOS','GANANCIA POR DIFERENCIA DE CAMBIO'])
        dict_gastos=calculateCard(df_pivot_funcion,col='Gastos_Generales',color=colors,list_partidas=['GASTOS DE VENTAS','GASTOS ADMINISTRATIVOS','GASTOS FINANCIEROS','GASTOS NO DEDUCIBLES','PERDIDA POR DIFERENCIA DE CAMBIO'])
        dict_costos=calculateCard(df_pivot_funcion,col='Costos_Generales',color=colors[:3],list_partidas=['COSTO DE VENTAS DE MERCADERIAS','COSTO DE PRODUCTOS MANUFACTURADOS','COSTO DEL SERVICIO'])
        #print(dict_ingresos)
        #print(dict_gastos)
        #print(dict_costos)
        #total_activo="{:,.2f}".format(df_bc[df_bc['grupo1']=='ACTIVO'][value_moneda].sum())
        total_ingresos="{:,.0f}".format(df_pivot_funcion['Ingresos_Generales'].sum())#df_pivot_funcion['Ingresos_Generales'].sum()
        total_gastos="{:,.0f}".format(df_pivot_funcion['Gastos_Generales'].sum())
        total_costos="{:,.0f}".format(df_pivot_funcion['Costos_Generales'].sum())
        card_ingreso=cardGF(value_total=f"{sig} {total_ingresos}",text='Ingresos',list_element=dict_ingresos)
        card_gastos=cardGF(value_total=f"{sig} {total_gastos}",text='Gastos',list_element=dict_gastos)
        card_costos=cardGF(value_total=f"{sig} {total_costos}",text='Costos',list_element=dict_costos)

        df_mes_c=df_pivot_funcion.groupby(['Mes','month'])[['Ingresos_Generales','Gastos_Generales','Costos_Generales']].sum().reset_index().sort_values('month',ascending=True)

        
       
        fig_ingreso = px.area(df_mes_c, x="Mes", y="Ingresos_Generales", template='none',title='INGRESOS')
        fig_ingreso.update_layout(height=250, margin=dict(l=50,r=20,b=60,t=80))
        fig_gastos = px.area(df_mes_c, x="Mes", y="Gastos_Generales", template='none',title='GASTOS')
        fig_gastos.update_layout(height=250, margin=dict(l=50,r=20,b=60,t=80))

        fig_costos = px.area(df_mes_c, x="Mes", y="Costos_Generales", template='none',title='COSTOS')
        fig_costos.update_layout(height=250, margin=dict(l=50,r=20,b=60,t=80))
        
        #df_ventas=df_[df_['grupo_funcion'].isin(['VENTAS DE MERCADERIAS'])]
        #df_ventas_test=df_ventas.groupby(['Mes','month','grupo_funcion'])[[value_moneda_funcion]].sum().reset_index().sort_values('month',ascending=True)
        #fig_costos = px.area(df_ventas_test, x="Mes", y=value_moneda_funcion, template='none',title='VENTAS',color='grupo_funcion')
        #fig_costos.update_layout(height=250, margin=dict(l=50,r=20,b=60,t=80))

        #if segment_table == "Ingresos":
        
            
        return card_ingreso,card_gastos,card_costos,fig_ingreso,fig_gastos,fig_costos
    
    @app.callback(
        Output("table-igc","children"),
        Input("year-input", "value"),
        Input("mes-input", "value"),
        Input("tipo-moneda",'value'),
        Input("segment-igc","value"),
    )
    def update_input_mes(year,mes,moneda,segment_igc):
        df=data_finanzas.copy()
        if moneda == 'soles':
            value_moneda='saldo_cargo_mof'
            value_moneda_funcion='importe_mof'
            sig='S/'
        elif moneda == 'dolares':
            value_moneda='saldo_cargo_mex'   
            value_moneda_funcion='importe_mex'
            sig='$'
        
        if mes == None:
            df_=df[df['Año']==year]
        elif mes != None:
            df_=df[(df['Año']==year)&(df['Mes']==mes)]

        if segment_igc == "Ingresos":
            list_segment=['INGRESOS FINANCIEROS','VENTAS DE MERCADERIAS','OTROS INGRESOS','GANANCIA POR DIFERENCIA DE CAMBIO']
        elif segment_igc == "Gastos":
            list_segment=['GASTOS DE VENTAS','GASTOS ADMINISTRATIVOS','GASTOS FINANCIEROS','GASTOS NO DEDUCIBLES','PERDIDA POR DIFERENCIA DE CAMBIO']
        elif segment_igc == "Costos":
            list_segment=['COSTO DE VENTAS DE MERCADERIAS','COSTO DE PRODUCTOS MANUFACTURADOS','COSTO DEL SERVICIO']

        df_table_partidas=df_[df_['grupo_funcion'].isin(list_segment)]
        if segment_igc == "Ingresos":
            df_table_partidas[value_moneda_funcion]=df_table_partidas[value_moneda_funcion]*-1
        
        df_www=df_table_partidas.groupby(['idcuenta','descripcion','grupo_funcion'])[[value_moneda_funcion]].sum().reset_index()
        df_www=df_www.rename(columns={'descripcion':'Cuenta','grupo_funcion':'Partida',value_moneda_funcion:sig})
        df_www=df_www.round(2)
        
        columnDefs = [{"field": i, "type": "rightAligned",'filter': True} for i in df_www.columns]
        table_grid=html.Div([
                dag.AgGrid(
                columnDefs=columnDefs,
                rowData=df_www.to_dict("records"),
                columnSize="sizeToFit",
                defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth":100},
                #columnDefs=columnDefs,
            ), 
        ])
        return table_grid

def dashEstadoSituacion2():
    #createTrimestre(df)
    all_partidas=list(data_finanzas['grupo1'].dropna().unique())+list(data_finanzas['grupo2'].dropna().unique())+list(data_finanzas['grupo3'].dropna().unique())+list(data_finanzas['grupo_funcion'].dropna().unique())
    all_periodo=data_finanzas['al_periodo'].unique()
    all_year=data_finanzas['Año'].unique()
    app = DjangoDash('es2', external_stylesheets=external_stylesheets)
    app.layout = html.Div([
    dbc.Row([
            Column(
                content=[
                 #btnCollapse() 
            ],size=1), 
            Column(
                content=[
                  dmc.Title("Estado de Situción Financiera", align="center",order=3,color="black"),
                dmc.Title(id='subtitle-periodo', align="center",order=4,color="black"),
                dmc.Title(id='subtitle-moneda', align="center",order=6,color="black"),
            ],size=7), 
            Column(
                content=[
                  select('periodo-input',texto='Periodos',place="",value=all_periodo[-1],data=[{'label': i, 'value': i} for i in all_periodo]),
            ],size=2), 
            Column(
                content=[
                  select('tipo-moneda',texto='Moneda',place="",data=[{"value": "soles", "label": "PEN"},{"value": "dolares", "label": "USD"},],value='dolares'),
            ],size=2), 

        ]),
        
            
            #dbc.Collapse(
            dbc.Row([
                Column(
                    content=[
                        loadingOverlay(html.Div(id='card-estado-situacion-financiera')),
                ],size=12), 
                
                
            ]),
            dbc.Row([
                Column(
                    content=[
                        
                    loadingOverlay(cardGraph(id_graph='figure-treemap-sf',id_maximize='btn-modal'))
                ],size=12), 
                
            ]),
    ])
    @app.callback(
        Output("subtitle-periodo", "children"),
        Output("subtitle-moneda", "children"),
        [
         Input("periodo-input", "value"),
         Input("tipo-moneda", "value")
        ],

        )
    def update_subtitles(periodo, moneda):
        df=data_finanzas[data_finanzas['al_periodo']==periodo]
        moth_text=df['Mes'].unique()[0]
        year=df['Año'].unique()[0]
        text_subtitle_periodo=f'{moth_text} del {year}'
        text_subtitle_moneda=f'Expresado en {moneda}'
        return text_subtitle_periodo,text_subtitle_moneda


    @app.callback(
        Output("card-estado-situacion-financiera", "children"),
        Output("figure-treemap-sf", "figure"),
        [
         Input("periodo-input", "value"),
         Input("tipo-moneda", "value")
        ],

        )
    def update_situacion_financiera(periodo,moneda):
        if moneda == 'soles':
            value_moneda='saldo_cargo_mof'
        elif moneda == 'dolares':
            value_moneda='saldo_cargo_mex'   
        
        simbolo='$' if value_moneda =='saldo_cargo_mex'else 'S/'
        
        df=data_finanzas[data_finanzas['al_periodo']==periodo]
        df_bc=df.groupby(['grupo1','grupo2','grupo3'])[[value_moneda]].sum().reset_index()
        #totales filtrados
        total_activo="{:,.2f}".format(df_bc[df_bc['grupo1']=='ACTIVO'][value_moneda].sum())
        total_pasivo=df_bc[df_bc['grupo1']=='PASIVO'][value_moneda].sum()
        total_patrimonio=df_bc[df_bc['grupo1']=='PATRIMONIO'][value_moneda].sum()
        total_pasivo_patri="{:,.2f}".format(total_pasivo+total_patrimonio)


        df_activo_corriente=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='ACTIVO',importe=value_moneda,partida_grupo_2='ACTIVO CORRIENTE',label_total='Total Activo Corriente')
        #bar_activo_corriente=df_activo_corriente.groupby(['ACTIVO CORRIENTE'])[[simbolo]].sum().reset_index()
        bar_activo_corriente=df_activo_corriente.drop(['Total'],axis=0)
        bar_activo_corriente=bar_activo_corriente[bar_activo_corriente[simbolo]!="0.00"]
        #df_testing=df_testing.groupby(['ACTIVO CORRIENTE'])[[simbolo]].sum().reset_index()
        #print(df_testing)
        df_activo_no_corriente=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='ACTIVO',importe=value_moneda,partida_grupo_2='ACTIVO NO CORRIENTE',label_total='Total Activo no Corriente')
        bar_activo_no_corriente=df_activo_no_corriente.drop(['Total'],axis=0)
        bar_activo_no_corriente=bar_activo_no_corriente[bar_activo_no_corriente[simbolo]!="0.00"]
        df_pasivo_corriente=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='PASIVO',importe=value_moneda,partida_grupo_2='PASIVO CORRIENTE',label_total='Total Pasivo Corriente')
        bar_pasivo_corriente=df_pasivo_corriente.drop(['Total'],axis=0)
        bar_pasivo_corriente=bar_pasivo_corriente[bar_pasivo_corriente[simbolo]!="0.00"]
        df_pasivo_no_corriente=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='PASIVO',importe=value_moneda,partida_grupo_2='PASIVO NO CORRIENTE',label_total='Total Pasivo no Corriente')
        bar_pasivo_no_corriente=df_pasivo_no_corriente.drop(['Total'],axis=0)
        bar_pasivo_no_corriente=bar_pasivo_no_corriente[bar_pasivo_no_corriente[simbolo]!="0.00"]
        df_patrimonio=DataFinanzas.dataframeBalanceAPP(df_bc,partida_grupo_1='PATRIMONIO',importe=value_moneda,partida_grupo_2='PATRIMONIO',label_total='Total Patrimonio')
        bar_patrimonio=df_patrimonio.drop(['Total'],axis=0)
        bar_patrimonio=bar_patrimonio[bar_patrimonio[simbolo]!="0.00"]
        #print(bar_patrimonio.info())
        #print(df_activo_corriente['ACTIVO CORRIENTE'].tail(1).unique()) 
        card_estado_situacion=html.Div([
                                dbc.Row([
                                    Column(content=[    
                                            cardGraph(fig=bar_es(bar_activo_corriente,x=simbolo,y='ACTIVO CORRIENTE',size=300,left=200),with_id=False,icon_maximize=False)
                                                            
                                           ],
                                    size=6),
                                    Column(content=[        
                                        cardGraph(fig=bar_es(bar_activo_no_corriente,x=simbolo,y='ACTIVO NO CORRIENTE',size=300,left=200),with_id=False,icon_maximize=False)
                                                            
                                           ],
                                    size=6),
                                ]),
                                dbc.Row([
                                    Column(content=[
                                        cardGraph(fig=bar_es(bar_pasivo_corriente,x=simbolo,y='PASIVO CORRIENTE',size=300,left=200),with_id=False,icon_maximize=False)
                                                        
                                           ],
                                    size=4),
                                    Column(content=[
                                        cardGraph(fig=bar_es(bar_pasivo_no_corriente,x=simbolo,y='PASIVO NO CORRIENTE',size=300,left=100),with_id=False,icon_maximize=False)
                                                          
                                           ],
                                    size=4),
                                    Column(content=[
                                        cardGraph(fig=bar_es(bar_patrimonio,x=simbolo,y='PATRIMONIO',size=300,left=150),with_id=False,icon_maximize=False)
                                                      
                                           ],
                                    size=4),
                                ]),
                                
                                ]),
                               
        treemap_graph=treemapEstadoSituacion(df_bc,moneda=value_moneda,titulo='',list_path=['grupo1', 'grupo2', 'grupo3'])
        return card_estado_situacion,treemap_graph