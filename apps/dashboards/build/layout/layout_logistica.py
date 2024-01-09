from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *





def logistica_build():
    strash = ["modal-bar-stock-items","modal-bar-stock-familia","modal-bar-top-producto","modal-bar-stock-abc-ventas",
          "modal-bar-stock-abc-valorizado","modal-pie-items-antiguedad","modal-pie-stock-antiguedad"]
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