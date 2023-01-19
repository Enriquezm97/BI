import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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