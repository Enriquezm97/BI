import dash_ag_grid as dag
from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *





def almacen_stock():
    strash = ["modal-bar-stock-items","modal-bar-stock-familia","modal-bar-top-producto","modal-bar-stock-abc-ventas",
          "modal-bar-stock-abc-valorizado","modal-pie-items-antiguedad","modal-pie-stock-antiguedad"]
    return Container([
        html.Div([dmc.Modal(title = '', id = i, fullScreen=False, zIndex=10000, size= "85%" )for i in strash]),
        
       Row([
            Column([
                 title(text = 'Stocks')  
            ],size=4), 
            Column(
            [
                Entry.select(
                    id = 'select-anio',
                    texto = 'Año',
                    size = 'sm',
                    clearable = True
                )
            ],size = 2),
            Column(
            [
                Entry.select(
                    id = 'select-grupo',
                    texto = 'Grupo',
                    size = 'sm',
                    clearable = True
                )
            ],size = 2),
            Column(
            [
                Entry.select(
                    id = 'select-rango',
                    texto = 'Rango de Antigüedad',
                    size = 'sm',
                    clearable = True
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
                                clearable=False
                            )
            ],size = 2),
                
        ]),
        Row([
            Column([
                Entry.chipGroup(id='chipgroup-mes')
            ]),
         ]),
        Row([
            
            Column([
                
                    card_graph(
                        id_graph = 'bar-stock-items', 
                        id_maximize = 'maximize-bar-stock-items',
                        height = 380
                    )
               
                  
            ],size=7), 
            Column([
                card_graph(
                    id_graph = 'bar-stock-familia', 
                    id_maximize = 'maximize-bar-stock-familia',
                    height = 380
                )
                
            ],size=5), 
            
        ]),
        Row([
            Column([
                
                card_graph(
                    id_graph = 'bar-top-producto', 
                    id_maximize = 'maximize-bar-top-producto',
                    height = 380
                )
                
            ],size=6), 
            
            Column([
                card_graph(
                    id_graph = 'pie-stock-antiguedad', 
                    id_maximize = 'maximize-pie-stock-antiguedad',
                    height = 380
                )
                    
            ],size=3), 
            Column([
                card_graph(
                    id_graph = 'pie-items-antiguedad', 
                    id_maximize = 'maximize-pie-items-antiguedad',
                    height = 380
                )
                  
            ],size=3),
        ]),
        Row([
            Column([
                card_graph(
                    id_graph = 'bar-stock-abc-ventas', 
                    id_maximize = 'maximize-bar-stock-abc-ventas',
                    height = 380
                )
                    
            ],size=6), 
            Column([
                card_graph(
                    id_graph = 'bar-stock-abc-valorizado', 
                    id_maximize = 'maximize-bar-stock-abc-valorizado',
                    height = 380
                )
                 
            ],size=6),  
        ]), 
        
    Div(id='notifications-update-data'),
    Store(id='data-values'),
])
    

def gestion_stock_():
    return Container([
        Row([
            Column([
                 title(text = 'GESTIÓN DE STOCKS')  
            ],size=4), 
            Column(
            [
                Entry.select(
                    id = 'select-anio',
                    texto = 'Año',
                    size = 'sm',
                    clearable = True
                )
            ],size = 2),
            Column(
            [
                Entry.select(
                    id = 'select-grupo',
                    texto = 'Grupo',
                    size = 'sm',
                    clearable = True
                )
            ],size = 2),
            Column(
            [
                Entry.select(
                    id = 'select-rango',
                    texto = 'Rango de Antigüedad',
                    size = 'sm',
                    clearable = True
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
                                clearable=False
                            )
            ],size = 2),
                
        ]),
    ])

def gestion_stock(data_almacen = []):
    return Container([
        Modal(id="modal_bar-minv-prom", size= "85%"),
        Modal(id="modal_bar-inv-val", size= "85%"),
        Row([
            Column([
                 title(text = 'Gestión de Stocks',order=1)  
            ],size=4),
            Column(
            [
                Entry.select(
                    id = 'select-grupo',
                    texto = 'Grupo',
                    size = 'md',
                    clearable = True,
                    searchable = True
                )
            ],size = 2),
            Column(
            [
                Entry.select(
                    id = 'select-subgrupo',
                    texto = 'Subgrupo',
                    size = 'md',
                    clearable = True,
                    searchable = True
                )
            ],size = 2),
            Column(
            [
                Entry.select(
                    id = 'select-marca',
                    texto = 'Marca',
                    size = 'md',
                    clearable = True,
                    searchable = True
                )
            ],size = 2),
            Column(
            [
                Entry.select(
                                id = 'select-moneda', texto = "Moneda", size = 'md',
                                data=[
                                     
                                    {"value": "dolares", "label": "USD"},
                                    {"value": "soles", "label": "PEN"}
                                    ],
                                value='dolares',
                                clearable=False
                            )
            ],size = 2),    
        ]),
        Row([
            Column(
            [
                #Entry.textInput(label='owo',id='input',icon=DashIconify(icon="ic:search"),)
                Row([
                    Column([
                        Entry.select(
                                id = 'select-tipo-val', texto = "Tipo de Valorización", size = 'md',
                                data=[
                                    {"value": "1", "label": "CONTABLE"},
                                    {"value": "2", "label": "ULTIMA COMPRA"},
                                    {"value": "3", "label": "ULTIMO PROMEDIO"},
                                    ],
                                value='1',
                                clearable=False
                            ),
                        
                        Entry.multiSelect(id = 'multiselect-almacen',texto='Almacen',data = data_almacen,place = 'Todos'),
                        dmc.Space(h=10),
                        Entry.textInput(id = 'text-input-find',label='Código o Descripción',size='md',place = 'Buscar...' ),#,icon=DashIconify(icon="ic:search")
                        dmc.Space(h=10),
                        dmc.Text("Consumo Promedio Mensual", size="md",weight=500),
                        dcc.RangeSlider(
                            min = 0,
                            marks=None,
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True,
                                "style": {"color": "Black", "fontSize": "30px", "font-size":"18px"},
                            },
                            id='range-slider-cpm',
                            
                        ),
                        dmc.NumberInput(
                            id = 'num-meses',
                            label="Número de Meses",
                            description="Ultimos meses",
                            value=6,
                            min=1,
                            step=1,
                            style={"width": 150},
                            size="md",
                            
                        )
                    
                    ]),

                ])
            ],size = 3),
            Column([
                Row([
                    Column([
                        card_value(text='CPM',radius='xs',id_value='card-cpm',color_section_title= '#33ce96')
                    ],size = 3),
                    Column([
                        card_value(text='INV. VAL.',radius='xs',id_value='card-invval',color_section_title= '#33ce96')
                    ],size = 3),
                    Column([
                        card_value(text='TI STOCK',radius='xs',id_value='card-stock',color_section_title= '#33ce96')
                    ],size = 3),
                    Column([
                        card_value(text='TI CONSUMO',radius='xs',id_value='card-consumo',color_section_title= '#33ce96')
                    ],size = 3),
                ]),
                Row([
                    Column([
                        
                            card_graph(id_graph = 'bar-minv-prom',height=350 , id_maximize = 'maxi_bar-minv-prom')
                        
                    ],size = 6),
                    Column([
                         
                             card_graph(id_graph = 'bar-inv-val',height=350, id_maximize = 'maxi_bar-inv-val')
                         
                    ],size = 6),
                ]),
                
            ],size = 9)
            
           
            
        ]),
        Row([
                    Column([
                        html.Div(children=[
                                Button.actionIcon(id='btn-download',icono='download',style={'position': 'absolute','top': '0px','right': '9px','z-index': '99'},),
                                        #actionIcon(ids=id_download,icono='download'),
                                dag.AgGrid(
                                        id="table",
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
                    
                    ]),
                   
                ]),
        Div(id='notifications-update-data'),
        Store(id='data-stock'),
        Store(id='data-values'),
        Store(id='data-table'),
        Download(),
    ])