from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *
from ..components.block_comp import *
from ..components.group_comp import *
from ..components.dict_sp_comp import nsp_rpt_ventas_detallado_comp
from ..utils.helpers import *
from ..components.block_comp import *
from ..components.dict_sp_comp import nsp_rpt_ventas_detallado_comp
#####
TIEMPO_DIMENSION = [  {'label': 'Mensual', 'value': 'Mes'}, {'label': 'Trimestral', 'value': 'Trimestre'},{'label': 'Semanal', 'value': 'Semana'},{'label': 'Fecha', 'value': 'Fecha'}]
DIMENSION_PIE = [{'label': 'Vendedor', 'value': 'Vendedor'},{'label': 'País', 'value': 'Pais'},{'label': 'Sucursal', 'value': 'Sucursal'},{'label': 'Mes', 'value': 'Mes'}]
DIMESION_BAR = [{'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},{'label': 'Producto', 'value': 'Producto'},{'label': 'Grupo Producto', 'value': 'Grupo Producto'},{'label': 'Cliente', 'value': 'Cliente'},{'label': 'Grupo Cliente', 'value': 'Grupo Cliente'}]
DIMENSION_CATEGORIA_CLIENTE = [{'label': 'Producto', 'value': 'Producto'},{'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},   {'label': 'Pais', 'value': 'Pais'},{'label': 'Vendedor', 'value': 'Vendedor'}]
DIMENSION_CATEGORIA_PRODUCTO = [{'label': 'Cliente', 'value': 'Cliente'},{'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},   {'label': 'Pais', 'value': 'Pais'},{'label': 'Vendedor', 'value': 'Vendedor'}]
DIMENSION_CATEGORIA_CULTIVO = [{'label': 'Cliente', 'value': 'Cliente'},{'label': 'Producto', 'value': 'Producto'},{'label': 'Grupo Producto', 'value': 'Grupo Producto'},{'label': 'Tipo de Venta', 'value': 'Tipo de Venta'},{'label': 'Pais', 'value': 'Pais'},{'label': 'Vendedor', 'value': 'Vendedor'}]
####
ELEMENTOS_DATAFRAME_PARA_FILTROS = ['Año','Producto','Cliente']
GRAF_DATA ={
    'DESCRIPCION': 'Importe Cliente',
    'TIPO_OUTPUT': 'bar',
    'VAR_CATEGORICO': ['Productos', 'Cliente'],
    'VAR_NUMERICO':['Importe Soles', 'Importe Dolares'],
    'LIMITE_ROW': 0,
    
}
DASHBOARD = {
    
}
from ...build.utils.compt_mantine import (
    Contenedor_dmc,
    titulo,
    cardHeader,
    Col
)


def informe_comercial(dict_ = {}):
    matriz_compt_output = [k for k in dict_['id_dash']['compt_output'].values()]
    return Contenedor_dmc(content=[
    
        Div([dmc.Modal(title = '', id = i, fullScreen=False, zIndex=10000, size= "85%" )for i in dict_['id_dash']['modal']]),
        cardHeader(titulo(texto=dict_['titulo_dashboard'],align = 'center',order=1,color=dict_['titulo_color'],),color_card=dict_['color_card_primary']),
        #Div([Entry.chipGroup(id='chipgroup-mes')]),
        #xs, sm, md, lg and xl 
        dmc.Grid([dmc.Col(Entry.select(id = i, texto = f, size = 'sm',clearable=True),xs=12,sm ="auto",md ="auto",lg ="auto", xl = "auto") for i,f in zip(dict_['id_dash']['compt_input'].keys(),dict_['id_dash']['compt_input'].values())]),
        dmc.Grid(children=[Col([
                card_graph_1(text=matriz_compt_output[3][i],
                            id_graph=matriz_compt_output[0][i],
                            id_maximize=f"maxi_{matriz_compt_output[0][i]}",
                            color_text = dict_['titulo_color'],
                            color_bg = dict_['color_card_primary']
                )if matriz_compt_output[2][i] == 1 else Div(id =matriz_compt_output[0][i],content= matriz_compt_output[3][i])
            ],size=matriz_compt_output[1][i])for i in range(4)#dict_['id_dash']['compt_output']
        ],gutter="xs"),
        dmc.NotificationsProvider([Div(id='notifications-update-data'),]),
        Store(id='data-values'),
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
CULTIVO_ = ['MANDARINA', 'NO ESPECIFICADO', 'GRANADA', 'KAKI', 'PALTA',
       'NARANJA', 'TANGELO', 'PECANA']

def card_chips(id_chipgroup = '',titulo = '',variant = 'outline',color_chip = 'green', color_text = 'white', elements = [], size = 'md', head = True):
        head_element = [dmc.Title(titulo, order=3),dmc.Divider(variant="solid"),dmc.Space(h=10)] if head == True else []
        return dmc.Card(
                        children = head_element+[
                            
                            html.Div(
                            [
                                dmc.ChipGroup(
                                    [
                                        dmc.Chip(
                                            x,
                                            value=x,
                                            size = size,
                                            variant= variant,
                                            styles= {
                                                    "label": {
                                                        "&[data-checked]": {
                                                        "&, &:hover": {
                                                            "backgroundColor": dmc.theme.DEFAULT_COLORS[color_chip][5],
                                                            "color": color_text,
                                                            },
                                                        },
                                                    }
                                            }
                                        )
                                        for x in elements
                                    ],
                                    id = id_chipgroup,
                                    value=[],
                                    multiple=True,
                                    mb=10,
                                
                                ),
                            ]
                        )
                        ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        #style={"width": 350},
                    )     

def card_filt_select(id_select = '', label = 'texto', clearable = True, searchable = False, size='md', value = None, data = [], place_holder = 'Todos'):
    return dmc.Card(
        children=[
            
            dmc.CardSection(
                children=[ dmc.Text(label, weight=500, size="md",align='center')],
               
                withBorder=True,
                inheritPadding=True,
                py="1",
                style={'background-color': '#white', 'color' : 'black'}
            ),
            dmc.Space(h=10),
            dmc.Select(
                    id = id_select,
                    clearable = clearable,
                    placeholder=place_holder,
                    size = size,
                    value = value,
                    data = data,
                    searchable = searchable,
                    
                    nothingFound= 'No encontrado'
                ),
            
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"position": "static"},
    )   

def card_filt_multiselect(id_multi = '', label = 'texto', searchable = True, size='md', value = None, data = [],  place_holder = 'Todos'):
    return dmc.Card(
        children=[
            
            dmc.CardSection(
                children=[ dmc.Text(label, weight=500, size="md",align='center')],
               
                withBorder=True,
                inheritPadding=True,
                py="1",
                style={'background-color': '#white', 'color' : 'black'}
            ),
            dmc.Space(h=10),
            dmc.MultiSelect(
                        id = id_multi,
                        placeholder = place_holder,
                        searchable = searchable,
                        nothingFound="Opción no encontrada",
                        value=value,
                        data=data,
                        style={'font-size': "90%"},
                        size=size, 
            )
            
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"position": "static"},
    ) 
def dict_dataframe(dataframe = None):
    list_year = sorted(dataframe['Año'].astype('string').unique())
    list_tv = sorted(dataframe['Tipo de Venta'].unique())
    list_moneda = [{"value": "Importe Dolares", "label": "USD"},{"value": "Importe Soles", "label": "PEN"}]
    return {
        'lista_anio':list_year,
        'value_anio': list_year[-1],
        'lista_tipo_venta':list_tv,
        'lista_moneda' : list_moneda,
        'value_moneda' : list_moneda[0]['value']
    }

def ventas_exportacion_agro(dict_data = {}, comp_filtros = {}):
   
    return Container([
        Modal(id="modal_pie_tipo_venta", size= "85%"),
        Modal(id="modal_bar_gp", size= "85%"),
        Modal(id="modal_bar_gc", size= "85%"),
        Modal(id="modal_bar_cliente_top", size= "85%"),
        Modal(id="modal_bar_producto_top", size= "85%"),
        Modal(id="modal_bar_mes", size= "85%"),
        #block_offcanvas_comercial_filter
        #block_offcanvas_comercial_filter
        #block_offcanvas_comercial_filter(dict_filtros = comp_filtros, diccionario_componentes = nsp_rpt_ventas_detallado_comp),
        DataDisplay.offcanvas(
            label='Filtros',
            componentes = [
                Entry.select(
                    id = 'select-grupo-producto',
                    texto = 'Grupo de Producto',
                    size = 'md',
                    clearable = True,
                    searchable = True
                ),
                Entry.select(
                    id = 'select-grupo-cliente',
                    texto = 'Grupo de Cliente',
                    size = 'md',
                    clearable = True,
                    searchable = True
                ),
                Entry.select(
                    id = 'select-producto',
                    texto = 'Producto',
                    size = 'md',
                    clearable = True,
                    searchable = True
                ),
                Entry.select(
                    id = 'select-cliente',
                    texto = 'Cliente',
                    size = 'md',
                    clearable = True,
                    searchable = True
                ),
            
            ]
        ),
        Row([
            Column([
                dmc.Card(children=[
                    dmc.Grid([
                        Column([
                                Button.btnFilter(style={'position': 'absolute','z-index': '99'}),
                                
                        ],size=1),
                        Column([
                                title(text=['Resumen de Ventas'],order=2)
                        ],size=2),
                        Column([
                           Entry.select(
                                    id = 'id_year',
                                    texto = 'Año',
                                    size = 'sm',
                                    clearable = True,
                                    styles={"label": {"color": "black"}},
                                    value = dict_data['value_anio'],
                                    data=dict_data['lista_anio']
                            )    
                        ],size=2),
                        Column([
                           Entry.multiSelect(
                                    id = 'id_tipo_venta',
                                    texto = 'Tipo de Venta',
                                    size='sm',
                                    data=dict_data['lista_tipo_venta'],
                                    place="Todos"
                        )    
                        ],size=5),
                        Column([
                           Entry.select(
                                    id = 'id_moneda',
                                    texto = 'Moneda',
                                    size = 'sm',
                                    clearable = False,
                                    styles={"label": {"color": "black"}},
                                    value = dict_data['value_moneda'],
                                    data=dict_data['lista_moneda'],
                                    searchable = True
                            )    
                        ],size=2),
                    ],gutter="xs")
                ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",         
                    style={"position": "static",'background-color':'white'},
                    p=8)
            ]),
            
            
        ]),
        
        Row([
            Column([
                
                card_graph_1(
                    text= 'Ventas por Tipo',
                    id_graph = 'pie_tipo_venta', 
                    id_maximize = 'maxi_pie_tipo_venta',
                    height=380
                )
                                
            ],size=4),
            Column([
                card_graph_1(
                    text= 'Ventas por Grupo Producto',
                    id_graph = 'bar_gp', 
                    id_maximize = 'maxi_bar_gp',
                    height=380
                )
                                  
            ],size=4),
            Column([
                card_graph_1(
                    text= 'Ventas por Grupo Cliente',
                    id_graph = 'bar_gc', 
                    id_maximize = 'maxi_bar_gc',
                    height=380
                )        
            ],size=4)
        ]),
        Row([
            Column([
                card_graph_1(
                    text= 'Ventas por Cliente (Top 20)',
                    id_graph = 'bar_cliente_top', 
                    id_maximize = 'maxi_bar_cliente_top',
                    height=380
                )
                                
            ],size=4),
            Column([
                card_graph_1(
                    text= 'Ventas por Producto (Top 20)',
                    id_graph = 'bar_producto_top', 
                    id_maximize = 'maxi_bar_producto_top',
                    height=380
                )
                                  
            ],size=4),
            Column([
                card_graph_1(
                    text= 'Ventas por Mes',
                    id_graph = 'bar_mes', 
                    id_maximize = 'maxi_bar_mes',
                    height=380
                )        
            ],size=4)
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        
        
    ])



"""
Container([
        #Div([Modal(id=f"modal-bar-comercial-productos", size= "85%") for i in ELEMENTOS_DATAFRAME_PARA_FILTROS]),
        #Modal(id="modal-bar-comercial-productos", size= "85%"),
        #Modal(id="modal-bar-comercial-mes", size= "85%"),
        #Modal(id="modal-pie-comercial-pais", size= "85%"),
        #Modal(id="modal-pie-comercial-vendedor", size= "85%"),
        #Modal(id="modal-funnel-comercial-selector_second", size= "85%"),
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


"""