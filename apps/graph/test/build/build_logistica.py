from ..utils.theme import Container
from ..utils.frame import *
from ..utils.components.components_main import *
from ..utils.blocks.block_card import *
from ..utils.components.components_filters import *
import dash_ag_grid as dag
strash = ["modal-bar-stock-items","modal-bar-stock-familia","modal-bar-top-producto","modal-bar-stock-abc-ventas",
          "modal-bar-stock-abc-valorizado","modal-pie-items-antiguedad","modal-pie-stock-antiguedad"]



def logistica_build():
    return Container([
        html.Div([dmc.Modal(title = '', id = i, fullScreen=False, zIndex=10000, size= "85%" )for i in strash]),
        
        Row([
            Column([
                dmc.Card(children=[
                    dmc.Grid(
                        children =[
                            Column([
                                Title.title(text = 'Stocks',color ="white")  
                            ],size=4),
                            Column(
                            [
                                Entry.select(
                                    id = 'select-anio',
                                    texto = 'Año',
                                    size = 'sm',
                                    clearable = True,
                                    styles = {
                                        "label": {
                                            "color": "white",
                                            #"backgroundColor": dmc.theme.DEFAULT_COLORS["yellow"][1],
                                        },
                                    }
                                    
                                )
                            ],size = 2),
                            Column(
                            [
                                Entry.select(
                                    id = 'select-grupo',
                                    texto = 'Grupo',
                                    size = 'sm',
                                    clearable = True,
                                    styles = {
                                        "label": {
                                            "color": "white",
                                            #"backgroundColor": dmc.theme.DEFAULT_COLORS["yellow"][1],
                                        },
                                    }
                                )
                            ],size = 2),
                            Column(
                            [
                                Entry.select(
                                    id = 'select-rango',
                                    texto = 'Rango de Antigüedad',
                                    size = 'sm',
                                    clearable = True,
                                    styles = {
                                        "label": {
                                            "color": "white",
                                            #"backgroundColor": dmc.theme.DEFAULT_COLORS["yellow"][1],
                                        },
                                    }
                                )
                            ],size = 2),
                            Column(
                            [
                                Entry.select(
                                                id = 'select-moneda', texto = "Moneda", size = 'sm',
                                                data=[
                                                    
                                                    {"value": "Dolares", "label": "USD"},
                                                    {"value": "Soles", "label": "PEN"}
                                                    ],
                                                value='Dolares',
                                                clearable=False,
                                                styles = {
                                                "label": {
                                                    "color": "white",
                                                    #"backgroundColor": dmc.theme.DEFAULT_COLORS["yellow"][1],
                                                },
                                            }
                                            )
                            ],size = 2),
                            
                        ],gutter="xs"
                    )
                ],
                withBorder=True,
                shadow="sm",
                radius="md",         
                style={"position": "static",'background-color':'black',"overflow":"visible"},#"position": "static",
                p=10),
                    
                
            ]),
             
    
        ]),
        Row([
            Column([
                Entry.chipGroup(id='chipgroup-mes')
            ]),
         ]),
        Row([
            
            Column([
                card_graph_1(
                    text='Stock Valorizado y N° Itemspor mes y año',
                    id_graph = 'bar-stock-items', 
                    id_maximize = 'maximize-bar-stock-items',
                    height = 350,
                    color_bg="black"
                ),
                
                  
            ],size=7), 
            Column([
                card_graph_1(
                    text='Stock por Grupo de Producto',
                    id_graph = 'bar-stock-familia', 
                    id_maximize = 'maximize-bar-stock-familia',
                    height = 350,
                    color_bg="black"
                ),

            ],size=5), 
            
        ]),
        Row([
            Column([
                card_graph_1(
                    text='Productos (Stock Valorizado Top 10)',
                    id_graph = 'bar-top-producto', 
                    id_maximize = 'maximize-bar-top-producto',
                    height = 350,
                    color_bg="black"
                ),
                
            ],size=4), 
            
            Column([
                card_graph_1(
                    text='Stock Valorizado segun Antigüedad',
                    id_graph = 'pie-stock-antiguedad', 
                    id_maximize = 'maximize-pie-stock-antiguedad',
                    height = 350,
                    color_bg="black"
                ),   
            ],size=4), 
            Column([
                card_graph_1(
                    text='Nro Items segun Antigüedad',
                    id_graph = 'pie-items-antiguedad', 
                    id_maximize = 'maximize-pie-items-antiguedad',
                    height = 350,
                    color_bg="black"
                ),
                 
            ],size=4),
        ]),
        Row([
            Column([
                card_graph_1(
                    text='Porcentaje Stock por ABC Ventas',
                    id_graph = 'bar-stock-abc-ventas', 
                    id_maximize = 'maximize-bar-stock-abc-ventas',
                    height = 350,
                    color_bg="black"
                ),
                  
            ],size=6), 
            Column([
                card_graph_1(
                    text='Porcentaje Stock por ABC Stock Valorizado',
                    id_graph = 'bar-stock-abc-valorizado', 
                    id_maximize = 'maximize-bar-stock-abc-valorizado',
                    height = 350,
                    color_bg="black"
                ),
                
            ],size=6),  
        ]), 
        
    Div(id='notifications-update-data'),
    Store(id='data-values'),
])



def alm_stock_build(df = None):
    return Container([
    html.Div([dmc.Modal(title = '', id = i, fullScreen=False, zIndex=10000, size= "85%" )for i in ['modal-bar-importe-stock','modal-pie-estadoinv','modal-bar-respon']]),
    Row([
        Column([
                 Title.title(text = 'Estado de Inventario', align='center')  
        ],size=12), 
    ]),
    Row([
        
        Column([
            datepicker_alm(dataframe = df, value_col = 'Última Fecha Ingreso',text = 'Rango Inicio', tipo = 'inicio')
                  
        ],size=2), 
        Column([
            datepicker_alm(dataframe = df, value_col = 'Última Fecha Ingreso',text = 'Rango Fin', tipo = 'fin')
        ],size=2), 
        Column([
            
                Entry.select(
                    id = 'select-almacen',
                    texto = 'Almacén',
                    size = 'sm',
                    clearable = True
                )
            
        ],size=2), 
        Column([
            
               Entry.select(
                    id = 'select-tipo',
                    texto = 'Tipo',
                    size = 'sm',
                    clearable = True
                ) 
             
        ],size=2), 
        Column([
            
               Entry.select(
                    id = 'select-grupo',
                    texto = 'Grupo',
                    size = 'sm',
                    clearable = True
                ) 
             
        ],size=2), 
        Column([
            Entry.select(
                id = 'select-moneda', texto = "Moneda", size = 'sm',
                data=[{"value": "Importe Dolares", "label": "USD"},{"value": "Importe Soles", "label": "PEN"} ],
                value='Importe Dolares',
                clearable=False
            ) 
             
        ],size=2),
    ]),
    Row([
        Column([
                card_segment(
                    id_graph = 'bar-importe-stock', 
                    id_maximize = 'aximize-bar-importe-stock',
                    id_segmented='segmented-col',
                    value = 'Sucursal',
                    data = [{'label': 'Sucursal', 'value': 'Sucursal'},
                            {'label': 'Almacén', 'value': 'Almacén'},
                            {'label': 'Tipo', 'value': 'Tipo'},
                            {'label': 'Grupo', 'value': 'Grupo'}],
                    height=300
                ),
                
                 
        ],size=8),
        Column([
            card_graph_1(
                text= 'Estado de Inventario',
                id_graph = 'pie-estadoinv', 
                id_maximize = 'maximize-pie-estadoinv',
                height = 330
            ),
            
        
        ],size=4),
    ]),
    Row([
        Column([
              html.Div(children=[
                dag.AgGrid(
                        id="table-status",
                        #rowData=df.to_dict("records"),
                        #columnDefs=[{"field": i,} for i in df.columns],#"cellStyle": {'font-size': 18}
                        defaultColDef = {
                            "resizable": True,
                            "initialWidth": 160,
                            "wrapHeaderText": True,
                            "autoHeaderHeight": True,
                            "minWidth":160,
                            "sortable": True, 
                            "filter": True
                        },
                        className="ag-theme-alpine headers1",
                        columnSize="sizeToFit",
                        style={'font-size': '13px'},
                        

            )])  
        ],size=8),
        Column([
            card_graph_1(
                text= 'N° Registros por Responsable',
                id_graph = 'bar-respon', 
                id_maximize = 'maximize-bar-respon',
                height = 400
            ),
           
        
        ],size=4),
    ]),
    Div(id='notifications-update-data'),
    Store(id='data-values'),
])
