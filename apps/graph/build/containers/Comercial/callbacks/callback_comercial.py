from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
from apps.graph.build.components.comercial import *
import dash_mantine_components as dmc

def filtroInformeVentas2(app,rubro,df):
    #if rubro == 'Agricola' or rubro == 'Agroindustrial':
        
        @app.callback(
            Output("year","data"),
            Output("month","data"),
            Output("cultivo-tipo","data"),
            Output("variedad-grupo","data"),
            Output("cliente","data"),
            Input("year","value"),
            Input("month","value"),
            Input("cultivo-tipo","value"),
            Input("variedad-grupo","value"),
            Input("cliente","value"),
        )
        #if rubro == 'Agricola' or rubro == 'Agroindustrial':
        def ventas(year,month,cultivo,variedad,cliente):
            if month != None:
                df_v=df[df['MES_TEXT']==month]
            else:
                df_v=df
            if rubro == 'Agricola' or rubro == 'Agroindustrial':
                df_ventas=df_v.groupby(['YEAR','MES_TEXT','RAZON_SOCIAL','CULTIVO','VARIEDAD'])[['IMPORTEMOF']].sum().reset_index()

                if year==None and cultivo == None and variedad== None and cliente==None:
                    options=df_ventas

                elif year!=None and cultivo == None and variedad== None and cliente==None:    
                    options=df_ventas[df_ventas['YEAR']==year]
                elif year==None and cultivo != None and variedad== None and cliente==None:    
                    options=df_ventas[df_ventas['CULTIVO']==cultivo]
                
                elif year==None and cultivo == None and variedad!= None and cliente==None:    
                    options=df_ventas[df_ventas['VARIEDAD']==variedad]
                
                elif year==None and cultivo == None and variedad== None and cliente!=None:    
                    options=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
                
                elif year!=None and cultivo != None and variedad== None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)]
                
                elif year!=None and cultivo == None and variedad!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)]
                
                elif year!=None and cultivo == None and variedad== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

                
                elif year==None and cultivo != None and variedad== None and cliente!=None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year==None and cultivo != None and variedad!= None and cliente==None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]
                
                elif year==None and cultivo == None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and cultivo != None and variedad!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]

                elif year!=None and cultivo != None and variedad== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and cultivo == None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]

                elif year==None and cultivo != None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and cultivo != None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]


                option_year=[{'label': i, 'value': i} for i in options['YEAR'].unique()] 
                option_cultivo=[{'label': i, 'value': i} for i in options['CULTIVO'].unique()] 
                option_variedad=[{'label': i, 'value': i} for i in options['VARIEDAD'].unique()] 
                option_cliente=[{'label': i, 'value': i} for i in options['RAZON_SOCIAL'].unique()]
                #MES_TEXT 
                option_mes=[{'label': i, 'value': i} for i in options['MES_TEXT'].unique()]
                return option_year,option_mes,option_cultivo,option_variedad,option_cliente
            else:
                tipo=cultivo
                grupo=variedad
                df_ventas=df_v.groupby(['YEAR','MES_TEXT','RAZON_SOCIAL','TIPOVENTA','GRUPO'])[['IMPORTEMOF']].sum().reset_index()
                
                if year==None and tipo == None and grupo== None and cliente==None:
                    options=df_ventas

                elif year!=None and tipo == None and grupo== None and cliente==None:    
                    options=df_ventas[df_ventas['YEAR']==year]
                elif year==None and tipo != None and grupo== None and cliente==None:    
                    options=df_ventas[df_ventas['TIPOVENTA']==tipo]
                
                elif year==None and tipo == None and grupo!= None and cliente==None:    
                    options=df_ventas[df_ventas['GRUPO']==grupo]
                
                elif year==None and tipo == None and grupo== None and cliente!=None:    
                    options=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
                
                elif year!=None and tipo != None and grupo== None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['TIPOVENTA']==tipo)]
                
                elif year!=None and tipo == None and grupo!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['GRUPO']==grupo)]
                
                elif year!=None and tipo == None and grupo== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

                
                elif year==None and tipo != None and grupo== None and cliente!=None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year==None and tipo != None and grupo!= None and cliente==None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)]
                
                elif year==None and tipo == None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['GRUPO']==grupo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and tipo != None and grupo!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)]

                elif year!=None and tipo != None and grupo== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['TIPOVENTA']==tipo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and tipo == None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['GRUPO']==tipo)&(df_ventas['RAZON_SOCIAL']==cliente)]

                elif year==None and tipo != None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and tipo != None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]
                    
                option_year=[{'label': i, 'value': i} for i in options['YEAR'].unique()] 
                option_tipo=[{'label': i, 'value': i} for i in options['TIPOVENTA'].unique()] 
                option_grupo=[{'label': i, 'value': i} for i in options['GRUPO'].unique()] 
                option_cliente=[{'label': i, 'value': i} for i in options['RAZON_SOCIAL'].unique()] 
                #MES_TEXT 
                option_mes=[{'label': i, 'value': i} for i in options['MES_TEXT'].unique()]
                
                return option_year,option_mes,option_tipo,option_grupo,option_cliente

def titleInformeVentas(app,rubro,titulo):
    
        @app.callback(
        
        Output("title","children"),
        Output("subtitle","children"),
        Input("year","value"),
        Input("cultivo-tipo","value"),
        Input("cliente","value"),
        Input("radio-moneda","value"),
        
        )
        def title_ventas(year,cultivo,cliente,moneda):
            if moneda =='Soles':
                importe=dmc.Badge(moneda,variant='filled',color='blue', size='lg')
            elif moneda == 'Dolares':
                importe=dmc.Badge(moneda,variant='filled',color='blue', size='lg')



            if rubro == 'Agricola' or rubro == 'Agroindustrial':
                #general=str(titulo)+' '+str(moneda)
                if year == None:
                    title=dmc.Title(children=[titulo,dmc.Badge('ALL',variant='filled',color='gray', size='lg'),importe], order=2,align='center')
                else:
                    title=dmc.Title(children=[titulo,dmc.Badge(year,variant='filled',color='gray', size='lg'),importe], order=2,align='center')


                if cliente == None and cultivo == None:
                    subtitle=dmc.Title(children=[], order=3,align='center')
                elif cliente != None and cultivo == None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg')], order=3,align='center')
                    #subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(variedad,variant='filled',color='indigo', size='lg'),estado], order=2,align='center')
                elif cliente != None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(cultivo,variant='filled',color='indigo', size='lg')], order=3,align='center')
                elif cliente == None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cultivo,variant='filled',color='indigo', size='lg')], order=3,align='center')
                    
                return title,subtitle
            else:
                #general=str(titulo)+' '+str(moneda)
                tipo=cultivo
                if year == None:
                    title=dmc.Title(children=[titulo,dmc.Badge('ALL',variant='filled',color='gray', size='lg'),importe], order=2,align='center')
                else:
                    title=dmc.Title(children=[titulo,dmc.Badge(year,variant='filled',color='gray', size='lg'),importe], order=2,align='center')

                if cliente == None and cultivo == None:
                    subtitle=dmc.Title(children=[], order=3,align='center')
                elif cliente != None and cultivo == None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg')], order=3,align='center')
                    #subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(variedad,variant='filled',color='indigo', size='lg'),estado], order=2,align='center')
                elif cliente != None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(cliente,variant='filled',color='gray', size='lg'),dmc.Badge(tipo,variant='filled',color='indigo', size='lg')], order=3,align='center')
                elif cliente == None and cultivo != None:
                    subtitle=dmc.Title(children=[dmc.Badge(tipo,variant='filled',color='indigo', size='lg')], order=3,align='center')
                    
                    
                    
                return title,subtitle
    

def drawGraphInformeVentas(app,rubro,df):
        df_ventas=df
    
        @app.callback(
        Output("card","figure"),
        Output("bar-naviera","figure"),
        Output("pais_top_facturado","figure"),
        Output("cultivo_top_facturado","figure"),
        Output("mes_top","figure"),
        #Output("graph-last","figure"),
        #Output("bar_top_cultivo","figure"),
        #Input('filter-data', 'data'),
        Input("year","value"),
        Input("cultivo-tipo","value"),
        Input("variedad-grupo","value"),
        Input("cliente","value"),
        #Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input("radio-moneda","value")
        )
        def ventas(year,cultivo,variedad,cliente,radio):
            if rubro == 'Agricola' or rubro == 'Agroindustrial':
            #options=pd.read_json(data, orient='split')
                if year==None and cultivo == None and variedad== None and cliente==None:
                    options=df_ventas

                elif year!=None and cultivo == None and variedad== None and cliente==None:    
                    options=df_ventas[df_ventas['YEAR']==year]
                elif year==None and cultivo != None and variedad== None and cliente==None:    
                    options=df_ventas[df_ventas['CULTIVO']==cultivo]
                
                elif year==None and cultivo == None and variedad!= None and cliente==None:    
                    options=df_ventas[df_ventas['VARIEDAD']==variedad]
                
                elif year==None and cultivo == None and variedad== None and cliente!=None:    
                    options=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
                
                elif year!=None and cultivo != None and variedad== None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)]
                
                elif year!=None and cultivo == None and variedad!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)]
                
                elif year!=None and cultivo == None and variedad== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

                
                elif year==None and cultivo != None and variedad== None and cliente!=None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year==None and cultivo != None and variedad!= None and cliente==None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]
                
                elif year==None and cultivo == None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and cultivo != None and variedad!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]

                elif year!=None and cultivo != None and variedad== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and cultivo == None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]

                elif year==None and cultivo != None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and cultivo != None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]


                #card
                if radio=='Soles':
                    importe='IMPORTEMOF'
                elif radio=='Dolares':
                    importe='IMPORTEMEX'
                total=options[importe].sum()
                #bar naviera top
                df_naviera_top_facturado=options.groupby(['DESCRIPCION'])[[importe]].sum().sort_values(importe,ascending=True).tail(15).reset_index()#.head(15)
                #PAIS PIE
                df_pais_pie=options.groupby(['PAIS'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
                #TOP DE CULTIVOS
                df_cultivo_top=options.groupby(['CULTIVO'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
                #MES TOP
                df_mes_top=options.groupby(['MES_TEXT','MONTH'])[[importe]].sum().reset_index().sort_values('MONTH',ascending=True).reset_index()
                df_mes_top['%']=(df_mes_top[importe]/options[importe].sum())*100
                #CULTIVO PESO
                #df_cultivo_peso=options.groupby(['CULTIVO'])[['PESONETO_PRODUCTO']].sum().reset_index().sort_values('PESONETO_PRODUCTO',ascending=True)#
                #TEMPLATE STYLES
                #graph3=options.groupby(['RAZON_SOCIAL'])[[importe]].sum().reset_index().sort_values(importe,ascending=True).tail(15)
                #cliente_importe = go.Figure()
                #cliente_importe.add_trace(go.Bar(x=graph3['RAZON_SOCIAL'],y=graph3[importe],text=graph3[importe],orientation='v',textposition='inside',texttemplate='%{text:.2s}',name=importe))#,marker_color="#01B8AA"
                #cliente_importe.update_layout(title='Ventas por Cliente (Top15)',titlefont={'size': 15},uniformtext_minsize=8,template='none')
                #cliente_importe.update_layout(autosize=True,height=350,margin=dict(l=70,r=70,b=100,t=80),xaxis=dict(showticklabels=True,tickfont=dict(size=11)),
                #            yaxis=dict( tickfont=dict(size=11)))
                #cliente_importe.update_layout(
                #        showlegend=True,
                #        legend=dict(
                #        orientation="h",
                #        yanchor="bottom",
                #        y=1.02,
                #        xanchor="right",
                #        x=1

                #        )

                #    )
                #cliente_importe.update_layout(xaxis_title="Cliente",yaxis_title=radio,legend_title="")
                #cliente_importe.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
            

                return card(total,'none',importe),barNaviera(df_naviera_top_facturado,'none',importe,radio,''),paisFacturado(df_pais_pie,'none',importe),cultivoFacturado(df_cultivo_top,'none',importe,'Venta por Cultivo','CULTIVO'),mesTop(df_mes_top,'none',importe)#,cliente_importe#,barCultivo(df_cultivo_peso,template)
            else:
                tipo=cultivo
                grupo=variedad
                if year==None and tipo == None and grupo== None and cliente==None:
                    options=df_ventas

                elif year!=None and tipo == None and grupo== None and cliente==None:    
                    options=df_ventas[df_ventas['YEAR']==year]
                elif year==None and tipo != None and grupo== None and cliente==None:    
                    options=df_ventas[df_ventas['TIPOVENTA']==tipo]
                
                elif year==None and tipo == None and grupo!= None and cliente==None:    
                    options=df_ventas[df_ventas['GRUPO']==grupo]
                
                elif year==None and tipo == None and grupo== None and cliente!=None:    
                    options=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
                
                elif year!=None and tipo != None and grupo== None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['TIPOVENTA']==tipo)]
                
                elif year!=None and tipo == None and grupo!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['GRUPO']==grupo)]
                
                elif year!=None and tipo == None and grupo== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

                
                elif year==None and tipo != None and grupo== None and cliente!=None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year==None and tipo != None and grupo!= None and cliente==None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)]
                
                elif year==None and tipo == None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['GRUPO']==grupo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and tipo != None and grupo!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)]

                elif year!=None and tipo != None and grupo== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['TIPOVENTA']==tipo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and tipo == None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['GRUPO']==tipo)&(df_ventas['RAZON_SOCIAL']==cliente)]

                elif year==None and tipo != None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and tipo != None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]

                if radio=='Soles':
                    importe='IMPORTEMOF'
                elif radio=='Dolares':
                    importe='IMPORTEMEX'
                total=options[importe].sum()
                #bar naviera top
                df_naviera_top_facturado=options.groupby(['DESCRIPCION'])[[importe]].sum().sort_values(importe,ascending=True).tail(15).reset_index()#.head(15)
                #PAIS PIE
                df_pais_pie=options.groupby(['PAIS'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
                #TOP DE CULTIVOS
                df_cultivo_top=options.groupby(['GRUPO'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
                #MES TOP
                df_mes_top=options.groupby(['MES_TEXT','MONTH'])[[importe]].sum().reset_index().sort_values('MONTH',ascending=True).reset_index()
                df_mes_top['%']=(df_mes_top[importe]/options[importe].sum())*100
                #CULTIVO PESO
                #df_cultivo_peso=options.groupby(['CULTIVO'])[['PESONETO_PRODUCTO']].sum().reset_index().sort_values('PESONETO_PRODUCTO',ascending=True)#
                #TEMPLATE STYLES
                #graph3=options.groupby(['RAZON_SOCIAL'])[[importe]].sum().reset_index().sort_values(importe,ascending=True).tail(15)
                #cliente_importe = go.Figure()
                #cliente_importe.add_trace(go.Bar(x=graph3['RAZON_SOCIAL'],y=graph3[importe],text=graph3[importe],orientation='v',textposition='inside',texttemplate='%{text:.2s}',name=importe))#,marker_color="#01B8AA"
                #cliente_importe.update_layout(title='Ventas por Cliente (Top15)',titlefont={'size': 15},uniformtext_minsize=8,template='none')
                #cliente_importe.update_layout(autosize=True,height=350,margin=dict(l=70,r=70,b=100,t=80),xaxis=dict(showticklabels=True,tickfont=dict(size=11)),
                #            yaxis=dict( tickfont=dict(size=11)))
                #cliente_importe.update_layout(
                #        showlegend=True,
                #        legend=dict(
                #        orientation="h",
                #        yanchor="bottom",
                #        y=1.02,
                #        xanchor="right",
                #        x=1

                #        )

                #    )
                #cliente_importe.update_layout(xaxis_title="Cliente",yaxis_title=radio,legend_title="")
                #cliente_importe.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
            

                return card(total,'none',importe),barNaviera(df_naviera_top_facturado,'none',importe,radio,'Producto'),paisFacturado(df_pais_pie,'none',importe),cultivoFacturado(df_cultivo_top,'none',importe,'Grupo de Venta','GRUPO'),mesTop(df_mes_top,'none',importe)#,cliente_importe
            
def drawGraphExportacionVentas(app,rubro,df):
        df_ventas=df
    
        @app.callback(
        Output('card-export', 'figure'),
        Output('pie-export', 'figure'),
        Output('bar-mesvariedad', 'figure'),
        #Output('bar-mesformato', 'figure'),
        Output('map-vpais', 'figure'),
        #Output("bar_top_cultivo","figure"),
        #Input('filter-data', 'data'),
        Input("year","value"),
        Input("cultivo-tipo","value"),
        Input("variedad-grupo","value"),
        Input("cliente","value"),
        #Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input("radio-moneda","value")
        )
        def ventas(year,cultivo,variedad,cliente,radio):
            if rubro == 'Agricola' or rubro == 'Agroindustrial':
            #options=pd.read_json(data, orient='split')
                if year==None and cultivo == None and variedad== None and cliente==None:
                    options=df_ventas

                elif year!=None and cultivo == None and variedad== None and cliente==None:    
                    options=df_ventas[df_ventas['YEAR']==year]
                elif year==None and cultivo != None and variedad== None and cliente==None:    
                    options=df_ventas[df_ventas['CULTIVO']==cultivo]
                
                elif year==None and cultivo == None and variedad!= None and cliente==None:    
                    options=df_ventas[df_ventas['VARIEDAD']==variedad]
                
                elif year==None and cultivo == None and variedad== None and cliente!=None:    
                    options=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
                
                elif year!=None and cultivo != None and variedad== None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)]
                
                elif year!=None and cultivo == None and variedad!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)]
                
                elif year!=None and cultivo == None and variedad== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

                
                elif year==None and cultivo != None and variedad== None and cliente!=None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year==None and cultivo != None and variedad!= None and cliente==None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]
                
                elif year==None and cultivo == None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and cultivo != None and variedad!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)]

                elif year!=None and cultivo != None and variedad== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['CULTIVO']==cultivo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and cultivo == None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]

                elif year==None and cultivo != None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and cultivo != None and variedad!= None and cliente!=None:
                    options=df_ventas[(df_ventas['CULTIVO']==cultivo)&(df_ventas['VARIEDAD']==variedad)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]

                if radio=='Soles':
                    importe='IMPORTEMOF'
                    simbolo="S/"
                    
                elif radio=='Dolares':
                    importe='IMPORTEMEX'
                    simbolo="$"
                
                #card
                total=options[importe].sum()
                
                #pie
                df_totalv_variedad=options.groupby(['PAIS'])[[importe]].sum().reset_index()
                #fig_sun = px.sunburst(df_totalv_variedad, path=['PAIS','CULTIVO','VARIEDAD'], values=importe,color_continuous_scale='RdBu')
                #fig_sun.update_layout(title={'text': 'test'},
                #          template="plotly_white"
                #          )
                #fig_sun.update_layout(margin = dict(t=40, b=45, l=30, r=0),height=280)
                #fig_sun.update_layout(font=dict(size=9))
                #fig_sun.update_traces(textinfo="label+'percent root")


                #bar exportación

                df_exportacion=options.groupby(['FECHA','RAZON_SOCIAL'])[[importe]].sum().reset_index()
                
                
                
                #BAR EXPORTACION 2

                df_totalv_meses_peso=options.groupby(['MONTH','MES_TEXT','UNDEX'])[[importe]].sum().sort_values('MONTH',ascending=True).reset_index()
                
                
                #MAP

                df_ventas_for_pais=options.groupby(['PAIS','latitud','longitud'])[[importe]].sum().reset_index()
                #df_ventas_for_pais=df_ventas_for_pais[df_ventas_for_pais['latitud'].notnull()]
                df_ventas_for_pais=df_ventas_for_pais[df_ventas_for_pais[importe]>0]

                
                line_graph = px.line(df_exportacion, x="FECHA", y=importe,title=f'Serie de Tiempo de Ventas',template='none',hover_data=['RAZON_SOCIAL'])
                line_graph.update_layout(height=400,margin=dict(l=55, r=30, t=70, b=40),xaxis_title='Fecha',
                    yaxis_title=radio,)
                #line_graph.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
                

                
                return (Cards.cardPrefix(total,'Ventas de Exportación',None,None,simbolo,'none'),
                        #PieChartLegendLeft(df_totalv_variedad['VARIEDAD'],df_totalv_variedad['IMPORTEMOF'],'Total Ventas por Variedad'),
                        Piechart.legendLeft(df_totalv_variedad['PAIS'],df_totalv_variedad[importe],'Ventas Exportadas','none'),
                        #fig_sun,
                        #Barchart.horizontalExport(df_exportacion,'FECHA','total_resumen',None,f'Ventas por Mes por Tipo de Venta {title}',False,'FECHA',radio,importe,template),
                        line_graph,
                        #Barchart.horizontalExport(df_totalv_meses_peso,'MES_TEXT','total_resumen','UNDEX',f'Ventas por Mes y Formato {title}',False,'Mes',radio,importe,template),
                        Maps.mapPais(df_ventas_for_pais,'latitud','longitud','PAIS',importe,'none'),
                        )

                #card
                
            else:
                tipo=cultivo
                grupo=variedad
                if year==None and tipo == None and grupo== None and cliente==None:
                    options=df_ventas

                elif year!=None and tipo == None and grupo== None and cliente==None:    
                    options=df_ventas[df_ventas['YEAR']==year]
                elif year==None and tipo != None and grupo== None and cliente==None:    
                    options=df_ventas[df_ventas['TIPOVENTA']==tipo]
                
                elif year==None and tipo == None and grupo!= None and cliente==None:    
                    options=df_ventas[df_ventas['GRUPO']==grupo]
                
                elif year==None and tipo == None and grupo== None and cliente!=None:    
                    options=df_ventas[df_ventas['RAZON_SOCIAL']==cliente]
                
                elif year!=None and tipo != None and grupo== None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['TIPOVENTA']==tipo)]
                
                elif year!=None and tipo == None and grupo!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['GRUPO']==grupo)]
                
                elif year!=None and tipo == None and grupo== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['RAZON_SOCIAL']==cliente)]

                
                elif year==None and tipo != None and grupo== None and cliente!=None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year==None and tipo != None and grupo!= None and cliente==None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)]
                
                elif year==None and tipo == None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['GRUPO']==grupo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and tipo != None and grupo!= None and cliente==None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)]

                elif year!=None and tipo != None and grupo== None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['TIPOVENTA']==tipo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and tipo == None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['YEAR']==year)&(df_ventas['GRUPO']==tipo)&(df_ventas['RAZON_SOCIAL']==cliente)]

                elif year==None and tipo != None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)&(df_ventas['RAZON_SOCIAL']==cliente)]
                
                elif year!=None and tipo != None and grupo!= None and cliente!=None:
                    options=df_ventas[(df_ventas['TIPOVENTA']==tipo)&(df_ventas['GRUPO']==grupo)&(df_ventas['RAZON_SOCIAL']==cliente)&(df_ventas['YEAR']==year)]

                if radio=='Soles':
                    importe='IMPORTEMOF'
                    simbolo="S/"
                    
                elif radio=='Dolares':
                    importe='IMPORTEMEX'
                    simbolo="$"
                
                #card
                total=options[importe].sum()
                
                #pie
                df_totalv_variedad=options.groupby(['TIPOVENTA'])[[importe]].sum().reset_index()
                #bar exportación

                df_exportacion=options.groupby(['FECHA','RAZON_SOCIAL'])[[importe]].sum().reset_index()
                
                
                
                #BAR EXPORTACION 2

                df_totalv_meses_peso=options.groupby(['MONTH','MES_TEXT','UNDEX'])[[importe]].sum().sort_values('MONTH',ascending=True).reset_index()
                
                
                #MAP

                df_ventas_for_pais=options.groupby(['PAIS','latitud','longitud'])[[importe]].sum().reset_index()
                #df_ventas_for_pais=df_ventas_for_pais[df_ventas_for_pais['latitud'].notnull()]
                df_ventas_for_pais=df_ventas_for_pais[df_ventas_for_pais[importe]>0]

                
                line_graph = px.line(df_exportacion, x="FECHA", y=importe,title=f'Serie de Tiempo de Ventas',template='none',hover_data=['RAZON_SOCIAL'])
                line_graph.update_layout(height=400,margin=dict(l=55, r=30, t=70, b=40),xaxis_title='Fecha',
                    yaxis_title=radio,)
                line_graph.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
                

                
                return (Cards.cardPrefix(total,'Ventas de Exportación',None,None,simbolo,'none'),
                        #PieChartLegendLeft(df_totalv_variedad['VARIEDAD'],df_totalv_variedad['IMPORTEMOF'],'Total Ventas por Variedad'),
                        Piechart.legendLeft(df_totalv_variedad['TIPOVENTA'],df_totalv_variedad[importe],'Ventas por Tipo','none'),
                        #Barchart.horizontalExport(df_exportacion,'FECHA','total_resumen',None,f'Ventas por Mes por Tipo de Venta {title}',False,'FECHA',radio,importe,template),
                        line_graph,
                        #Barchart.horizontalExport(df_totalv_meses_peso,'MES_TEXT','total_resumen','UNDEX',f'Ventas por Mes y Formato {title}',False,'Mes',radio,importe,template),
                        Maps.mapPais(df_ventas_for_pais,'latitud','longitud','PAIS',importe,'none'),
                        )