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
from apps.graph.test.utils.crum import get_empresa,get_data_connection
from apps.graph.test.data import data_comercial
from apps.graph.test.utils.functions.functions_transform import *
from apps.graph.test.Connection.apis import connection_api
from crum import get_current_user
from apps.graph.test.utils.crum import get_empresa
"""""""""""" #MODIFICAR EN EL ETL COMERCIAL




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
    'Moneda':{'tipo_componente':'select'},
    'Cultivo':{'tipo_componente':'select'},
    'Variedad':{'tipo_componente':'select'},
    
}

input_ventas_samplast={
    'Año':{'tipo_componente':'select'},
    'Cliente':{'tipo_componente':'select'},
    'Grupo Producto':{'tipo_componente':'select'},
    'Moneda':{'tipo_componente':'select'},
    
    
}
#anio_campania = sorted(df_ventas_detalle['YEAR'].unique())

def informeComercial(codigo= '',rubro_empresa = 'Agricola'):
    dff = connection_api(test='no')
    df_ventas_detalle = etl_comercial(dff)
    df_ventas_detalle.to_parquet("ventas_detalle.parquet")
    
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
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
                                                    id_maximize = 'maximize-bar-comercial-productos',
                                                    id_item = 'first'
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
                                                id_maximize = 'maximize-pie-comercial-vendedor',
                                                
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
    create_callback_filter_comercial_informe(app = app,dataframe =df_ventas_detalle, rubro= rubro_empresa)    
    create_title_comercial_informe(app=app,title='Informe de Ventas ', rubro= rubro_empresa)
    create_callback_download_data(app)
    create_graph_informe_comercial(app)
    create_callback_opened_modal(app, modal_id="modal-bar-comercial-productos",children_out_id="bar-comercial-productos", id_button="maximize-bar-comercial-productos",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-bar-comercial-mes",children_out_id="bar-comercial-mes", id_button="maximize-bar-comercial-mes",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-pie-comercial-pais",children_out_id="pie-comercial-pais", id_button="maximize-pie-comercial-pais",height_modal=600)
    create_callback_opened_modal(app, modal_id="modal-pie-comercial-vendedor",children_out_id="pie-comercial-vendedor", id_button="maximize-pie-comercial-vendedor",height_modal=600)
    create_callback_opened_modal(app, modal_id="modal-funnel-comercial-selector_second",children_out_id="funnel-comercial-selector_second", id_button="maximize-funnel-comercial-selector_second",height_modal=700)

def ventaSegmented(codigo = '',rubro_empresa = 'Agricola', filtros = input_dict_general ):
    #df_ventas_detalle = data_comercial(empresa=get_empresa())
    #dff = connection_api(test='si')
    
    dff = connection_api(test='no')
    df_ventas_detalle = etl_comercial(dff)
    
    #df_ventas_detalle=etl_comercial(dff)
    print(df_ventas_detalle.columns)
    id_list = extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id') 
    id_list_title=extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id',for_title=True) 
    app = DjangoDash(name=codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Container([
        Modal(id="modal-line-comercial-st", size= "85%"),
        Modal(id="modal-pie-comercial", size= "65%"),
        Modal(id="modal-bar-comercial", size= "90%"),
        
        block_offcanvas_comercial_filter(dict_filtros = filtros, diccionario_componentes= dict_components_comercial()),
        Row([
                Column([
                    Button.btnFilter(style={'position': 'absolute','z-index': '99'}),
                    dmc.Title(children=['Seguimiento de Ventas'],order=2,align='center')
                    #Div(id='title')
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
                                                id_maximize = 'maximize-line-comercial-st',
                                                height=300
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
                                                id_maximize = 'maximize-pie-comercial',
                                                height=300
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
    #create_title_comercial_informe(app=app,title='Seguimiento de Ventas ')#, id_inputs=id_list_title
    create_graph_comercial_segmented(app=app)
    create_callback_opened_modal(app, modal_id="modal-line-comercial-st",children_out_id="line-comercial-st", id_button="maximize-line-comercial-st")
    create_callback_opened_modal(app, modal_id="modal-pie-comercial",children_out_id="pie-comercial", id_button="maximize-pie-comercial")
    create_callback_opened_modal(app, modal_id="modal-bar-comercial",children_out_id="bar-comercial", id_button="maximize-bar-comercial",height_modal=600)


def ventasClientes(codigo = '',rubro_empresa = 'Agricola', filtros = input_ventas_x ):
    #df_ventas_detalle = data_comercial(empresa=get_empresa())
    #dff = connection_api(test='si')
    
    dff = connection_api(test='no')
    df_ventas_detalle = etl_comercial(dff)
    
    #df_ventas_detalle=etl_comercial(dff)
    
    id_list = extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id') 
    id_list_title=extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id',for_title=True) 
    app = DjangoDash(name=codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Container([
        Modal(id="modal-bar-comercial", size= "85%"),
        Modal(id="modal-bar-secundario-comercial", size= "85%"),
        Modal(id="modal-line-comercial-st", size= "85%"),
        block_offcanvas_comercial_filter(dict_filtros = filtros, diccionario_componentes= dict_components_comercial(),
                                        add_filter =[
                                            dmc.Divider(variant="solid"),
                                            dmc.Text("% de Clientes Mostrados", size="14",weight=500),
                                            Entry.slider(id = 'slider-percent', value = 10 , 
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
                    dmc.Title(children=['Ventas Clientes'],order=2,align='center')               
                    #Div(id='title')
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
                
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-comercial', id_maximize = 'maximize-bar-comercial',height=800))
                #DataDisplay.loadingOverlay(cardGraphwithfilter(id_maximize='maximize-bar-comercial',id_graph='bar-comercial',slider_id ='id-slider'))
                
            ],size=5),
            Column([
                Row([
                    Column([
                    cardSection(text='Total de Ventas',radius='xs',icon="ion:cash-outline",id_value='card-1')
                    
                    ],size=3),
                    
                    Column([
                    cardSection(text='Total de Clientes',radius='xs',icon="ion:person",id_value='card-2')
                    
                    ],size=3),
                    Column([
                    cardSection(text='N° de Paises',radius='xs',icon="ion:earth-outline",id_value='card-3')
                    
                    ],size=3),
                    Column([
                    cardSection(text='N° de Vendedores',radius='xs',icon="ion:people-circle-outline",id_value='card-4')
                    
                    ],size=3)
                     
                ]), 
               Row([
                    Column([
                        Picking.segmented(id='segmented-bar-categoria',value='Producto',data=[  {'label': 'Producto', 'value': 'Producto'},
                                                                            {'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},   
                                                                            {'label': 'Pais', 'value': 'Pais'},
                                                                            {'label': 'Vendedor', 'value': 'Vendedor'}]),
                        DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-secundario-comercial', id_maximize = 'maximize-bar-secundario-comercial',height=300))
                    ])
                
                ]), 
               Row([
                    Column([
                        Picking.segmented(id='segmented-st',value='Mes',data=[  {'label': 'Mensual', 'value': 'Mes'},
                                                                            {'label': 'Trimestral', 'value': 'Trimestre'},
                                                                            {'label': 'Semanal', 'value': 'Semana'},
                                                                            {'label': 'Fecha', 'value': 'Fecha'}]),
                        DataDisplay.loadingOverlay(cardGraph(id_graph = 'line-comercial-st', id_maximize = 'maximize-line-comercial-st',height=300))
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
    #create_title_comercial_informe(app=app,title='Ventas Clientes ', id_inputs=id_list_title)
    create_graph_comercial_bar(app)
    create_graph_comercial_crossfiltering(app=app)
    create_callback_opened_modal(app, modal_id="modal-bar-comercial",children_out_id="bar-comercial", id_button="maximize-bar-comercial",height_modal=900)
    create_callback_opened_modal(app, modal_id="modal-bar-secundario-comercial",children_out_id="bar-secundario-comercial", id_button="maximize-bar-secundario-comercial",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-line-comercial-st",children_out_id="line-comercial-st", id_button="maximize-line-comercial-st",height_modal=700)
    
def ventasProductos(codigo = '',rubro_empresa = 'Agricola', filtros = input_ventas_x ):
    #df_ventas_detalle = data_comercial(empresa=get_empresa())
    #dff = connection_api(test='si')
    
    dff = connection_api(test='no')
    df_ventas_detalle = etl_comercial(dff)
    
    #df_ventas_detalle=etl_comercial(dff)
    
    id_list = extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id') 
    id_list_title=extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id',for_title=True) 
    app = DjangoDash(name=codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Container([
        Modal(id="modal-bar-comercial", size= "85%"),
        Modal(id="modal-bar-secundario-comercial", size= "85%"),
        Modal(id="modal-line-comercial-st", size= "85%"),
        block_offcanvas_comercial_filter(dict_filtros = filtros, diccionario_componentes= dict_components_comercial(),
                                        add_filter =[
                                            dmc.Divider(variant="solid"),
                                            dmc.Text("% de Productos Mostrados", size="14",weight=500),
                                            Entry.slider(id = 'slider-percent', value = 10 , 
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
                    dmc.Title(children=['Ventas Productos'],order=2,align='center')  
                    #Div(id='title')
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
                
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-comercial', id_maximize = 'maximize-bar-comercial',height=800))
                #DataDisplay.loadingOverlay(cardGraphwithfilter(id_maximize='maximize-bar-comercial',id_graph='bar-comercial',slider_id ='id-slider'))
                
            ],size=5),
            Column([
                Row([
                    Column([
                    cardSection(text='Total de Ventas',radius='xs',icon="ion:cash-outline",id_value='card-1')
                    
                    ],size=3),
                    
                    Column([
                    cardSection(text='Total de Productos',radius='xs',icon="",id_value='card-2')
                    
                    ],size=3),
                    Column([
                    cardSection(text='N° de Paises',radius='xs',icon="ion:earth-outline",id_value='card-3')
                    
                    ],size=3),
                    Column([
                    cardSection(text='N° de Vendedores',radius='xs',icon="ion:people-circle-outline",id_value='card-4')
                    
                    ],size=3)
                     
                ]), 
               Row([
                    Column([
                        Picking.segmented(id='segmented-bar-categoria',value='Cliente',data=[  {'label': 'Cliente', 'value': 'Cliente'},
                                                                            {'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},   
                                                                            {'label': 'Pais', 'value': 'Pais'},
                                                                            {'label': 'Vendedor', 'value': 'Vendedor'}]),
                        DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-secundario-comercial', id_maximize = 'maximize-bar-secundario-comercial',height=300))
                    ])
                
                ]), 
               Row([
                    Column([
                        Picking.segmented(id='segmented-st',value='Mes',data=[  {'label': 'Mensual', 'value': 'Mes'},
                                                                            {'label': 'Trimestral', 'value': 'Trimestre'},
                                                                            {'label': 'Semanal', 'value': 'Semana'},
                                                                            {'label': 'Fecha', 'value': 'Fecha'}]),
                        DataDisplay.loadingOverlay(cardGraph(id_graph = 'line-comercial-st', id_maximize = 'maximize-line-comercial-st',height=300))
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
    #create_title_comercial_informe(app=app,title='Ventas Productos ', id_inputs=id_list_title)
    create_graph_comercial_bar(app,columns_top='Producto')
    create_graph_comercial_crossfiltering(app=app,column = 'Producto')
    create_callback_opened_modal(app, modal_id="modal-bar-comercial",children_out_id="bar-comercial", id_button="maximize-bar-comercial",height_modal=900)
    create_callback_opened_modal(app, modal_id="modal-bar-secundario-comercial",children_out_id="bar-secundario-comercial", id_button="maximize-bar-secundario-comercial",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-line-comercial-st",children_out_id="line-comercial-st", id_button="maximize-line-comercial-st",height_modal=700)
    
    
def ventasCultivos(codigo = '',rubro_empresa = 'Agricola', filtros = input_ventas_x ):
    #df_ventas_detalle = data_comercial(empresa=get_empresa())
    #dff = connection_api(test='si')
    
    dff = connection_api(test='no')
    df_ventas_detalle = etl_comercial(dff)
    
    #df_ventas_detalle=etl_comercial(dff)
    
    id_list = extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id') 
    id_list_title=extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id',for_title=True) 
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Container([
        Modal(id="modal-bar-comercial", size= "85%"),
        Modal(id="modal-bar-secundario-comercial", size= "85%"),
        Modal(id="modal-line-comercial-st", size= "85%"),
        block_offcanvas_comercial_filter(dict_filtros = filtros, diccionario_componentes= dict_components_comercial(),
                                        add_filter =[
                                            dmc.Divider(variant="solid"),
                                            dmc.Text("% de Cultivos Mostrados", size="14",weight=500),
                                            Entry.slider(id = 'slider-percent', value =100 , 
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
                    dmc.Title(children=['Ventas Cultivos'],order=2,align='center')  
                    #Div(id='title')
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
                
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-comercial', id_maximize = 'maximize-bar-comercial',height=800))
                #DataDisplay.loadingOverlay(cardGraphwithfilter(id_maximize='maximize-bar-comercial',id_graph='bar-comercial',slider_id ='id-slider'))
                
            ],size=5),
            Column([
                Row([
                    Column([
                    cardSection(text='Total de Ventas',radius='xs',icon="ion:cash-outline",id_value='card-1')
                    
                    ],size=3),
                    
                    Column([
                    cardSection(text='Total de Cultivos',radius='xs',icon="ion:leaf-outline",id_value='card-2')
                    
                    ],size=3),
                    Column([
                    cardSection(text='N° de Paises',radius='xs',icon="ion:earth-outline",id_value='card-3')
                    
                    ],size=3),
                    Column([
                    cardSection(text='N° de Vendedores',radius='xs',icon="ion:people-circle-outline",id_value='card-4')
                    
                    ],size=3)
                     
                ]), 
               Row([
                    Column([
                        Picking.segmented(id='segmented-bar-categoria',value='Cliente',data=[  
                                                                            {'label': 'Cliente', 'value': 'Cliente'},
                                                                            {'label': 'Producto', 'value': 'Producto'},
                                                                            {'label': 'Grupo Producto', 'value': 'Grupo Producto'},
                                                                            {'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},   
                                                                            {'label': 'Pais', 'value': 'Pais'},
                                                                            {'label': 'Vendedor', 'value': 'Vendedor'}]),
                        DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-secundario-comercial', id_maximize = 'maximize-bar-secundario-comercial',height=300))
                    ])
                
                ]), 
               Row([
                    Column([
                        Picking.segmented(id='segmented-st',value='Mes',data=[  {'label': 'Mensual', 'value': 'Mes'},
                                                                            {'label': 'Trimestral', 'value': 'Trimestre'},
                                                                            {'label': 'Semanal', 'value': 'Semana'},
                                                                            {'label': 'Fecha', 'value': 'Fecha'}]),
                        DataDisplay.loadingOverlay(cardGraph(id_graph = 'line-comercial-st', id_maximize = 'maximize-line-comercial-st',height=300))
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
    #create_title_comercial_informe(app=app,title='Ventas Cultivos ', id_inputs=id_list_title)
    create_graph_comercial_bar(app,columns_top='Cultivo')
    create_graph_comercial_crossfiltering(app=app,column = 'Cultivo')
    create_callback_opened_modal(app, modal_id="modal-bar-comercial",children_out_id="bar-comercial", id_button="maximize-bar-comercial",height_modal=900)
    create_callback_opened_modal(app, modal_id="modal-bar-secundario-comercial",children_out_id="bar-secundario-comercial", id_button="maximize-bar-secundario-comercial",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-line-comercial-st",children_out_id="line-comercial-st", id_button="maximize-line-comercial-st",height_modal=700)
    
def ventasComparativo(codigo = '',rubro_empresa = 'Agricola', filtros = input_ventas_x ):
    #df_ventas_detalle = data_comercial(empresa=get_empresa())
    #dff = connection_api(test='si')
    
    dff = connection_api(test='no')
    df_ventas_detalle = etl_comercial(dff)
    
    #df_ventas_detalle=etl_comercial(dff)
    
    df_ventas_detalle['Año']=df_ventas_detalle['Año'].astype("string")
    year_list=sorted(df_ventas_detalle['Año'].unique())
    dict_year=dict(zip(year_list,px.colors.qualitative.Antique))
    
    id_list = extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id') 
    id_list_title=extraer_list_value_dict (dict_input = filtros, dict_componentes= dict_components_comercial(), tipe_value='id',for_title=True) 
    app = DjangoDash(name =  codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    
    
    app.layout = Container([
        Modal(id="modal-pie-year-comparativo", size= "75%"),
        Modal(id="modal-bar-st-comparativo", size= "90%"),
        block_offcanvas_comercial_filter(dict_filtros = filtros, diccionario_componentes= dict_components_comercial()),
        Row([
            Column([
                Button.btnFilter(style={'position': 'absolute','z-index': '99'}),  
                dmc.Title(children=['Comparativo de Ventas Anuales'],order=2,align='center'),                  
                Div(id='title')
            ],size=8),
            Column([
                 dmc.MultiSelect(id="multiselect-year",label="Seleccione Años",value=[str(year_list[-2]), str(year_list[-3])],data=year_list,size='lg'),
                #Div(content=[Entry.multiSelect(id = 'multiselect-year',texto = 'Seleccione Años', data = year_list, value = [str(year_list[-2]), str(year_list[-3])])])
            ],size=4)
        ]),
        Row([
            Column([
                DataDisplay.loadingOverlay(
                    tableDag(id ='tabla-interactiva',dashGridOptions={"rowSelection": "multiple"}, style={'font-size':14, 'height': 350, "width": "100%"},column_size=None )
                )
            ],size = 3),
            Column([ 
                    DataDisplay.loadingOverlay(
                        tableDag(id ='tabla-resultado',dashGridOptions={"rowSelection": "multiple"}, style={'font-size':14, 'height': 350},column_size=None )
                        
                    )
            ],size = 6),
            Column([
                 DataDisplay.loadingOverlay(cardGraph(id_graph = 'pie-year-comparativo', id_maximize = 'maximize-pie-year-comparativo'))
            ],size = 3),
        ]),
        Row([
            Column([
             Picking.segmented(id='segmented-st',value='Mes Num',data=[  {'label': 'Mensual', 'value': 'Mes Num'},
                                                                        {'label': 'Trimestral', 'value': 'Trimestre_'},
                                                                        {'label': 'Semanal', 'value': 'Semana_'},]),
             DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-st-comparativo', id_maximize = 'maximize-bar-st-comparativo'))
            ],size = 12)
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
    ])
    create_callback_offcanvas_filters(app)
    create_callback_filter_comercial_simple(app, dataframe=df_ventas_detalle,id_inputs= id_list, id_outputs= id_list)
    create_title_comercial_informe(app=app,title='', id_inputs=id_list_title)
    callback_table_interactive(app,list_empty = [],dict_year = dict_year)
    callback_table_resultado(app, list_for_graph = [],dict_colors= dict_year)
    create_callback_opened_modal(app, modal_id="modal-pie-year-comparativo",children_out_id="pie-year-comparativo", id_button="maximize-pie-year-comparativo",height_modal=600)
    create_callback_opened_modal(app, modal_id="modal-bar-st-comparativo",children_out_id="pie-bar-st-comparativo", id_button="maximize-bar-st-comparativo",height_modal=700)
    
