import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify
import dash_core_components as dcc
import plotly.express as px
import dash_ag_grid as dag
import pandas as pd


button_style = {
    'position': 'absolute',
    'top': '4px',
    'right': '4px',
    'z-index': '99'
}
button_style_2 = {'position': 'absolute','bottom': '4px','right': '4px','z-index': '99'}
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

def cardGraph(id_maximize='id-maximize',id_download='id-download',id_graph='id-graph',with_id=True,fig=None,icon_maximize=True):
    if icon_maximize == True:
        #padding
        if with_id == True:
            return html.Div([
                dmc.Card(
                                    children=[
                                        actionIcon(ids=id_maximize,style=button_style),
                                        #actionIcon(ids=id_download,icono='download'),
                                        dcc.Graph(id=id_graph)
                                        
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
                                        actionIcon(ids=id_maximize,style=button_style),
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
                                            dcc.Graph(id=id_graph)
                                            
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
                                            dcc.Graph(figure=fig)
                                            
                                        ],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px"}
                                    )
                ])


def cardTableDag(df=pd.DataFrame(),id_table='id-table',id_maximize='id-maximize',id_download='id-download',size_table='360',data_call=False,icon_maximize=True):
    if icon_maximize == True:
        if data_call == True:
            return html.Div([
                dmc.Card(
                                    children=[
                                        actionIcon(ids=id_maximize,style=button_style),
                                        #actionIcon(ids=id_download,icono='download'),
                                        dag.AgGrid(
                                            id=id_table,
                                            columnDefs=[{"field": i, "type": "rightAligned"} for i in df.columns],
                                            rowData=df.to_dict("records"),
                                            defaultColDef={"filter": True, "sortable": True, "floatingFilter": True,"resizable": True,},
                                            dashGridOptions={"rowSelection": "multiple"},
                                            style={'max-height': f'{size_table}px','overflow': "auto"},
                                            className="ag-theme-balham",
                                            #defaultColDef=
                                        ),
                                            
                                    ],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px"}

                                
                                )
            ])
        else: 
            return html.Div([
                dmc.Card(
                                    children=[
                                        actionIcon(ids=id_maximize,style=button_style),
                                        #actionIcon(ids=id_download,icono='download'),
                                        dag.AgGrid(
                                            id=id_table,
                                            defaultColDef={"filter": True, "sortable": True, "floatingFilter": True,"resizable": True,},
                                            dashGridOptions={"rowSelection": "multiple"},
                                            style={'max-height': f'{size_table}px','overflow': "auto"}
                                            #defaultColDef=
                                        ),
                                            
                                    ],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px"}

                                
                                )
            ])
    else:
            if data_call == True:
                return html.Div([
                    dmc.Card(
                                        children=[
                                            #actionIcon(ids=id_maximize,style=button_style),
                                            #actionIcon(ids=id_download,icono='download'),
                                            dag.AgGrid(
                                                id=id_table,
                                                columnDefs=[{"field": i, "type": "rightAligned"} for i in df.columns],
                                                rowData=df.to_dict("records"),
                                                defaultColDef={"filter": True, "sortable": True, "floatingFilter": True,"resizable": True,},
                                                dashGridOptions={"rowSelection": "multiple"},
                                                style={'max-height': f'{size_table}px','overflow': "auto"}
                                                #defaultColDef=
                                            ),
                                                
                                        ],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px"}

                                    
                                    )
                ])
            else: 
                return html.Div([
                    dmc.Card(
                                        children=[
                                            #actionIcon(ids=id_maximize,style=button_style),
                                            #actionIcon(ids=id_download,icono='download'),
                                            dag.AgGrid(
                                                id=id_table,
                                                defaultColDef={"filter": True, "sortable": True, "floatingFilter": True,"resizable": True,},
                                                dashGridOptions={"rowSelection": "multiple"},
                                                style={'max-height': f'{size_table}px','overflow': "auto"}
                                                #defaultColDef=
                                            ),
                                                
                                        ],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px"}

                                    
                                    )
                ])
            
def cardShowTotal(card_id='id-card',title_card='',value=0,simbolo='$',icon="ion:cash-outline"):  
     return html.Div([
                dmc.Card(
                    
                    html.Div(
                        [
                            html.H5(
                                [
                                    DashIconify(icon=icon, width=30,className="me-1"),
                                    title_card,
                                ]
                            ),
                            html.H2(f"{simbolo}{value:,}"),
                            #html.H5(
                            #    [f"{round(change, 2)}%", html.I(className=icon), " 24hr"],
                            #    className=f"text-{color}",
                            #),
                        ],
                        #className=f"border-{color} border-start border-5",
                    ),
                    className="text-center text-nowrap my-2 p-2",
                withBorder=True,
                shadow="sm",
                radius="md",
                id=card_id,
                
                )
            ])          