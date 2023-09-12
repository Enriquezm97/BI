from dash import dcc,html
import dash_mantine_components as dmc
import plotly.graph_objs as go
from apps.graph.test.utils.components.components_main import Button
from apps.graph.test.utils.figures import create_graph_empty
from apps.graph.test.utils.components.components_main import Entry
from dash_iconify import DashIconify

graph_empty = create_graph_empty('Esperando carga de DATA')

def cardGraph(
    id_maximize='id-maximize',
    id_download='id-download',
    id_graph='id-graph',
    with_id=True,
    fig=None,
    icon_maximize=True,
    height = 400
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
                                    style={'padding': "0px", 'height':height}
                                
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
                                    style={'padding': "0px", 'height':height}
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
                                        style={'padding': "0px", 'height':height}
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
                                        style={'padding': "0px", 'height':height}
                                    )
                ])
                
def cardGraphwithfilter(id_maximize='id-maximize',id_graph='id-graph',slider_id =''):
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
    

def cardSection(id_value = '',shadow='xl', radius='md', border =  True, text = '', num = 0, color_text ='white',color_section_title = '#0d6efd',contenido ='numero', content = [], padding_section=5,color_section_content = 'white', icon =''):
    if contenido == 'numero':
            section =  dmc.Text(children=[dmc.Center(children=num,id=id_value)], weight=500, style={"fontSize": 30})
                            
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
                    
                    #py="xs",
                    #bg = "blue"
                ),
                dmc.CardSection(children = section,p=padding_section,style={'backgroundColor':color_section_content}),
            ],
            withBorder = border,
            shadow = shadow,
            radius = radius,

        )
    
    
    
color1 = 'rgb(71, 214, 171)'
color2 = 'rgb(3, 20, 26)'
color3 = 'rgb(79, 205, 247)'
fontweight = 700
def cardGF(id = 'card-value',value_total=90000,text='owo',list_element=[{'value': 59, 'color': color1, 'label': '59%', "tooltip": "Docs - 14GB"},{'value': 35, 'color': color2, 'label': '35%'},{'value': 25, 'color': color3},]):
    return dmc.Card(
                
                children=[
                dmc.Group([
                    dmc.Text(id = id ,children=value_total,style={"fontSize": 25}, weight=fontweight),
                    #dmc.Text('18%', size='xs', color='rgb(9, 146, 104)'),
                    #dmc.Text(html.I(className='fas fa-arrow-up fa-fw fa-xs'), color='rgb(9, 146, 104)')
                ], spacing='0.5rem', sx={'align-items': 'baseline'}),
                dmc.Text(text, size='xl', color='dimmed'),
                dmc.Progress(
                    size='lg',
                    sections=list_element, 
                    #mt='2.125rem'
                ),
                

                ],
                withBorder=True,
                shadow='xl',
                radius='md',
                #style={'width': 440}
            )