from django_plotly_dash import DjangoDash
from apps.graph.test.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from apps.graph.test.utils.theme import themeProvider, Container
from apps.graph.test.utils.frame import Column, Row, Div, Store, Download, Modal,Modal
from apps.graph.test.utils.components.components_main import Entry, Button, DataDisplay,Picking
from apps.graph.test.utils.blocks.block_filters import block_comercial_filters_IV,block_offcanvas_comercial_filter,offcanvas_comercial_config
from apps.graph.test.utils.tables import tableDag
from apps.graph.test.utils.functions.callbacks.callbacks_comercial import *
from apps.graph.test.utils.blocks.block_card import cardGraph,cardSection,cardGraphwithfilter
from apps.graph.test.utils.functions.callbacks.callbacks_ import *
from apps.graph.test.utils.components.components_filters import dict_components_comercial, datepicker_
from apps.graph.test.utils.functions.functions_dict import extraer_list_value_dict

from apps.graph.test.constans import MESES_ORDER
from crum import get_current_user
"""""""""""" #MODIFICAR EN EL ETL COMERCIAL
df_ventas_detalle=pd.read_parquet('comercial_new_etl.parquet', engine='pyarrow')
df_ventas_detalle['Tipo de Movimiento'] = df_ventas_detalle['Tipo de Movimiento'].astype(object)
df_ventas_detalle['Tipo de Venta'] = df_ventas_detalle['Tipo de Venta'].astype(object)
df_ventas_detalle['Tipo de Condicion'] = df_ventas_detalle['Tipo de Condicion'].astype(object)
df_ventas_detalle['Grupo Producto'] = df_ventas_detalle['Grupo Producto'].astype(object)
df_ventas_detalle['Subgrupo Producto'] = df_ventas_detalle['Subgrupo Producto'].astype(object)
df_ventas_detalle['Vendedor'] = df_ventas_detalle['Vendedor'].astype(object)

df_ventas_detalle['Tipo de Movimiento'] = df_ventas_detalle['Tipo de Movimiento'].fillna('NO ESPECIFICADO')
df_ventas_detalle['Tipo de Venta'] = df_ventas_detalle['Tipo de Venta'].fillna('NO ESPECIFICADO')
df_ventas_detalle['Tipo de Condicion'] = df_ventas_detalle['Tipo de Condicion'].fillna('NO ESPECIFICADO')
df_ventas_detalle['Grupo Producto'] = df_ventas_detalle['Grupo Producto'].fillna('NO ESPECIFICADO')
df_ventas_detalle['Subgrupo Producto'] = df_ventas_detalle['Subgrupo Producto'].fillna('NO ESPECIFICADO')
df_ventas_detalle['Vendedor'] = df_ventas_detalle['Vendedor'].fillna('NO ESPECIFICADO')

df_ventas_detalle['Cliente']=df_ventas_detalle['Cliente'].str[:30]
df_ventas_detalle['Producto']=df_ventas_detalle['Producto'].str[:30]
#.str[:30]

df_ventas_detalle['Fecha']=df_ventas_detalle['Fecha'].apply(lambda a: pd.to_datetime(a).date())

input_dict_general={
    'Año':{'tipo_componente':'select'},
    'Cliente':{'tipo_componente':'select'},
    'Cultivo':{'tipo_componente':'select'},
    'Variedad':{'tipo_componente':'select'},
    'Grupo Producto':{'tipo_componente':'select'},
    'Moneda':{'tipo_componente':'select'}
}


input_ventas_x={
    
    'Cliente':{'tipo_componente':'select'},
    'Grupo Producto':{'tipo_componente':'select'},
    'Moneda':{'tipo_componente':'select'}
}
#anio_campania = sorted(df_ventas_detalle['YEAR'].unique())

def informeComercial(rubro_empresa = 'Agricola'):
    
    app = DjangoDash('informe-comercial',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Modal(id="modal-bar-comercial-productos", size= "85%"),
        Modal(id="modal-bar-comercial-mes", size= "85%"),
        Modal(id="modal-pie-comercial-pais", size= "85%"),
        Modal(id="modal-pie-comercial-vendedor", size= "85%"),
        Modal(id="modal-funnel-comercial-selector_second", size= "85%"),
        Row([
                
                Column([
                    Div(id='title')
                ],size=10),
                Column([Button.btnDownload()],size=1),
                Column([Button.btnConfig()],size=1),
        ]),
        
        offcanvas_comercial_config,
        #block_comercial_filters_IV(rubro= rubro_empresa),
        Row([
            Column([
              block_comercial_filters_IV(rubro= rubro_empresa, orientation = 'v')      
            ],size=2),
            
            Column([
                Row([
                    Column([
                            Entry.chipGroup(id='chipgroup-mes')
                    ]),
                ]),
                
                Row([
                    Column([
                            Row([
                        
                                    Column([
                                            DataDisplay.loadingOverlay(
                                                cardGraph(
                                                    id_graph='bar-comercial-productos', 
                                                    id_maximize = 'maximize-bar-comercial-productos'
                                                )
                                            )
                                    ]) 
                            ]),
                            Row([
                                Column([
                                    DataDisplay.loadingOverlay(
                                            cardGraph(
                                                id_graph = 'bar-comercial-mes', 
                                                id_maximize = 'maximize-bar-comercial-mes'
                                            )
                                    )
                                ]) 
                                
                            ])
                    ],size=6),
                    Column([
                            Row([
                                Column([    
                                    DataDisplay.loadingOverlay(
                                            cardGraph(
                                                id_graph = 'pie-comercial-pais', 
                                                id_maximize = 'maximize-pie-comercial-pais'
                                            )
                                    )
                                ],size=6), 
                                Column([    
                                    DataDisplay.loadingOverlay(
                                            cardGraph(
                                                id_graph = 'pie-comercial-vendedor', 
                                                id_maximize = 'maximize-pie-comercial-vendedor'
                                            )
                                    )
                                ],size=6) 
                            ]),
                            Row([
                                Column([
                                    DataDisplay.loadingOverlay(
                                            cardGraph(
                                                id_graph='funnel-comercial-selector_second', 
                                                id_maximize = 'maximize-funnel-comercial-selector_second'
                                            )
                                        )
                                ]) 
                                  
                            ])   
                    ],size=6)
                ]),
                
                
                
                
                
            ],size=10),
                
        ]),
    Div(id='notifications-update-data'),
    Store(id='data-values'),
    Download(),
    Modal(id='modal'),    
    ])
    create_callback_offcanvas_filters(app,id_input_btn = "btn-config")
    create_callback_filter_comercial_informe(app = app,dataframe =df_ventas_detalle)    
    create_title_comercial_informe(app=app,title='Informe de Ventas ')
    create_callback_download_data(app)
    create_graph_informe_comercial(app)
    create_callback_opened_modal(app, modal_id="modal-bar-comercial-productos",children_out_id="bar-comercial-productos", id_button="maximize-bar-comercial-productos",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-bar-comercial-mes",children_out_id="bar-comercial-mes", id_button="maximize-bar-comercial-mes",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-pie-comercial-pais",children_out_id="pie-comercial-pais", id_button="maximize-pie-comercial-pais",height_modal=600)
    create_callback_opened_modal(app, modal_id="modal-pie-comercial-vendedor",children_out_id="pie-comercial-vendedor", id_button="maximize-pie-comercial-vendedor",height_modal=600)
    create_callback_opened_modal(app, modal_id="modal-funnel-comercial-selector_second",children_out_id="funnel-comercial-selector_second", id_button="maximize-funnel-comercial-selector_second",height_modal=700)

def ventaSegmented(rubro_empresa = 'Agricola', filtros = input_dict_general ):
    id_list = extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id') 
    id_list_title=extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id',for_title=True) 
    app = DjangoDash('segmented-comercial',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)

    app.layout = Container([
        Modal(id="modal-line-comercial-st", size= "85%"),
        Modal(id="modal-pie-comercial", size= "65%"),
        Modal(id="modal-bar-comercial", size= "90%"),
        
        block_offcanvas_comercial_filter(dict_filtros = filtros, diccionario_componentes= dict_components_comercial()),
        Row([
                Column([
                    Button.btnFilter(style={'position': 'absolute','z-index': '99'}),
                    
                    Div(id='title')
                ],size=11),
                Column([Button.btnDownload()],size=1),
                
        ]),
        Row([
            Column([Entry.chipGroup(id='chipgroup-mes')])
        ]),
        Row([
            Column([
                Picking.segmented(id='segmented-st',value='Mes',data=[  {'label': 'Mensual', 'value': 'Mes'},
                                                                            {'label': 'Trimestral', 'value': 'Trimestre'},
                                                                            {'label': 'Semanal', 'value': 'Semana'},
                                                                            {'label': 'Fecha', 'value': 'Fecha'}]),
                DataDisplay.loadingOverlay(
                                            cardGraph(
                                                id_graph = 'line-comercial-st', 
                                                id_maximize = 'maximize-line-comercial-st'
                                            )
                                    )
            ],size=7),
            Column([
                Picking.segmented(id='segmented-pie',value='Vendedor',data=[  {'label': 'Vendedor', 'value': 'Vendedor'},
                                                                            {'label': 'País', 'value': 'Pais'},
                                                                            {'label': 'Sucursal', 'value': 'Sucursal'},
                                                                            {'label': 'Mes', 'value': 'Mes'}]),
                DataDisplay.loadingOverlay(
                                            cardGraph(
                                                id_graph = 'pie-comercial', 
                                                id_maximize = 'maximize-pie-comercial'
                                            )
                                    )
            
            ],size=5),
        ]),
            Row([
                Column([
                Picking.segmented(id='segmented-bar',value='Tipo de Venta',data=[  {'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},
                                                                                    {'label': 'Producto', 'value': 'Producto'},
                                                                                    {'label': 'Grupo Producto', 'value': 'Grupo Producto'},
                                                                                    {'label': 'Cliente', 'value': 'Cliente'},
                                                                                    {'label': 'Grupo Cliente', 'value': 'Grupo Cliente'},
                                                                            ]),
                DataDisplay.loadingOverlay(
                                            cardGraph(
                                                id_graph = 'bar-comercial', 
                                                id_maximize = 'maximize-bar-comercial'
                                            )
                                    )
            ],size=10),
            Column([
               cardSection(text = 'Configurador Bar', color_text ='black',color_section_title = 'white',contenido ='tabla',color_section_content= '#d6d9db',
                    content = [
                        dmc.Checkbox(id="checkbox-ticked", label="Mostrar Tickeds", mb=10, checked=True,size="md"),
                        dmc.Text("% del Total del Importe", size="14",weight=500),
                        Entry.slider(id = 'slider-percent', value = 80 , 
                                     marks = [{"value": 20, "label": "20%"},
                                              {"value": 50, "label": "50%"},
                                              {"value": 80, "label": "80%"}], 
                                     label_tick = False,  step = 1,
                                      minimo = 0, maximo = 100),
                        
                    ],padding_section=25)

            ],size=2),
            
        
        ]),
    Div(id='notifications-update-data'),
    Store(id='data-values'),
    Download(),
        
    ])
    #{'Año' : {'select':{'id':'select-anio','componente':select_anio},'multiselect':multiselect_anio}}
    create_callback_offcanvas_filters(app)
    create_callback_filter_comercial_segmented(app, dataframe=df_ventas_detalle,id_inputs= id_list, id_outputs= id_list)
    create_title_comercial_informe(app=app,title='Seguimiento de Ventas ', id_inputs=id_list_title)
    create_graph_comercial_segmented(app=app)
    create_callback_opened_modal(app, modal_id="modal-line-comercial-st",children_out_id="line-comercial-st", id_button="maximize-line-comercial-st")
    create_callback_opened_modal(app, modal_id="modal-pie-comercial",children_out_id="pie-comercial", id_button="maximize-pie-comercial")
    create_callback_opened_modal(app, modal_id="modal-bar-comercial",children_out_id="bar-comercial", id_button="maximize-bar-comercial",height_modal=600)


def ventasClientes(rubro_empresa = 'Agricola', filtros = input_ventas_x ):
    id_list = extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id') 
    id_list_title=extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id',for_title=True) 
    app = DjangoDash('clientes-comercial',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)

    app.layout = Container([
        Modal(id="modal-bar-comercial", size= "85%"),
        Modal(id="modal-bar-secundario-comercial", size= "85%"),
        Modal(id="modal-line-comercial-st", size= "85%"),
        block_offcanvas_comercial_filter(dict_filtros = filtros, diccionario_componentes= dict_components_comercial(),
                                        add_filter =[
                                            dmc.Divider(variant="solid"),
                                            dmc.Text("% de Clientes Mostrados", size="14",weight=500),
                                            Entry.slider(id = 'slider-percent', value = 20 , 
                                                        marks = [{"value": 20, "label": "20%"},
                                                                {"value": 50, "label": "50%"},
                                                                {"value": 80, "label": "80%"}], 
                                                        label_tick = False,  step = 10,
                                                        minimo = 10, maximo = 100),
                                        ]
        ),
        Row([
            Column([
                    Button.btnFilter(style={'position': 'absolute','z-index': '99'}),                    
                    Div(id='title')
            ],size=8),
            Column([
                datepicker_(dataframe=df_ventas_detalle, name_fecha = 'Fecha', name_anio = 'Año', tipo = 'Inicio')
            ],size=2),
            Column([
                datepicker_(dataframe=df_ventas_detalle, name_fecha = 'Fecha', name_anio = 'Año', tipo = 'Fin')
            ],size=2),
        ]),
        Row([
            Column([
                
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-comercial', id_maximize = 'maximize-bar-comercial'))
                #DataDisplay.loadingOverlay(cardGraphwithfilter(id_maximize='maximize-bar-comercial',id_graph='bar-comercial',slider_id ='id-slider'))
                
            ],size=5),
            Column([
                Row([
                    Column([
                    cardSection(text='Total de Ventas',radius='xs',icon="ion:cash-outline",id_value='card-total')
                    
                    ],size=3),
                    
                    Column([
                    cardSection(text='Total de Clientes',radius='xs',icon="ion:person",id_value='card-clientes')
                    
                    ],size=3),
                    Column([
                    cardSection(text='N° de Paises',radius='xs',icon="ion:earth-outline",id_value='card-pais')
                    
                    ],size=3),
                    Column([
                    cardSection(text='N° de Vendedores',radius='xs',icon="ion:people-circle-outline",id_value='card-vendedor')
                    
                    ],size=3)
                     
                ]), 
               Row([
                    Column([
                        Picking.segmented(id='segmented-bar-categoria',value='Producto',data=[  {'label': 'Producto', 'value': 'Producto'},
                                                                            {'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},   
                                                                            {'label': 'Pais', 'value': 'Pais'},
                                                                            {'label': 'Vendedor', 'value': 'Vendedor'}]),
                        DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-secundario-comercial', id_maximize = 'maximize-bar-secundario-comercial'))
                    ])
                
                ]), 
               Row([
                    Column([
                        Picking.segmented(id='segmented-st',value='Mes',data=[  {'label': 'Mensual', 'value': 'Mes'},
                                                                            {'label': 'Trimestral', 'value': 'Trimestre'},
                                                                            {'label': 'Semanal', 'value': 'Semana'},
                                                                            {'label': 'Fecha', 'value': 'Fecha'}]),
                        DataDisplay.loadingOverlay(cardGraph(id_graph = 'line-comercial-st', id_maximize = 'maximize-line-comercial-st'))
                    ])
                
                ]), 
            ],size=7),
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
    ])
    create_callback_offcanvas_filters(app)
    create_callback_filter_comercial_ventas(app, dataframe=df_ventas_detalle,id_inputs= id_list, id_outputs= id_list)
    create_title_comercial_informe(app=app,title='Ventas Clientes ', id_inputs=id_list_title)
    create_graph_comercial_bar(app)
    create_graph_comercial_crossfiltering(app=app)
    create_callback_opened_modal(app, modal_id="modal-bar-comercial",children_out_id="bar-comercial", id_button="maximize-bar-comercial",height_modal=900)
    create_callback_opened_modal(app, modal_id="modal-bar-secundario-comercial",children_out_id="bar-secundario-comercial", id_button="maximize-bar-secundario-comercial",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-line-comercial-st",children_out_id="line-comercial-st", id_button="maximize-line-comercial-st",height_modal=700)