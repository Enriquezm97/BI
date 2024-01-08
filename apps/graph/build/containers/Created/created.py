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
from apps.graph.build.components.bootstrap_components.layout import Column
from apps.graph.build.components.mantine_react_components.radio import radioGroup
from apps.graph.build.components.mantine_react_components.selects import select,multiSelect
from apps.graph.build.components.mantine_react_components.alert import alert
from apps.graph.build.components.mantine_react_components.loaders import loadingOverlay
from apps.graph.build.components.mantine_react_components.cards import cardGraph,cardTableDag,cardShowTotal,actionIcon,button_style
import dash_ag_grid as dag

from apps.graph.test.utils.functions.functions_transform import etl_bc,pivot_data_finanzas

from apps.graph.build.components.mantine_react_components.title import *
from apps.graph.models import Indicador,TipoIndicador

from apps.graph.build.components.mantine_react_components.selects import *
from apps.graph.build.components.mantine_react_components.textbox import *
from apps.graph.build.components.mantine_react_components.checkbox import *
from apps.graph.build.components.mantine_react_components.button import *
from apps.graph.build.components.mantine_react_components.alert import *
from apps.graph.build.components.mantine_react_components.spoiler import *
from apps.graph.build.components.mantine_react_components.loaders import loadingOverlay


from apps.graph.data.transform_finanzas import *

from apps.graph.test.utils.functions.functions_transform import etl_bc,pivot_data_finanzas
from apps.graph.test.utils.frame import Modal
from apps.graph.test.utils.functions.callbacks.callbacks_ import create_callback_opened_modal

from apps.graph.test.Connection.apis import connection_api
from apps.graph.test.utils.crum import get_indicadores_name,get_nombre_user, get_empresa
from apps.graph.test.layouts.finanzas import formula_samplast,formula_paraiso

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
        height=330,
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
    #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
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
    ACTIVO=df_ratios['ACTIVO']
                     
    PASIVO=df_ratios['PASIVO']
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


from apps.graph.build.containers.Formularios.form_crear_indicador import df_bc_nisira
from apps.graph.data.transform_finanzas import *
from apps.graph.data.gets import getApi

def IndicadorDash(nombres,formulas,
           rango_desde_1,rango_hasta_1,rango_color_1,
           rango_desde_2,rango_hasta_2,rango_color_2,
           rango_desde_3,rango_hasta_3,rango_color_3,
           comentario,empresa,codigo):
    empresa_login = get_empresa()
    if empresa_login == 'FUNDO EL PARAISO':
        dfff = connection_api(sp_name='nsp_eeff_json2')
    else:
        dfff = connection_api(sp_name='nsp_eeff_json')
    
    df_bcomprobacion=etl_bc(dfff)
    print(df_bcomprobacion)
    external_stylesheets = [dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP,dbc.icons.FONT_AWESOME]


    app = DjangoDash(name = codigo,external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        Modal(id="btn-modal", size= "85%"),
        Modal(id="btn-modal-2", size= "85%"),
        Modal(id="btn-modal-3", size= "85%"),   
        dbc.Row([
            
            Column(
                content=[
                    multiSelect(ids="drop-year",texto="Año",value=[sorted(df_bcomprobacion['Año'].unique())[-1]]),
            ],size=4), 

            Column(
                content=[
                    select(ids="dp-ejex",texto="Eje X",place="Seleccione Tipo",
                            data=[{'label': 'Periodo', 'value': 'Periodo'},{'label': 'Trimestre', 'value': 'Trimestre'}],
                            value='Trimestre'),
            ],size=2), 
            Column(
                content=[
                    multiSelect(ids="drop-multi",texto="Seleccionar rangos"),
            ],size=4), 
            Column(
                content=[
                    radioGroup(ids="rbtn-moneda",
                               texto="Moneda",
                               children=[dmc.Radio(label='S/', value='soles'),dmc.Radio(label='$', value='dolares')],
                               value="soles",
                    ),
            ],size=2), 

        ]),
        dbc.Row([#'graph-stack2'
            #cardGraph(id_maximize='id-maximize-st',id_download='id-download',id_graph='st-comercial',with_id=True,fig=None,icon_maximize=True)         
            Column(content=[loadingOverlay(cardGraph(id_graph='graph-stack2',id_maximize='maximize-graph-stack2'))],size=9), 
            Column(content=[loadingOverlay(html.Div(id='tablet'))],size=3), #,style={'max-height': '390px','overflow': "auto"}
            
        ]),
        #graph-prueba
        dbc.Row([#graph-prueba
            Column(content=[loadingOverlay(cardGraph(id_graph='graph-prueba',id_maximize='maximize-graph-prueba'))],size=6),
            Column(content=[loadingOverlay(cardGraph(id_graph='graph-comparativo',id_maximize='maximize-graph-comparativo'))],size=6),
            
            
        ]),
        dbc.Row([#
            
            Column(content=[loadingOverlay(html.Div([dmc.Alert(comentario,title="Comentario :",color="blue")]))],size=12),
            
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
        out_year=[{'label': i, 'value': i} for i in df_bcomprobacion['Año'].unique()] 
        name=nombres.upper()
        formula=formulas.upper()
        
        
            #df_ratios_trim_dolar
        if ejex=='Trimestre':
            if rbtnmoneda=='sol' or rbtnmoneda=='soles':
                #df_ratios=rat.df_ratios_trim.copy()
                df_ratios=pivot_data_finanzas(etapa ='Trimestre',moneda = 'soles',df = df_bcomprobacion)
                if empresa_login == 'SAMPLAST':
                    df_ratios = df_ratios.drop(['PATRIMONIO_y'],axis=1)
                    df_ratios = df_ratios.rename(columns={'PATRIMONIO_x':'PATRIMONIO'})
                else:
                    df_ratios = df_ratios.drop(['PATRIMONIO_y','Ingresos Financieros_y'],axis=1)
                    df_ratios = df_ratios.rename(columns={'PATRIMONIO_x':'PATRIMONIO','Ingresos Financieros_x':'Ingresos Financieros'})
                
            elif rbtnmoneda=='dolar' or rbtnmoneda=='dolares':
                    #df_ratios=rat.df_ratios_trim_dolar.copy()
                df_ratios=pivot_data_finanzas(etapa ='Trimestre',moneda ='dolares',df =df_bcomprobacion)
                if empresa_login == 'SAMPLAST':
                    df_ratios = df_ratios.drop(['PATRIMONIO_y'],axis=1)
                    df_ratios = df_ratios.rename(columns={'PATRIMONIO_x':'PATRIMONIO'})
                else:
                    df_ratios = df_ratios.drop(['PATRIMONIO_y','Ingresos Financieros_y'],axis=1)
                    df_ratios = df_ratios.rename(columns={'PATRIMONIO_x':'PATRIMONIO','Ingresos Financieros_x':'Ingresos Financieros'})
                
            column='Trimestre'
            group=['Año','Trimestre']
            x='Trimestre'
            #out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()]   
            
        elif ejex=='Periodo':
            if rbtnmoneda=='sol' or rbtnmoneda=='soles':
                #df_ratios=rat.df_ratios_trim.copy()
                #'Periodo','soles'
                #df_ratios=df_ratios_periodo_soles
                df_ratios=pivot_data_finanzas(etapa ='Periodo',moneda='soles',df=df_bcomprobacion)
                if empresa_login == 'SAMPLAST':
                    df_ratios = df_ratios.drop(['PATRIMONIO_y'],axis=1)
                    df_ratios = df_ratios.rename(columns={'PATRIMONIO_x':'PATRIMONIO'})
                else:
                    df_ratios = df_ratios.drop(['PATRIMONIO_y','Ingresos Financieros_y'],axis=1)
                    df_ratios = df_ratios.rename(columns={'PATRIMONIO_x':'PATRIMONIO','Ingresos Financieros_x':'Ingresos Financieros'})
                
            elif rbtnmoneda=='dolar' or rbtnmoneda=='dolares':
                    #df_ratios=rat.df_ratios_trim_dolar.copy()
                df_ratios=pivot_data_finanzas(etapa ='Periodo',moneda='dolares',df = df_bcomprobacion)
                if empresa_login == 'SAMPLAST':
                    df_ratios = df_ratios.drop(['PATRIMONIO_y'],axis=1)
                    df_ratios = df_ratios.rename(columns={'PATRIMONIO_x':'PATRIMONIO'})
                else:
                    df_ratios = df_ratios.drop(['PATRIMONIO_y','Ingresos Financieros_y'],axis=1)
                    df_ratios = df_ratios.rename(columns={'PATRIMONIO_x':'PATRIMONIO','Ingresos Financieros_x':'Ingresos Financieros'})
                
                #df_ratios=df_ratios.sort_values('month',ascending=True)
            column='Periodo'
            group=['Año','Mes','Mes Num']
            x='Mes'
            #out_serie=[{'label': i, 'value': i} for i in df_ratios[column].unique()] 

        if filt_year !=None :
            df_ratios=df_ratios[df_ratios['Año'].isin(filt_year)]
            print("hay valor")
        elif filt_year ==None:
            df_ratios=df_ratios[df_ratios['Año'].isin(df_ratios['Año'].unique())]
            print("es none")
        elif len(filt_year) == 0:
            df_ratios=df_ratios[df_ratios['Año'].isin(df_ratios['Año'].unique())]
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
            df_filtro=df_filtro.sort_values(['Año','Mes Num'],ascending=True)
        else:
            df_filtro=df_filtro
        
        #df2=df2.sort_values('al_periodo',ascending=True)
        df = pd.DataFrame()
        df['Agrupado']=df_filtro[column]
        if empresa_login == 'SAMPLAST':
            df['valor']=formula_samplast(formula,df_filtro)
        else:
            df['valor']=formula_paraiso(formula,df_filtro)
        promedio=df['valor'].sum()/len(df['Agrupado'].unique())
        df['promedio']=promedio
        df=df.round(3)
        
        df_stack=df_filtro[group]
        if empresa_login == 'SAMPLAST':
            df_stack['valor']=formula_samplast(formula,df_filtro)
        else:
            df_stack['valor']=formula_paraiso(formula,df_filtro)
        #PROBAR
        #df_stack['Año']=df_stack['Año']
        if x == 'Mes':
            df_stack=df_stack.sort_values(['Mes Num','Año'],ascending=True)
        else:
            df_stack=df_stack
        

        fig2 = px.line(df_stack, x=x, y='valor',template="none",title="Comparativo por Año (Serie de Tiempo)",color='Año', markers=True)#, facet_row="Año",facet_row_spacing=0.1#,text='valor'
        fig2.update_layout(autosize=True,margin=dict(l=60,r=40,b=40,t=50),height=300)
        fig2.add_hrect(y0=rango_desde_1,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.2)
        fig2.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.2)
        fig2.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.2)
        
        fig_comparative = px.bar(df_stack, x=x, y='valor',color="Año", barmode='group',height=300,template='none',text="valor",title="Comparativo por Año (Barras Agrupadas)",)
        fig_comparative.update_traces(textposition='outside',texttemplate='%{text:.3f}',cliponaxis=False,)
        fig_comparative.update_layout(margin=dict(l=30,r=30,b=30,t=50,pad=0,autoexpand=True),height=330)  
        fig_comparative.add_hrect(y0=rango_desde_1,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.2)
        fig_comparative.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.2)
        fig_comparative.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.2)
        
        
        return [figure__line(df['Agrupado'],df['valor'],df['promedio'],f"{name} (Serie de Tiempo)",'Valor','Promedio',rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3),
                #TableDtScrolling_no_format_nototal(df,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3),
                html.Div([
                                        actionIcon(ids='id-maximize-table',style=button_style),
                                        #actionIcon(ids=id_download,icono='download'),
                                        dag.AgGrid(
            
                                            columnDefs=[{"field": "Agrupado", "type": "leftAligned"},{"field": "valor", "type": "leftAligned"}],
                                            rowData=df.to_dict("records"),
                                            defaultColDef={ "sortable": True},
                                            dashGridOptions={"rowSelection": "multiple"},
                                            style={'max-height': '300px','overflow': "auto"},
                                            className="ag-theme-balham",
                                            getRowStyle= {
                                                "styleConditions": [
                                                    {
                                                        "condition": f"params.data.valor >= {rango_desde_1} && params.data.valor <= {rango_hasta_1}",
                                                        "style": {"backgroundColor": rango_color_1},
                                                    },
                                                    {
                                                        "condition": f"params.data.valor >= {rango_desde_2} && params.data.valor <= {rango_hasta_2}",
                                                        "style": {"backgroundColor": rango_color_2},
                                                    },
                                                    {
                                                        "condition": f"params.data.valor >= {rango_desde_3} && params.data.valor <= {rango_hasta_3}",
                                                        "style": {"backgroundColor": rango_color_3},
                                                    },
                                                    
                                                ]
                                            }
                                            #defaultColDef=
                                        ),
                ]),
                
                out_serie,
                out_year,
                fig2,
                fig_comparative
            ]
    create_callback_opened_modal(app, modal_id="btn-modal",children_out_id="graph-stack2", id_button="maximize-graph-stack2",height_modal=600)   
    create_callback_opened_modal(app, modal_id="btn-modal-2",children_out_id="graph-prueba", id_button="maximize-graph-prueba",height_modal=600)  
    create_callback_opened_modal(app, modal_id="btn-modal-3",children_out_id="graph-comparativo", id_button="maximize-graph-comparativo",height_modal=600)   


def formIndicador(empresa,usuario):#empresa,usuario
    """"""
    
    """"""
    #df_bcomprobacion=dataBcEmpresa(empresa)
    df_bcomprobacion=df_bc_nisira.copy()

    idind_list=list(TipoIndicador.objects.all().values_list('id',flat=True))
    tipoind_list=list(TipoIndicador.objects.all().values_list('name_tipo_indicador',flat=True))
    list_dicts=[]
    for (i,j) in zip(tipoind_list,idind_list):
        list_dicts.append({'label': i, 'value': j})

    app = DjangoDash('form_indicador', external_stylesheets=[dbc.themes.BOOTSTRAP])#
    app.layout = html.Div([
    
    dbc.Row([
            Column(content=[title(text="Crear Indicador Financiero")],size=12),
             
    ]),
    dbc.Row([
        dbc.Col([ 
                 
                        dbc.Row([
                            dbc.Col([
                                select(ids="tipo-indicador",texto="Tipo de Indicador",place="Seleccione Tipo",data=list_dicts,size='sm'),
                            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-1"),
                            dbc.Col([
                                textInput(label="Nombre de Indicador",ids="nombre-indicador"),
                                

                            ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-1"),


                        ]),
                        dbc.Row([
                            dbc.Col([
                                select(ids="partidas-indicador",texto="Partidas",size='sm'),
                                
                            ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-1"),
                            dbc.Col([
                                textInput(label="Ingrese Fórmula",ids="formula-indicador"),
                                

                            ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-1"),


                        ]),
                        dbc.Row([
                            dbc.Col([
                                dmc.Card(
                                children=[
                                    
                                    dmc.CardSection(
                                        dmc.Center(
                                            style={"width": "100%"},
                                            children=[
                                                #
                                                dbc.Row([
                                                    dbc.Col([
                                                        dmc.Center(
                                                                style={"height":"100%", "width": "100%"},#
                                                                children=[
                                                                    dmc.Text("Rango Negativo :", weight=450),
                                                                ],
                                                            ),
                                                                                                                                
                                                            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                                    numberInput(label="Desde",ids="desde1"),
                                                                ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                                    numberInput(label="Hasta",ids="hasta1"),
                                                                ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                                    dbc.Label(""),
                                                                    dbc.Input(
                                                                        type="color",
                                                                        id="color1",
                                                                        value="#F70808",
                                                                        style={"width": 45, "height": 40},
                                                                    ),

                                                                ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),
                                                ]),
                                            ],
                                        ),
                                        
                                    ),
                                    
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                py="xs"
                                #style={"width": 350},
                            ),
                                

                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-1"),
                        ]),
                            
                        dbc.Row([
                            dbc.Col([
                                dmc.Card(
                                children=[
                                    
                                    dmc.CardSection(
                                        dmc.Center(
                                            style={"width": "100%"},
                                            children=[
                                                dbc.Row([
                            
                                                    dbc.Col([
                                                        dmc.Center(
                                                            style={"height":"100%", "width": "100%"},#
                                                            children=[dmc.Text("Rango Medio :", weight=450),],
                                                        ),
                                                        
                                                        

                                                    ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                        numberInput(label="Desde",ids="desde2"),

                                                    ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                        numberInput(label="Hasta",ids="hasta2"),

                                                    ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-3"),
                                                    dbc.Col([
                                                        dbc.Label(""),
                                                        dbc.Input(
                                                            type="color",
                                                            id="color2",
                                                            value="#FFF817",
                                                            style={"width": 45, "height": 40},
                                                        ),

                                                    ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-3"),


                                                ]),
                                            ]),
                                        

                                    ),
                                    
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                py="xs"
                                #style={"width": 350},
                            ),
                                

                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-1"),
                        ]),    
                            
                        dbc.Row([
                            dbc.Col([
                                dmc.Card(
                                children=[
                                    
                                    dmc.CardSection(
                                        dmc.Center(
                                            style={"width": "100%"},
                                            children=[
                                                dbc.Row([
                                                    dbc.Col([
                                                        dmc.Center(
                                                                style={"height":"100%", "width": "100%"},#
                                                                children=[
                                                                    dmc.Text("Rango Positivo :", weight=450),
                                                                ],
                                                            ),
                                                                                                                                
                                                            ],width=4,className="col-xl-4 col-md-4 col-sm-12 col-12 mb-1"),
                                                    dbc.Col([
                                                        numberInput(label="Desde",ids="desde3"),
                                                        

                                                    ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-1"),
                                                    dbc.Col([
                                                        numberInput(label="Hasta",ids="hasta3"),
                                                        
                                                    ],width=3,className="col-xl-3 col-md-3 col-sm-12 col-12 mb-1"),
                                                    dbc.Col([
                                                        dbc.Label(""),
                                                        dbc.Input(
                                                            type="color",
                                                            id="color3",
                                                            value="#66FF2E",
                                                            style={"width": 45, "height": 40},
                                                        ),

                                                    ],width=2,className="col-xl-2 col-md-2 col-sm-12 col-12 mb-1"),


                                                ]),
                                            ]),
                                        

                                    ),
                                    
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                py="xs"
                                #style={"width": 350},
                            ),
                                

                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-1"),
                        ]),

                        
                        
                        
                        dbc.Row([
                            
                            dbc.Col([
                                #dbc.Label("Desde"),
                                #dbc.Input(type="number", min=0.0, max=10000.0, step=0.1),
                                dcc.Checklist(
                                                id='favorito',
                                                options=[
                                                    {'label': 'Indicador Favorito', 'value': True},
                                                    
                                                ],
                                                value=False,

                                            ),
                                
                                #html.P(),
                                textAreaInput(ids="comentario",label="Comentarios")
                               
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                            


                        ]),
                        dbc.Row([
                            
                            dbc.Col([
                                button(text="Guardar",ids="guardar"),
                                #dbc.Button("Guardar", color="dark", className="me-1",id="guardar", n_clicks=0),
                            ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),
                            dbc.Col([
                                button(text="Mostrar",ids="mostrar"),
                                #dbc.Button("Mostrar", color="dark", className="me-1",id="mostrar", n_clicks=0),
                            ],width=6,className="col-xl-6 col-md-12 col-sm-12 col-12 mb-3"),


                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Div(id="respuesta") 
                            ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3"),
                        ])

                                    
         ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
         dbc.Col([
            loadingOverlay(dbc.Card(dcc.Graph(id='graph1'),className="shadow-sm")),
                #html.P(),
                #dbc.Alert(children='owo', color="light"), 
            html.Div(id="alert-comentario") 
                 #html.H2(["Example heading", dbc.Badge("New", className="ms-1")]),
                # html.Hr(),
         ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
    ]),

    dbc.Row([
        dbc.Col([
            #dmc.Anchor(z
            #    "Todos los Indicadores",
            #    href="/indicadores/",
            #)
            html.A("Todos los Indicadores Financieros", href="../indicadores", className="alert-link"),
           # html.A("Todos los Indicadores", href="/indicadores", className="alert-link"),
        ],width=12,className="col-xl-12 col-md-12 col-sm-12 col-12 mb-3")
    ])
    ])