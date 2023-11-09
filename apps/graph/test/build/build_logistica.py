from ..utils.theme import Container
from ..utils.frame import *
from ..utils.components.components_main import *
from ..utils.blocks.block_card import *
from ..utils.components.components_filters import *
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
    Row([
        Column([
                 Title.title(text = 'Almacén')  
        ],size=4), 
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
    ]),
    Row([
        
    ]),
    Div(id='notifications-update-data'),
    Store(id='data-values'),
])
