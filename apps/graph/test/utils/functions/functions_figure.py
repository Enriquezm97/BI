import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def create_stack_np(dataframe = pd.DataFrame(), lista = []):
    return np.stack(tuple(dataframe[elemento] for elemento in lista),axis = -1)

def pie_(df = pd.DataFrame(),label_col = '', 
             value_col = '',list_or_color = None, dict_color = None,
             title = '', textinfo = 'percent+label+value' , textposition = 'inside',
             height = 300, showlegend = True, color_list = [], textfont_size = 12,hole=0
             
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
                hovertemplate = "<b>%{label}</b> <br>Porcentaje:<b> %{percent} </b></br>Importe: <b>%{value}</b>",
                name='',
                hole=hole
                )
        )    

        figure.update_layout(
            title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
        
        )
        figure.update_traces(textposition = textposition, textinfo = textinfo)
        figure.update_traces(hoverinfo='label+percent+value', textfont_size = textfont_size,marker=dict(line=dict(color='#000000', width=1)))
        figure.update_layout(height = height,margin = dict(t=40, b=30, l=10, r=10),showlegend = showlegend)
        
        return figure

def bar_figure_d(dataframe = None, x = '', y = '', text = '', orientation = 'h', title = '', height = 450):
    fig = go.Figure()
    fig.add_trace(go.Bar(
      x = dataframe[x],
      y = dataframe[y],
      text = dataframe[text],
      name = "",
      textposition = 'outside',
      texttemplate="%{x}",
      orientation = orientation,
      cliponaxis = False,

      hovertemplate ='<br>'+y+': <b>%{y}</b><br>'+x+': <b>%{x}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        template= 'none',
        margin = dict( l = 20, r = 40, b = 40, t = 40, pad = 5, autoexpand = True),
        height = height
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=12),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=12),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(xaxis_tickformat = ',')
    return fig

def figure_stock_var_y2(df = None, height = 450):
    stock_var_df = df.groupby(['Año', 'Mes','Mes_'])[['Stock valorizado']].sum().sort_values(['Año','Mes_']).reset_index()
    stock_items_df = df.groupby(['Año', 'Mes','Mes_'])[['Stock valorizado']].count().sort_values(['Año','Mes_']).reset_index()
    stock_items_df = stock_items_df.rename(columns = {'Stock valorizado':'Nro Items'})
    stock_var_items_df = stock_var_df.merge(stock_items_df,how = 'inner',on=["Año","Mes","Mes_"])
    fig = go.Figure()

    fig.add_trace(go.Bar(
    x = [stock_var_items_df['Año'],stock_var_items_df['Mes']],
    y = stock_var_items_df['Stock valorizado'],
    name = "Stock Valorizado",
    cliponaxis=False,
    hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+'Stock Valorizado'+': <b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig.add_trace(
        go.Scatter(
            x=[stock_var_items_df['Año'],stock_var_items_df['Mes']],
            y=stock_var_items_df['Nro Items'],
            yaxis="y2",
            name="Nro Items",
            marker=dict(color="crimson"),
            cliponaxis=False,
            hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+'Nro Items'+': <b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
        )
    )
    fig.update_layout(
        #legend=dict(orientation="v"),
        yaxis=dict(
            title=dict(text="Stock"),
            side="left",
            range=[0, stock_var_items_df['Stock valorizado'].max()]
        ),
        yaxis2=dict(
            title=dict(text="Nro Items"),
            side="right",
            range=[0, stock_var_items_df['Nro Items'].max()],
            overlaying="y",
            tickmode="auto",
        ),
        template= 'none'
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        title = f"<b>{'STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO'}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=14),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=14),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    return fig

def figure_bar_familia(df = None, height = 450):
    stock_familias_df = df.groupby(['Familia'])[['Stock valorizado']].sum().sort_values('Stock valorizado',ascending=True).reset_index()
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
    x = stock_familias_df['Stock valorizado'],
    y = stock_familias_df['Familia'],
    text = stock_familias_df['Stock valorizado'],
    name = "",
    textposition = 'outside',
    texttemplate="%{x}",
    orientation='h',
    cliponaxis=False,
    
    hovertemplate ='<br>'+'Familia'+': <b>%{y}</b><br>'+'Stock Valorizado'+': <b>%{x}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig2.update_layout(
        title = f"<b>{'STOCK POR FAMILIAS'}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        template= 'none',
        margin = dict( l = 20, r = 40, b = 40, t = 40, pad = 5, autoexpand = True),
        height = height
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig2.update_xaxes(tickfont=dict(size=12),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig2.update_yaxes(tickfont=dict(size=12),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig2.update_layout(xaxis_tickformat = ',')
    return fig2

def figure_bar_top_producto(df = None, height = 450):
    top_10_df= df.groupby(['Descripción'])[['Stock valorizado']].sum().sort_values(['Stock valorizado'],ascending = True).tail(10).reset_index()
    return bar_figure_d(dataframe = top_10_df, x = 'Stock valorizado', y = 'Descripción', text = 'Stock valorizado', orientation = 'h', title = 'Top 10 Productos', height = height)

def figure_bar_relative(df = None, height = 300, eje_color = 'ABC Ventas', title = ''):
    stock_abc_dff=df.groupby(['Año', 'Mes','Mes_',eje_color])[['Stock valorizado']].sum().sort_values(['Año','Mes_']).reset_index()
    lista_letras = sorted(stock_abc_dff[eje_color].unique())
    pivot_stick_adc_dff=stock_abc_dff.pivot_table(index=['Año', 'Mes','Mes_'],values=('Stock valorizado'),columns=(eje_color)).sort_values(['Año','Mes_']).reset_index()
    for letra in lista_letras:
        pivot_stick_adc_dff[f'{letra} %'] = pivot_stick_adc_dff[letra]/(pivot_stick_adc_dff[lista_letras].sum(axis=1))
    #pivot_stick_adc_dff['B %'] = pivot_stick_adc_dff['B']/(pivot_stick_adc_dff[['A','B','C']].sum(axis=1))
    #pivot_stick_adc_dff['C %'] = pivot_stick_adc_dff['C']/(pivot_stick_adc_dff[['A','B','C']].sum(axis=1))
    x_stock_abc = [pivot_stick_adc_dff['Año'],pivot_stick_adc_dff['Mes']]
    fig_e = go.Figure()
    for letra in lista_letras:
        fig_e.add_bar(x = x_stock_abc,
                    y = pivot_stick_adc_dff[f'{letra} %'],
                    name = letra,
                    customdata=create_stack_np(pivot_stick_adc_dff,letra),
                    hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+''+': <b>%{y}</b>'+'<br>'+letra+': <b>%{customdata[0]:,.0f}</b><br>',
                                    
                    #hoverlabel=dict(font_size=15,bgcolor="white")
                    )
    """
    fig_e.add_bar(x = x_stock_abc,
                y = pivot_stick_adc_dff['B %'],
                name = 'B',
                customdata=create_stack_np(pivot_stick_adc_dff,"B"),
                hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+''+': <b>%{y}</b>'+'<br>'+'B'+': <b>%{customdata[0]:,.0f}</b><br>',
                )
    fig_e.add_bar(x = x_stock_abc,
                y = pivot_stick_adc_dff['C %'],
                name = 'C',
                customdata=create_stack_np(pivot_stick_adc_dff,"C"),
                hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+''+': <b>%{y}</b>'+'<br>'+'C'+': <b>%{customdata[0]:,.0f}</b><br>',
                )
    """
    fig_e.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig_e.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        margin = dict( l = 50, r = 40, b = 70, t = 70, pad = 5, autoexpand = True),
        height = height
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig_e.update_layout(barmode="relative")
    fig_e.update_layout(yaxis_tickformat = '.0%', template='none')
    return fig_e

def figure_pie_rango_stock(df = None, height = 350):
    
    rango_stock_df = df.groupby(['Rango antigüedad del stock'])[['Stock valorizado']].sum().sort_values(['Rango antigüedad del stock']).reset_index()
    return pie_(df = rango_stock_df, label_col = 'Rango antigüedad del stock', value_col = 'Stock valorizado',
             title = '% Stock Segun Antigüedad', textinfo = 'percent+label' , textposition = 'outside',
             height = height, showlegend = False, color_list = px.colors.qualitative.Set3, textfont_size = 12,
    )
    
def figure_pie_rango_stock_count(df = None, height = 350):
    
    rango_stock_count_df = df.groupby(['Rango antigüedad del stock'])[['Stock valorizado']].count().sort_values(['Rango antigüedad del stock']).reset_index()
    return pie_(df = rango_stock_count_df, label_col = 'Rango antigüedad del stock', value_col = 'Stock valorizado',
             title = '% Stock Segun Antigüedad', textinfo = 'percent+label' , textposition = 'outside',
             height = height, showlegend = False, color_list = px.colors.qualitative.Set3, textfont_size = 12,
             hole = .6     
    )