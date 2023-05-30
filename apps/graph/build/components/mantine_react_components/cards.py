import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify
import dash_core_components as dcc
import plotly.express as px

button_style = {
    'position': 'absolute',
    'top': '4px',
    'right': '4px',
    'z-index': '9999'
}
button_style_2 = {
    'position': 'absolute',
    'bottom': '4px',
    'right': '4px',
    'z-index': '9999'
}
def actionIcon(variant="default",color="blue",ids='btn-filter',style=button_style_2,icono='maximize'):
    return html.Div(
            dmc.ActionIcon(
                            DashIconify(icon=f"feather:{icono}"), 
                            color=color, 
                            variant=variant,
                            id=ids,
                            n_clicks=0,
                            mb=10,
                            style=style
                        ),
        )

def cardIndex(title,link,graph,shadou,descripcion="Descripción"):
    return html.Div(
        dmc.Card(
                                children=[
                                    dmc.CardSection(
                                        dmc.Group(
                                            children=[
                                                html.A(title,href=link)
                                            #    dmc.Anchor(
                                            #    title,
                                            #    href=link,
                                            #)
                                               
                                                
                                            ],
                                            position="apart",
                                        ),
                                        withBorder=True,
                                        inheritPadding=True,
                                        py="xs",
                                    ),
                                    
                                    dmc.CardSection(
                                        children=[graph],
                                        #dmc.Image(
                                        #    src=image,
                                        #    mt="sm",
                                        #    height=300
                                        #),
                                    ),
                                    dmc.Text(
                                        children=[
                                            dmc.Text(
                                                [
                                                    
                                                    descripcion,
                                                ]
                                            ),
                                        ],
                                        mt="sm",
                                        color="dimmed",
                                        size="sm",
                                    ),

                                ],
                                withBorder=True,
                                shadow=shadou,
                                radius="md",
                                #style={"width": 350},
                            )
    )

def cardGraph(id_maximize='id-maximize',id_download='id-download',id_graph='id-graph'):
    return html.Div([
        dmc.Card(
                            children=[
                                actionIcon(ids=id_maximize,style=button_style),
                                actionIcon(ids=id_download,icono='download'),
                                dcc.Graph(id=id_graph)
                                
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                           
                        )
    ])