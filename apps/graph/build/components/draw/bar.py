import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from apps.graph.build.utils.dict_colors import *

def bar_ctrl(df,x,y,txt,color,titulo,tipo_bar,legend,formato,position=None):
    fig=px.bar(df, 
                        x=x, 
                        y=y,
                        text=txt,
                        color=color,
                        title=titulo,
                        color_discrete_sequence=px.colors.qualitative.G10,
                        template='none',
                        barmode=tipo_bar,
                        
                      )
    fig.update_traces(textposition='outside',textfont_size=15,texttemplate=formato)
    fig.update_layout(showlegend=legend)
    fig.update_layout(margin=dict(l=50,r=20,b=30,t=70,pad=0,autoexpand=True),)  
    if legend == True:
        fig.update_layout(
        margin=dict(l=50,r=20,b=30,t=120,pad=0,autoexpand=True),
        legend_title_text='',
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,traceorder="reversed",
                                title_font_family="Arial",font=dict(family="Arial",size=9,color="black"),
                                bgcolor="white",bordercolor="Black",borderwidth=1,
                                ))  
    if position=='h':
        fig.update_layout(margin=dict(l=120,r=20,b=30,t=70,pad=0,autoexpand=True),)
    return fig

def BarGOV_SX(x, y,title,prueba,dinero,x_title,y_title):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=y,y=x,name=title,text=x,orientation='v',textposition='outside',texttemplate='%{text:.2s}'))#,marker={'color':[diccionario[i]for i in prueba]}
    try:
        fig.update_layout(marker={'color':[dict_cultivos[i]for i in prueba]})
    except: 
        pass
    fig.update_layout(title=title,
                        titlefont={'color': 'black','size': 15},
                        uniformtext_minsize=8, #uniformtext_mode='hide',
                        template='plotly_white')
    fig.update_layout(
        autosize=True,
        #width=100,
        #height=380,
        margin=dict(
            l=60,
            r=40,
            b=30,
            t=70,
            pad=0,
            autoexpand=True
        ),
        hovermode='closest',
        hoverlabel=dict(

        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        
        #showgrid=False,
        #modeclic='event+select'
        xaxis=dict(
            
            showticklabels=True,
            #showline=False,
            #showgrid=False,
            #linecolor='black',
            #linewidth=1,
            #ticks='outside',
            tickfont=dict(
                    #family='Arial',
                    color='black',
                    size=11
                       )
        ),
        yaxis=dict(
            gridcolor='#F2F2F2',
            showline=True,
            showgrid=True,
            ticks='outside',
            tickfont=dict(
                    family='Arial',
                    color='black',
                    size=12
                       )
        )
    
        )
    fig.update_layout(
    
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend_title="",)
        
     
    #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    #fig.add_trace(go.Scatter(x=[2, 6], y=[1,1]), row=1, col=1)
    if dinero=='soles':
        fig.update_yaxes(tickprefix="S./")
    elif dinero== 'dolares': 
        fig.update_yaxes(tickprefix="$")
    elif dinero==None:
        fig.update_yaxes(tickprefix="")
    return fig


def barCharTrace(df_,partida,ejex='Año',ejey='dolares'):
    fig = go.Figure()
    
        
    fig.add_trace(go.Bar(x=df_['Año'],
                            y=df_[partida],
                            name=partida,
                            marker_color='rgb(55, 83, 109)'
                            ))
    #fig.add_trace(go.Bar(x=df_pronostico['Año'],s
    #                        y=df_pronostico[partida],
    #                        name=f'Pronostico - {partida}',
    #                        marker_color='rgb(26, 118, 255)'
    #                        ))
    fig.update_layout(barmode='stack',title=f'Comparativo por Año - {partida}',template='none')
    fig.update_layout(legend=dict(yanchor="bottom",y=1.02,xanchor="right",x=1,orientation="h",),height=320)#,bgcolor="#F1F2F7"
    fig.update_layout(xaxis_title=ejex,yaxis_title=ejey)
    fig.update_xaxes(type='category')
    return fig