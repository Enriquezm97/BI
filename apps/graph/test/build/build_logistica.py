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
                 Title.title(text = 'Stocks')  
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
                DataDisplay.loadingOverlay(
                        cardGraph(
                                id_graph = 'bar-stock-items', 
                                id_maximize = 'maximize-bar-stock-items',
                                height = 380
                                )
                )
                  
            ],size=4), 
            Column([
                DataDisplay.loadingOverlay(
                        cardGraph(
                                id_graph = 'bar-stock-familia', 
                                id_maximize = 'maximize-bar-stock-familia',
                                height = 380
                                )
                )   
            ],size=4), 
            Column([
                DataDisplay.loadingOverlay(
                        cardGraph(
                                id_graph = 'bar-top-producto', 
                                id_maximize = 'maximize-bar-top-producto',
                                height = 380
                                )
                )
            ],size=4), 
        ]),
        Row([
            Column([
               DataDisplay.loadingOverlay(
                        cardGraph(
                                id_graph = 'bar-stock-abc-ventas', 
                                id_maximize = 'maximize-bar-stock-abc-ventas',
                                height = 350
                                )
                )    
            ],size=3), 
            Column([
                DataDisplay.loadingOverlay(
                        cardGraph(
                                id_graph = 'bar-stock-abc-valorizado', 
                                id_maximize = 'maximize-bar-stock-abc-valorizado',
                                height = 350
                                )
                )   
            ],size=3), 
            Column([
                DataDisplay.loadingOverlay(
                        cardGraph(
                                id_graph = 'pie-stock-antiguedad', 
                                id_maximize = 'maximize-pie-stock-antiguedad',
                                height = 350
                                )
                )    
            ],size=3), 
            Column([
                DataDisplay.loadingOverlay(
                        cardGraph(
                                id_graph = 'pie-items-antiguedad', 
                                id_maximize = 'maximize-pie-items-antiguedad',
                                height = 350
                                )
                )    
            ],size=3), 
        ]),
    Div(id='notifications-update-data'),
    Store(id='data-values'),
])



def alm_stock_build(df = None):
    return Container([
    html.Div([dmc.Modal(title = '', id = i, fullScreen=False, zIndex=10000, size= "85%" )for i in ['modal-bar-importe-stock','modal-pie-estadoinv','modal-bar-respon']]),
    Row([
        Column([
                 Title.title(text = 'Stock Almacén', align='center')  
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
                Picking.segmented(id='segmented-col',value='Sucursal',data=[  {'label': 'Sucursal', 'value': 'Sucursal'},
                                                                            {'label': 'Almacén', 'value': 'Almacén'},
                                                                            {'label': 'Tipo', 'value': 'Tipo'},
                                                                            {'label': 'Grupo', 'value': 'Grupo'}]),
                DataDisplay.loadingOverlay(
                    
                        cardGraph(
                                id_graph = 'bar-importe-stock', 
                                id_maximize = 'maximize-bar-importe-stock',
                                height = 300
                                )
                )  
        ],size=8),
        Column([
            DataDisplay.loadingOverlay(
                    
                        cardGraph(
                                id_graph = 'pie-estadoinv', 
                                id_maximize = 'maximize-pie-estadoinv',
                                height = 330
                                )
                )
        
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
            DataDisplay.loadingOverlay(
                    
                        cardGraph(
                                id_graph = 'bar-respon', 
                                id_maximize = 'maximize-bar-respon',
                                height = 400
                                )
                )
        
        ],size=4),
    ]),
    Div(id='notifications-update-data'),
    Store(id='data-values'),
])
