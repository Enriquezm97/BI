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

def BarGOV_SX(x, y,title,prueba,dinero,x_title,y_title,promedio,y2):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=y,y=x,name=title,text=x,orientation='v',textposition='outside',texttemplate='%{text:.2s}',marker={'color':[dict_cultivos[i]for i in prueba]}))#,marker={'color':[diccionario[i]for i in prueba]}
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
        legend_title="",
        
        )
    fig.add_trace( go.Scatter( x=y, y=promedio,name='Promedio',mode='lines' ))#[1.5, 1, 1.3, 0.7, 0.8, 0.9]
    fig.update_layout(showlegend=True,legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1

                    ))
    fig.add_trace(go.Scatter(
                        x=y,
                        y=y2,
                        name="Hectáreas",
                        yaxis="y4",
                        text=y2,
                        #marker_color="#1f1587",
                        textposition='bottom right',
                        texttemplate='{text:.2s}'
                    ))
    fig.update_layout(
                    yaxis4=dict(title="Hectáreas",anchor="x",overlaying="y",side="right",titlefont_size=12,tickfont_size=12)
                    )
    fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    #fig.add_trace(go.Scatter(x=[2, 6], y=[1,1]), row=1, col=1)
    if dinero=='soles':
        fig.update_yaxes(tickprefix="S./")
    elif dinero== 'dolares': 
        fig.update_yaxes(tickprefix="$")
    elif dinero==None:
        fig.update_yaxes(tickprefix="")
    return fig