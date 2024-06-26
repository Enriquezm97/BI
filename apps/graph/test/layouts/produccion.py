from django_plotly_dash import DjangoDash
from apps.graph.test.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from apps.graph.test.utils.theme import themeProvider, Container
from apps.graph.test.utils.frame import Column, Row, Div, Store, Download, Modal
from apps.graph.test.utils.components.components_main import Entry, Button, DataDisplay,Picking
from apps.graph.test.utils.blocks.block_filters import offcanvas_recurso_agricola,offcanvas_costos_agricola
from apps.graph.test.utils.tables import tableDag
from apps.graph.test.utils.functions.callbacks.callbacks_produccion import *
from apps.graph.test.utils.functions.callbacks.callbacks_ import create_callback_opened_modal
from apps.graph.test.utils.blocks.block_card import cardGraph,card,cardSection,card_segment,card_graph_1
from ..Connection.apis import connection_api_agricola



"""LA DATA DE PRUEBA"""
#from apps.graph.build.containers.Agricola.Agricola import df_var_agricolas_default,df_costos_agricola_default,df_var_agricolas_pivot_default
import dash_mantine_components as dmc
from dash import ctx
import dash
#from crum import get_current_request



#plan de siembra
def ejecucionCampania(codigo=''):

    #df_var_agricolas_default= data_agricola(empresa=get_empresa())[0]
    #df_var_agricolas_default= pd.read_parquet('agricola.parquet', engine='pyarrow')#connection_api_agricola(tipo = 'fertilizantes')
    df_var_agricolas_default = connection_api_agricola(tipo = 'fertilizantes')
    print(df_var_agricolas_default)
    campaña_list=sorted(df_var_agricolas_default['AÑO_CULTIVO'].unique())
    app = DjangoDash(name=codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Container([
            Modal(id="modal-line-recurso-agricola", size= "85%"),
            offcanvas_recurso_agricola,
            Row([
                Column([
                    dmc.Card(children=[
                        dmc.Grid(children=[
                            Column([Button.btnFilter()],size=1),
                            Column([
                                Div(id='title')
                            ],size=10),
                            Column([Button.btnDownload(style={'position': 'absolute','top': '4px','right': '10px','z-index': '99'})],size=1),
                            Column([
                                Entry.select(id = 'select-campania',
                                            texto = "Campaña-Cultivo",
                                            size = 'sm',
                                            data = [{'label': i, 'value': i} for i in campaña_list],
                                            value = campaña_list[-1],
                                            clearable=False
                                            )#,value='2018-Palta'
                            ],size=2),
                            Column([
                                Entry.select(id='select-variedad',texto="Variedades",size='sm')
                            ],size=3),
                            Column([
                                Entry.select(id='select-lote',texto="Lotes",size='sm')
                            ],size=3),
                            Column([
                                Div(id = 'label-range-inicio-campania',style={'padding-top':'35px'}),

                                #Entry.datepickerRange(id='datepicker-date-campania',label='Inicio-Fin(Campaña)',disabled=True)
                            ],size=2),
                            Column([
                                Div(id = 'label-range-fin-campania',style={'padding-top':'35px'})
                            
                            ],size=2),
                        ],gutter='xs')
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",         
                    style={"position": "static",'background-color':'white',"overflow":"visible"},#"position": "static",
                    p=10
                    )
                ]),
                
                
                
            ]),
            Row([
                
                
            ]),
            Row([
                Column([
                    DataDisplay.loadingOverlay(
                    card_segment(
                        id_graph = 'line-recurso-agricola', 
                        id_maximize = 'maximize-line-recurso-agricola',
                        id_segmented='segmented-recurso',
                        #value = 'Mes',
                        #data = [{'label': 'Mensual', 'value': 'Mes'},{'label': 'Trimestral', 'value': 'Trimestre'},{'label': 'Semanal', 'value': 'Semana'},{'label': 'Fecha', 'value': 'Fecha'}],
                        height=400
                    )),
                    
                ],size=12),
                #Column([
                    
                #    DataDisplay.loadingOverlay(Div(id='table-grid-lotes'))
                #],size=5),
            ]),
            Row([
                Column([
                    dmc.Tabs(
                        [
                            dmc.TabsList(
                                [
                                    dmc.Tab("Variedad", value="Variedad"),
                                    dmc.Tab("Lote", value="Lote"),
                                    
                                ]
                            ),
                            dmc.TabsPanel(Div( id = 'table-variedad'), value="Variedad"),
                            dmc.TabsPanel(Div( id = 'table-lote'), value="Lote"),
                            
                        ],
                        value="Variedad",
                    )
                    
                ])    
            
            ]),
            
            
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
        Modal(id='modal')
        
    ])
    create_callback_offcanvas_filters(app)
    create_callback_filter_agricola_recurso(app=app,dataframe=df_var_agricolas_default)
    create_title_ejecucion_campania(app , title = 'Ejecución de Campaña ')
    create_callback_download_data(app)
    create_callback_recurso_agricola(app)
    create_callback_modal_graph(app,id_modal = 'modal', id_btn_modal = 'maximize-line-recurso-agricola', id_figure = 'line-recurso-agricola')
    create_callback_opened_modal(app, modal_id="modal-line-recurso-agricola",children_out_id="line-recurso-agricola", id_button="maximize-line-recurso-agricola",height_modal=700)
    
def costosCampania(codigo=''):
    #df_costos_agricola_default= pd.read_parquet('costos.parquet', engine='pyarrow')#connection_api_agricola(tipo = 'costos')
    
    
    df_costos_agricola_default=connection_api_agricola(tipo = 'costos')

    anio_campania = sorted(df_costos_agricola_default['AÑO_CAMPAÑA'].unique())
    app = DjangoDash(name=codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Container([
        Modal(id="modal-bar-costos-cultivo", size= "85%"),
        Modal(id="modal-bar-costos-variedad", size= "85%"),
        Modal(id="modal-pie-costos-tipo", size= "85%"),
        Modal(id="modal-map-costos-lt", size= "85%"),
        Modal(id="modal-bar-costos-lote", size= "85%"),
        offcanvas_costos_agricola,
        Row([   
                Column([
                    dmc.Card(children=[
                        dmc.Grid(children=[
                            Column([
                            Button.btnFilter(style={'position': 'absolute','z-index': '99'}),
                            Div(id='title',style={'left': '50px'})#,'position': 'absolute'
                        ],size=5),
                        Column([
                            Entry.select(
                                id = 'select-anio',
                                texto = "Año de Campaña",
                                size = 'sm',
                                #data = [{'label': i, 'value': i} for i in anio_campania],
                                value = anio_campania[-1],
                                clearable=True
                            )    
                        ],size=2),
                        Column([
                            Entry.select(
                                id = 'select-cultivo',
                                texto = "Cultivo",
                                size = 'sm',
                            ) 
                        ],size=2),
                        Column([
                            Entry.select(
                                id = 'select-variedad',
                                texto = "Variedad",
                                size = 'sm',
                            ) 
                        ],size=2),
                        Column([Button.btnDownload(style={'position': 'absolute','top': '4px','right': '10px','z-index': '99'})],size=1),
                        ])
                    ])
                ]),
                
            ]),
        
        Row([
        Column([
            card_graph_1(
                    text='Costos por Cultivo',
                    id_graph = 'bar-costos-cultivo', 
                    id_maximize = 'maximize-bar-costos-cultivo',
                    height = 485,
                    color_bg="black"
            ),
           
        ],size=4),
        Column([
            card_graph_1(
                    text='Costos por Variedad',
                    id_graph = 'bar-costos-variedad', 
                    id_maximize = 'maximize-bar-costos-variedad',
                    height = 485,
                    color_bg="black"
            ),
            
        ],size=4),
        Column([
            Row([Column([DataDisplay.loadingOverlay(Div(id='card-costos-total'))])]),
            Row([
                Column([
                    DataDisplay.loadingOverlay(Div(id='card-costos-ha'))
                ],size=6),
                Column([
                    DataDisplay.loadingOverlay(Div(id='card-costos-cultivo'))
                ],size=6)
            ]),
            Row([Column([
                card_graph_1(
                    text='Tipo de Costo',
                    id_graph = 'pie-costos-tipo', 
                    id_maximize = 'maximize-pie-costos-tipo',
                    height = 280,
                    color_bg="black"
                ),
                    
                ])
            ]),
            #Row([Column([DataDisplay.loadingOverlay(Div(id='card-costos-cultivo'))])]),
        ],size=4),
        
        ]), 

        Row([
           Column([
               card_graph_1(
                    text='Mapa',
                    id_graph = 'map-costos-lt', 
                    id_maximize = 'maximize-map-costos-lt',
                    height = 300,
                    color_bg="black"
                ),
                 
            ],size=5), 
           Column([
                card_graph_1(
                    text='Costos por Lote',
                    id_graph = 'bar-costos-lote', 
                    id_maximize = 'maximize-bar-costos-lote',
                    height = 300,
                    color_bg="black"
                ),
            ],size=7), 
        ]),

        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
        Modal(id='modal'),
        
    ])
    create_callback_offcanvas_filters(app)
    create_callback_filter_agricola_costos(app,dataframe = df_costos_agricola_default)
    create_title_costos_campania(app, title ='Costos de Campaña ')
    create_callback_download_data(app)
    create_callback_costos_agricola(app)
    create_callback_opened_modal(app, modal_id="modal-bar-costos-cultivo",children_out_id="bar-costos-cultivo", id_button="maximize-bar-costos-cultivo",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-bar-costos-variedad",children_out_id="bar-costos-variedad", id_button="maximize-bar-costos-variedad",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-pie-costos-tipo",children_out_id="pie-costos-tipo", id_button="maximize-pie-costos-tipo",height_modal=500)
    create_callback_opened_modal(app, modal_id="modal-map-costos-lt",children_out_id="map-costos-lt", id_button="maximize-map-costos-lt",height_modal=600)
    create_callback_opened_modal(app, modal_id="modal-bar-costos-lote",children_out_id="bar-costos-lote", id_button="maximize-bar-costos-lote",height_modal=700)
    #create_callback_modal_graph(app, id_modal = 'modal', id_btn_modal = 'maximize-bar-costos-cultivo', id_figure = 'bar-costos-cultivo')
    """
    @app.callback(
    Output('test', "children"),
    #Output('modal', "is_open"),
    
    Input('maximize-bar-costos-cultivo', "n_clicks"),
    #Input('bar-costos-cultivo','figure'),
    #
    Input('maximize-bar-costos-variedad', "n_clicks"),
    #Input('bar-costos-variedad','figure'),
    #
    Input('maximize-pie-costos-tipo', "n_clicks"),
    #Input('pie-costos-tipo','figure'),
    #
    Input('maximize-map-costos-lt', "n_clicks"),
    #Input('map-costos-lt','figure'),
    #
    Input('maximize-bar-costos-lote', "n_clicks"),
    #Input('bar-costos-lote','figure'),
    #prevent_initial_call=True,
    )
    
    def display(*args,**kwargs):
        #n_clicks_cultivo,n_clicks_variedad,n_clicks_tipo,n_clicks_map,n_clicks_lote
        #da = kwargs['dash_app']
        #n_clicks_cultivo, #figure_bar_cultivo,
                #      n_clicks_variedad,# figure_bar_variedad,
                #      n_clicks_tipo, #figure_pie_tipo,
                #      n_clicks_map, #figure_map,
                #      n_clicks_lote, #figure_bar_lote,
                
        
        #):
        print(args)
        print(kwargs)
        #da = kwargs['dash_app']
        #ctx = kwargs['callback_context']  # try this
        #if n_clicks:
        #    return not is_open
        #return is_open,DataDisplay.modalMaximize(Graph(figure = convert_dict_to_graph(figure)))
        #from dash import ctx
        
        
        button_id = ctx.triggered_id if not None else 'No clicks yet'
        
        print(ctx.triggered_id)
        
        #print()
        #owo="Args are [%s], the extra parameter dash_app is %s and kwargs are %s" %(button_id, kwargs)
        #print(owo)
        return button_id#button_id,kwargs
        
        #################################################
       
        "Args are [%s] and the extra parameter dash_app is %s" %(",".join(args), dash_app)
        if n_clicks_cultivo == True:#True, 
            return DataDisplay.modalMaximize(Graph(figure = convert_dict_to_graph(figure_bar_cultivo))),True
        elif n_clicks_variedad == True:
            return DataDisplay.modalMaximize(Graph(figure = convert_dict_to_graph(figure_bar_variedad))),True
        elif n_clicks_tipo == True:
            return DataDisplay.modalMaximize(Graph(figure = convert_dict_to_graph(figure_pie_tipo))),True
        elif n_clicks_map == True:
            return DataDisplay.modalMaximize(Graph(figure = convert_dict_to_graph(figure_map))),True
        elif n_clicks_lote == True:
            return DataDisplay.modalMaximize(Graph(figure = convert_dict_to_graph(figure_bar_lote))),True
        else:#False,
            return  no_update
    
        """

def resumenCampania():

    #df_var_agricolas_default=pd.read_parquet('agricola.parquet', engine='pyarrow')
    #campaña_list=sorted(df_var_agricolas_default['AÑO_CULTIVO'].unique())
    app = DjangoDash('resumen_campania',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([
                Column([
                    #Button.btnFilter(style={'position': 'absolute','z-index': '99'}),
                    Div(content=['Resumen Campaña'],id='title',style={'left': '50px'})#,'position': 'absolute'
                ],size=4),

                    Column([
                        card(
                            Entry.select(
                                id = 'select-anio',
                                texto = "AÑO DE CAMPAÑA",
                                size = 'xs',
                                #data = [{'label': i, 'value': i} for i in anio_campania],
                                #value = anio_campania[-1],
                                clearable=False
                            )    
                    )
                ],size=2),
                Column([
                    card(
                    Entry.select(
                        id = 'select-cultivo',
                        texto = "CULTIVO",
                        size = 'xs',
                        clearable=False
                    ) 
                )
                ],size=2),
                Column([
                    card(
                    Entry.select(
                        id = 'select-variedad',
                        texto = "VARIEDAD",
                        size = 'xs',
                    ) 
                )
                ],size=2),
               
                Column([
                    card(
                        Entry.select(
                        id = 'select-tipo-variable',
                        texto = "RECURSO",
                        size = 'xs',
                        clearable=False
                    ) )
                    
                ],size=2),
                
            ]),
        Row([
            Column([
                Row([Column([cardSection(text='Plan Campaña',num=20000,radius='xs')])]),
                Row([Column([cardSection(text='Plan Campaña',num=20000,radius='xs')])]),
                Row([Column([
                    cardSection(text='% Avance',num=20000,radius='xs',contenido ='tabla',
                                content=[
                                    dmc.Center(
                                        dmc.RingProgress(
                                            id="ring-progress",
                                            sections=[{"value": 100, "color": "indigo"}],
                                            label=dmc.Center(dmc.Text("100%", color="indigo",size="lg",weight=700)),
                                            size=200,
                                            thickness=20,
                                        ),
                                    )
                                ]
                    )
                    
                    ])
                ]),
                
                
            ],size=3),
            Column([
                cardSection(text = 'Tabla',radius='xs',color_text ='black',color_section_title = 'white',contenido ='tabla', 
                            content = [
                               tableDag(rules_col=['owwo','awa'])
                            ]
                )
            ],size=6),
            Column([
            cardSection(text = 'LOTES',radius='xs',color_text ='black',color_section_title = 'white',contenido ='tabla', 
                            content = [
                              
                            ]
                )
            ],size=3),
        ])
    ])

def rtesind_sin_estado():
    import dash
    a2 = DjangoDash("Ex2",)

    a2.layout = html.Div([
        dcc.RadioItems(id="dropdown-one",options=[{'label':i,'value':j} for i,j in [
        ("O2","Oxygen"),("N2","Nitrogen"),("CO2","Carbon Dioxide")]
        ],value="Oxygen"),
        html.Div(id="output-one")
        ])
    """
    @a2.callback(
    dash.dependencies.Output('output-one','children'),
    [dash.dependencies.Input('dropdown-one','value')]
    )
    def callback_c(*args, **kwargs):
        return "Args are [%s], the extra parameter  and kwargs are %s" %(",".join(args), kwargs)
    """
    @a2.callback(
    dash.dependencies.Output('output-one','children'),
    [dash.dependencies.Input('dropdown-one','value')]
    )
    def callback_c(*args,**kwargs):
        
        return "Args are [%s] and kwargs are %s" %(",".join(args), kwargs)
