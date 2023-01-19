from dash.dependencies import Output, Input, State
import plotly.express as px
import plotly.graph_objects as go
from dash import html,dcc,dash_table

from apps.graph.data.data import *
df_bcomprobacion=dataBalanceComprobacion.data_general('68.168.108.184')
def calcular_ratio(df_ratios):
        df_ratios['PATRIMONIO NETO']=df_ratios['ACTIVO    ']-df_ratios['PASIVO    ']
        df_ratios['ACTIVO CORRIENTE']=df_ratios['ACTIVO    ']-df_ratios['ACTIVO NO CORRIENTE']
        df_ratios['PASIVO NO CORRIENTE']=df_ratios['PASIVO CORRIENTE']-df_ratios['PASIVO    ']
        #df_ratios['CUENTAS POR COBRAR']=df_ratios['Cuentas Por Cobrar Diversas -  Relacionadas']+df_ratios['Cuentas por Cobrar Comerciales - Relacionadas Contenido']+df_ratios['Cuentas por Cobrar Comerciales - Terceros']+df_ratios['Cuentas por Cobrar Diversas -Terceros']+df_ratios['Cuentas por Cobrar al Personal a los Accionistas ( Socios) Directores y Gerentes']
        df_ratios['INVENTARIOS']=df_ratios['Existencias (Neto)']+df_ratios['Activos Biologicos']#(['Parte Corriente de Activo Biológico'])
        #df_ratios['CUENTAS POR PAGAR']=df_ratios['Cuentas por Pagar Comerciales - Relacionadas']+df_ratios['Cuentas por Pagar Comerciales - Terceros']+df_ratios['Cuentas por Pagar Diversas - Relacionadas']+df_ratios['Cuentas por Pagar Diversas - Terceros']+df_ratios['Cuentas por Pagar a los Accionistas (Socios), Directores y Gerentes']
        df_ratios['GASTO EN CAPITAL']=df_ratios['ACTIVO CORRIENTE']-df_ratios['PASIVO CORRIENTE']
        #df_ratios['PASIVO CORRIENTE']-df_ratios['ACTIVO CORRIENTE']
        df_ratios['ACTIVO FIJO']=df_ratios['Activo Fijo (neto)']
        df_ratios['CASH']=df_ratios['Efectivo y Equivalentes de Efectivo']
        df_ratios['DEUDA TOTAL']=df_ratios['Sobregiros Bancarios']+df_ratios['Obligaciones Financieras']
        df_ratios['ratio_liquidez'] = df_ratios['ACTIVO CORRIENTE']/df_ratios['PASIVO CORRIENTE']
        df_ratios['ratio_rapido'] = (df_ratios['ACTIVO CORRIENTE']-df_ratios['INVENTARIOS'])/df_ratios['PASIVO CORRIENTE']
        df_ratios['ratio_cash'] = df_ratios['CASH']/df_ratios['PASIVO CORRIENTE']
        df_ratios['deuda_activos']=df_ratios['DEUDA TOTAL']/df_ratios['ACTIVO    ']
        df_ratios['deuda_patrimonio'] = df_ratios['DEUDA TOTAL']/df_ratios['PATRIMONIO_x']
        df_ratios['apalancamiento'] = df_ratios['ACTIVO    ']/df_ratios['PATRIMONIO NETO']
        df_ratios['DEUDA_ESTR'] = df_ratios['PASIVO    '] - df_ratios['ACTIVO CORRIENTE'] 
        return df_ratios
def SerieTiempo(ejex,moneda):
    
        if ejex =='Trimestre':
            ejex='TRIM'
            group=['year','trimestre',ejex]
        elif ejex =='Periodo':
            ejex='al_periodo'
            group=['year','Mes','month',ejex]
        elif ejex =='Año':
            ejex=['year2']    
            group=['year2']
        df_niv1_trim=df_bcomprobacion.groupby(group+['grupo1'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        df_niv2_trim=df_bcomprobacion.groupby(group+['grupo2'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        df_niv3_trim=df_bcomprobacion.groupby(group+['grupo3'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        df_niv4_trim=df_bcomprobacion.groupby(group+['grupo_funcion'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        df_niv5_trim=df_bcomprobacion.groupby(group+['grupo_naturaleza'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        if moneda == 'soles':
            tipo='saldo_cargo_mof'
        elif moneda == 'dolares':
            tipo='saldo_cargo_mex'
        df_niv1_pivot_trim=pd.pivot_table(df_niv1_trim,index=group,columns='grupo1',values=tipo)
        df_niv1_pivot_trim=df_niv1_pivot_trim.reset_index()

        df_niv2_pivot_trim=pd.pivot_table(df_niv2_trim,index=group,columns='grupo2',values=tipo)
        df_niv2_pivot_trim=df_niv2_pivot_trim.reset_index()

        df_niv3_pivot_trim=pd.pivot_table(df_niv3_trim,index=group,columns='grupo3',values=tipo)
        df_niv3_pivot_trim=df_niv3_pivot_trim.reset_index()

        df_niv4_pivot_trim=pd.pivot_table(df_niv4_trim,index=group,columns='grupo_funcion',values=tipo)
        df_niv4_pivot_trim=df_niv4_pivot_trim.reset_index()

        df_niv5_pivot_trim=pd.pivot_table(df_niv5_trim,index=group,columns='grupo_naturaleza',values=tipo)
        df_niv5_pivot_trim=df_niv5_pivot_trim.reset_index()

        df_ratios_first_trim=df_niv1_pivot_trim.merge(df_niv2_pivot_trim,how='inner',left_on=ejex,right_on=ejex)
        df_ratios_first_trim=df_ratios_first_trim.merge(df_niv3_pivot_trim,how='inner',left_on=ejex,right_on=ejex)
        calcular_ratio(df_ratios_first_trim)
    
        return df_ratios_first_trim
df_ratios_trim=SerieTiempo('Trimestre','soles')
df_ratios_trim_dolar=SerieTiempo('Trimestre','dolares')
    #
df_ratios=SerieTiempo('Periodo','soles')
df_ratios_periodo_dolares=SerieTiempo('Periodo','dolares')

df_ratios_year_soles=SerieTiempo('Año','soles')
df_ratios_year_dolares=SerieTiempo('Año','dolares')

lista_partidas=['ACTIVO',
                'PASIVO',
                'PATRIMONIO',
                'ACTIVO FIJO NETO',
                'ACTIVO NO CORRIENTE',
                'PASIVO CORRIENTE',
                'ACTIVO FIJO NETO',
                'ACTIVOS ADQUIRIDOS EN ARRENDAMIENTO',
                'ACTIVOS BIOLOGICOS',
                'ACTIVOS DIFERIDOS',
                'ANTICIPOS DE CLIENTES',
                'ANTICIPOS DE PROVEEDORES',
                'CAPITAL ADICIONAL',
                'CAPITAL SOCIAL',
                'CUENTAS POR COBRAR DIVERSAS RELACIONADAS',
                'CUENTAS POR COBRAR COMERCIALES RELACIONADAS CONTENIDO',
                'CUENTAS POR COBRAR COMERCIALES TERCEROS',
                'CUENTAS POR COBRAR DIVERSASTERCEROS',
                'CUENTAS POR COBRAR AL PERSONAL A LOS ACCIONISTAS DIRECTORES Y GERENTES',
                'CUENTAS POR PAGAR COMERCIALES RELACIONADAS',
                'CUENTAS POR PAGAR COMERCIALES TERCEROS',
                'CUENTAS POR PAGAR DIVERSAS RELACIONADAS',
                'CUENTAS POR PAGAR DIVERSAS TERCEROS',
                'CUENTAS POR PAGAR A LOS ACCIONISTAS DIRECTORES Y GERENTES',
                'DEPRECIACION',
                'DESVALORIZACION DE EXISTENCIAS',
                'DESVALORIZACION DEL ACTIVO INMOVILIZADO',
                'EFECTIVO Y EQUIVALENTES DE EFECTIVO',
                'ESTIMACION DE CUENTAS DE COBRANZA DUDOSA',
                'EXCEDENTE DE REVALUACION VOLUNTARIA',
                'EXISTENCIAS NETO',
                'INSTRUMENTO FINANCIERO',
                'INVERSIONES MOBILIARIAS E INMOBILIARIAS',
                'OBLIGACIONES FINANCIERAS',
                'PASIVO DIFERIDO',
                'PROVISIONES',
                'REMUNERACIONES POR PAGAR Y PROVISIONES DEL PERSONAL',
                'RESERVAS',
                'RESULTADOS ACUMULADOS',
                'SERVICIOS Y OTROS CONTRATOS POR ANTICIPADO',
                'SOBREGIROS BANCARIOS',
                'TRIBUTOS Y APORTACIONES POR PAGAR',
                'PATRIMONIO NETO',
                'ACTIVO CORRIENTE',
                'PASIVO NO CORRIENTE',
                'CUENTAS POR COBRAR',
                'INVENTARIOS',
                'CUENTAS POR PAGAR',
                'GASTO EN CAPITAL',
                'ACTIVO FIJO',
                'CASH',
                'DEUDA TOTAL',
                'RATIO DE LIQUIDEZ',
                'RATIO RAPIDO',
                'RATIO DE CASH',
                'DEUDA ACTIVOS',
                'DEUDA PATRIMONIO',
                'APALANCAMIENTO',
                'DEUDA ESTR',
                'IMPUESTO A LA SGANACIAS',
                'CAMBIOS EN EL VALOR RAZONABLE DE LOS ACTIVOS BIOLOGICOS',
                'DIFERENCIA DE CAMBIONETA',
                'FLUCTUACION DE INVERSIONES EN SUBSIDIARIAS',
                'GASTOS CONTRATO DE COLABORACION',
                'GASTOS DE ADMINISTRACION',
                'GASTOS DEVENTA',
                'GASTOS FINANCIEROS NETO',
                'OTROS INGRESOS NETO',
                'RECUPERACION DRAWBACK',
                'VENTAS',
                'IMPUESTO A LA RENTA',
                'CARGAS DIVERSAS DE GESTION',
                'CARGAS FINANCIERAS',
                'CARGAS DE PERSONAL',
                'COMPRAS',
                'COSTO DE VENTAS',
                'DESCUENTOS CONCEDIDOS',
                'DIFERENCIA DE CAMBIO',
                'GANANCIA PERDIDA POR MEDICION DE ACTIVOS',
                'GASTOS DE SERVICIOS PRESTADOS POR TERCEROS',
                'INGRESOS DIVERSOS',
                'INGRESOS FINANCIEROS',
                'INGRESOS POR DIFERENCIA DE CAMBIO',
                'PRODUCCION ALMACENADA',
                'PRODUCCION INMOVILIZADA',
                'PROVISIONES DEL EJERCICIO',
                'TRIBUTOS',
                'VARIACION DE EXISTENCIAS'
            ]

def TableDtScrolling_no_format_nototal(dff,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3):#
    #df = get_data()
    rango_desde_1=str(rango_desde_1)
    rango_hasta_1=str(rango_hasta_1)
    rango_desde_2=str(rango_desde_2)
    rango_hasta_2=str(rango_hasta_2)
    rango_desde_3=str(rango_desde_3)
    rango_hasta_3=str(rango_hasta_3)
    fig = dash_table.DataTable(#id=idd, 
                                    columns=[
                                        dict(id='Agrupado', name='Serie de Tiempo'),
                                        dict(id='valor', name='Valor',type= "numeric", format= Format(group=",", precision=3,scheme="f")),
                                    ],
                                    #{"name": c, "id": c,
                                     #"type": "numeric", "format": Format(group=",", precision=4,scheme="f")} for c in dff
                                     #],
                                     #data=df.to_dict('records'),
                                     style_header={
                                        'textAlign': 'center',
                                        #"textTransform": "Uppercase",
                                        "fontWeight": "bold",
                                        "backgroundColor": "#dcdcdc",
                                        "padding": "10px 0px",
                                    },
                                    #sort_action='native',
                                    style_cell={'textAlign': 'left','fontSize':12},#,"textTransform": "Uppercase"
                                   
                                    data=dff.to_dict('records'),
                                    page_action="none",
                                     page_current= 0,
                                     virtualization = True,
                                     fixed_rows = {'headers': True},
                                     #style_table={'height': '280px','overflowY': 'auto'},
                                    style_data_conditional=[
                                   
                                    {
                                        'if': {
                                            'filter_query': '{valor} >='+rango_desde_1+' && {valor} <='+rango_hasta_1+'',# 0.9#&&{valor} <='+limite+'
                                            'column_id': 'valor'
                                        },
                                        'backgroundColor': rango_color_1,
                                        'color': 'black'
                                    },
                                    {
                                        'if': {
                                                'filter_query': '{valor} >= '+rango_desde_2+' && {valor} <='+rango_hasta_2+'',#
                                                'column_id': 'valor'
                                                
                                            },
                                            'backgroundColor': rango_color_2,
                                            'color': 'black'
                                    },
                                    {
                                        'if': {
                                                'filter_query': '{valor} >='+rango_desde_3+' && {valor} <='+rango_hasta_3+'',
                                                'column_id': 'valor'
                                            },
                                            'backgroundColor': rango_color_3,
                                            'color': 'white'
                                    },
                                    ]
                                 )
    return fig

def figure__line(x,y,y2,name,namex,namey,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3):#,esperado,permitido,limite
    fig = go.Figure()

    #fig.update_layout(yaxis_tickformat = '.0%')
    fig.add_trace(go.Scatter(x=x, y=y,text=y,textposition="bottom center",
                        mode='lines+markers',
                        name=namex,line=dict( width=3)))
    fig.add_trace(go.Scatter(x=x, y=y2,
                        mode='lines',
                        name=namey,line=dict( width=2)))
    fig.update_layout(
        autosize=True,
        #width=,
        height=390,
        margin=dict(
            l=60,
            r=40,
            b=60,
            t=70,
            #pad=4,
            autoexpand=True

        ),
        legend=dict(orientation= 'h',yanchor="bottom",xanchor='center', x= 0.5, y= 1,font=dict(size=10,color="black"),),#family="Courier",
    )
    
    fig.update_layout(template='none', title=name)
    fig.add_hrect(y0=rango_desde_1,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.2)
    fig.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.2)
    fig.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.2)
    #fig.add_hrect(y0=limite,y1=maximo, line_width=0, fillcolor="#fc2100", opacity=0.2)

    
    return fig

def EvaluarFormula(formula,df_ratios):#rbtnmoneda,ejex
    ACTIVO=df_ratios['ACTIVO    ']
                     
    PASIVO=df_ratios['PASIVO    ']
    PATRIMONIO=df_ratios['PATRIMONIO_x']
    ACTIVOFIJONETO=df_ratios['Activo Fijo (neto)']
    ACTIVONOCORRIENTE=df_ratios['ACTIVO NO CORRIENTE']
    PASIVOCORRIENTE=df_ratios['PASIVO CORRIENTE']
    ACTIVOFIJONETO=df_ratios['Activo Fijo (neto)']
    ACTIVOSADQUIRIDOSENARRENDAMIENTO=df_ratios['Activos Adquiridos en Arrendamiento']
    ACTIVOSBIOLOGICOS=df_ratios['Activos Biologicos']
    ACTIVOSDIFERIDOS=df_ratios['Activos Diferidos']
    ANTICIPOSDECLIENTES=df_ratios['Anticipos de Clientes']
    ANTICIPOSDEPROVEEDORES=df_ratios['Anticipos de Proveedores']
    #CAPITALADICIONAL=df_ratios['Capital Adicional']
    CAPITALSOCIAL=df_ratios['Capital Social']
    #CUENTASPORCOBRARDIVERSASRELACIONADAS=df_ratios['Cuentas Por Cobrar Diversas -  Relacionadas']
    #CUENTASPORCOBRARCOMERCIALESRELACIONADASCONTENIDO=df_ratios['Cuentas por Cobrar Comerciales - Relacionadas Contenido']
    CUENTASPORCOBRARCOMERCIALESTERCEROS=df_ratios['Cuentas por Cobrar Comerciales - Terceros']
    CUENTASPORCOBRARDIVERSASTERCEROS=df_ratios['Cuentas por Cobrar Diversas -Terceros']
    CUENTASPORCOBRARALPERSONALALOSACCIONISTASDIRECTORESYGERENTES=df_ratios['Cuentas por Cobrar al Personal a los Accionistas ( Socios) Directores y Gerentes']
    #CUENTASPORPAGARCOMERCIALESRELACIONADAS=df_ratios['Cuentas por Pagar Comerciales - Relacionadas']
    CUENTASPORPAGARCOMERCIALESTERCEROS=df_ratios['Cuentas por Pagar Comerciales - Terceros']
    #CUENTASPORPAGARDIVERSASRELACIONADAS=df_ratios['Cuentas por Pagar Diversas - Relacionadas']
    CUENTASPORPAGARDIVERSASTERCEROS=df_ratios['Cuentas por Pagar Diversas - Terceros']
    CUENTASPORPAGARALOSACCIONISTASDIRECTORESYGERENTES=df_ratios['Cuentas por Pagar a los Accionistas (Socios), Directores y Gerentes']
    DEPRECIACION=df_ratios['Depreciación']
    #DESVALORIZACIONDEEXISTENCIAS=df_ratios['Desvalorizacion de Existencias']
    #DESVALORIZACIONDELACTIVOINMOVILIZADO=df_ratios['Desvalorización del Activo Inmovilizado']
    EFECTIVOYEQUIVALENTESDEEFECTIVO=df_ratios['Efectivo y Equivalentes de Efectivo']
    ESTIMACIONDECUENTASDECOBRANZADUDOSA=df_ratios['Estimacion de Cuentas de Cobranza Dudosa']
    #EXCEDENTEDEREVALUACIONVOLUNTARIA=df_ratios['Excedente de Revaluación Voluntaria']
    EXISTENCIASNETO=df_ratios['Existencias (Neto)']
    #INSTRUMENTOFINANCIERO=df_ratios['Instrumento Financiero']
    #INVERSIONESMOBILIARIASEINMOBILIARIAS=df_ratios['Inversiones Mobiliarias e Inmobiliarias']
    OBLIGACIONESFINANCIERAS=df_ratios['Obligaciones Financieras']
    PASIVODIFERIDO=df_ratios['Pasivo Diferido']
    #PROVISIONES=df_ratios['Provisiones']
    REMUNERACIONESPORPAGARYPROVISIONESDELPERSONAL=df_ratios['Remuneraciones por Pagar y Provisiones del Personal']
    #RESERVAS=df_ratios['Reservas']
    RESULTADOSACUMULADOS=df_ratios['Resultados Acumulados']
    SERVICIOSYOTROSCONTRATOSPORANTICIPADO=df_ratios['Servicios y otros contratos por Anticipado']
    SOBREGIROSBANCARIOS=df_ratios['Sobregiros Bancarios']
    TRIBUTOSYAPORTACIONESPORPAGAR=df_ratios['Tributos y Aportaciones por Pagar']

    PATRIMONIONETO=df_ratios['PATRIMONIO NETO']
    ACTIVOCORRIENTE=df_ratios['ACTIVO CORRIENTE']
    PASIVONOCORRIENTE=df_ratios['PASIVO NO CORRIENTE']
    #CUENTASPORCOBRAR=df_ratios['CUENTAS POR COBRAR']
    INVENTARIOS=df_ratios['INVENTARIOS']
    #CUENTASPORPAGAR=df_ratios['CUENTAS POR PAGAR']
    GASTOENCAPITAL=df_ratios['GASTO EN CAPITAL']
    ACTIVOFIJO=df_ratios['Activo Fijo (neto)']
    CASH=df_ratios['CASH']
    DEUDATOTAL=df_ratios['DEUDA TOTAL']
    RATIODELIQUIDEZ=df_ratios['ratio_liquidez']
    RATIORAPIDO=df_ratios['ratio_rapido']
    RATIODECASH=df_ratios['ratio_cash']
    DEUDAACTIVOS=df_ratios['deuda_activos']
    DEUDAPATRIMONIO=df_ratios['deuda_patrimonio']
    APALANCAMIENTO=df_ratios['apalancamiento']
    DEUDAESTR=df_ratios['DEUDA_ESTR']

    
    formula=formula.replace(" ", "")
    return eval(formula)


def test(app,nombres,formulas):
    @app.callback(
 
    Output("graph-prueba", "figure"),
    Output("tablet","children"),
    Output("drop-multi", "options"),
    Output("drop-year","options"),
    Output("graph-stack2", "figure"),
    Input("rbtn-moneda","value"),
    Input("drop-year","value"),
    Input("dp-ejex","value"),
    Input("drop-multi", "value"),

    )
    def owo(rbtnmoneda,filt_year,ejex,filtro):
        out_year=[{'label': i, 'value': i} for i in df_bcomprobacion['year'].unique()] 
        name=nombres.upper()
        formula=formulas.upper()
            #df_ratios_trim_dolar
        if ejex=='trimestre':
            if rbtnmoneda=='sol' or rbtnmoneda=='soles':
                df_ratios=df_ratios_trim.copy()
                #df_ratios=rat.df_ratios_trim.copy()

            elif rbtnmoneda=='dolar' or rbtnmoneda=='dolares':
                    df_ratios=df_ratios_trim_dolar.copy()

            column='TRIM'
            group=['year','trimestre']
            x='trimestre'
            out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()]   
            
        elif ejex=='periodo':
            if rbtnmoneda=='sol' or rbtnmoneda=='soles':
                df_ratios=df_ratios

                #df_ratios=df_ratios.sort_values('month',ascending=True)
            elif rbtnmoneda=='dolar' or rbtnmoneda=='dolares':
                    df_ratios=df_ratios_periodo_dolares.copy()

            column='al_periodo'
            group=['year','Mes','month']
            x='Mes'
            out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()] 
        print(df_ratios)
        if filt_year !=None :
            df_ratios=df_ratios[df_ratios['year'].isin(filt_year)]
        elif filt_year ==None:
            df_ratios=df_ratios[df_ratios['year'].isin(df_ratios['year'].unique())]
            #print('owo')
        #print(df_ratios)
        if filtro == None or len(filtro)==0:
            df_filtro=df_ratios
        elif filtro !=None or len(filtro)>0:
            df_filtro=df_ratios[df_ratios[column].isin(filtro)]
        
        #df = pd.DataFrame()
        #df['Agrupado']=df_ratios[column]
        #df['valor']=func.EvaluarFormula(formula,df_ratios)
        #promedio=df['valor'].sum()/len(df['Agrupado'].unique())
        #df['promedio']=promedio
        #minimo=df['valor'].min()
        #maximo=df['valor'].max()
        #last_year=df_filtro['year'].unique()[-1]
        #df2=df_filtro[df_filtro['year']==last_year]
        #print(df2)
        if ejex == 'periodo':
            df_filtro=df_filtro.sort_values(['year','month'],ascending=True)
        else:
            df_filtro=df_filtro
        #df2=df2.sort_values('al_periodo',ascending=True)
        df = pd.DataFrame()
        df['Agrupado']=df_filtro[column]
        df['valor']=EvaluarFormula(formula,df_filtro)
        promedio=df['valor'].sum()/len(df['Agrupado'].unique())
        df['promedio']=promedio
        #print(df)
        
        #df['year']=df_filtro['year2']
        
        #df_stack = pd.DataFrame()
        #df_stack=df_filtro
        #df_stack=df_ratios[group]
        df_stack=df_filtro[group]
        df_stack['valor']=EvaluarFormula(formula,df_filtro)#df_ratios
        df_stack['Año']=df_stack['year']
        if x == 'Mes':
            df_stack=df_stack.sort_values(['month','Año'],ascending=True)
        else:
            df_stack=df_stack
        #fig = px.bar(df_stack, x=x, y='valor',text='valor', facet_row="Año",template="plotly_white",title="Comparativo",color_discrete_sequence=px.colors.qualitative.G10)#, facet_col="sex"#, color="smoker"
        #px.bar(df_stack, x=x, y='valor',text='valor', facet_row="Año",template="plotly_white",title="Comparativo",color_discrete_sequence=px.colors.qualitative.G10)
        #fig.update_yaxes(matches=None)
        #fig.update_layout(autosize=True,margin=dict(l=60,r=40,b=40,t=50))
        #fig.update_traces(texttemplate='%{text:.4s}', textposition='inside')
        ############################################
        #,color_discrete_sequence=px.colors.sequential.Viridis)#, facet_col="sex"#, color="smoker"
        #px.bar(df_stack, x=x, y='valor',text='valor', facet_row="Año",template="plotly_white",title="Comparativo",color_discrete_sequence=px.colors.qualitative.G10)
        #fig.update_yaxes(matches=None)
        colors = {
                'background': '#ffffff',
                'text': '#7FDBFF'
            }
        fig2 = px.line(df_stack, x=x, y='valor',text='valor', facet_row="Año",facet_row_spacing=0.1,template="seaborn",title="Comparativo",color='Año')
        fig2.update_layout(autosize=True,margin=dict(l=60,r=40,b=40,t=50))
        fig2.update_traces(textposition="bottom center",texttemplate='%{text:.3f}',textfont_size=12)#,texttemplate='%{text:.2s}'
        fig2.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True,gridcolor='#f9f4f4')
        fig2.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True,gridcolor='#f9f4f4')
        fig2.update_layout(
            plot_bgcolor=colors['background'],
            #paper_bgcolor='blue',
            #font_color=colors['text']
        )
        fig2.add_hrect(y0=rango_desde_1,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.2)
        fig2.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.2)
        fig2.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.2)
        #fig2.update_yaxes(showticklabels=False)
        #fig2.update_traces(texttemplate='%{text:.4s}', textposition='inside')
        #fig2.update_layout(hovermode="x unified")

        return figure__line(df['Agrupado'],df['valor'],df['promedio'],name,'Valor','Promedio',rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3),TableDtScrolling_no_format_nototal(df,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3),out_serie,out_year,fig2
