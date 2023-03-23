import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from apps.graph.build.utils.dict_colors import *

def paisFacturado(df_pais_pie,template,importe,title):
    #ultimo_year=sorted(df_pais_pie['YEAR'].unique())[-1]
    pais_top_facturado = go.Figure()

    pais_top_facturado.add_trace(go.Pie(labels=df_pais_pie['PAIS'], values=df_pais_pie[importe]))#,rotation=100
    pais_top_facturado.update_traces(hoverinfo="label+percent+value")#, hole=.4)#label+value+percent
        #fig.update_traces(textposition='inside', textinfo='percent+label')
    pais_top_facturado.update_traces(textposition='inside', textinfo='label+value',textfont=dict(size=13))#line=dict(color='#000000', width=1)#colors=px.colors.qualitative.D3, , marker=dict(line=dict(color='#000000', width=1)),rotation=90
    pais_top_facturado.update_layout(
                                title={
                                'text': title,
                                #'y':0.9,
                                #'x':0.5,
                                },
                                titlefont={'size': 15},
                                showlegend=False,
                                template=template
                                )
    pais_top_facturado.update_layout(margin = dict(t=40, b=10, l=10, r=30),height=250)#,height=330
    #pais_top_facturado.update_layout(paper_bgcolor='#f7f7f7')
    return pais_top_facturado
