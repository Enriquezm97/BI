import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from apps.graph.build.utils.dict_colors import *
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import  html

color1 = 'rgb(71, 214, 171)'
color2 = 'rgb(3, 20, 26)'
color3 = 'rgb(79, 205, 247)'

fontweight = 700

def cardGF(value_total=90000,text='owo',list_element=[{'value': 59, 'color': color1, 'label': '59%', "tooltip": "Docs - 14GB"},{'value': 35, 'color': color2, 'label': '35%'},{'value': 25, 'color': color3},]):
    return dmc.Card(
                
                children=[
                dmc.Group([
                    dmc.Text(value_total,style={"fontSize": 25}, weight=fontweight),
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
   
def calculateCard(df,col='Ingresos_Generales',color=[],list_partidas=[],pivot=True,col_=''):
            total=df[col].sum()
            lista_diccionario=[]
            for element,color in zip(list_partidas,color):
                if pivot==True:
                    percent_value=round((df[element].sum()/total)*100)
                else:
                    df_filtro=df[df[col_]==element]
                    percent_value=round((df_filtro[col].sum()/total)*100)
                dicts={'value': percent_value, 'color': color, 'label': f'{percent_value}%', "tooltip": element}
                #print(f"UNA ITERACION:{(df[element].sum()/total)*100}")
                lista_diccionario.append(dicts)
            return lista_diccionario