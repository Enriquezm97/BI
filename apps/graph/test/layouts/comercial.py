from django_plotly_dash import DjangoDash
from apps.graph.test.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from apps.graph.test.utils.theme import themeProvider, Container
from apps.graph.test.utils.frame import Column, Row, Div, Store, Download, Modal, Divider
from apps.graph.test.utils.components import Entry, Button, DataDisplay,Picking
from apps.graph.test.utils.blocks.block_filters import block_comercial_filters_IV
from apps.graph.test.utils.tables import tableDag
from apps.graph.test.utils.functions.callbacks.callbacks_comercial import *
from apps.graph.test.utils.blocks.block_card import cardGraph

df_ventas_detalle=pd.read_parquet('comercial_new_etl.parquet', engine='pyarrow')

#anio_campania = sorted(df_ventas_detalle['YEAR'].unique())

def informeComercial(rubro_empresa = 'Agricola'):
    
    app = DjangoDash('informe-comercial',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([
                #Column([Button.btnFilter()],size=1),
                Column([
                    Div(id='title')
                ],size=11),
                Column([Button.btnDownload()],size=1),
        ]),
        
        
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
                                                    id_maximize = 'maximize-bar-comercial-productos'
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
                                                id_maximize = 'maximize-pie-comercial-vendedor'
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
    create_callback_filter_comercial_informe(app = app,dataframe =df_ventas_detalle)    
    create_title_comercial_informe(app=app,title='Informe de Ventas ')
    create_graph_informe_comercial(app)

def ventaSegmented(rubro_empresa = 'Agricola'):
    
    app = DjangoDash('informe-comercial',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([])
