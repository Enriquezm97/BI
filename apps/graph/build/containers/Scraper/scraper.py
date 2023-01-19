from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

import requests
from bs4 import BeautifulSoup
from lxml import etree

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)
external_stylesheets=[dbc.themes.BOOTSTRAP]

def card_nofigure(valor,delta,title,subtitle):
    return dbc.Card(dbc.CardBody([
                        html.H6(children=title,style={'margin-bottom': '0px', 'color': 'white','textAlign': 'center','margin-bottom': '-40px'}),
                        html.H6(children=subtitle,style={'color': 'white','textAlign': 'center','margin-bottom': '30px'}),#, className="card-subtitle"
                        html.H4(children=valor,style={'color': 'white','textAlign': 'center'}),
        ]),style={'height': '100px'},color="dark")

def card(valor,delta,prefijo,title,subtitle):
    card = go.Figure(
            go.Indicator(
            mode = "number+delta",
            #mode = "number",
            #number_font_color="black",
            number_font_size=30,
            value =valor,#d.total_if,
            delta = {"reference": delta},
            title = {"text": f"{title}<br><span style='font-size:14;color:gray'>{subtitle}</span><br>"},
            #{"text": title,"font": {'size': 15}},#"font": {'size': 15,'family': "Arial"}
            number = {'prefix':prefijo },
            #position="top",
            #domain = {'y': [0, 1], 'x': [0.25, 0.75]}
        ))
        

    card.update_layout(
            showlegend=False,
            #plot_bgcolor="white",
            margin=dict(t=35,l=0,b=0,r=0),
            height=100,
            template="none",
            paper_bgcolor = "lightgray"
        )
    card.update_xaxes(visible=False, fixedrange=True)
    card.update_yaxes(visible=False, fixedrange=True)
    return card

def HomeScraper():
    app = DjangoDash('scraper', external_stylesheets=external_stylesheets)
    url='https://cuantoestaeldolar.pe/'
    page= requests.get(url)
    s = BeautifulSoup(page.text,'lxml')
    dom=etree.HTML(str(s))

    comprasunat=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[1]/div[2]/div/div[1]/p')[0].text)
    subcomprasunat=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[1]/div[2]/div/div[1]/span/div/p')[0].text)

    ventasunat=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[1]/div[2]/div/div[2]/p')[0].text)
    subventasunat=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[1]/div[2]/div/div[2]/span/div/p')[0].text)

    compradolar=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[2]/div[2]/div/div[1]/p')[0].text)
    subcompradolar=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[2]/div[2]/div/div[1]/span/div/p')[0].text)

    ventadolar=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[2]/div[2]/div/div[2]/p')[0].text)
    subventadolar=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[2]/div[2]/div/div[2]/span/div/p')[0].text)

    compraeuro=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[3]/div[2]/div/div[1]/p')[0].text)
    subcompraeuro=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[3]/div[2]/div/div[1]/span/div/p')[0].text)

    ventaeuro=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[3]/div[2]/div/div[2]/p')[0].text)
    subventaeuro=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[3]/div[2]/div/div[2]/span/div/p')[0].text)

    
    app.layout = html.Div([
        dbc.Row([
            dbc.Col([
                    html.H3(children="Resumen Home", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'}),
                    #html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
        ]),
        dbc.Row([
            dbc.Col([
                    card_nofigure(comprasunat,subcomprasunat,'Sunat','Compra')
                    #html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
            ],width=12,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                    card_nofigure(ventasunat,subventasunat,'Sunat','Venta')
                    
                    #html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
            ],width=12,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                    card_nofigure(compradolar,subcompradolar,'Dolar','Compra')
                    
                    #html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
            ],width=12,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                    card_nofigure(ventadolar,subventadolar,'Dolar','Venta')
                    
                    #html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
            ],width=12,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                    card_nofigure(compraeuro,subcompraeuro,'Euro','Compra')
                    
                    #html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
            ],width=12,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                    card_nofigure(ventaeuro,subventaeuro,'Euro','Venta')
                   
                    #html.H5(id="subtitle", style={'margin-bottom': '0px', 'color': 'black','textAlign': 'center'})
            ],width=12,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3")
        ])

    ])