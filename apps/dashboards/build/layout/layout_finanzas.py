from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *
#
from apps.graph.build.components.mantine_react_components.actionIcon import *
from apps.graph.build.components.mantine_react_components.selects import *
from apps.graph.build.components.bootstrap_components.offcanvas import *
from apps.graph.build.components.mantine_react_components.radio import *
import dash_ag_grid as dag

def balance_general(formato = []):
    return Container([
        html.Div([dmc.Modal(title = '', id = i, fullScreen=True, zIndex=10000, size= "85%" )for i in ['modal_fondo-maniobra-graph','modal_activo-group3-graph','modal_pasivo-group3-graph']]),
        Row([
            Column([
                dmc.Card(children=[
                    dmc.Grid(
                        children=[
                            Column(title(text = 'Balance General',color="white"), size=3),
                            Column(
                                Entry.select(
                                    id = 'select-formato',
                                    texto = 'Formato',
                                    size = 'sm',
                                    value=formato[0],
                                    data = formato,
                                    clearable = False,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=2),
                            Column(
                                Entry.select(
                                    id = 'select-anio',
                                    texto = 'Año',
                                    size = 'sm',
                                    clearable = True,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=2),
                            
                            Column(
                                Entry.select(
                                    id = 'select-mes',
                                    texto = 'Mes',
                                    size = 'sm',
                                    clearable = True,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=2),
                            Column(
                                Entry.select(
                                id = 'select-trismestre',
                                texto = 'Trimestre',
                                size = 'sm',
                                clearable = True,
                                styles={"label": {"color": "white"}}
                                
                            )
                            , size=2),
                            Column(
                                #Entry.select(
                                #    id = 'select-moneda', texto = "Moneda", size = 'sm',
                                #    data=[
                                        
                                #        {"value": "dolares", "label": "USD"},
                                #        {"value": "soles", "label": "PEN"}
                                #        ],
                                #    value='dolares',
                                #    clearable=False
                                #)
                                dmc.Select(
                                    id = 'select-moneda',
                                    clearable = False,
                                    placeholder='Todos',
                                    label = 'Moneda',
                                    size = 'sm',
                                    value = 'dolares',
                                    data = [
                                        {"value": "dolares", "label": "USD"},
                                        {"value": "soles", "label": "PEN"}
                                    ],
                                    searchable = False,
                                    styles={"label": {"color": "white"}}
                                    
                                    #nothingFound= 'No encontrado'
                                )
                            , size=1),
                            
                        ],
                        gutter="xs",
                    )
                    
                ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",         
                    style={"position": "static",'background-color':'#00353e'}
                ),
                
            ])
        ]),
        Row([
            Column([
                Div(id='table-js')
            ])
        ]),
        Row([
            #Column([
                
                
            #],size=4),
            Column([
                card_graph_1(text='Activo',id_graph='activo-group3-graph',id_maximize='maxi_activo-group3-graph',height = 300)
            ],size=6),
            Column([
                card_graph_1(text='Pasivo',id_graph='pasivo-group3-graph',id_maximize='maxi_pasivo-group3-graph',height = 300)
            ],size=6),
        ]),
        Row([   
            Column([
                #card_value(contenido='tabla',
                #           text='Balance General', 
                #           padding_section=0,
                #           radius='0px',
                #           color_section_content="#00353e",
                #           color_section_title="#00353e",
                #           content=[
                #               dag.AgGrid(
                #                    id = 'table-dag',
                #                    className="ag-theme-balham"
                #                )
                #           ]
                #),
                card_graph_1(id_graph='fondo-maniobra-graph',id_maximize='maxi_fondo-maniobra-graph',text='Fondo de Maniobra',height =300)
                
            ])
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
    ])
    
def balance_activo_pasivo(formato = []):
    return Container([
        html.Div([dmc.Modal(title = '', id = i, fullScreen=True, zIndex=10000, size= "85%" )for i in ['modal_ap-pie-graph','modal_avsp-line-graph','modal_comp-pasivo-graph','modal_comp-activo-graph']]),
        Row([
            Column([
                dmc.Card(children=[
                    dmc.Grid(
                        children=[
                            Column(title(text = 'Activo & Pasivo',color="white"), size=3),
                            Column(
                                Entry.select(
                                    id = 'select-formato',
                                    texto = 'Formato',
                                    size = 'sm',
                                    value=formato[0],
                                    data = formato,
                                    clearable = False,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=2),
                            Column(
                                Entry.select(
                                    id = 'select-anio',
                                    texto = 'Año',
                                    size = 'sm',
                                    clearable = True,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=2),
                            
                            Column(
                                Entry.select(
                                    id = 'select-mes',
                                    texto = 'Mes',
                                    size = 'sm',
                                    clearable = True,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=2),
                            Column(
                                Entry.select(
                                id = 'select-trismestre',
                                texto = 'Trimestre',
                                size = 'sm',
                                clearable = True,
                                styles={"label": {"color": "white"}}
                                
                            )
                            , size=2),
                            Column(
                                dmc.Select(
                                    id = 'select-moneda',
                                    clearable = False,
                                    placeholder='Todos',
                                    label = 'Moneda',
                                    size = 'sm',
                                    value = 'dolares',
                                    data = [
                                        {"value": "dolares", "label": "USD"},
                                        {"value": "soles", "label": "PEN"}
                                    ],
                                    searchable = False,
                                    styles={"label": {"color": "white"}}
                                    
                                    #nothingFound= 'No encontrado'
                                )
                            , size=1),
                            
                        ],
                        gutter="xs",
                    )
                    
                ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",         
                    style={"position": "static",'background-color':'#00353e'}
                ),
                
            ])
        ]),
        Row([
            Column([
                card_graph_1(id_graph='ap-pie-graph',id_maximize='maxi_ap-pie-graph',text='Activo & Pasivo',height =300)
                
            ],size=4),
            Column([
                card_graph_1(text='Activo vs Pasivo',id_graph='avsp-line-graph',id_maximize='maxi_avsp-line-graph',height = 300)
            ],size=8),
        ]),
        Row([
            Column([
                card_graph_1(text='Composicion del Pasivo',id_graph='comp-pasivo-graph',id_maximize='maxi_comp-pasivo-graph',height =320)
                
            ],size=12),
            
        ]),
        Row([
            Column([
                card_graph_1(text='Composicion del Activo',id_graph='comp-activo-graph',id_maximize='maxi_comp-activo-graph',height = 320)
            ],size=12),
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
    ])

def bg_analisis_activo(formato = [],years = []):
    return Container([
        html.Div([dmc.Modal(title = '', id = i, fullScreen=True, zIndex=10000, size= "85%" )for i in ['modal_activo-graph','modal_actvant-graph','modal_corr-ncorr-graph','modal_cuentas-act-graph']]),
        Row([
            Column([
                dmc.Card(children=[
                    dmc.Grid(
                        children=[
                            Column(title(text = 'Análisis del Activo',color="white"), size=3),
                            Column(
                                Entry.select(
                                    id = 'select-formato',
                                    texto = 'Formato',
                                    size = 'sm',
                                    value=formato[0],
                                    data = formato,
                                    clearable = False,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=2),
                            Column(
                                Entry.multiSelect(
                                    id = 'select-anio',
                                    texto = 'Año',
                                    place='Todos',
                                    value=[years[-1],years[-2]],
                                    data= years,
                                    size='sm',
                                    styles={"label": {"color": "white"}}
                                    
                                )
                            , size=4),
                            
                            Column(
                                Entry.select(
                                    id = 'select-mes',
                                    texto = 'Mes',
                                    size = 'sm',
                                    clearable = True,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=1),
                            Column(
                                Entry.select(
                                id = 'select-trismestre',
                                texto = 'Trimestre',
                                size = 'sm',
                                clearable = True,
                                styles={"label": {"color": "white"}}
                                
                            )
                            , size=1),
                            Column(
                                dmc.Select(
                                    id = 'select-moneda',
                                    clearable = False,
                                    placeholder='Todos',
                                    label = 'Moneda',
                                    size = 'sm',
                                    value = 'dolares',
                                    data = [
                                        {"value": "dolares", "label": "USD"},
                                        {"value": "soles", "label": "PEN"}
                                    ],
                                    searchable = False,
                                    styles={"label": {"color": "white"}}
                                    
                                    #nothingFound= 'No encontrado'
                                )
                            , size=1),
                            
                        ],
                        gutter="xs",
                    )
                    
                ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",         
                    style={"position": "static",'background-color':'#00353e'}
                ),
                
            ])
        ]),
        Row([
            Column([
                card_graph_1(id_graph='activo-graph',id_maximize='maxi_activo-graph',text='Activo',height =300)
                
            ],size=4),
            Column([
                card_graph_1(text='Activo Año Comparativo',id_graph='actvant-graph',id_maximize='maxi_actvant-graph',height = 300)
            ],size=8),
        ]),
        Row([
            Column([
                card_graph_1(text='Activo corriente vs no corriente',id_graph='corr-ncorr-graph',id_maximize='maxi_corr-ncorr-graph',height =320)
                
            ],size=6),
            Column([
                card_graph_1(text='Cuenta de Activos',id_graph='cuentas-act-graph',id_maximize='maxi_cuentas-act-graph',height = 320)
            ],size=6),
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
    ])
    

def bg_analisis_pasivo(formato = [],years=[],data_cuenta = [], value_cuenta = []):
    return Container([
        html.Div([dmc.Modal(title = '', id = i, fullScreen=True, zIndex=10000, size= "85%" )for i in ['modal_pasivo-graph','modal_pasvant-graph','modal_corr-ncorr-graph','modal_cuentas-pas-graph']]),
        Row([
            Column([
                dmc.Card(children=[
                    dmc.Grid(
                        children=[
                            Column(title(text = 'Análisis del Pasivo',color="white"), size=3),
                            Column(
                                Entry.select(
                                    id = 'select-formato',
                                    texto = 'Formato',
                                    size = 'sm',
                                    value=formato[0],
                                    data = formato,
                                    clearable = False,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=2),
                            Column(
                                Entry.multiSelect(
                                    id = 'select-anio',
                                    texto = 'Año',
                                    place='Todos',
                                    value=[years[-1],years[-2]],
                                    data= years,
                                    size='sm',
                                    styles={"label": {"color": "white"}}
                                    
                                )
                            , size=4),
                            
                            Column(
                                Entry.select(
                                    id = 'select-mes',
                                    texto = 'Mes',
                                    size = 'sm',
                                    clearable = True,
                                    styles={"label": {"color": "white"}}
                                )
                            , size=1),
                            Column(
                                Entry.select(
                                id = 'select-trismestre',
                                texto = 'Trimestre',
                                size = 'sm',
                                clearable = True,
                                styles={"label": {"color": "white"}}
                                
                            )
                            , size=1),
                            Column(
                                dmc.Select(
                                    id = 'select-moneda',
                                    clearable = False,
                                    placeholder='Todos',
                                    label = 'Moneda',
                                    size = 'sm',
                                    value = 'dolares',
                                    data = [
                                        {"value": "dolares", "label": "USD"},
                                        {"value": "soles", "label": "PEN"}
                                    ],
                                    searchable = False,
                                    styles={"label": {"color": "white"}}
                                    
                                    #nothingFound= 'No encontrado'
                                )
                            , size=1),
                            
                        ],
                        gutter="xs",
                    )
                    
                ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",         
                    style={"position": "static",'background-color':'#00353e'}
                ),
                
            ])
        ]),
        Row([
            Column([
                card_graph_1(id_graph='pasivo-graph',id_maximize='maxi_pasivo-graph',text='Pasivo',height =300)
                
            ],size=4),
            Column([
                card_graph_1(text='Pasivo Año Comparativo',id_graph='pasvant-graph',id_maximize='maxi_pasvant-graph',height = 300)
            ],size=8),
        ]),
        Row([
            Column([
                card_graph_1(text='Pasivo corriente vs no corriente',id_graph='corr-ncorr-graph',id_maximize='maxi_corr-ncorr-graph',height =320)
                
            ],size=6),
            Column([
                card_graph_select(text='Cuenta de Pasivos',id_graph='cuentas-pas-graph',id_maximize='maxi_cuentas-pas-graph',height = 320,data= data_cuenta,value=value_cuenta)
            ],size=6),
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        Download(),
    ])