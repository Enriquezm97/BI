import pandas as pd
from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from ..utils.theme import Container
from ..utils.frame import *
from ..utils.components.components_main import *
from ..utils.blocks.block_card import *
from ..utils.functions.callbacks.callbacks_logistica import *
from ..utils.functions.functions_transform import clean_inventarios
from ..Connection.apis import connection_api
from ..utils.functions.callbacks.callbacks_ import *
#logistica_df = pd.read_parquet('logistica.parquet', engine='pyarrow')

#print(logistica_df)


    
def logistica_dash(filtros = ['select-anio','select-grupo','select-rango']):
    dff  = connection_api(sp_name = 'nsp_stocks_bi_samplast')
    logistica_df = clean_inventarios(df = dff)

    app = DjangoDash('logistica_',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Modal(id="modal-bar-stock-items", size= "85%"),
        Modal(id="modal-bar-stock-familia", size= "85%"),
        Modal(id="modal-bar-top-producto", size= "85%"),
        Modal(id="modal-bar-stock-abc-ventas", size= "85%"),
        Modal(id="modal-bar-stock-abc-valorizado", size= "85%"),
        Modal(id="modal-pie-items-antiguedad", size= "85%"),
        Modal(id="modal-pie-stock-antiguedad", size= "85%"),
        Row([
            Column([
                 Title.title(text = 'Inventarios')  
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
    filter_callback(app, filt = filtros, dataframe = logistica_df)
    graph_log(app)
    opened_modal(app, modal_id="modal-bar-stock-items",children_out_id="bar-stock-items", id_button="maximize-bar-stock-items",height_modal=900)
    
    opened_modal(app, modal_id="modal-bar-stock-familia",children_out_id="bar-stock-familia", id_button="maximize-bar-stock-familia",height_modal=900)
    opened_modal(app, modal_id="modal-bar-top-producto",children_out_id="bar-top-producto", id_button="maximize-bar-top-producto",height_modal=900)
    opened_modal(app, modal_id="modal-bar-stock-abc-ventas",children_out_id="bar-stock-abc-ventas", id_button="maximize-bar-stock-abc-ventas",height_modal=900)
    opened_modal(app, modal_id="modal-bar-stock-abc-valorizado",children_out_id="bar-stock-abc-valorizado", id_button="maximize-bar-stock-abc-valorizado",height_modal=900)
    opened_modal(app, modal_id="modal-pie-stock-antiguedad",children_out_id="pie-stock-antiguedad", id_button="maximize-pie-stock-antiguedad",height_modal=900)
    opened_modal(app, modal_id="modal-pie-items-antiguedad",children_out_id="pie-items-antiguedad", id_button="maximize-pie-items-antiguedad",height_modal=900)