from dash import Dash, dcc, html, Input, Output,State,dash_table
from dash.dash_table.Format import Format, Group, Scheme, Symbol

import plotly.express as px
import plotly.graph_objects as go

import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
from apps.graph.data.data import *
from apps.graph.build.components.mantine_react_components.cards import cardIndex
import json




def prueba():
    #external_script = [dbc.themes.BOOTSTRAP]
    app = DjangoDash('test', external_stylesheets=[dbc.themes.BOOTSTRAP])
    df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/hofstede-cultural-dimensions.csv",
    delimiter=";",
    )
    df.replace(to_replace="#NULL!", value=0, inplace=True)

    #app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



   




    app.layout = html.Div(
        [
            html.H1("Balance de Comprobación - Grupo 1"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col([
                        dbc.Card(
                                [
                                
                                    html.Div(
                                        [
                                            dbc.Label("GRUPO CORE"),
                                            dcc.Dropdown(
                                                id="grupo1",
                                                options=[{"label": col, "value": col} for col in df_bcomprobacion["grupo1"].dropna().unique()],
                                                #value=df_bcomprobacion["grupo3"].unique()[0],
                                                multi=True,
                                                
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            dbc.Label("Moneda"),
                                            dbc.RadioItems(  
                                                id="moneda",
                                                options=[
                                                                {'label': 'Soles', 'value': 'saldo_cargo_mof'},
                                                                {'label': 'Dolares', 'value': 'saldo_cargo_mex'},
                                                                
                                                        ],
                                                        value='saldo_cargo_mof',
                                                        labelStyle={'display': 'inline-block'}
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            dbc.Label("Serie de Tiempo"),
                                            dbc.RadioItems(  
                                                id="serie",
                                                options=[
                                                                {'label': 'Año', 'value': 'year'},
                                                                {'label': 'Trimestre', 'value': 'TRIM'},
                                                                {'label': 'Periodo', 'value': 'al_periodo'},
                                                                
                                                        ],
                                                        value='al_periodo',
                                                        labelStyle={'display': 'inline-block'}
                                            ),
                                        ]
                                    ),
                                ],
                                body=True,
                                )

                    ],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                    dbc.Col([dcc.Graph(id="graph-1")],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
                ],
                
            ),
            dbc.Row([
                dbc.Col([dcc.Graph(id="graph-2")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                #dbc.Col([dcc.Graph(id="graph-x")],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
            ]),
            
            dbc.Row([
                dbc.Col([dcc.Graph(id="graph-3")],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                #dbc.Col([dcc.Graph(id="graph-y")],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
            ]),
        ]
    )

    

    # Update Bar Chart Callback Function
    @app.callback(Output("graph-1", "figure"),
                  Output("graph-2", "figure"),  
                  #Output("graph-3", "figure"),
                  #Output("graph-x", "figure"),
                  Input("grupo1", "value"),
                  Input("moneda", "value"),
                  Input("serie", "value"),
                 )
    def make_country_graph(grupo1,moneda,serie):
        if grupo1 == None:
            dff = df_bcomprobacion
        else:
            dff = df_bcomprobacion[df_bcomprobacion['grupo1'].isin(grupo1)]

        dff_1=dff.groupby(['grupo1',serie])[[moneda]].sum().reset_index()
        dff_2=dff.groupby(['grupo2',serie])[[moneda]].sum().reset_index()
        #dff_3=dff.groupby(['grupo3',serie])[[moneda]].sum().reset_index()

        
        
        
        
        fig = px.line(dff_1, x=serie, y=moneda, color='grupo1',template='plotly_white')
        fig.update_layout(xaxis_tickfont_size=10,title='Resumen Partidas Grupo 1',height=380)
        
 
        fig2 = px.line(dff_2, x=serie, y=moneda, color='grupo2',custom_data=['grupo2'],template='plotly_white')#
        fig2.update_layout(xaxis_tickfont_size=10,title='Resumen Partidas Grupo 2',height=380)
        fig2.update_layout(clickmode='event+select')
        fig2.update_traces(marker_size=20)
        #fig3 = px.line(dff_3, x=serie, y=moneda, color='grupo3',template='plotly_white',color_discrete_sequence=px.colors.qualitative.Dark24)
        #fig3.update_layout(xaxis_tickfont_size=10,title='Resumen Partidas Grupo 3',height=380)

        #
        
        return fig,fig2#,fig3
    





    
    @app.callback(#Output("graph-1", "figure"),
                  #Output("graph-2", "figure"),  
                  Output("graph-3", "figure"),
                  #Output("graph-x", "figure"),
                  Input("grupo1", "value"),
                  Input("moneda", "value"),
                  Input("serie", "value"),
                  Input('graph-2', 'clickData'),
                 )
    def make_graph2(grupo1,moneda,serie,clickData):
        if clickData != None:
            partida=clickData['points'][0]['customdata']
            print(partida)
        if grupo1 == None and clickData == None:
            dff = df_bcomprobacion
            titulo='Resumen Partidas Grupo 3'
        elif grupo1 != None and clickData == None:
            dff = df_bcomprobacion[df_bcomprobacion['grupo1'].isin(grupo1)]
            titulo=f'Resumen Partidas Grupo 3 - {grupo1}'
        elif grupo1 != None and clickData != None:
            
            dff = df_bcomprobacion[(df_bcomprobacion['grupo1'].isin(grupo1))&(df_bcomprobacion['grupo2'].isin(partida))]
            titulo=f'Resumen Partidas Grupo 3 - {grupo1} - {partida}'
        elif grupo1 == None and clickData != None:
            
            dff = df_bcomprobacion[(df_bcomprobacion['grupo2'].isin(partida))]
            titulo=f'Resumen Partidas Grupo 3 - {partida}'
        dff_3=dff.groupby(['grupo3',serie])[[moneda]].sum().reset_index()
        
        fig3 = px.line(dff_3, x=serie, y=moneda, color='grupo3',template='plotly_white',color_discrete_sequence=px.colors.qualitative.Dark24)
        fig3.update_layout(xaxis_tickfont_size=10,title=titulo,height=380)
        return fig3
    """
    app.layout = html.Div([
        html.Div([
            html.Div([dbc.Card(dcc.Graph(id='graph2'),className="")],className="col-3 mb-8"),
            html.Div([dbc.Card(dcc.Graph(id='graph2'),className="")],className="col-3 mb-8"),
            html.Div([dbc.Card(dcc.Graph(id='graph2'),className="")],className="col-3 mb-8"),
            html.Div([dbc.Card(dcc.Graph(id='graph2'),className="")],className="col-3 mb-8"),
        ],className="row"),
        html.Div([
            html.Div([dbc.Card(dcc.Graph(id='graph2'),className="")],className="col-8 mb-8"),
            html.Div([dbc.Card(dcc.Graph(id='graph2'),className="")],className="col-4 mb-8"),
        ],className="row"),
        dbc.Row([
            
            dbc.Col([dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")],className="col"),
            dbc.Col([dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")],className="col"),
            dbc.Col([dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")],className="col"),
            dbc.Col([dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")],className="col"),
        ],className="row"),
        dbc.Row([
            dbc.Col([dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")],className="col-8"),
            dbc.Col([dbc.Card(dcc.Graph(id='graph2'),className="shadow-sm")],className="col-4"),
        ],className="row"),
    ])
    """
def tailwindcss():
    import dash
    import pandas as pd
    import plotly.express as px
    from dash import dcc, html

    external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
    app = DjangoDash('test',external_scripts=external_script,)

    df = pd.DataFrame(
            {
                "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
                "Amount": [4.2, 1.0, 2.1, 2.32, 4.20, 5.0],
                "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
            }
        )
    fruit_count = df.Fruit.count()
    total_amt = df.Amount.sum()
    city_count = df.City.count()
    variables = df.shape[1]
    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    fig1 = px.box(df, x="City", y="Amount", color="City")
    app.layout = html.Div(
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H1(children="Dash Tailwindcss Mastery", className=" py-3 text-5xl font-bold text-gray-800"),
                            html.Div(
                                children="""
                Dash with Tailwindcss = 💝 .
            """,
                                className="text-left prose prose-lg text-2xl  py-3 text-gray-600",
                            ),
                        ],
                        className="w-full mx-14 px-16 shadow-lg bg-white -mt-14 px-6 container my-3 ",
                    ),
                    html.Div(
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        f"${total_amt}",
                                        html.Br(),
                                        html.Span("Total Sales", className="text-lg font-bold ml-4"),
                                    ],
                                    className=" shadow-xl py-4 px-14 text-5xl bg-[#76c893] text-white  font-bold text-gray-800",
                                ),
                                html.Div(
                                    children=[
                                        fruit_count,
                                        html.Br(),
                                        html.Span("Fruit Count", className="text-lg font-bold ml-4"),
                                    ],
                                    className=" shadow-xl py-4 px-24 text-5xl bg-[#1d3557] text-white  font-bold text-gray-800",
                                ),
                                html.Div(
                                    children=[
                                        variables,
                                        html.Br(),
                                        html.Span("Variabales", className="inline-flex items-center text-lg font-bold ml-4"),
                                    ],
                                    className=" shadow-xl py-4 px-24 text-5xl bg-[#646ffa] text-white  font-bold text-gray-800",
                                ),
                                html.Div(
                                    children=[
                                        city_count,
                                        html.Br(),
                                        html.Span("City Count", className="text-lg font-bold ml-4"),
                                    ],
                                    className="w-full shadow-xl py-4 px-24 text-5xl bg-[#ef553b] text-white  font-bold text-gray-800",
                                ),
                            ],
                            className="my-4 w-full grid grid-flow-rows grid-cols-1 lg:grid-cols-4 gap-y-4 lg:gap-[60px]",
                        ),
                        className="flex max-w-full justify-between items-center ",
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    dcc.Graph(id="example-graph", figure=fig),
                                ],
                                className="shadow-xl w-full border-3 rounded-sm",
                            ),
                            html.Div(
                                children=[
                                    dcc.Graph(id="example-graph1", figure=fig1),
                                ],
                                className="w-full shadow-2xl rounded-sm",
                            ),
                        ],
                        className="grid grid-cols-1 lg:grid-cols-2 gap-4",
                    ),
                ],
                className="bg-[#ebeaee]  flex py-14 flex-col items-center justify-center ",
            ),
            #className="bg-[#ebeaee] container mx-auto px-14 py-4",
        )

def prueba2():

    data = px.data.stocks()

    app = DjangoDash('test2', external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dmc.Container(
        [
            dmc.Title(
                "Equity prices - Line chart and Table data", align="center"),
            dmc.Space(h=20),
            dmc.Button("Download Table Data", id="btn_csv"),
            dcc.Download(id="download-dataframe-csv"),
            dmc.Space(h=10),
            dmc.MultiSelect(
                label="Select stock you like!",
                placeholder="Select all stocks you like!",
                id="stock-dropdown",
                value=["GOOG", "AAPL"],
                data=[{"label": i, "value": i} for i in data.columns[1:]],
            ),
            dmc.Space(h=60),
            dmc.SimpleGrid(
                [
                    dcc.Graph(id="line_chart"),
                    dash_table.DataTable(
                        data.to_dict("records"),
                        [{"name": i, "id": i} for i in data.columns],
                        page_size=10,
                        style_table={"overflow-x": "auto"},
                    ),
                ],
                cols=2,
                id="simple_grid_layout",
                breakpoints=[
                    {"maxWidth": 1500, "cols": 2, "spacing": "md"},
                    {
                        "maxWidth": 992,
                        "cols": 1,
                        "spacing": "sm",
                    },  # common screen size for small laptops
                    {
                        "maxWidth": 768,
                        "cols": 1,
                        "spacing": "sm",
                    },  # common screen size for tablets
                ],
            ),
        ],
        fluid=True,
    )


    @app.callback(
        Output("line_chart", "figure"),
        Input("stock-dropdown", "value"),
    )
    def select_stocks(stocks):
        fig = px.line(data_frame=data, x="date", y=stocks, template="simple_white")
        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25), yaxis_title="Price", xaxis_title="Date"
        )
        return fig


    @app.callback(
        Output("download-dataframe-csv", "data"),
        Input("btn_csv", "n_clicks"),
        prevent_initial_call=True,
    )
    def func(n_clicks):
        return dcc.send_data_frame(data.to_csv, "mydf.csv")

def make_hover_image(link):
    return html.Div(
        [
            html.Img(
                src=link,
                style={'height':270, 'max-width':'100%'},#,'opacity':0.8
                #style={'height':'10%', 'width':'10%','opacity':0.3}
                #style={'opacity':0.3},
            ),
            
        ],
        #className="hover-container",
        #style={'opacity':0.3,'position':'relative'}
    )

def make_card(title,hrefs,link):
    
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    dbc.NavLink(
                        title,
                        href=hrefs,
                    ),
                ]
            ),
            dbc.CardBody(
                [
                    html.A(
                        make_hover_image(link),
                        href=hrefs,
                        style={'height':270, 'max-width':'100%'},
                        #id='testing',
                    ),
                    html.P(
                        'sin comentario',
                        className="card-text p-2 border-top",
                    ),
                ],
            ),
            # tooltip disabled for now
            # dbc.Tooltip(page["description"], target=tooltip_id),
        ],
        className="m-2 shadow ",
    )
