import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from apps.graph.build.utils.dict_colors import *

def figure__line(x,y,y2,name,namex,namey,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3):#,esperado,permitido,limite
    fig = go.Figure()

    #fig.update_layout(yaxis_tickformat = '.0%')
    fig.add_trace(go.Scatter(x=x, y=y,text=y,textposition="bottom center",
                        mode='lines+markers',
                        name=namex,line=dict( width=3)))
    fig.add_trace(go.Scatter(x=x, y=y2,
                        mode='lines',
                        name=namey,line=dict( width=2)))
    fig.update_layout(
        autosize=True,
        #width=,
        height=390,
        margin=dict(
            l=60,
            r=40,
            b=60,
            t=70,
            #pad=4,
            autoexpand=True

        ),
        legend=dict(orientation= 'h',yanchor="bottom",xanchor='center', x= 0.5, y= 1,font=dict(size=10,color="black"),),#family="Courier",
    )
    
    fig.update_layout(template='none', title=name)
    #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    fig.add_hrect(y0=rango_desde_1,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.2)
    fig.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.2)
    fig.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.2)
    
    #fig.add_hrect(y0=limite,y1=maximo, line_width=0, fillcolor="#fc2100", opacity=0.2)

    
    return fig