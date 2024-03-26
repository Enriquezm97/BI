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
            return DataDisplay.loadingOverlay(
                dmc.Card(children=[Button.actionIcon(id=id_maximize),dcc.Graph(id=id_graph,figure = graph_empty)],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px", 'height':height}
                        )
            )
            
        elif with_id == False:
            return DataDisplay.loadingOverlay(
                dmc.Card( children=[Button.actionIcon(id=id_maximize),dcc.Graph(figure=fig)],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px", 'height':height}
                        )
            )
            
    else:
            if with_id == True:
                return DataDisplay.loadingOverlay(
                    dmc.Card(children=[dcc.Graph(id=id_graph,figure = graph_empty)],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px", 'height':height}
                            )
                    )
                
            elif with_id == False:
                return DataDisplay.loadingOverlay(
                    dmc.Card(children=[dcc.Graph(figure = fig)],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px", 'height':height}
                                    )
                )

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
    
def card_small(id_value = '',text = ''):
  
    return dmc.Card(
            id='card',
            children=[
            dmc.Group([
                dmc.Text(id= id_value , size='1.5rem', weight=700),
                #dmc.Text('18%', size='xs', color='rgb(9, 146, 104)'),
                #dmc.Text(html.I(className='fas fa-arrow-up fa-fw fa-xs'), color='rgb(9, 146, 104)')
            ], spacing='0.5rem', sx={'align-items': 'baseline'}),
            dmc.Text(text, size='mb', color='dimmed'),
           
           

            ],
            withBorder=True,
            shadow='xl',
            radius='md',
        )
    
def card_stack(id_value = '',text = 'cpm'):
  
    return dmc.Card(
            id='card',
            children=[
            dmc.Group([
                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('CPM', color='black',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-cpm' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-1',
                ),
                
                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('INV VAL', color='black',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-invval' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-2',
                ),
                #
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('TOTAL STOCK', color='black',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-total-stock' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-2',
                ),
                #
                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('TI STOCK', color='black',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-stock' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-3',
                ),

                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('TI CON', color='black',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-consumo' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-4',
                ),
               
                
                #dmc.Text('18%', size='xs', color='rgb(9, 146, 104)'),
                #dmc.Text(html.I(className='fas fa-arrow-up fa-fw fa-xs'), color='rgb(9, 146, 104)')
            ], sx={'align-items': 'baseline'},grow=True,id='group-1'),#, spacing='0.5rem'
            
           
           

            ],
            withBorder=True,
            shadow='xl',
            radius='md',
        )
    

def card_graph_1(id_maximize='id-maximize', id_graph='id-graph',height = 300,icon ='',text ='',color_text = 'white',color_bg = "#00353e"):
    return dmc.Card(
            children=[
                dmc.CardSection(
                    children=[  
                            dmc.Text(children =[dmc.Center(children=[DashIconify(icon=icon, width=25,className="me-1"),text])] , weight=500, color= color_text),
                    ],
                    withBorder=True,
                    inheritPadding=True,
                    p = 2,
                    style={'backgroundColor':color_bg},

                ),
                DataDisplay.loadingOverlay(
                dmc.CardSection(children = [
                    
                        Button.actionIcon(id=id_maximize),dcc.Graph(id=id_graph,figure = graph_empty, config={'showEditInChartStudio': True,'plotlyServerURL': "https://chart-studio.plotly.com",'locale': 'es',})
                   
                ],p=0,style={'backgroundColor':'white','height':height,}),
                 )
            ],
            withBorder = True,
            shadow = 'xl',
            radius = 'xs',
            style={"position": "static",'height':height},
            p=0

        )
    

def card_graph_select(id_maximize='id-maximize', id_graph='id-graph',height = 300,icon ='',text ='',id_select = 'select-cuenta',data = [],value = None):
    return dmc.Card(
            children=[
                dmc.CardSection(
                    children=[  
                            dmc.Text(children =[dmc.Center(children=[DashIconify(icon=icon, width=25,className="me-1"),text])] , weight=500, color='white'),
                    ],
                    withBorder=True,
                    inheritPadding=True,
                    p = 2,
                    style={'backgroundColor':"#00353e"},

                ),
                DataDisplay.loadingOverlay(
                dmc.CardSection(children = [
                        Entry.select(id = id_select,size = 'xs',clearable = False,searchable=True,data = data,value=value,style = {'font-size': "80%",'position': 'absolute','top': '4px','left': '4px','z-index': '99', 'width':'150px'}),
                        Button.actionIcon(id=id_maximize),dcc.Graph(id=id_graph,figure = graph_empty)
                   
                ],p=0,style={'backgroundColor':'white','height':height,}),
                 )
            ],
            withBorder = True,
            shadow = 'xl',
            radius = 'md',
            style={"position": "static",'height':height},
            p=0

        )