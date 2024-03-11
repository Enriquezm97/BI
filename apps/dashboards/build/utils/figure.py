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


def bar_horizontal(df = None, height = 350 , x = '',y = '',name_x = '',name_y = '',color = '#3aa99b', title = ''):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df[x],
    y = df[y],
    name = '',
    cliponaxis=False,
    marker=dict(color = color,cornerradius=15),
    hovertemplate ='<br>'+name_y+': <b>%{y}</b><br>'+name_x+': <b>%{x:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),
    orientation='h'
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+name_y+'</b>'),
            side="left",
            #range=[0, df['Meses Inventario'].max()]
        ),
        
        xaxis_title='<b>'+name_x+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 14,
        height = height,
        template = 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=11),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=11),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 20, b = 40, t = 40))
    return fig

def bar_ver(df = None, height = 400 , x = '',y = '',name_x = '',name_y = '',color = '#3aa99b', title = '',showticklabels_x = True, botton_size = 30):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df[x],
    y = df[y],
    name = '',
    cliponaxis=False,
    marker=dict(color = color,cornerradius=15),
    hovertemplate ='<br>'+name_x+': <b>%{x}</b><br>'+name_y+': <b>%{y:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),
    text=df[y],
    texttemplate='%{text:.2s}',
    textposition = "outside",
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+name_y+'</b>'),
            side="left",
            #range=[0, df['Meses Inventario'].max()]
        ),
        
        xaxis_title='<b>'+name_x+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 14,
        height = height,
        template = 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=11),color='black',showticklabels = showticklabels_x,title_font_family="sans-serif",title_font_size = 12,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=11),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    if botton_size == None:
        fig.update_layout(margin=dict(r = 20, t = 20,l=40))
    else:
        fig.update_layout(margin=dict(r = 20, t = 20,l=40, b= botton_size))
    return fig

def bar_hor(df = None, height = 350 , x = '',y = '',name_x = '',name_y = '',color = '#3aa99b', title = ''):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df[x],
    y = df[y],
    name = '',
    cliponaxis=False,
    marker=dict(color = color,cornerradius=15),
    hovertemplate ='<br>'+name_y+': <b>%{y}</b><br>'+name_x+': <b>%{x:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),
    orientation='h'
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+name_y+'</b>'),
            side="left",
            #range=[0, df['Meses Inventario'].max()]
        ),
        
        xaxis_title='<b>'+name_x+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 14,
        height = height,
        template = 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=11),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=11),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)  
    #fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 20, b = 30, t = 20,l =50))
    return fig

def pie_(df = pd.DataFrame(),label_col = '', 
             value_col = '',list_or_color = None, dict_color = None,
             title = '', textinfo = 'percent+label+value' , textposition = 'inside',
             height = 300, showlegend = True, color_list = [], textfont_size = 12, hole = 0,
             template = 'plotly_white'
             
    ):
        if dict_color != None:
            marker_colors = [dict_color[i]for i in df[label_col]] if type(dict_color) == dict else list_or_color
        elif color_list != None  and dict_color == None:
            marker_colors = color_list
        elif color_list == None  and dict_color == None:
              marker_colors = px.colors.qualitative.Plotly 
        figure = go.Figure()
        figure.add_trace(
            go.Pie(labels=df [label_col],values=df[value_col],
                marker_colors = marker_colors,
                #hovertemplate='<br><b>'+label_col+': %{labels}</b><br><b>'+value_col+': %{value:,.2f}</b>'
                hoverlabel=dict(font_size=15,bgcolor="white"),
                hovertemplate = "<b>%{label}</b> <br><b> %{percent}</b></br><b>%{value:,.0f}</b>",
                name='',
                rotation=10,
                )
        )    

        figure.update_layout(
            title={'text': f"<b>{title}</b>"},
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
            template = template
        
        )
        figure.update_traces(textposition = textposition, textinfo = textinfo, hole = hole)
        figure.update_traces(hoverinfo='label+percent+value', textfont_size = textfont_size)
        figure.update_layout(height = height,margin = dict(t=20, b=60, l=60, r=60),showlegend = showlegend)
        figure.update_layout(legend=dict(
                                #orientation="h",
                                #yanchor="bottom",
                                #y=1.02,
                                #xanchor="right",
                                #x=1,
                                font=dict(size=10,color="black"),
                            ))
        return figure


def line_(
        df = pd.DataFrame(), x = '', y = '', color = None, height = 360,x_title = '',
        y_title = '', title_legend = '', order = {}, title ='',
        template = 'plotly_white', discrete_color = {}, custom_data=[],
        hover_template = '', size_text = 11, legend_orizontal = True, markers = False,legend_font_size = 12,
        tickfont_x = 11, tickfont_y = 11
    ):
        figure = px.line(
            df, x = x, y = y, color = color , template = template,
            color_discrete_map = discrete_color, 
             hover_name = color,
            custom_data = custom_data,
            markers = markers,
            category_orders=order,
            #color_discrete_sequence  = '#0d6efd'
        )
        figure.update_layout(
            title = f"<b>{title}</b>",
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
            margin = dict( l = 20, r = 40, b = 20, t = 40, pad = 0, autoexpand = True),
            height = height,
            xaxis_title = '<b>'+x_title+'</b>',
            yaxis_title = '<b>'+y_title+'</b>',
            legend_title_text = title_legend,
            legend=dict(font=dict(size=legend_font_size,color="black"))
        )
        figure.update_traces(hovertemplate =hover_template,cliponaxis=False)
        figure.update_xaxes(tickfont=dict(size=tickfont_x),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True) 
        figure.update_yaxes(tickfont=dict(size=tickfont_y),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)
        figure.update_layout(hovermode="x unified",hoverlabel=dict(font_size=size_text,font_family="sans-serif",bgcolor='rgba(255,255,255,0.75)'))
        if legend_orizontal == True:
            figure.update_layout(legend=dict(orientation="h",yanchor="bottom",xanchor="right",y=1.02,x=1))
        return figure


def figure_two_traces(df = None, height = 300 , trace = [],colors = []):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = [df['Año'],df['Mes_']],
        y = df[trace[0]],
        name = trace[0],
        marker=dict(color=colors[0]),
        mode="markers+lines",
        cliponaxis=False,
        hovertemplate ='<br><b>%{x}</b><br><b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig.update_layout(hovermode="x unified")
    
    fig.add_trace(
        go.Scatter(
            x=[df['Año'],df['Mes_']],
            y=df[trace[1]],
            name=trace[1],
            marker=dict(color=colors[1]),
            mode="markers+lines",
            cliponaxis=False,
            hovertemplate ='<br><b>%{x}</b><br><b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
        )
    )
    fig.update_layout(hovermode="x unified")
    
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        #title = f"<b>{}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template= 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=12),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=12),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',',margin = dict(t=20,b=100,r=20))
    
    
    return fig

def figure_n_traces(df = None, height = 300 , trace = [],colors = [],ejex = [], hover_unified = True):
    fig = go.Figure()
    if len(ejex)==1:
        ejexx =df[ejex[0]]
    elif len(ejex)==2: 
        ejexx =[df[ejex[0]],df[ejex[1]]]#
    for value,color in zip(trace,colors):
        
        fig.add_trace(go.Scatter(
            x = ejexx,
            y = df[value],
            name = value,
            marker=dict(color=color),
            mode="markers+lines",
            cliponaxis=False,
            #hovertemplate ='<br><b>%{x}</b><br><b>%{y}</b>',
            hoverlabel=dict(font_size=16,bgcolor="white")
        ))
        if hover_unified == True:
            fig.update_layout(hovermode="x unified")
        else:
            fig.update_traces(hovertemplate ='<br><b>%{x}</b><br><b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white"))
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=-0
    ))
    fig.update_layout(
        #title = f"<b>{}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template= 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=12),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=12),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)  
    if len(ejex)==1:
        fig.update_layout(yaxis_tickformat = ',',margin = dict(t=20,b=60,r=20))
    elif len(ejex)==2: 
        fig.update_layout(yaxis_tickformat = ',',margin = dict(t=20,b=100,r=20))
    
    
    return fig





