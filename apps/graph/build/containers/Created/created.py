from dash import html,dcc,dash_table
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from dash.dependencies import Output, Input, State
from dash.dash_table.Format import Format, Group, Scheme, Symbol
from apps.graph.data.data import *
from apps.graph.data.transform_finanzas import *
import plotly.express as px
import plotly.graph_objects as go

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from apps.graph.build.components.mantine_react_components.radio import radioGroup
from apps.graph.build.components.mantine_react_components.selects import select,multiSelect
from apps.graph.build.components.mantine_react_components.alert import alert
from apps.graph.build.components.mantine_react_components.loaders import loadingOverlay
#df_bc=df_bcomprobacion

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
                                        'backgroundColor': 'white',
                                        'fontWeight': 'bold',
                                        'text-align': 'center',
                                        'font-family': 'sans-serif',
                                        'font-size': '15px',
                                    },
                                    #sort_action='native',
                                    style_cell={
                                            'font-family': 'sans-serif',
                                            'font-size': '12px',
                                            'text_align': 'center',
                                    },#,"textTransform": "Uppercase"
                                   
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
    fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    fig.add_hrect(y0=rango_desde_1,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.2)
    fig.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.2)
    fig.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.2)
    fig.add_layout_image(
        dict(
            source="https://www.nisira.com.pe/images/logo.png",
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=2,
            sizey=2,
            sizing="stretch",
            opacity=0.5,
            layer="below")
        )
    #fig.add_hrect(y0=limite,y1=maximo, line_width=0, fillcolor="#fc2100", opacity=0.2)

    
    return fig

def EvaluarFormula(formula,df_ratios):#rbtnmoneda,ejex
    ACTIVO=df_ratios['ACTIVO    ']
                     
    PASIVO=df_ratios['PASIVO    ']
    PATRIMONIO=df_ratios['PATRIMONIO_x']
    ACTIVONOCORRIENTE=df_ratios['ACTIVO NO CORRIENTE']
    PASIVOCORRIENTE=df_ratios['PASIVO CORRIENTE']
    try:
        ACTIVOFIJONETO=df_ratios['Activo Fijo (neto)']
    except:
        pass
    try:
        ACTIVOSADQUIRIDOSENARRENDAMIENTO=df_ratios['Activos Adquiridos en Arrendamiento']
    except:
        pass
    
    try:
        ACTIVOSBIOLOGICOS=df_ratios['Activos Biologicos']
    except:
        pass
        
    try:
        ACTIVOSDIFERIDOS=df_ratios['Activos Diferidos']
    except:
        pass
    
    try:
        ANTICIPOSDECLIENTES=df_ratios['Anticipos de Clientes']
    except:
        pass
    
    try:
        ANTICIPOSDEPROVEEDORES=df_ratios['Anticipos de Proveedores']
    except:
        pass
    
    try:
        CAPITALSOCIAL=df_ratios['Capital Social']
    except:
        pass
    
    try:
        CUENTASPORCOBRARCOMERCIALESTERCEROS=df_ratios['Cuentas por Cobrar Comerciales - Terceros']
    except:
        pass
    
    try:
        CUENTASPORCOBRARDIVERSASTERCEROS=df_ratios['Cuentas por Cobrar Diversas -Terceros']
    except:
        pass
    
    try:
        CUENTASPORCOBRARALPERSONALALOSACCIONISTASDIRECTORESYGERENTES=df_ratios['Cuentas por Cobrar al Personal a los Accionistas ( Socios) Directores y Gerentes']
    except:
        pass
    
    try:
        CUENTASPORPAGARCOMERCIALESTERCEROS=df_ratios['Cuentas por Pagar Comerciales - Terceros']
    except:
        pass
    
    try:
        CUENTASPORPAGARDIVERSASTERCEROS=df_ratios['Cuentas por Pagar Diversas - Terceros']
    except:
        pass
    
    try:
        CUENTASPORPAGARALOSACCIONISTASDIRECTORESYGERENTES=df_ratios['Cuentas por Pagar a los Accionistas (Socios), Directores y Gerentes']
    except:
        pass
    try:
        DEPRECIACION=df_ratios['Depreciación']
    except:
        pass
    
    try:
        EFECTIVOYEQUIVALENTESDEEFECTIVO=df_ratios['Efectivo y Equivalentes de Efectivo']
    except:
        pass
    
    try:
        ESTIMACIONDECUENTASDECOBRANZADUDOSA=df_ratios['Estimacion de Cuentas de Cobranza Dudosa']
    except:
        pass
    
    try:
        EXISTENCIASNETO=df_ratios['Existencias (Neto)']
    except:
        pass
    
    try:
        OBLIGACIONESFINANCIERAS=df_ratios['Obligaciones Financieras']
    except:
        pass
    
    try:
        PASIVODIFERIDO=df_ratios['Pasivo Diferido']
    except:
        pass
    
    try:
        REMUNERACIONESPORPAGARYPROVISIONESDELPERSONAL=df_ratios['Remuneraciones por Pagar y Provisiones del Personal']
    except:
        pass
    
    try:
        RESULTADOSACUMULADOS=df_ratios['Resultados Acumulados']
    except:
        pass
    
    try:
        SERVICIOSYOTROSCONTRATOSPORANTICIPADO=df_ratios['Servicios y otros contratos por Anticipado']
    except:
        pass
    
    try:
        SOBREGIROSBANCARIOS=df_ratios['Sobregiros Bancarios']
    except:
        pass
    
    try:
        TRIBUTOSYAPORTACIONESPORPAGAR=df_ratios['Tributos y Aportaciones por Pagar']
    except:
        pass
    
    try:
        PATRIMONIONETO=df_ratios['PATRIMONIO NETO']
    except:
        pass
    
    try:
        ACTIVOCORRIENTE=df_ratios['ACTIVO CORRIENTE']
    except:
        pass
    
    try:
        PASIVONOCORRIENTE=df_ratios['PASIVO NO CORRIENTE']
    except:
        pass
    
    try:
        INVENTARIOS=df_ratios['INVENTARIOS']
    except:
        pass
    
    try:
        GASTOENCAPITAL=df_ratios['GASTO EN CAPITAL']
    except:
        pass
    
    try:
        CASH=df_ratios['CASH']
    except:
        pass
    
    try:
        DEUDATOTAL=df_ratios['DEUDA TOTAL']
    except:
        pass
    
    try:
        RATIODELIQUIDEZ=df_ratios['ratio_liquidez']
    except:
        pass
    
    try:
        RATIORAPIDO=df_ratios['ratio_rapido']
    except:
        pass
    
    try:
        RATIODECASH=df_ratios['ratio_cash']
    except:
        pass
    
    try:
        DEUDAACTIVOS=df_ratios['deuda_activos']
    except:
        pass
    
    try:
        DEUDAPATRIMONIO=df_ratios['deuda_patrimonio']
    except:
        pass
    
    try:
        APALANCAMIENTO=df_ratios['apalancamiento']
    except:
        pass
    
    try:
        DEUDAESTR=df_ratios['DEUDA_ESTR']
    except:
        pass
    ### POR AHOR HASTA TERMINAR ALGORITMO
    try:
        CAJABANCOS=df_ratios['Caja Bancos']
    except:
        pass
    
    try:
        CLIENTES=df_ratios['Clientes']
    except:
        pass
    
    try:
        CUENTASPORCOBRARDIVERSAS=df_ratios['Cuentas por Cobrar Diversas']
    except:
        pass

    try:
        CUENTASPORCOBRARAACCYPERSONAL=df_ratios['Cuentas por Cobrar a Acc. y Personal']
    except:
        pass
    try:
        CUENTASPORPAGARDIVERSAS=df_ratios['Cuentas por Pagar Diversas']
    except:
        pass
    try:
        DEPRECIACIONYARMOTIZACIONACUMULADA=df_ratios['Depreciación y Amortizacion Acumulada']
    except:
        pass
    try:
        EXISTENCIAS=df_ratios['Existencias']
    except:
        pass
    try:
        INMUEBLEMAQUINARIAYEQUIPO=df_ratios['Inmueble, Maquinaria y Equipo']
    except:
        pass
    
    try:
        INTANGIBLES=df_ratios['Intangibles']
    except:
        pass

    try:
        PROVEEDORES=df_ratios['Proveedores']
    except:
        pass

    try:
        REMUNERACIONESPORPAGAR=df_ratios['Remuneraciones por Pagar']
    except:
        pass

    try:
        RESERVAS=df_ratios['Reservas']
    except:
        pass
    
    try:
        TRIBUTOSPORPAGAR=df_ratios['Tributos por Pagar']
    except:
        pass
    #CAPITALADICIONAL=df_ratios['Capital Adicional']
    
    #CUENTASPORCOBRARDIVERSASRELACIONADAS=df_ratios['Cuentas Por Cobrar Diversas -  Relacionadas']
    #CUENTASPORCOBRARCOMERCIALESRELACIONADASCONTENIDO=df_ratios['Cuentas por Cobrar Comerciales - Relacionadas Contenido']
    
    
    
    #CUENTASPORPAGARCOMERCIALESRELACIONADAS=df_ratios['Cuentas por Pagar Comerciales - Relacionadas']
    
    #CUENTASPORPAGARDIVERSASRELACIONADAS=df_ratios['Cuentas por Pagar Diversas - Relacionadas']
    
    
    
    #DESVALORIZACIONDEEXISTENCIAS=df_ratios['Desvalorizacion de Existencias']
    #DESVALORIZACIONDELACTIVOINMOVILIZADO=df_ratios['Desvalorización del Activo Inmovilizado']
    
    
    #EXCEDENTEDEREVALUACIONVOLUNTARIA=df_ratios['Excedente de Revaluación Voluntaria']
    
    #INSTRUMENTOFINANCIERO=df_ratios['Instrumento Financiero']
    #INVERSIONESMOBILIARIASEINMOBILIARIAS=df_ratios['Inversiones Mobiliarias e Inmobiliarias']
    
    
    #PROVISIONES=df_ratios['Provisiones']
    
    #RESERVAS=df_ratios['Reservas']
    
    #CUENTASPORCOBRAR=df_ratios['CUENTAS POR COBRAR']
    
    #CUENTASPORPAGAR=df_ratios['CUENTAS POR PAGAR']
    
    formula=formula.replace(" ", "")
    return eval(formula)

def IndicadorDash(nombres,formulas,
           rango_desde_1,rango_hasta_1,rango_color_1,
           rango_desde_2,rango_hasta_2,rango_color_2,
           rango_desde_3,rango_hasta_3,rango_color_3,
           comentario,empresa):
    df_bcomprobacion=dataBcEmpresa(empresa)
    external_stylesheets = [dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP,dbc.icons.FONT_AWESOME]
  


    app = DjangoDash('TESTVIEW',external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        
        dbc.Row([
            
            dbc.Col([
                    
                    multiSelect(ids="drop-year",texto="Año",value=[sorted(df_bcomprobacion['year'].unique())[-1]]),
                    
            ],width=3,className="col-xl-3 col-md-4 col-sm-12 col-12 mb-3"),
            dbc.Col([
                    select(ids="dp-ejex",texto="Eje X",place="Seleccione Tipo",
                            data=[{'label': 'Periodo', 'value': 'Periodo'},{'label': 'Trimestre', 'value': 'Trimestre'}],
                            value='Trimestre'),
                    
            ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
            dbc.Col([
                    multiSelect(ids="drop-multi",texto="Seleccionar rangos"),
                   
                    
            ],width=5,className="col-xl-5 col-md-5 col-sm-12 col-12 mb-3"),
            dbc.Col([
                radioGroup(ids="rbtn-moneda",
                               texto="Moneda",
                               children=[dmc.Radio(label='S/', value='soles'),dmc.Radio(label='$', value='dolares')],
                               value="soles",
                    ),
                
            ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
        ]),
        dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-prueba')))],width=9,className="col-xl-9 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([loadingOverlay(html.Div(id='tablet',style={'max-height': '390px','overflow': "auto"}))],width=3,className="col-xl-3 col-md-12 col-sm-12 col-12 mb-3")
        ]),
        
        dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-comparativo')))],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            
            
        ]),
        dbc.Row([
            dbc.Col([loadingOverlay(dbc.Card(dcc.Graph(id='graph-stack2')))],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
            dbc.Col([#dbc.Alert(comentario, color="primary")
                    html.Div(
                    [
                        dmc.Alert(
                            comentario,
                            title="Comentario :",
                            #id="test",
                            color="blue",
                            #duration=3000,
                        ),
                    ]
                ),
                    #alert(text=comentario,title="Comentario :", color="blue",ids='alerto')
            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
        ]),
    ])

    

    @app.callback(
 
    Output("graph-prueba", "figure"),
    Output("tablet","children"),
    Output("drop-multi", "data"),
    Output("drop-year","data"),
    Output("graph-stack2", "figure"),
    Output("graph-comparativo", "figure"),
    Input("rbtn-moneda","value"),
    Input("drop-year","value"),
    Input("dp-ejex","value"),
    Input("drop-multi", "value"),
    )
    def owo(rbtnmoneda,filt_year,ejex,filtro):
        out_year=[{'label': i, 'value': i} for i in df_bcomprobacion['year'].unique()] 
        name=nombres.upper()
        formula=formulas.upper()
        print(filt_year)
        
            #df_ratios_trim_dolar
        if ejex=='Trimestre':
            if rbtnmoneda=='sol' or rbtnmoneda=='soles':
                #df_ratios=rat.df_ratios_trim.copy()
                df_ratios=balancePivot('Trimestre','soles',df_bcomprobacion)
                
            elif rbtnmoneda=='dolar' or rbtnmoneda=='dolares':
                    #df_ratios=rat.df_ratios_trim_dolar.copy()
                df_ratios=balancePivot('Trimestre','dolares',df_bcomprobacion)
            column='TRIM'
            group=['year','trimestre']
            x='trimestre'
            #out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()]   
            
        elif ejex=='Periodo':
            if rbtnmoneda=='sol' or rbtnmoneda=='soles':
                #df_ratios=rat.df_ratios_trim.copy()
                #'Periodo','soles'
                #df_ratios=df_ratios_periodo_soles
                df_ratios=balancePivot('Periodo','soles',df_bcomprobacion)
                #df_ratios=df_ratios.sort_values('month',ascending=True)
            elif rbtnmoneda=='dolar' or rbtnmoneda=='dolares':
                    #df_ratios=rat.df_ratios_trim_dolar.copy()
                df_ratios=balancePivot('Periodo','dolares',df_bcomprobacion)
                #df_ratios=df_ratios.sort_values('month',ascending=True)
            column='al_periodo'
            group=['year','Mes','month']
            x='Mes'
            #out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()] 

        if filt_year !=None :
            df_ratios=df_ratios[df_ratios['year'].isin(filt_year)]
            print("hay valor")
        elif filt_year ==None:
            df_ratios=df_ratios[df_ratios['year'].isin(df_ratios['year'].unique())]
            print("es none")
        elif len(filt_year) == 0:
            df_ratios=df_ratios[df_ratios['year'].isin(df_ratios['year'].unique())]
            print("lista vacia")

        out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()]
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
        if ejex == 'Periodo':
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

        fig2 = px.line(df_stack, x=x, y='valor',text='valor',template="none",title="Comparativo",color='Año')#, facet_row="Año",facet_row_spacing=0.1
        fig2.update_layout(autosize=True,margin=dict(l=60,r=40,b=40,t=50))
        fig2.update_traces(textposition="bottom center",texttemplate='%{text:.3f}',textfont_size=12)#,texttemplate='%{text:.2s}'
        #fig2.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True,gridcolor='#f9f4f4')
        #fig2.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True,gridcolor='#f9f4f4')
        fig2.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
        #fig2.add_hrect(y0=rango_desde_1,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.2)
        #fig2.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.2)
        #fig2.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.2)
        #fig2.update_yaxes(showticklabels=False)
        #fig2.update_traces(texttemplate='%{text:.4s}', textposition='inside')
        #fig2.update_layout(hovermode="x unified")
        fig_comparative = px.bar(df_stack, x=x, y='valor',color="Año", barmode='group',height=400,template='none',text="valor",title="Comparativo por Año",)
        fig_comparative.update_traces(textposition='outside',texttemplate='%{text:.3f}')
        fig_comparative.update_layout(margin=dict(l=30,r=30,b=30,t=50,pad=0,autoexpand=True))  
        fig_comparative.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
        fig_comparative.add_hrect(y0=0,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.1)
        fig_comparative.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.1)
        fig_comparative.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.1)
        
        return figure__line(df['Agrupado'],df['valor'],df['promedio'],name,'Valor','Promedio',rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3),TableDtScrolling_no_format_nototal(df,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3),out_serie,out_year,fig2,fig_comparative
        
        
        """"
        colors = {
                'background': '#ffffff',
                'text': '#7FDBFF'
            }
        
        #print(dataBalanceComprobacion.definir_st_bc('68.168.108.184','Trimestre','soles'))
        out_year=[{'label': i, 'value': i} for i in df_bcomprobacion['year'].unique()] 
        name=nombres.upper()
        formula=formulas.upper()
        df_ratios=dataBalanceComprobacion.definir_st_bc(ip,ejex,rbtnmoneda)

        if ejex=='trimestre' and filt_year !=None: 
            column='TRIM'
            group=['year','trimestre']
            x='trimestre'
            out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()]
            df_ratios=df_ratios[df_ratios['year'].isin(filt_year)]

        elif ejex=='trimestre' and filt_year ==None:      
            column='TRIM'
            group=['year','trimestre']
            x='trimestre'
            out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()]
            df_ratios=df_ratios[df_ratios['year'].isin(df_ratios['year'].unique())]

        elif ejex=='periodo' and filt_year !=None:
            column='al_periodo'
            group=['year','Mes','month']
            x='Mes'
            out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()]
            df_ratios=df_ratios[df_ratios['year'].isin(filt_year)] 
        elif ejex=='periodo' and filt_year ==None:
            column='al_periodo'
            group=['year','Mes','month']
            x='Mes'
            out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()]
            df_ratios=df_ratios[df_ratios['year'].isin(df_ratios['year'].unique())] 
        
        #if filt_year !=None :
        #    df_ratios=df_ratios[df_ratios['year'].isin(filt_year)]
        #elif filt_year ==None:
        #    df_ratios=df_ratios[df_ratios['year'].isin(df_ratios['year'].unique())]

        #print(df_ratios)

        if filtro == None and ejex == 'periodo':
            df_filtro=df_ratios.sort_values(['year_x','month_x'],ascending=True)

           
                
        elif filtro != None and ejex == 'trimestre':
            df_filtro=df_ratios[df_ratios[column].isin(filtro)]
        
        else:
            df_filtro=df_ratios
        df = pd.DataFrame()
        df['Agrupado']=df_filtro[column]
        df['valor']=EvaluarFormula(formula,df_filtro)
        promedio=df['valor'].sum()/len(df['Agrupado'].unique())
        df['promedio']=promedio
        df_stack=df_filtro[group]
        df_stack['valor']=EvaluarFormula(formula,df_filtro)
        df_stack['Año']=df_stack['year']
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

        figure1=figure__line(df['Agrupado'],df['valor'],df['promedio'],name,'Valor','Promedio',rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3)
        table=TableDtScrolling_no_format_nototal(df,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3)
        figure_compuesto=fig2
        #print(df_filtro)    

        #x='trimestre'

        return figure1,table,out_serie,out_year,figure_compuesto
        """


