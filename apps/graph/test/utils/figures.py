
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from apps.graph.test.constans import DIC_RECURSOS_AGRICOLA,COLORS_G10,DICT_CULTIVOS_COLOR,DICT_TIPO_COSTO
from apps.graph.test.utils.functions.functions_data import create_stack_np, create_hover_custom


def convert_dict_to_graph(
    figure_dict = {}, height= 500, ejey_size_title = 9,
    ejey_size_ticked = 13
    
    ):
    figure = go.Figure(figure_dict)
    figure.update_layout(height = height),
    figure.update_layout(yaxis=dict(
                                titlefont_size = ejey_size_title,
                                tickfont_size = ejey_size_ticked
                            )
                         )
    return figure

def create_graph_empty(text=''):
    layout = dict(
        autosize=True,
        annotations=[dict(text=text, showarrow=False)],
        #paper_bgcolor="#1c2022",
        #plot_bgcolor="#1c2022",
        #font_color="#A3AAB7",
        font=dict(color="FFFF", size=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )
    return {"data": [], "layout": layout}

class GraphLinepx():
    def line_(
        df = pd.DataFrame(), x = '', y = '', color = None, height = 360,x_title = '',
        y_title = '', title_legend = '', order = {}, title ='',
        template = 'plotly_white', discrete_color = {}, custom_data=[],
        hover_template = '', size_text = 11, legend_orizontal = True, markers = False,legend_font_size = 12,
        tickfont_x = 11, tickfont_y = 11, 
    ):
        ejex = 'Semana' if x == 'week' else 'Fecha'
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
    

class GraphBargo():
    def bar_(df = pd.DataFrame(), x = '', y = '', text = '', orientation = 'v', height = 400 ,
        title = '', space_ticked = 130, xaxis_title = '',yaxis_title = '', showticklabel_x = True, 
        showticklabel_y = True , color_dataframe= '#145f82',list_or_color = None, customdata = [],
        template = 'plotly_white', size_tickfont = 11, title_font_size = 20, clickmode = False,
        ticklabel_color = 'rgba(0, 0, 0, 0.7)',plot_bgcolor = 'white', paper_bgcolor = 'white',left = 40
    ):  
        #print(df)
        figure = go.Figure()
        if len(customdata)>0:
            custom = create_stack_np(dataframe = df, lista = customdata)
            hover_aditional_datacustom = create_hover_custom(lista = customdata)
        else:
            custom = []
            hover_aditional_datacustom = ""
            
        if orientation == 'h':
            value_left = space_ticked
            value_bottom = 40
            hover = '<br>'+y+': <b>%{y}</b><br>'+x+': <b>%{x:,.2f}</b>'+hover_aditional_datacustom
        elif orientation == 'v': 
            value_left = 60
            value_bottom = space_ticked
            hover = '<br>'+x+': <b>%{x}</b><br>'+y+': <b>%{y:,.2f}</b>'+hover_aditional_datacustom
            
        if  type(list_or_color) == list:
                value_colors =  list_or_color  
           # if len(list_or_color) == 2:
           #     diccionario_colors = list_or_color[0] 
           #     column= list_or_color[1]
           #     value_colors=[diccionario_colors[i] for i in df[column]]
           #elif len(list_or_color) != 2:
           #     value_colors =  list_or_color  
                
                
        elif type(list_or_color) == dict:
            #print(df.columns)
            #if 'CULTIVO' in df.columns:
            #    print('w')
            #    value_colors = [list_or_color[i] for i in df['CULTIVO']]
            #else :
                try :
                    value_colors = [list_or_color[i] for i in df[x]]
                except:
                    value_colors = [list_or_color[i] for i in df[y]]
        else :
            value_colors = color_dataframe
        figure.add_trace(
            go.Bar(y = df[y],
                   x = df[x],   
                   text = df[text],
                   
                   orientation = orientation,
                   textposition = 'outside',
                   texttemplate =' %{text:.2s}',
                   marker_color = [DICT_CULTIVOS_COLOR[i]for i in df[color_dataframe]] if color_dataframe == 'CULTIVO' else value_colors,    
                  # marker_color = value_colors,
                   opacity=0.9,
                   name = '',
                   customdata = custom,
                   hovertemplate=hover,
                   #hoverinfo='none',
                   hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'),
                   cliponaxis=False,
            )
        )
        
        figure.update_layout(
                template = template,
                title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                #title_font_color="#145f82",
                xaxis_title='<b>'+xaxis_title+'</b>',
                yaxis_title='<b>'+yaxis_title+'</b>',
                legend_title="",
                #font=dict(size=15,color="black"),
                title_font_family="sans-serif", 
                title_font_size = title_font_size,
                title_font_color = "rgba(0, 0, 0, 0.7)",
                height = height, 
                
        )
        if clickmode == True:
            figure.update_layout(clickmode='event+select')
        size_list = len(df[x].unique()) if orientation == 'v' else len(df[y].unique())
        figure.update_xaxes(tickfont=dict(size=size_tickfont),color=ticklabel_color,showticklabels = showticklabel_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
        figure.update_yaxes(tickfont=dict(size=size_tickfont),color=ticklabel_color,showticklabels = showticklabel_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
        figure.update_layout(autosize=True,margin=dict(l = left, r = 40, b= 40, t = 20, ) )#
        figure.update_layout(plot_bgcolor = plot_bgcolor, paper_bgcolor = paper_bgcolor)
        if  size_list== 1:
            figure.update_layout(bargap=0.7)
        elif size_list== 2:
            figure.update_layout(bargap=0.4)
        elif size_list== 3:
            figure.update_layout(bargap=0.3)

        return figure

class GraphBarpx():
    def bar_(df = pd.DataFrame(), x = '', y = '', orientation = 'v', height = 400 ,
        title = '', xaxis_title = '',yaxis_title = '', showticklabel_x = True, 
        showticklabel_y = True , customdata = [],left_space = 40,bottom_space = 40,
        template = 'plotly_white', size_tickfont = 11, title_font_size = 20, clickmode = False
    ):      
            if len(customdata)>0:
                custom = create_stack_np(dataframe = df, lista = customdata)
                hover_aditional_datacustom = create_hover_custom(lista = customdata)
            else:
                custom = []
                hover_aditional_datacustom = ""
            figure=px.bar(df, x=x, y=y,text=y,custom_data=custom)
            figure.update_traces(hovertemplate='<br>'+x+': <b>%{x}</b><br>'+y+': <b>%{y:,.2f}</b>'+hover_aditional_datacustom)
            
            figure.update_xaxes(type='category')
            figure.update_traces(texttemplate='%{text:,.0f}', textposition='outside',cliponaxis=False,hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'))
            
            figure.update_layout(
                template = template,
                title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                #title_font_color="#145f82",
                xaxis_title='<b>'+xaxis_title+'</b>',
                yaxis_title='<b>'+yaxis_title+'</b>',
                legend_title="",
                #font=dict(size=15,color="black"),
                title_font_family="sans-serif", 
                title_font_size = title_font_size,
                title_font_color = "rgba(0, 0, 0, 0.7)",
                height = height, 
                
            )
            if clickmode == True:
                figure.update_layout(clickmode='event+select')
            #size_list = len(df[x].unique()) if orientation == 'v' else len(df[y].unique())
            figure.update_xaxes(tickfont=dict(size=size_tickfont),color='rgba(0, 0, 0, 0.7)',showticklabels = showticklabel_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
            figure.update_yaxes(tickfont=dict(size=size_tickfont),color='rgba(0, 0, 0, 0.7)',showticklabels = showticklabel_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
            figure.update_layout(margin=dict(l = left_space, r = 40, b= bottom_space, t = 40, pad = 1))
            #figure.update_yaxes(showline=True, linewidth=2, linecolor='black')#, gridcolor='Red'
            
            
            return figure
class GraphAreapx():
    def area_(
        df = pd.DataFrame(), x = '', y = '', color = None, height = 360,x_title = '',
        y_title = '', title_legend = '', order = {}, title ='',
        template = 'plotly_white', discrete_color = {}, custom_data=[],
         size_text = 11, legend_orizontal = True, markers = False,legend_font_size = 12,
        tickfont_x = 11, tickfont_y = 11
    ):
        figure = px.area(
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
            margin = dict( l = 20, r = 20, b = 10, t = 40, pad = 0, autoexpand = True),
            height = height,
            xaxis_title = '<b>'+x_title+'</b>',
            yaxis_title = '<b>'+y_title+'</b>',
            legend_title_text = title_legend,
            legend=dict(font=dict(size=legend_font_size,color="black"))
        )
        figure.update_traces(hovertemplate ='<br>'+y+': <b>%{y:,.2f}</b>',
                             cliponaxis=False)
        figure.update_xaxes(tickfont=dict(size=tickfont_x),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True) 
        figure.update_yaxes(tickfont=dict(size=tickfont_y),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)
        figure.update_layout(hovermode="x unified",hoverlabel=dict(font_size=size_text,font_family="sans-serif",bgcolor='rgba(255,255,255,0.75)'))#
        if legend_orizontal == True:
            figure.update_layout(legend=dict(orientation="h",yanchor="bottom",xanchor="right",y=1.02,x=1))
        return figure
        
        

class GraphPiego():
    def pie_(df = pd.DataFrame(),label_col = '', 
             value_col = '',list_or_color = None, dict_color = None,
             title = '', textinfo = 'percent+label+value' , textposition = 'inside',
             height = 300, showlegend = True, color_list = [], textfont_size = 12,
             plot_bgcolor = 'white', paper_bgcolor = 'white',top = 40
             
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
        figure.update_layout(height = height,margin = dict(t=top, b=30, l=30, r=30),showlegend = showlegend)
        figure.update_layout(plot_bgcolor = plot_bgcolor, paper_bgcolor = paper_bgcolor)
        return figure
    
class GraphMapgo():
    def map_agricola_scatter(df = pd.DataFrame(),importe = 'SALDO_MEX', ubicacion = [-79.536047,-7.034728], zoom = 13, height = 300):
            fig = go.Figure()
            for lista_string,lote in zip(df['POLYGON'].unique(),df['CONSUMIDOR'].unique()):
                lote_df = df.query(f"CONSUMIDOR == '{lote}'")
                cultivo = lote_df['CULTIVO'].unique()[0]
                df['hover_cultivo'] = cultivo
                df['hover_lote'] = lote
                df['hover_variedad'] = lote_df['VARIEDAD'].unique()[0]
                df['hover_costo'] = lote_df[importe].sum()
                #df['hover_ha'] = lote_df['AREA_CAMPAÑA'].sum()
                lista_coord=eval(lista_string)
                fig.add_trace(go.Scattermapbox(
                    mode="lines",
                    lon=[coord[0] for coord in lista_coord],
                    lat=[coord[1] for coord in lista_coord],
                    fill='toself',
            
                    fillcolor=DICT_CULTIVOS_COLOR[cultivo],#
                    line=dict(color="black",width=2),##
                    #hovertext=lote,
                    name='',
                    customdata=np.stack((df['hover_cultivo'], df['hover_lote'],df['hover_variedad'],df['hover_costo']),axis = -1),#{y:$,.0f}
                    hovertemplate='<br><b>Lote: %{customdata[1]}</b><br><b>Cultivo: %{customdata[0]}</b><br><b>Variedad: %{customdata[2]}</b><br><b>Importe: %{customdata[3]:,.2f}</b>',
                    hoverlabel=dict(font_size=15,bgcolor=DICT_CULTIVOS_COLOR[cultivo])
                ))

                # Configurar el diseño del mapa
                fig.update_layout(
                    mapbox=dict(
                        center = dict(lon=ubicacion[0],lat=ubicacion[1]),#,-79.53234131
                        style = "open-street-map",
                        zoom = zoom
                    ),
                    showlegend = False
                )
                fig.update_layout(height = height, margin = dict(t=0, b=0, l=0, r=0))
            
                                
            return fig

class GraphFunnelgo():
    def funnel_(df = pd.DataFrame(), x = '', y = '', text = '', height = 400 ,
        title = '', xaxis_title = '',yaxis_title = '', showticklabel_x = True, 
        showticklabel_y = True ,list_or_color = [],
        template = 'plotly_white',size_tickfont = 11,
        plot_bgcolor = 'white', paper_bgcolor = 'white',ticklabel_color = 'rgba(0, 0, 0, 0.7)'
    ):  
        
        figure = go.Figure(go.Funnel(
                    y = df[y],
                    x = df[x],
                    name='',
                    textposition = "outside",
                    textinfo = "value+percent total",
                    marker_color = list_or_color,
                    hovertemplate='<br>'+y+': <b>%{y}</b><br>'+x+':<b> %{x:,.2f}</b>',
                    hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'),
                    cliponaxis=False,
                    #marker = {"color": marker_colors},
                    
                    #marker_colors = marker_colors,
                    #marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
                    #"line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
                    #connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}}
                    )
        )
        
        figure.update_layout(
                template = template,
                title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                #title_font_color="#145f82",
                xaxis_title='<b>'+xaxis_title+'</b>',
                yaxis_title='<b>'+yaxis_title+'</b>',
                legend_title="",
                title_font_family="sans-serif", 
                title_font_size = 18,
                title_font_color = "rgba(0, 0, 0, 0.7)",
                height = height, 
        )
        figure.update_xaxes(tickfont=dict(size=size_tickfont),color=ticklabel_color,showticklabels = showticklabel_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
        figure.update_yaxes(tickfont=dict(size=size_tickfont),color=ticklabel_color,showticklabels = showticklabel_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)
        figure.update_layout(margin=dict(l = 50, r = 40, b= 20, t = 20, pad = 1))
        figure.update_layout(plot_bgcolor = plot_bgcolor, paper_bgcolor = paper_bgcolor)
        return figure

