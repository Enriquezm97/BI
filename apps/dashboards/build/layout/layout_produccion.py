from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *
from ..components.block_comp import *
from ..components.group_comp import *
#from ..components.dict_sp_comp import nsp_rpt_ventas_detallado_comp


def ejecucion_campania(dataframe = None):
    return Container([
        Modal(id="modal-line-recurso-agricola", size= "85%"),
        agricola_offcanvas_filt(),
        Row([
            Column([Button.btnFilter()],size=1),
            Column([Div(id='title')],size=10),
            Column([Button.btnDownload()],size=1),
        ]),
        Row([
            Column([
                Entry.select(
                    id = 'select-campania',
                    texto = "Campaña-Cultivo",
                    size = 'sm',
                    data = [],#{'label': i, 'value': i} for i in campaña_list
                    value = None,#campaña_list[-1]
                    clearable=False
                )
            ],size = 2),
            Column([Entry.select(id='select-variedad',texto="Variedades",size='sm')],size = 3),
            Column([Entry.select(id='select-lote',texto="Lotes",size='sm')],size = 3),
            Column([Div(id = 'label-range-inicio-campania'),],size = 2),
            Column([Div(id = 'label-range-fin-campania')],size = 2),
        ]),
        Row([
            Column([
                Picking.segmented(id='segmented-recurso'),
                card_graph(
                    id_graph='line-recurso-agricola', 
                    id_maximize = 'maximize-line-recurso-agricola'
                )
                
            ])
        ]),
        Row([
            Column([
               dmc.Tabs(
                        [
                            dmc.TabsList(
                                [
                                    dmc.Tab("Variedad", value="Variedad"),
                                    dmc.Tab("Lote", value="Lote"),
                                    
                                ]
                            ),
                            dmc.TabsPanel(Div( id = 'table-variedad'), value="Variedad"),
                            dmc.TabsPanel(Div( id = 'table-lote'), value="Lote"),
                            
                        ],
                        value="Variedad",
                    ) 
            ])
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
        Modal(id='modal')
        
    ])