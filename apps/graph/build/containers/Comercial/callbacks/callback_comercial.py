from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
from apps.graph.build.components.comercial import *


def filtroInformeVentas2(app,rubro,df):
    #if rubro == 'Agricola' or rubro == 'Agroindustrial':
        
        @app.callback(
            Output("year","data"),
            Output("cultivo-tipo","data"),
            Output("variedad-grupo","data"),
            Output("cliente","data"),
            Input("year","value"),
            Input("cultivo-tipo","value"),
            Input("variedad-grupo","value"),
            Input("cliente","value"),
        )
        #if rubro == 'Agricola' or rubro == 'Agroindustrial':
        def ventas(year,cultivo,variedad,cliente):
            if rubro == 'Agricola' or rubro == 'Agroindustrial':
                df_ventas=df.groupby(['YEAR','RAZON_SOCIAL','CULTIVO','VARIEDAD'])[['IMPORTEMOF']].sum().reset_index()

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
                
                return option_year,option_cultivo,option_variedad,option_cliente
            else:
                tipo=cultivo
                grupo=variedad
                df_ventas=df.groupby(['YEAR','RAZON_SOCIAL','TIPOVENTA','GRUPO'])[['IMPORTEMOF']].sum().reset_index()
                
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
                
                return option_year,option_tipo,option_grupo,option_cliente

def titleInformeVentas(app,rubro):
    
        @app.callback(
        
        Output("title","children"),
        Output("subtitle","children"),
        Input("year","value"),
        Input("cultivo-tipo","value"),
        Input("cliente","value"),
        Input("radio-moneda","value"),
        
        )
        def title_ventas(year,cultivo,cliente,moneda):
            if rubro == 'Agricola' or rubro == 'Agroindustrial':
                general='Informe de Ventas'+' '+str(moneda)
                if year == None:
                    title=general
                else:
                    title=general+' '+str(year)
                if cliente == None and cultivo == None:
                    subtitle=''
                elif cliente != None and cultivo == None:
                    subtitle=str(cliente)
                elif cliente != None and cultivo != None:
                    subtitle=str(cliente)+' '+str(cultivo)
                elif cliente == None and cultivo != None:
                    subtitle=str(cultivo)
                    
                return title,subtitle
            else:
                general='Informe de Ventas'+' '+str(moneda)
                tipo=cultivo
                if year == None:
                    title=general
                else:
                    title=general+' '+str(year)
                if cliente == None and tipo == None:
                    subtitle=''
                elif cliente != None and tipo == None:
                    subtitle=str(cliente)
                elif cliente != None and tipo != None:
                    subtitle=str(cliente)+' '+str(tipo)
                elif cliente == None and tipo != None:
                    subtitle=str(tipo)
                    
                    
                return title,subtitle
    

def drawGraphInformeVentas(app,rubro,df):
        df_ventas=df
    
        @app.callback(
        Output("card","figure"),
        Output("bar-naviera","figure"),
        Output("pais_top_facturado","figure"),
        Output("cultivo_top_facturado","figure"),
        Output("mes_top","figure"),
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
            

                return card(total,'none',importe),barNaviera(df_naviera_top_facturado,'none',importe,radio,'Producto'),paisFacturado(df_pais_pie,'none',importe),cultivoFacturado(df_cultivo_top,'none',importe,'Venta por Cultivo','CULTIVO'),mesTop(df_mes_top,'none',importe)#,barCultivo(df_cultivo_peso,template)
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
                df_cultivo_top=options.groupby(['TIPOVENTA'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
                #MES TOP
                df_mes_top=options.groupby(['MES_TEXT','MONTH'])[[importe]].sum().reset_index().sort_values('MONTH',ascending=True).reset_index()
                df_mes_top['%']=(df_mes_top[importe]/options[importe].sum())*100
                #CULTIVO PESO
                #df_cultivo_peso=options.groupby(['CULTIVO'])[['PESONETO_PRODUCTO']].sum().reset_index().sort_values('PESONETO_PRODUCTO',ascending=True)#
                #TEMPLATE STYLES
            

                return card(total,'none',importe),barNaviera(df_naviera_top_facturado,'none',importe,radio,'Producto'),paisFacturado(df_pais_pie,'none',importe),cultivoFacturado(df_cultivo_top,'none',importe,'Venta por Tipo','TIPOVENTA'),mesTop(df_mes_top,'none',importe)