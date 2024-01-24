from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *
from ..components.block_comp import *
from ..components.group_comp import *
from ..components.dict_sp_comp import nsp_rpt_ventas_detallado_comp
#####
TIEMPO_DIMENSION = [  {'label': 'Mensual', 'value': 'Mes'}, {'label': 'Trimestral', 'value': 'Trimestre'},{'label': 'Semanal', 'value': 'Semana'},{'label': 'Fecha', 'value': 'Fecha'}]
DIMENSION_PIE = [{'label': 'Vendedor', 'value': 'Vendedor'},{'label': 'País', 'value': 'Pais'},{'label': 'Sucursal', 'value': 'Sucursal'},{'label': 'Mes', 'value': 'Mes'}]
DIMESION_BAR = [{'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},{'label': 'Producto', 'value': 'Producto'},{'label': 'Grupo Producto', 'value': 'Grupo Producto'},{'label': 'Cliente', 'value': 'Cliente'},{'label': 'Grupo Cliente', 'value': 'Grupo Cliente'}]
DIMENSION_CATEGORIA_CLIENTE = [{'label': 'Producto', 'value': 'Producto'},{'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},   {'label': 'Pais', 'value': 'Pais'},{'label': 'Vendedor', 'value': 'Vendedor'}]
DIMENSION_CATEGORIA_PRODUCTO = [{'label': 'Cliente', 'value': 'Cliente'},{'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},   {'label': 'Pais', 'value': 'Pais'},{'label': 'Vendedor', 'value': 'Vendedor'}]
DIMENSION_CATEGORIA_CULTIVO = [{'label': 'Cliente', 'value': 'Cliente'},{'label': 'Producto', 'value': 'Producto'},{'label': 'Grupo Producto', 'value': 'Grupo Producto'},{'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},{'label': 'Pais', 'value': 'Pais'},{'label': 'Vendedor', 'value': 'Vendedor'}]
####

def informe_comercial(rubro_empresa = ''):
    return Container([
        Modal(id="modal-bar-comercial-productos", size= "85%"),
        Modal(id="modal-bar-comercial-mes", size= "85%"),
        Modal(id="modal-pie-comercial-pais", size= "85%"),
        Modal(id="modal-pie-comercial-vendedor", size= "85%"),
        Modal(id="modal-funnel-comercial-selector_second", size= "85%"),
        Row([
            Column([Div(id='title')],size=11),
            Column([Button.btnDownload()],size=1),
        ]),
        Row([
            Column([
              comercial_block_filt(rubro= rubro_empresa, orientation = 'v')      
            ],size=2),
            Column([
                Row([
                    Column([Entry.chipGroup(id = 'chipgroup-mes')])
                ]),
                Row([
                    Column([
                        Row([
                            Column([
                                DataDisplay.loadingOverlay(
                                    card_graph(
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
                                    card_graph(
                                        id_graph = 'bar-comercial-mes', 
                                        id_maximize = 'maximize-bar-comercial-mes'
                                    )
                                )
                            ])
                        ])
                        
                    ],size = 6),
                    Column([
                        Row([
                            Column([
                                DataDisplay.loadingOverlay(
                                    card_graph(
                                        id_graph = 'pie-comercial-pais', 
                                        id_maximize = 'maximize-pie-comercial-pais'
                                    )
                                )
                            ],size = 6),
                            Column([
                                DataDisplay.loadingOverlay(
                                    card_graph(
                                        id_graph = 'pie-comercial-vendedor', 
                                        id_maximize = 'maximize-pie-comercial-vendedor',
                                    )
                                )
                            ],size = 6)
                        ]),
                        
                        Row([
                            Column([
                                DataDisplay.loadingOverlay(
                                    card_graph(
                                       id_graph='funnel-comercial-selector_second', 
                                       id_maximize = 'maximize-funnel-comercial-selector_second'
                                    )
                                )
                            ])
                        ])
                    ],size = 6)    
                ]),
            ],size = 10),
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
        Modal(id='modal'),
    ])

def seguimiento_comercial(filtros = {}):
    return Container([
        Modal(id="modal-line-comercial-st", size= "85%"),
        Modal(id="modal-pie-comercial", size= "65%"),
        Modal(id="modal-bar-comercial", size= "90%"),
        comercial_offcanvas_filt(dict_filt = filtros, dict_comp = nsp_rpt_ventas_detallado_comp()),
        Row([   
            Column([
                Button.btnFilter(style = {'position': 'absolute','z-index': '99'}),
                title(text = 'Seguimiento de Ventas', order = 2, align = 'center')
            ]),
            Column([Button.btnDownload()],size=1),
        ]),
        Row([
            Column([Entry.chipGroup(id='chipgroup-mes')])
        ]),
        Row([
            Column([
                Picking.segmented(id='segmented-st',value='Mes',data = TIEMPO_DIMENSION ),
                DataDisplay.loadingOverlay(
                    card_graph(
                        id_graph = 'line-comercial-st', 
                        id_maximize = 'maximize-line-comercial-st',
                        height=300
                    )
                )
            ],size = 7),
            Column([
                Picking.segmented(id='segmented-pie',value='Vendedor',data = DIMENSION_PIE), 
                DataDisplay.loadingOverlay(
                    card_graph(
                        id_graph = 'pie-comercial', 
                        id_maximize = 'maximize-pie-comercial',
                        height=300
                    )
                )
            ],size = 5)
        ]),
        Row([
            Column([
                Picking.segmented(id = 'segmented-bar', value= 'Tipo de Venta',data = DIMESION_BAR),
                DataDisplay.loadingOverlay(
                    card_graph(
                        id_graph = 'bar-comercial', 
                        id_maximize = 'maximize-bar-comercial'
                    )
                )
            ],size = 12),

        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
    ])

def ventas_clientes(filtros = {}, dataframe = None):
    return Container([
        Modal(id="modal-bar-comercial", size= "85%"),
        Modal(id="modal-bar-secundario-comercial", size= "85%"),
        Modal(id="modal-line-comercial-st", size= "85%"),
        comercial_offcanvas_filt(dict_filt = filtros, 
                                 dict_comp = nsp_rpt_ventas_detallado_comp(),
                                 add_filter = [
                                     DataDisplay.text(text = '% de Clientes Mostrados',weight = 500, size = 14),
                                     slider_percent(value = 10)
                                ]
        ),
        Row([
            Column([
                Button.btnFilter(style = {'position': 'absolute','z-index': '99'}),
                title(text = 'Ventas Clientes', order = 2, align = 'center')
            ],size = 8),
            Column([
                datepicker_range_comercial(dataframe =  dataframe, tipo = 'Inicio')
            ],size = 2),
            Column([
                datepicker_range_comercial(dataframe =  dataframe, tipo = 'Fin')
            ],size = 2)
        ]),
        Row([
            Column([
                DataDisplay.loadingOverlay(
                    card_graph(
                        id_graph = 'bar-comercial', 
                        id_maximize = 'maximize-bar-comercial',
                        height = 800)
                )
            ],size = 5),
            Column([
                Row([
                    Column([
                        card_value(text='Total de Ventas',radius='xs',icon="ion:cash-outline",id_value='card-1')
                    ],size = 3),
                    Column([
                        card_value(text='N° de Clientes',radius='xs',icon="ion:person",id_value='card-2')
                    ],size = 3),
                    Column([
                        card_value(text='N° de Paises',radius='xs',icon="ion:earth-outline",id_value='card-3')
                    ],size = 3),
                    Column([
                        card_value(text='N° de Vendedores',radius='xs',icon="ion:people-circle-outline",id_value='card-4')
                    ],size = 3),
                ]),
                Row([
                    Column([
                        Picking.segmented(id='segmented-bar-categoria',value = 'Producto', data =  DIMENSION_CATEGORIA_CLIENTE),
                        DataDisplay.loadingOverlay(
                            card_graph(
                                id_graph = 'bar-secundario-comercial', 
                                id_maximize = 'maximize-bar-secundario-comercial',
                                height=300
                            )
                        )
                    ])
                ]),
                Row([
                    Column([
                        Picking.segmented(id='segmented-st',value='Mes',data = TIEMPO_DIMENSION),
                        DataDisplay.loadingOverlay(
                            card_graph(
                                id_graph = 'line-comercial-st', 
                                id_maximize = 'maximize-line-comercial-st',
                                height=300
                            )
                        )
                    ])
                ]),
            ],size = 7)
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
        
    ])

def ventas_productos(filtros = {}, dataframe = None):
    return Container([
        Modal(id="modal-bar-comercial", size= "85%"),
        Modal(id="modal-bar-secundario-comercial", size= "85%"),
        Modal(id="modal-line-comercial-st", size= "85%"),
        comercial_offcanvas_filt(dict_filt = filtros, 
                                 dict_comp = nsp_rpt_ventas_detallado_comp(),
                                 add_filter = [
                                     DataDisplay.text(text = '% de Productos Mostrados',weight = 500, size = 14),
                                     slider_percent(value = 10)
                                ]
        ),
        Row([
            Column([
                Button.btnFilter(style = {'position': 'absolute','z-index': '99'}),
                title(text = 'Ventas Productos', order = 2, align = 'center')
            ],size = 8),
            Column([
                datepicker_range_comercial(dataframe =  dataframe, tipo = 'Inicio')
            ],size = 2),
            Column([
                datepicker_range_comercial(dataframe =  dataframe, tipo = 'Fin')
            ],size = 2)
        ]),
        
        Row([
            Column([
                DataDisplay.loadingOverlay(
                    card_graph(
                        id_graph = 'bar-comercial', 
                        id_maximize = 'maximize-bar-comercial',
                        height = 800)
                )
            ],size = 5),
            Column([
                Row([
                    Column([
                        card_value(text='Total de Ventas',radius='xs',icon="ion:cash-outline",id_value='card-1')
                    ],size = 3),
                    Column([
                        card_value(text='N° de Productos',radius='xs',icon="ion:person",id_value='card-2')
                    ],size = 3),
                    Column([
                        card_value(text='N° de Paises',radius='xs',icon="ion:earth-outline",id_value='card-3')
                    ],size = 3),
                    Column([
                        card_value(text='N° de Vendedores',radius='xs',icon="ion:people-circle-outline",id_value='card-4')
                    ],size = 3),
                ]),
                Row([
                    Column([
                        Picking.segmented(id='segmented-bar-categoria',value = 'Producto', data =  DIMENSION_CATEGORIA_PRODUCTO),
                        DataDisplay.loadingOverlay(
                            card_graph(
                                id_graph = 'bar-secundario-comercial', 
                                id_maximize = 'maximize-bar-secundario-comercial',
                                height=300
                            )
                        )
                    ])
                ]),
                Row([
                    Column([
                        Picking.segmented(id='segmented-st',value='Mes',data = TIEMPO_DIMENSION),
                        DataDisplay.loadingOverlay(
                            card_graph(
                                id_graph = 'line-comercial-st', 
                                id_maximize = 'maximize-line-comercial-st',
                                height=300
                            )
                        )
                    ])
                ]),
            ],size = 7)
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
    ])

def ventas_cultivos(filtros = {}, dataframe = None):
    return Container([
        Modal(id="modal-bar-comercial", size= "85%"),
        Modal(id="modal-bar-secundario-comercial", size= "85%"),
        Modal(id="modal-line-comercial-st", size= "85%"),
        comercial_offcanvas_filt(dict_filt = filtros, 
                                 dict_comp = nsp_rpt_ventas_detallado_comp(),
                                 add_filter = [
                                     DataDisplay.text(text = '% de Cultivos Mostrados',weight = 500, size = 14),
                                     slider_percent(value = 10)
                                ]
        ),
        Row([
            Column([
                Button.btnFilter(style = {'position': 'absolute','z-index': '99'}),
                title(text = 'Ventas Cultivos', order = 2, align = 'center')
            ],size = 8),
            Column([
                datepicker_range_comercial(dataframe =  dataframe, tipo = 'Inicio')
            ],size = 2),
            Column([
                datepicker_range_comercial(dataframe =  dataframe, tipo = 'Fin')
            ],size = 2)
        ]),
        
        Row([
            Column([
                DataDisplay.loadingOverlay(
                    card_graph(
                        id_graph = 'bar-comercial', 
                        id_maximize = 'maximize-bar-comercial',
                        height = 800)
                )
            ],size = 5),
            Column([
                Row([
                    Column([
                        card_value(text='Total de Ventas',radius='xs',icon="ion:cash-outline",id_value='card-1')
                    ],size = 3),
                    Column([
                        card_value(text='N° de Cultivos',radius='xs',icon="ion:person",id_value='card-2')
                    ],size = 3),
                    Column([
                        card_value(text='N° de Paises',radius='xs',icon="ion:earth-outline",id_value='card-3')
                    ],size = 3),
                    Column([
                        card_value(text='N° de Vendedores',radius='xs',icon="ion:people-circle-outline",id_value='card-4')
                    ],size = 3),
                ]),
                Row([
                    Column([
                        Picking.segmented(id='segmented-bar-categoria',value = 'Producto', data =  DIMENSION_CATEGORIA_CULTIVO),
                        DataDisplay.loadingOverlay(
                            card_graph(
                                id_graph = 'bar-secundario-comercial', 
                                id_maximize = 'maximize-bar-secundario-comercial',
                                height=300
                            )
                        )
                    ])
                ]),
                Row([
                    Column([
                        Picking.segmented(id='segmented-st',value='Mes',data = TIEMPO_DIMENSION),
                        DataDisplay.loadingOverlay(
                            card_graph(
                                id_graph = 'line-comercial-st', 
                                id_maximize = 'maximize-line-comercial-st',
                                height=300
                            )
                        )
                    ])
                ]),
            ],size = 7)
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
    ])
########TEST DATA
VARIEDAD_=['Satsuma_Iwasaki', 'NO ESPECIFICADO', 'Wonderful',
       'ROJO BRILLANTE', 'Clementina Oronules', 'Zutano', 'Ettinger',
       'Nova', 'Clementina Nour', 'Washington Navel', 'Tango', 'Minneola',
       'Hass', 'Washington Tardia', 'Murcott', 'Lamb Hass', 'Bacon',
       'PECANA']



def ventas_exportacion_agro(rubro_empresa = ''):
    return Container([
        Modal(id="modal-bar-comercial-productos", size= "85%"),
        Modal(id="modal-bar-comercial-mes", size= "85%"),
        Modal(id="modal-pie-comercial-pais", size= "85%"),
        Modal(id="modal-pie-comercial-vendedor", size= "85%"),
        Modal(id="modal-funnel-comercial-selector_second", size= "85%"),
        Row([
            Column([Div(content=['test title'])],size=11),
            Column([Button.btnDownload()],size=1),
        ]),
        Row([
            Column([
                dmc.Card(
                    children=[
                        html.Div(
                        [
                            dmc.ChipGroup(
                                [
                                    dmc.Chip(
                                        x,
                                        value=x,
                                        variant="outline",
                                        styles= {
                                                    "label": {
                                                        "&[data-checked]": {
                                                            "&, &:hover": {
                                                                "backgroundColor": dmc.theme.DEFAULT_COLORS["green"][5],
                                                                "color": "white",
                                                            },
                                                        },
                                                    }
                                                }
                                    )
                                    for x in VARIEDAD_
                                ],
                                id="chips-callback",
                                value=[VARIEDAD_[0]],
                                multiple=True,
                                mb=10,
                                align='stretch'
                            ),
                            dmc.Text(id="chips-values-output"),
                        ]
                    )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    #style={"width": 350},
                )    
            
            ],size=2),
            Column([],size=9),
        ]),
    ])