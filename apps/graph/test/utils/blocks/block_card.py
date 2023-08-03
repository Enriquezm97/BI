from dash import dcc,html
import dash_mantine_components as dmc
import plotly.graph_objs as go
from apps.graph.test.utils.components import Button
from apps.graph.test.utils.figures import create_graph_empty

graph_empty = create_graph_empty('Esperando carga de DATA')

def cardGraph(
    id_maximize='id-maximize',
    id_download='id-download',
    id_graph='id-graph',
    with_id=True,
    fig=None,
    icon_maximize=True
):
    if icon_maximize == True:
        #padding
        if with_id == True:
            return html.Div([
                dmc.Card(
                                    children=[
                                        Button.actionIcon(id=id_maximize),
                                        #actionIcon(ids=id_download,icono='download'),
                                        dcc.Graph(id=id_graph,figure = graph_empty)
                                        
                                    ],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px"}
                                
                                )
            ])
        elif with_id == False:
            return html.Div([
                dmc.Card(
                                    children=[
                                        Button.actionIcon(id=id_maximize),
                                        #actionIcon(ids=id_download,icono='download'),
                                        dcc.Graph(figure=fig)
                                        
                                    ],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px"}
                                )
            ])
    else:
            if with_id == True:
                return html.Div([
                    dmc.Card(
                                        children=[
                                            #actionIcon(ids=id_maximize,style=button_style),
                                            #actionIcon(ids=id_download,icono='download'),
                                            dcc.Graph(id=id_graph,figure = graph_empty)
                                            
                                        ],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px"}
                                    )
                ])
            elif with_id == False:
                return html.Div([
                    dmc.Card(
                                        children=[
                                            #actionIcon(ids=id_maximize,style=button_style),
                                            #actionIcon(ids=id_download,icono='download'),
                                            dcc.Graph(figure = fig)
                                            
                                        ],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px"}
                                    )
                ])
                
def cardDivider(
    value = 1000,
    text = '',
    list_element = [
        {'value': 59, 'color': 'rgb(71, 214, 171)', 'label': '59%', "tooltip": "Docs - 14GB"},
        {'value': 35, 'color': 'rgb(3, 20, 26)', 'label': '35%'},
        {'value': 25, 'color': 'rgb(79, 205, 247)'},
    ]
):
    return dmc.Card(
                
                children=[
                dmc.Group([
                    dmc.Text( value ,style = {"fontSize": 18}, weight = 700),#25
                ], spacing='0.5rem', sx={'align-items': 'baseline'}),
                dmc.Text(text, size='md', color='blue',weight=500),
                dmc.Progress(
                    size='lg',
                    sections=list_element, 
                ),

                ],
                withBorder=True,
                shadow='xl',
                radius='md',
                #style = {'height':150}
            )
   