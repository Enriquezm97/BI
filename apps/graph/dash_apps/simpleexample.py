from dash import Dash, dcc, html, Input, Output,State,dash_table
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dash_table.Format import Format, Group, Scheme, Symbol

def pie_chart(df,moneda):
    fig5 = px.pie(df, values=moneda, names='grupo_funcion',template="none",
             title='',hole=.6
             #hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'}
             )
    fig5.update_traces(textposition='inside', textinfo='percent+label',textfont_size=10)

    #fig2.update_layout(height=330,margin=dict(l=60,r=40,b=20,t=50))#,legend=dict(y=-0.7,xanchor="center",x=0.5)
    fig5.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5,
        #title_font_family="Times New Roman",
        font=dict(
            #family="Courier",
            size=8,
            color="black"
        ),
    ))
    fig5.update_traces(textposition='outside', textinfo='percent+label',textfont_size=10)
    fig5.update_layout(margin = dict(t=0, b=60, l=10, r=10),height=350)
    return fig5

def line_chart(df,moneda):
    fig6 = px.line(df, x="Mes", y=moneda, color='grupo_funcion',template="none",title='')
    fig6.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5,
       #title_font_family="Times New Roman",
        font=dict(
            #family="Courier",
            size=8,
            color="black"
        ),
    ))
    fig6.update_layout(
        
        xaxis_title='',
        yaxis_title='',
        legend_title='',
        
    )
    fig6.update_layout(margin = dict(t=0, b=100, l=40, r=30),height=350)
    return fig6

def bar_ori(df,moneda):
    fig8 = px.bar(df, x=moneda, y="year", 
                 color="grupo_funcion", barmode="group",orientation='h',template='none',text=moneda,title='')
    fig8.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5,
        #title_font_family="Times New Roman",
        font=dict(
        #    family="Courier",
            size=8,
            color="black"
        ),
    ))
    fig8.update_layout(
        
        xaxis_title='',
        yaxis_title='',
        legend_title="",
        
        )
    fig8.update_traces(textposition='outside')
    fig8.update_layout(margin = dict(t=0, b=60, l=40, r=30),height=350)
    return fig8
def table_dash(df):
    return dash_table.DataTable(
                    id='table-gastos',
                    columns=[{"name": c, "id": c,} for c in df],# "type": "numeric", "format": Format(group=",", precision=2,scheme="f")
                    active_cell={"row": 0, "column": 0, "column_id": 0, "row_id": 0},
                    sort_action="native",
                    data=df.to_dict('records'),
                    style_cell={'fontSize':11,"textTransform": "Uppercase",'textAlign': 'left',},
                    style_header={

                                       'textAlign': 'center',
                                        #"textTransform": "Uppercase",
                                        "fontWeight": "bold",
                                        "backgroundColor": "#ffffff",
                                        "padding": "10px 0px",
                                    },
    ),
def GraphwithHeader(idd,title):
    #df = get_data()
    
    return dbc.Card([
        dbc.CardHeader(html.H6(title, style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),style={"background": "white"}),
        dbc.CardBody([
        dcc.Graph(id=idd)#,style={"maxHeight": "800px", "overflow": "scroll",'font_family': 'cursive','font_size': '10px'}
        ])
        #dcc.Graph(id=idd),className="shadow-sm")
        ], color="light", outline=True)



app = DjangoDash('gastos_operativos', external_stylesheets=[dbc.themes.SANDSTONE])#url_theme1, dbc.icons.BOOTSTRAP, dbc_css,

app.layout = html.Div([
            dbc.Row([
                    
                        dbc.Col([
                            html.H3('GASTOS OPERATIVOS',className=" py-3 text-5xl font-bold text-gray-800"),#id='title''textAlign': 'center'# style={'margin-bottom': '0px', 'color': 'black'},
                            #html.H5(id='subtitle', style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
                            
                        ],width=8,className="col-xl-8 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([
                            dcc.Dropdown(
                                id='years',
                                multi=False,
                                searchable= True,
                                placeholder= '',
                                options=[],
                                style={
                                    
                                    'font-size': "90%",
                                    #'min-height': '2px',
                                    },
                                )    

                        ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                        dbc.Col([
                            dcc.RadioItems( 
                            id='moneda',
                            options=[
                                {'label': 'S/', 'value': 'saldo_cargo_mof'},
                                {'label': '$', 'value': 'saldo_cargo_mex'},
                                
                            ],
                            value='saldo_cargo_mex',
                        ) 

                        ],width=2,className="col-xl-2 col-md-12 col-sm-12 col-12 mb-3"),
                    ]),
            dbc.Row([
                dbc.Col([GraphwithHeader('graph1','Composición de Gastos Operativos')],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([GraphwithHeader('graph2','Composición Mensual de Gastos Operativos')],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
                dbc.Col([GraphwithHeader('graph3','Comparación de Gastos Anual')],width=4,className="col-xl-4 col-md-12 col-sm-12 col-12 mb-3"),
            ]),
            #rowGraphs.colsGraphThree('graph1','graph2','graph3'),
            dbc.Row([dbc.Col([html.Div(html.Div(id='table-gastos'))],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")])
        ])
