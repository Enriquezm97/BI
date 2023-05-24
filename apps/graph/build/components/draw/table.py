import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_mantine_components as dmc

def createRowTable(df):
    values = df.values
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Tbody(rows)]
    return table

def createTableDMC(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table

def tableDMC(table_data):
    return html.Div([
        dmc.Table(
                striped=True,
                highlightOnHover=True,
                withBorder=True,
                withColumnBorders=True,
                children=table_data
        )
    ])

def tableSimpleDMC(table_data):
    return html.Div([
        dmc.Table(
                
                children=table_data,
                verticalSpacing='xs',
                horizontalSpacing='xs',
        )
    ])