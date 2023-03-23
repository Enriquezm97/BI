
import plotly.express as px
import plotly.graph_objects as go

colors=["#01B8AA","#8D6FD1","#73B761","#CD4C46","#71AFE2","#95DABB","#F2C80F","#581B44","#ff8300","#263550"]
def card(total_if,template,importe):
    if importe == 'IMPORTEMOF':
        prefijo='S/'
    elif importe == 'IMPORTEMEX':
        prefijo='$'
    card = go.Figure(
            go.Indicator(
            mode = "number+delta",
            #mode = "number",
            #number_font_color="black",
            number_font_size=35,
            value =total_if,#d.total_if,
            #delta = {"reference": 0, "valueformat": ".0f"},
            title = {"text": "Ventas Totales","font": {'size': 15}},#"font": {'size': 15,'family': "Arial"}
            number = {'prefix':prefijo },
            #position="top",
            #domain = {'y': [0, 1], 'x': [0.25, 0.75]}
        ))
        

    card.update_layout(
            showlegend=False,
            #plot_bgcolor="white",
            margin=dict(t=35,l=0,b=0,r=0),
            height=100,
            template=template,
        )
    card.update_xaxes(visible=False, fixedrange=True)
    card.update_yaxes(visible=False, fixedrange=True)
    #card.update_layout(paper_bgcolor='#f7f7f7')
    return card
#GRAPH - BAR HORIZONTAL
def barNaviera(df_naviera_top_facturado,template,importe,x_title,y_title):
    Bar_top_naviera = go.Figure()
    Bar_top_naviera.add_trace(go.Bar(x=df_naviera_top_facturado[importe],y=df_naviera_top_facturado['DESCRIPCION'],text=df_naviera_top_facturado[importe],orientation='h',
                                    textposition='outside',texttemplate='%{text:.2s}',#,marker_color=px.colors.qualitative.Dark24,#marker_color=colors,
                                    marker_color="#145f82",
                                    hovertemplate =
                                        '<br><b>Producto</b>:%{y}'+
                                        '<br><b>Importe</b>: %{x:.2f}<br>',
                                    hoverlabel=dict(
                                    #bgcolor="white",
                                    font_size=11,
                                    #font_family="Arial"
                                    ),
                                    name=''
                                ))#.2s
                            #marker=dict(colors=),
                            #marker={'color':[diccionario[i]for i in prueba]}
                            #  color=x,
                            #  colorscale='algae',
                            #  showscale=False),
                            #))
    Bar_top_naviera.update_layout(title={
                                            'text':'Ventas por Producto',
                                            
                                        },
                                titlefont={'size': 13},
                            #titlefont={'color': 'black','size': 20},
                            #uniformtext_minsize=8, uniformtext_mode='hide',
                            
                            
                            template=template)
    Bar_top_naviera.update_layout(
            autosize=True,
            #width=,
            #height=380,
            margin=dict(
                l=250,
                r=50,
                b=40,
                t=50,
                #pad=4,
                #autoexpand=True

            ),
            yaxis=dict(
                titlefont_size=7,
                tickfont_size=7,
                #showticklabels=False,
                
                
            ),
            
            )
    Bar_top_naviera.update_layout(
        
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend_title="",
        
        )
    #Bar_top_naviera.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    return Bar_top_naviera

def paisFacturado(df_pais_pie,template,importe):
    pais_top_facturado = go.Figure()

    pais_top_facturado.add_trace(go.Pie(labels=df_pais_pie['PAIS'], values=df_pais_pie[importe]))#,rotation=100
    pais_top_facturado.update_traces(hoverinfo="label+value+percent")#, hole=.4)#label+value+percent
        #fig.update_traces(textposition='inside', textinfo='percent+label')
    pais_top_facturado.update_traces(textposition='inside', textinfo='label+percent+value', marker=dict(colors=px.colors.qualitative.T10),textfont=dict(size=10),rotation=90)#line=dict(color='#000000', width=1)
    pais_top_facturado.update_layout(
                                title={
                                'text': 'Ventas por País',
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

def cultivoFacturado(df_cultivo_top,template,importe,title,label):
    cultivo_top_facturado = go.Figure()


    cultivo_top_facturado.add_trace(go.Pie(labels=df_cultivo_top[label], values=df_cultivo_top[importe],hole=.5))#,rotation=100
    cultivo_top_facturado.update_traces(hoverinfo="label+value+percent")#, hole=.4)#label+value+percent
        #fig.update_traces(textposition='inside', textinfo='percent+label')
    cultivo_top_facturado.update_traces(textposition='outside', textinfo='label+percent',textfont=dict(size=8),rotation=150, marker=dict(colors=px.colors.qualitative.T10))#line=dict(color='#000000', width=1)#, marker=dict(colors=colors)
    cultivo_top_facturado.update_layout(
                                title=title,
                                #'y':0.9,
                                #'x':0.5,
                                
                                titlefont={'size': 15},
                                showlegend=False,
                                template=template
                                )
    cultivo_top_facturado.update_layout(margin = dict(t=40, b=10, l=30, r=30),height=250)#,height=330
    #cultivo_top_facturado.update_layout(paper_bgcolor='#f7f7f7')
    return cultivo_top_facturado
# BAR VERTICAL
def mesTop(df_mes_top,template,importe):
    mes_top = go.Figure()
    mes_top.add_trace(go.Bar(x=df_mes_top['MES_TEXT'],y=df_mes_top[importe],text=df_mes_top[importe],orientation='v',textposition='outside',texttemplate='%{text:.2s}',marker_color="#145f82",))#,marker_color="#01B8AA"
    mes_top.update_layout(
                            title={
                                    'text':'Ventas por Mes',
                                        'y': 0.93,
                                        'x': 0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top',
                            },
                            titlefont={'size': 13},
                            uniformtext_minsize=8,# uniformtext_mode='hide',
                            template=template)
    mes_top.update_layout(
            autosize=True,
            #width=100,
            height=300,
            margin=dict(
                l=40,
                r=40,
                b=20,
                t=50,
                #pad=4,
                #autoexpand=True
            ),
            #hovermode='closest',
            #hoverlabel=dict( ),
            #paper_bgcolor='white',
            #plot_bgcolor='white',
            
            #showgrid=False,
            #modeclic='event+select'
            xaxis=dict(
                
                showticklabels=True,
                
                #linecolor='black',
                #linewidth=1,
                #ticks='outside',
                tickfont=dict(
                        #family='Arial',
                        #color='black',
                        size=12
                        )
            ),
            yaxis=dict(
                showticklabels=True,
                #gridcolor='#F2F2F2',
                #showline=True,
                #showgrid=True,
                #ticks='outside',
                tickfont=dict(
                        #family='Arial',
                        #color='black',
                        size=12
                        )
            )
            
            ) 
    mes_top.add_trace(go.Scatter(
            x=df_mes_top['MES_TEXT'],
            y=df_mes_top['%'],
            name="%",
            yaxis="y4",
            text=df_mes_top['%'],
            #marker_color="#1f1587",
            textposition='bottom right',
            texttemplate='%{text:.2s}'
        ))
    mes_top.update_layout(
        
        yaxis4=dict(
                
                title="%",
                titlefont=dict(
                    #color="#1f1587"
                ),
                tickfont=dict(
                    #color="#1f1587"
                ),
                anchor="x",
                overlaying="y",
                side="right",
                titlefont_size=12,
                tickfont_size=12,
                tickprefix="%",
                #showtickprefix="last",
            ),
    )
    mes_top.update_layout(
        showlegend=False,

    )
    #mes_top.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    return mes_top

def barCultivo(df_cultivo_peso,template):

    Bar_top_cultivo = go.Figure()
    Bar_top_cultivo.add_trace(go.Bar(x=df_cultivo_peso['PESONETO_PRODUCTO']/10000000,y=df_cultivo_peso['CULTIVO'],text=df_cultivo_peso['PESONETO_PRODUCTO'],orientation='h',textposition='inside',texttemplate='%{text:.2s}'))#.2s#,marker_color=colors
                            #marker=dict(colors=),
                            #marker={'color':[diccionario[i]for i in prueba]}
                            #  color=x,
                            #  colorscale='algae',
                            #  showscale=False),
                            #))
    Bar_top_cultivo.update_layout(title={
                                            'text':'Peso Exportado(Millones Kg)',
                                            
                                        },
                            #titlefont={'color': 'black','size': 20},
                            #uniformtext_minsize=8, uniformtext_mode='hide',
                            
                            
                            template=template)
    Bar_top_cultivo.update_layout(
            autosize=True,
            #width=,
            height=470,
            margin=dict(
                l=75,
                r=20,
                b=40,
                t=50,
                #pad=4,
                #autoexpand=True

            ),
            yaxis=dict(
                titlefont_size=10,
                tickfont_size=10,
                #showticklabels=False,
                
                
            ),
            
            )
    Bar_top_cultivo.update_layout(
        
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        
        )
    return Bar_top_cultivo
    
def card_ventas(valor,prefijo,title):
    card = go.Figure(
            go.Indicator(
            mode = "number+delta",
            #mode = "number",
            #number_font_color="black",
            number_font_size=35,
            value =valor,#d.total_if,
            #delta = {"reference": 0, "valueformat": ".0f"},
            title = {"text": title,"font": {'size': 16}},#"font": {'size': 15,'family': "Arial"}
            number = {'prefix':prefijo },
            #position="top",
            #domain = {'y': [0, 1], 'x': [0.25, 0.75]}
        ))
        

    card.update_layout(
            showlegend=False,
            #plot_bgcolor="white",
            margin=dict(t=35,l=0,b=0,r=0),
            height=100,
            template="none",
        )
    card.update_xaxes(visible=False, fixedrange=True)
    card.update_yaxes(visible=False, fixedrange=True)
    #card.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    return card

class Cards():
    def cardPrefix(values,title,y,delta,prefix,template):
        if template==None:
            template="plotly_white"
        fig = go.Figure(
                go.Indicator(
                        mode = "number+delta",number_font_size=35,
                        value = values,
                        delta = {"reference": delta, "valueformat": "f"},
                        title = {"text": title,"font": {'size': 20}},#'font = {'color': "darkblue", 'family': "Arial"},'family': "Arial"}"font": {'size': 15}
                        number = {'prefix': prefix},
                    )
        )
        fig.add_trace(
                go.Scatter(
                        y = y,
                        fill='tonexty',
                        hovertemplate=None,
                        mode='lines',
                        hoverinfo='skip'
                        )
                    )
        fig.update_layout(
            showlegend=False,
            margin=dict(t=35,l=0,b=0,r=0),
            height=100,
            template=template,
        )
        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=False, fixedrange=True)
        
        #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
        return fig


class Barchart():
    def horizontalExport(df,x,y,flush,title,legend,x_title,y_title,hover_data,template):#,custom,hovertemplate
        if template==None:
            template="plotly_white"
        fig = px.bar(df, x=x, y=y,color=flush,hover_data=[hover_data],text=hover_data,color_discrete_sequence=px.colors.qualitative.T10+px.colors.qualitative.Dark24)#,color_discrete_map=Variedad
        #,custom_data=custom
        fig.update_traces(textposition="none")
        fig.update_layout(
                height=390,
                title={
                        'text':title,
                        'y': 0.93,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                    },
                font=dict(size=11),
                template=template,
                showlegend=legend,
                margin=dict(l=30, r=30, t=70, b=5),
                yaxis=dict(fixedrange=True),
                xaxis=dict(fixedrange=True),
            )
        fig.update_layout(
            xaxis_title=x_title,
            yaxis_title=y_title,
            legend_title="",
        )
        fig.update_layout(
                    legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=1.25,
                    xanchor="center",
                    x=0.5
        ))
        fig.update_traces(
                    hoverinfo='none',
                    hoverlabel=dict(font_size=15)
        )
    
        return fig


class Piechart():
    def legendLeft(label,values,title,template):
        if template==None:
            template="plotly_white"
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=label, values=values))#,rotation=100
        fig.update_traces(hoverinfo="label+value+percent", marker=dict(colors=px.colors.qualitative.T10+px.colors.qualitative.Dark24))#, hole=.4)#label+value+percent
        fig.update_traces(textposition='inside', textinfo='percent')
        fig.update_layout(title={'text': title},
                          template=template
                          )
        fig.update_layout(margin = dict(t=40, b=45, l=30, r=0),height=280)
        fig.update_layout(showlegend=True)
        fig.update_layout(font=dict(size=9))
        #fig.update_layout(paper_bgcolor='#f7f7f7')
        #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
        return fig

class Linechart():pass

class Maps():
    def mapPais(df,lat,lon,flush,size,template):
        mapbox = px.scatter_mapbox(df, lat=lat, lon=lon,color=flush, size=size,size_max=70, zoom=1,template=template,color_discrete_sequence=px.colors.qualitative.T10+px.colors.qualitative.Dark24)
        mapbox.update_layout(
                    height=390,
                    mapbox=dict(
                        accesstoken='pk.eyJ1IjoiZW5yaXF1ZXo5NyIsImEiOiJja3RjNjFzNHkyMmVwMm9wbDByZG0wM3BuIn0.uTzX-97GtCDnM6I661nxFg',  # Create free account on Mapbox site and paste here access token
                        
                    ),
                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    hovermode='closest',
                    autosize=True,
                    hoverlabel=dict( font_size=15)
        )
        #mapbox.update_layout(paper_bgcolor='#f7f7f7')
        
        return mapbox