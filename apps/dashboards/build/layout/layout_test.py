from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *
#
from apps.graph.build.components.mantine_react_components.actionIcon import *
from apps.graph.build.components.mantine_react_components.selects import *
from apps.graph.build.components.bootstrap_components.offcanvas import *
from apps.graph.build.components.mantine_react_components.radio import *

#
import dash_ag_grid as dag

def test_dashboard(codigo= '',data_almacen = []):
    return Container([
        Modal(id="modal-bar-minv-prom", size= "85%"),
        Modal(id="modal-bar-inv-val", size= "85%"),
        Row([
            Column([
                 title(text = 'Gestión de Stocks (Últimos 6 meses)',order=2)  
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
                                     
                                    {"value": "PROMEDIOMEX", "label": "USD"},
                                    {"value": "PROMEDIOMOF", "label": "PEN"}
                                    ],
                                value='PROMEDIOMOF',
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
                        Entry.multiSelect(id = 'multiselect-almacen',texto='Almacen',data = data_almacen,place = 'Todos'),
                        dmc.Space(h=10),
                        Entry.textInput(id = 'text-input-find',label='Buscar Código o Descripción',icon=DashIconify(icon="ic:search"),size='md',place = 'Buscar...' ),
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
                        
                            card_graph(id_graph = 'bar-minv-prom',height=350 , id_maximize = 'maximize-bar-minv-prom')
                        
                    ],size = 6),
                    Column([
                         
                             card_graph(id_graph = 'bar-inv-val',height=350, id_maximize = 'maximize-bar-inv-val')
                         
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


def resize_dashboard():
    
    return Container([])

"""
html.Div([
    PanelGroup(
        id='panel-group',
        children=[
            Panel(
                id='panel-1',
                children=[
                    html.H1('Black')
                ],
            ),
            PanelResizeHandle(html.Div(style={"backgroundColor": "grey", "height": "100%", "width": "5px"})),
            Panel(
                id='panel-2',
                children=[
                    html.H1('White')
                ],
                style={"backgroundColor": "black", "color": "white"}
            )
        ], direction='horizontal'
    )
], style={"height": "100vh"})
"""