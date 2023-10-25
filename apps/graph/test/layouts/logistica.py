import pandas as pd
from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from ..utils.theme import Container
from ..utils.frame import *
from ..utils.components.components_main import *
from ..utils.blocks.block_card import *
from ..utils.functions.callbacks.callbacks_logistica import *

logistica_df = pd.read_parquet('logistica.parquet', engine='pyarrow')

print(logistica_df)

def logistica_dash(filtros = ['select-anio','select-familia','select-rango']):
    app = DjangoDash('logistica_',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        #Row([
        #        Column([
        #            Div(id='title')
        #        ],size=12), 
        #]),
        Row([
            Column([
                 Title.title(text = 'Stocks')  
            ],size=6), 
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
                    id = 'select-familia',
                    texto = 'Familia',
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
    filter_callback(app, filt = filtros, dataframe = logistica_df)
    graph_log(app)