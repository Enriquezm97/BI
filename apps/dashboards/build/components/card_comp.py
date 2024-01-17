import dash_mantine_components as dmc
import plotly.graph_objs as go
from dash import dcc,html
from dash_iconify import DashIconify
from ..components.display_comp import * 
from ..components.layout_comp import * 
from ..components.figure_comp import graph_empty 

graph_empty = graph_empty('Esperando carga')

def card_graph(id_maximize='id-maximize', id_graph='id-graph',with_id=True,fig=None,icon_maximize=True,height = 400,id_item = ''):
    if icon_maximize == True:
        #padding
        if with_id == True:
            return html.Div([
                dmc.Card(children=[Button.actionIcon(id=id_maximize),dcc.Graph(id=id_graph,figure = graph_empty)],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px", 'height':height}
                        )
            ])
        elif with_id == False:
            return html.Div([
                dmc.Card( children=[Button.actionIcon(id=id_maximize),dcc.Graph(figure=fig)],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px", 'height':height}
                        )
            ])
    else:
            if with_id == True:
                return html.Div([
                    dmc.Card(children=[dcc.Graph(id=id_graph,figure = graph_empty)],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px", 'height':height}
                            )
                ])
            elif with_id == False:
                return html.Div([
                    dmc.Card(children=[dcc.Graph(figure = fig)],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px", 'height':height}
                                    )
                ])

def cardGraphwithfilter(id_maximize='id-maximize',id_graph='id-graph',slider_id =''):
            return html.Div([
                dmc.Card(children=[Button.actionIcon(id=id_maximize),dcc.Graph(id=id_graph,figure = graph_empty)],
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

def card(content = [],shadow='xl', radius='md', border =  True):
    return dmc.Card(
                
                children = content,
                withBorder = border,
                shadow = shadow,
                radius = radius,
                p = 8
            )
    
def card_value(id_value = '',shadow='xl', radius='md', border =  True, text = '', num = 0, color_text ='white',color_section_title = '#228be6',contenido ='numero', content = [], padding_section=5,color_section_content = 'white', icon =''):
    if contenido == 'numero':
            section =  dmc.Text(children=[dmc.Center(children=num,id=id_value)], weight=500, style={"fontSize": 25})
                            
    elif contenido == 'tabla':
            section = content      
    return dmc.Card(
            children=[
                dmc.CardSection(
                    children=[  
                            dmc.Text(children =[dmc.Center(children=[DashIconify(icon=icon, width=25,className="me-1"),text])] , weight=500, color=color_text),
                    ],
                    withBorder=True,
                    inheritPadding=True,
                    p = 5,
                    style={'backgroundColor':color_section_title},

                ),
                dmc.CardSection(children = section,p=padding_section,style={'backgroundColor':color_section_content}),
            ],
            withBorder = border,
            shadow = shadow,
            radius = radius,

        )
def cardGF(id = 'card-value',value_total=90000,text='owo',list_element=[{'value': 59, 'color': 'rgb(71, 214, 171)', 'label': '59%', "tooltip": "Docs - 14GB"},{'value': 35, 'color': 'rgb(3, 20, 26)', 'label': '35%'},{'value': 25, 'color': 'rgb(79, 205, 247)'},]):
    return dmc.Card(
                
                children=[
                    dmc.Group([
                        dmc.Text(id = id ,children=value_total,style={"fontSize": 25}, weight=700),
                    ], spacing='0.5rem', sx={'align-items': 'baseline'}),
                    dmc.Text(text, size='xl', color='dimmed'),
                    dmc.Progress(
                        size='lg',
                        sections=list_element, 
                    ),
                ],
                withBorder=True,
                shadow='xl',
                radius='md',
                #style={'width': 440}
            )