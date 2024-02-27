from dash import dcc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np

def bar_logistica_y1(df = None, height = 450 , moneda = 'Soles'):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df['DESCRIPCION'],
    y = df['Meses Inventario'],
    name = "Meses Inventario",
    cliponaxis=False,
    marker=dict(color="#3aa99b"),
    hovertemplate ='<br>'+'Producto'+': <b>%{x}</b><br>'+'Meses Inventario'+': <b>%{y}</b>',hoverlabel=dict(font_size=13,bgcolor="white")
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+'Meses Inventario'+'</b>'),
            side="left",
            range=[0, df['Meses Inventario'].max()]
        ),
        
        template= 'none',
        xaxis_title='<b>'+'Producto'+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>Meses de Inventario Promedio</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template = 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=13),color='black',showticklabels = False,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 40, b = 40))
    return fig

def bar_logistica_y2(df = None, height = 450 , moneda = 'Soles', y_col = ''):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df['DESCRIPCION'],
    y = df[y_col],
    name = 'Inventario Valorizado',
    cliponaxis=False,
    marker=dict(color="#5175c7"),
    hovertemplate ='<br>'+'Producto'+': <b>%{x}</b><br>'+'Inventario Valorizado'+': <b>%{y:,.2f}</b>',hoverlabel=dict(font_size=13,bgcolor="white")
    ))
    fig.add_trace(
        go.Scatter(
            x= df['DESCRIPCION'],
            y= df['Meses Inventario'],
            yaxis="y2",
            name="Meses de Inventario",
            marker=dict(color="#3aa99b"),
            cliponaxis=False,
            hovertemplate ='<br>'+'Producto'+': <b>%{x}</b><br>'+'Meses de Inventario'+': <b>%{y}</b>',hoverlabel=dict(font_size=13,bgcolor="white")
        )
    )
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+'Inventario Valorizado'+'</b>'),
            side="left",
            range=[0, df[y_col].max()]
        ),
        yaxis2=dict(
            title=dict(text='<b>'+'Meses Inventario'+'</b>'),
            side="right",
            range=[0, df['Meses Inventario'].max()],
            overlaying="y",
            tickmode="auto",
        ),
        template= 'none',
        xaxis_title='<b>'+'Producto'+'</b>',
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        title = f"<b>Variación de Inventario Valorizado</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template = 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=13),color='black',showticklabels = False,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(b = 40))
    
    return fig