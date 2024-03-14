from django_plotly_dash import DjangoDash
from apps.graph.test.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from apps.graph.test.utils.theme import themeProvider, Container,Contenedor
from apps.graph.test.utils.frame import Column, Row, Div, Store, Download, Modal,Modal
from apps.graph.test.utils.components.components_main import Entry, Button, DataDisplay,Picking
from apps.graph.test.utils.blocks.block_filters import block_comercial_filters_IV,block_offcanvas_comercial_filter,offcanvas_comercial_config
from apps.graph.test.utils.tables import tableDag
from apps.graph.test.utils.functions.callbacks.callbacks_comercial import *
from apps.graph.test.utils.blocks.block_card import cardGraph,cardSection,cardGraphwithfilter
from apps.graph.test.utils.functions.callbacks.callbacks_ import *
from apps.graph.test.utils.components.components_filters import dict_components_comercial, datepicker_
from apps.graph.test.utils.functions.functions_dict import extraer_list_value_dict
#from apps.graph.test.data import finanzas_dff,pivot_data_finanzas,data_finanzas
from apps.graph.models import TipoIndicador
#
from apps.graph.test.utils.crum import get_indicadores_name,get_nombre_user, get_empresa,get_id_user
import dash_bootstrap_components as dbc
from apps.graph.save import RegistrarIndicador,ActualizarIndicador,EliminarIndicador
from apps.graph.test.utils.figures import *
import dash_ag_grid as dag
from apps.graph.test.Connection.apis import connection_api
from apps.graph.test.utils.functions.functions_transform import *
from crum import get_current_user

def formula_samplast(formula = '',df = pd.DataFrame()):
    ACTIVO = df['ACTIVO']
    PASIVO = df['PASIVO']
    PATRIMONIO = df['PATRIMONIO']
    ACTIVONOCORRIENTE = df['Activo no corriente']
    PASIVOCORRIENTE = df['Pasivo corriente']
    PASIVONOCORRIENTE = df['Pasivo no corriente']
    CAPITALSOCIAL=df['Capital social']
    CUENTASPORCOBRARCOMERCIALESRELACIONADAS=df['Cuentas por cobrar comerciales - relacionadas, neto']
    CUENTASPORCOBRARDIVERSASRELACIONADAS=df['Cuentas por cobrar comerciales - terceros, neto']
    CUENTASPORCOBRARDIVERSASTERCEROS=df['Cuentas por cobrar diversas - relacionadas, neto']
    CUENTASPORCOBRARDIVERSASTERCEROS=df['Cuentas por cobrar diversas - terceros, neto']
    CUENTASPORPAGARALDIRECTORIO=df['Cuentas por pagar al directorio, corto plazo']
    CUENTASPORPAGARCOMERCIALESRELACIONADAS=df['Cuentas por pagar comerciales - relacionadas, neto']
    CUENTASPORPAGARCOMERCIALESTERCEROS=df['Cuentas por pagar comerciales-terceros, neto']
    CUENTASPORPAGARDIVERSASRELACIONADAS=df['Cuentas por pagar diversas - relacionadas, neto']
    CUENTASPORPAGARDIVERSASTERCEROS=df['Cuentas por pagar diversas - terceros, neto']
    EFECTIVOYEQUIVALENTEDEEFECTIVO=df['Efectivo y equivalentes de efectivo']
    EXISTENCIAS=df['Existencias, neto']
    INTANGIBLES=df['Intangibles, neto']
    OBLIGACIONESFINANCIERAS=df['Obligaciones financieras']
    OTROSACTIVOSCORRIENTES=df['Otros activos corrientes']
    OTROSACTIVOSNOCORRIENTES=df['Otros activos no corrientes']
    OTROSGASTOSPAGADOSPORANTICIPADO=df['Otros gastos pagados por anticipado']
    PROPIEDADPLANTAYEQUIPO=df['Propiedad, planta y equipo, neto']
    PROVISIONES=df['Provisiones']
    PRESTAMOSALPERSONALYACCIONISTAS=df['Préstamos al personal y accionistas']
    REMUNERACIONESPORPAGAR=df['Remuneraciones por pagar']
    RESERVALEGAL=df['Reserva Legal']
    RESULTADOSACUMULADOS=df['Resultados acumulados']
    SOBREGIROSBANCARIOS=df['Sobregiros bancarios']
    TRIBUTOSCONTRAPRESENTACIONESYAPORTES=df['Tributos, contraprestaciones y aportes']
    COSTODEVENTASLINEAFILMAUTOMATICO=df['Costo de ventas línea film Automático']
    COSTODEVENTASLINEAFILMCOLORES=df['Costo de ventas línea film Colores']
    COSTODEVENTASLINEAFILMMANUAL=df['Costo de ventas línea film Manual']
    COSTODEVENTASLINEAFILMPREESTIRADO=df['Costo de ventas línea film Pre-Estirado']
    DIFERENCIADECAMBIONETO=df['Diferencia de cambio, neto']
    GASTOSDEADMINISTRACION=df['Gastos de administración']
    GASTOSDEDISTRIBUCIONYVENTAS=df['Gastos de distribución y ventas']
    GASTOSFINANCIEROS=df['Gastos financieros']
    INGRESOSFINANCIEROS=df['Ingresos financieros']
    OTROSCOSTOSOPERACIONALES=df['Otros Costos Operacionales']
    OTROSINGRESOSOPERACIONALES=df['Otros Ingresos Operacionales']
    OTROSINGRESOS=df['Otros ingresos']
    VENTASLINEAFILMAUTOMATICO=df['Ventas línea film - Automático']
    VENTASLINEAFILMCOLORES=df['Ventas línea film - Colores']
    VENTASLINEAFILMMANUAL=df['Ventas línea film - Manual']
    VENTASLINEAFILMPREESTIRADO=df['Ventas línea film - Pre-Estirado']
    formula=formula.replace(" ", "")
    return eval(formula)
def formula_paraiso(formula = '',df = pd.DataFrame()):
    ACTIVO = df['ACTIVO']
    PASIVO = df['PASIVO']
    PATRIMONIO = df['PATRIMONIO']
    try:
        ACTIVOSNOCORRIENTES = df['ACTIVOS NO CORRIENTES']
    except:
        pass
    try:
        PASIVOSNOCORRIENTES = df['PASIVOS NO CORRIENTES']
    except:
        pass
    try:
        PASIVOSCORRIENTES = df['PASIVOS CORRIENTES']
    except:
        pass
    try:
        ACTIVOSPORIR = df['ACT. POR IR Y PARTICIPACIONES DIFERID.']
    except:
        pass
    try:
        ACTIVOSBIOLOGICOS = df['ACTIVOS BIOLOGICOS']
    except:
        pass    
    try:
        ACTIVOSINTANGIBLES = df['ACTIVOS INTANGIBLES (NETO)']
    except:
        pass
    try:
        ANTICIPOSDEPROVEEDORES = df['ANTICIPOS DE PROVEEDORES']
    except:
        pass
    try:
        CAPITAL = df['CAPITAL']
    except:
        pass
    try:
        CAPITALADICIONAL = df['CAPITAL ADICIONAL']
    except:
        pass
    try:
        CREDITOSAFAVOR = df['CREDITOS A FAVOR']
    except:
        pass
    try:
        CUENTASPORCOBRARCOMERCIALESNETO = df['CUENTAS POR COBRAR COMERCIALES NETO']
    except:
        pass
    try:
        CUENTASPORPAGARALOSACCIONISTAS = df['CUENTAS POR PAGAR A LOS ACCIONISTAS (SOCIOS), DIRECTORES Y GERENTES']
    except:
        pass
    try:
        CUENTASPORPAGARCOMERCIALES = df['CUENTAS POR PAGAR COMERCIALES']
    except:
        pass
    try:
        CUENTASPORPAGARDIVERSAS = df['CUENTAS POR PAGAR DIVERSAS']
    except:
        pass
    try:
        EFECTIVOYEQUIVALENTESDEEFECTIVO = df['EFECTIVO Y EQUIVALENTES DE EFECTIVO']
    except:
        pass
    try:
        EXISTENCIAS = df['EXISTENCIAS (NETO)']
    except:
        pass
    try:
        GASTOSCONTRATADOSPORANTICIPADO = df['GASTOS CONTRATADOS POR ANTICIPADO']
    except:
        pass
    try:
        INMUEBLEMAQUINARIAYEQUIPO = df['INMUEBLE MAQUINARIA Y EQUIPO (NETO)']
    except:
        pass
    try:
        INVERSIONESMOBILIARIASEINMOBILIARIAS = df['INVERSIONES MOBILIARIAS E INMOBILIARIAS']
    except:
        pass
    try:
        OBLIGACIONESFINANCIERASCORTOPLAZO = df['OBLIGACIONES FINANCIERAS CORTO PLAZO']
    except:
        pass
    try:
        OBLIGACIONESFINANCIERASLARGOPLAZO = df['OBLIGACIONES FINANCIERAS LARGO PLAZO']
    except:
        pass
    try:
        OTRASCUENTASPORCOBRARNETO = df['OTRAS CUENTAS POR COBRAR NETO']
    except:
        pass
    try:
        OTRASCUENTASPORPAGAR = df['OTRAS CUENTAS POR PAGAR']
    except:
        pass
    try:
        PROVISIONES= df['PROVISIONES']
    except:
        pass
    try:
        REMUNERACIONESYPARTICIPACIONESPORPAGAR = df['REMUNERACIONES Y PARTICIPACIONES POR PAGAR']
    except:
        pass
    try:
        RESULTADOSACUMULADOS= df['RESULTADOS ACUMULADOS']
    except:
        pass
    try:
        SOBREGIRO = df['SOBREGIRO']
    except:
        pass
    try:
        TRIBUTOSYAPORTESPORPAGAR= df['TRIBUTOS Y APORTES POR PAGAR']
    except:
        pass
    try:
        COSTODEVENTAS= df['Costo de ventas']
    except:
        pass
    try:
        GASTOSFINANCIEROS= df['Gastos Financieros']
    except:
        pass
    try:
        GASTOSDEADMINISTRACION= df['Gastos de Administración']
    except:
        pass
    try:
        GASTOSDEVENTA= df['Gastos de Venta']
    except:
        pass
    try:
        INGRESOSFINANCIEROS= df['Ingresos Financieros']
    except:
        pass
    try:
        OTROSGASTOS = df['Otros Gastos']
    except:
        pass
    try:
        OTROSINGRESOS = df['Otros Ingresos']
    except:
        pass
    try:
        VENTASNETAS = df['Ventas Netas (ingresos operacionales)']
    except:
        pass
    try:
        CARGASDIVERSASDEGESTION= df['Cargas Diversas de Gestión']
    except:
        pass
    try:
        CARGASFINANCIERAS= df['Cargas Financieras']
    except:
        pass
    try:
        CARGASDEPERSONAL= df['Cargas de Personal']
    except:
        pass
    try:
        COMPRAS = df['Compras']
    except:
        pass
    try:
        OTROSGASTOS= df['Otros Gastos']
    except:
        pass
    try:
        COSTOSDEVENTAS= df['Costo de Ventas']
    except:
        pass
    try:
        DIFERENCIADECAMBIO= df['Diferencia de Cambio']
    except:
        pass
    try:
        GASTOSDESERVICIOSPRESTADOSPORTERCEROS= df['Gastos de Servicios Prestados por Terceros']
    except:
        pass
    try:
        INGRESOSDIVERSOS= df['Ingresos Diversos']
    except:
        pass
    try:
        INGRESOSPORDIFERENCIADECAMBIO = df['Ingresos por Diferencia de Cambio']
    except:
        pass
    try:
        PRODUCCIONALMACENADA= df['Produccion Almacenada']
    except:
        pass
    try:
        PRODUCCIONINMOVILIZADA = df['Producción Inmovilizada']
    except:
        pass
    try:
        PROVISIONESDELEJERCICIO= df['Provisiones del Ejercicio']
    except:
        pass
    try:
        TRIBUTOS= df['Tributos']
    except:
        pass
    try:
        VARIACIONDEEXISTENCIAS= df['Variacion de Existencias']
    except:
        pass
    try:
        VENTAS= df['Ventas']
    except:
        pass
    formula=formula.replace(" ", "")
    return eval(formula)

def formula_smartcold(formula = '',df = pd.DataFrame()):
    ACTIVO = df['ACTIVO']
    PASIVO = df['PASIVO']
    PATRIMONIO = df['PATRIMONIO']
    ACTIVOCORRIENTE = df['ACTIVO CORRIENTE']
    ACTIVONOCORRIENTE = df['ACTIVO NO CORRIENTE']
    PASIVOCORRIENTE = df['PASIVO CORRIENTE']
    CAPITALSOCIAL = df['Capital Social']
    CUENTASPORCOBRARDIVERSASRELACIONADAS = df['Cuentas por Cobrar Diversas  Relacionadas']
    CUENTASPORCOBRARDIVERSASTERCEROS = df['Cuentas por Cobrar Diversas Terceros']
    CUENTASPORCOBRARRELACIONADAS = df['Cuentas por Cobrar Relacionadas']
    CUENTASPORCOBRARTERCEROS = df['Cuentas por Cobrar Terceros']
    CUENTASPORCOBRARALPERSONALALOSACCIONISTAS = df['Cuentas por Cobrar al Personal a los Accionistas']
    CUENTASPORPAGARCOMERCIALES = df['Cuentas por Pagar Comerciales']
    CUENTASPORPAGARDIVERSASCORRIENTE = df['Cuentas por Pagar Diversas (Corriente)']
    CUENTASPORPAGARVINCULADAS = df['Cuentas por Pagar Vinculadas']
    EFECTIVOYEQUIVALENTEAEFECTIVO = df['Efectivo y equivalente a efectivo']
    EXISTENCIAS = df['Existencias']
    INMUEBLEMAQUINARIAYEQUIPO = df['Inmueble, Maquinaria y Equipo']
    INTANGIBLE = df['Intangible']
    PRODUCTOSENPROCESO = df['Productos en Proceso']
    PERDIDASACUMULADAS = df['Pérdidas Acumuladas']
    REMUNERACIONESPORPAGAR = df['Remuneraciones por Pagar']
    SERVICIOSYOTROSCONTRATOSPORANTICIPADOS = df['Servicios y Otros Contratos por Anticipados']
    TRIBUTOSPORPAGAR = df['Tributos por Pagar']
    MENOSEFECTIVO = df['menos efectivo']
    GASTOSADMINISTRATIVOS = df['GASTOS ADMINISTRATIVOS']
    formula=formula.replace(" ", "")
    return eval(formula)

def figure__line2(x,y,y2,name,namex,namey,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3):#,esperado,permitido,limite
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
        height=300,
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

def tipo_partida(lista = []):
    list_ingresos = []
    list_gastos = []
    list_costos = []
    list_otros = []
    partidas_ = [x for x in lista if x != None]
    for partida in partidas_:
        if 'Ventas' in partida:
            list_ingresos.append(partida)
        elif 'ingreso' in partida:
            list_ingresos.append(partida)
        elif 'Ingreso' in partida:
            list_ingresos.append(partida)
        elif 'Gasto' in partida:
            list_gastos.append(partida)
        elif 'Costo' in partida:
            list_costos.append(partida)
        else:
            list_otros.append(partida)
    return {
        'Ingresos': list_ingresos,
        'Gastos': list_gastos,
        'Costos': list_costos
        }


def estadoResultados(codigo = ''):
    if get_empresa() == 'FUNDO EL PARAISO':
        dfff = connection_api(sp_name='nsp_eeff_json2')
        
        #finanzas_df = etl_bc(dfff)
        #ingresos = ['Ingresos financieros','Otros Ingresos Operacionales','Otros ingresos','Ventas línea film - Automático','Ventas línea film - Colores', 'Ventas línea film - Manual','Ventas línea film - Pre-Estirado']
        #gastos = ['Gastos de administración', 'Gastos de distribución y ventas','Gastos financieros']
        #costos = ['Costo de ventas línea film Automático','Costo de ventas línea film Colores','Costo de ventas línea film Manual','Costo de ventas línea film Pre-Estirado','Otros Costos Operacionales']
        #g_funcion_dict ={'Ingresos': ingresos,
        #             'Gastos': gastos,
        #             'Costos': costos
        #}
    else:
        dfff = connection_api(sp_name='nsp_eeff_json')
        
        #finanzas_df = finanzas_dff.copy()
        #ingresos = ['Ingresos Financieros','Ventas Netas (ingresos operacionales)','Otros Ingresos']#Ventas Netas (ingresos operacionales)
        #gastos = ['Gastos Financieros', 'Gastos de Administración', 'Gastos de Venta','Otros Gastos']
        #costos = ['Costo de ventas']
        #g_funcion_dict ={'Ingresos': ingresos,
        #             'Gastos': gastos,
        #             'Costos': costos
        #}
    finanzas_df = etl_bc(dfff)
    g_funcion_dict = tipo_partida(lista = finanzas_df['grupo_funcion'].unique())
    
    year_list = sorted(finanzas_df['Año'].unique())
    

    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Container([
        Modal(id="modal-area-finanzas-ingresos", size= "85%"),
        Modal(id="modal-area-finanzas-gastos", size= "85%"),
        Modal(id="modal-area-finanzas-costos", size= "85%"),
        Row([
                
                Column([
                    Div(id='title'),
                    Entry.chipGroup(id='chipgroup-mes')
                ],size=8),
                Column([
                    Entry.select(id = 'select-anio',
                                 texto = "Año",
                                 size = 'md',
                                 data = [{'label': i, 'value': i} for i in year_list],
                                 value = year_list[-1],
                                 clearable=False
                                 )#,value='2018-Palta'
                ],size=2),
                Column([
                    Entry.select(id = 'select-moneda',
                                 texto = "Moneda",
                                 size = 'md',
                                 data = [{"value": "importe_mof", "label": "PEN"},{"value": "importe_mex", "label": "USD"}],
                                 value = 'importe_mex',
                                 clearable=False
                                 )#,value='2018-Palta'
                ],size=2),
                
        ]),
        Row([
            Column([Div(id='card-ingresos')],size=4),
            Column([Div(id='card-gastos')],size=4),
            Column([Div(id='card-costos')],size=4),
        ]),
        Row([
            Column([
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'area-finanzas-ingresos', id_maximize = 'maximize-area-finanzas-ingresos',height=250))
            ],size=4),
            Column([
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'area-finanzas-gastos', id_maximize = 'maximize-area-finanzas-gastos',height=250))
            ],size=4),
            Column([
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'area-finanzas-costos', id_maximize = 'maximize-area-finanzas-costos',height=250))
            ],size=4),
        ]),
        
        Row([
            Column([
                Picking.segmented(id='segmented-igc',value='Ingresos',data=['Ingresos','Gastos','Costos']),
                 DataDisplay.loadingOverlay(html.Div(id='table-igc'))
            ])
        ]),
    Div(id='notifications-update-data'),
    Store(id='data-values'),
    ])
    @app.callback(
        Output("chipgroup-mes","children"),
        Output("data-values","data"),
        Output("notifications-update-data","children"),
        Input("select-anio","value")
    )
    def update_data_bc(year):
        df = finanzas_df[finanzas_df['Año'] == year]
        return [
            [dmc.Chip(x,value=x,variant="outline",radius= 'xs',size='xs')for x in order_mes_text(df['Mes'].unique())],
            df.to_dict('series'),
            DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'), 
        ]
    
    @app.callback(
        Output("title","children"),
        Input('select-anio',"value"),
        Input('select-moneda','value')
    )
    def update_title(year,moneda):
            moneda_text = 'Dolares' if moneda == 'importe_mex' else 'Soles'
            return dmc.Title(children=[f'Estado de Resultados en el año {year} ({moneda_text})'],order=2,align='center')
    
    @app.callback(
        
        Output("area-finanzas-ingresos","figure"),
        Output("area-finanzas-gastos","figure"),
        Output("area-finanzas-costos","figure"),
        Input("data-values","data"),
        Input("select-moneda","value"),
        Input("chipgroup-mes","value"),
    )
    def update_graph_bc(*args):
        df = pd.DataFrame(args[0])
        moneda = args[1]
        
        meses_list = args[2]
        moneda_text = 'Dolares' if moneda == 'importe_mex' else 'Soles'
        if meses_list != None and len(meses_list)==0:
            dff =df.copy()
        elif meses_list != None:
            dff = df[df['Mes'].isin(meses_list)]
        else:
            dff = df.copy()
        
        bc_df = pd.pivot_table(dff,index=['Año','Mes','Mes Num','Periodo'],columns='grupo_funcion',values = moneda).fillna(0).reset_index()
        
        
        for col_ingresos in g_funcion_dict['Ingresos']:
            bc_df[col_ingresos] = bc_df[col_ingresos]*-1
        
        bc_df['Ingresos Generales'] = bc_df[g_funcion_dict['Ingresos']].sum(axis=1)
        bc_df['Gastos Generales'] = bc_df[g_funcion_dict['Gastos']].sum(axis=1)
        bc_df['Costos Generales'] = bc_df[g_funcion_dict['Costos']].sum(axis=1)
        
        bd_st_df = bc_df.groupby(['Mes','Mes Num'])[['Ingresos Generales','Gastos Generales','Costos Generales']].sum().reset_index().sort_values('Mes Num',ascending=True)
        
        #fig_ingreso = px.area(bd_st_df, x="Mes", y="Ingresos Generales", template='none',title='INGRESOS')
        #fig_ingreso.update_layout(height=250, margin=dict(l=50,r=20,b=60,t=80))
        fig_ingreso = GraphAreapx.area_(bd_st_df,x='Mes', y='Ingresos Generales',title= 'Ingresos',height=250, x_title='Mes',y_title='Ingresos Generales',size_text=14,template='none' )
        fig_gastos = GraphAreapx.area_(bd_st_df,x='Mes', y='Gastos Generales',title= 'Gastos',height=250, x_title='Mes',y_title='Gastos Generales',size_text=14,template='none' )

        fig_costos = GraphAreapx.area_(bd_st_df,x='Mes', y='Costos Generales',title= 'Costos',height=250, x_title='Mes',y_title='Costos Generales',size_text=14,template='none' )

        return [fig_ingreso,fig_gastos,fig_costos]
    
    @app.callback(
        
        Output("table-igc","children"),
        Input("data-values","data"),
        Input("select-moneda","value"),
        Input("chipgroup-mes","value"),
        Input("segmented-igc",'value')
    )
    def update_graph_bc2(*args):
        df = pd.DataFrame(args[0])
        moneda = args[1]
        meses_list = args[2]
        segmented = args[3]
        moneda_text = 'Dolares' if moneda == 'importe_mex' else 'Soles'
        if meses_list != None and len(meses_list)==0:
            dff =df.copy()
        elif meses_list != None:
            dff = df[df['Mes'].isin(meses_list)]
        else:
            dff = df.copy()
      
        table_cuentas_df =dff[dff['grupo_funcion'].isin(g_funcion_dict[segmented])]  
        
        if segmented == "Ingresos":
            table_cuentas_df[moneda]=table_cuentas_df[moneda]*-1
        df_www=table_cuentas_df.groupby(['idcuenta','descripcion','grupo_funcion'])[[moneda]].sum().reset_index()
        df_www=df_www.rename(columns={'descripcion':'Cuenta','grupo_funcion':'Partida',moneda:moneda_text})
        #df_table.apply(lambda x: "{:,}".format(x[importe]), axis=1)
        df_www[moneda_text]=df_www.apply(lambda x: "{:,.2f}".format(x[moneda_text]), axis=1)
        columnDefs = [{"field": i, "type": "rightAligned",'filter': True} for i in df_www.columns]
        return tableDag(id='w',columnDefs = columnDefs, dataframe= df_www, theme="ag-theme-balham",dashGridOptions = None)
    create_callback_opened_modal(app, modal_id="modal-area-finanzas-ingresos",children_out_id="area-finanzas-ingresos", id_button="maximize-area-finanzas-ingresos",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-area-finanzas-gastos",children_out_id="area-finanzas-gastos", id_button="maximize-area-finanzas-gastos",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-area-finanzas-costos",children_out_id="area-finanzas-costos", id_button="maximize-area-finanzas-costos",height_modal=700)

def tipo_utilidad(lista = []):
    utilidad_bruta = []
    utilidad_operativa = []
    utilidad_neta = []
    utilidad_otros = []
    partidas_ = [x for x in lista if x != None]
    for partida in partidas_:
        if 'Ventas' in partida or 'Costo' in partida:
            utilidad_bruta.append(partida)
        elif 'Gastos financieros' in partida or 'Gastos Financieros' in partida:
            utilidad_neta.append(partida)
        elif 'Ingresos financieros' in partida or 'Ingresos Financieros' in partida:
            utilidad_neta.append(partida)    
        elif 'Diferencia de cambio' in partida:
            utilidad_neta.append(partida)    
        elif 'Gasto' in partida or 'Otros' in partida:
            utilidad_operativa.append(partida)
        else:
            utilidad_otros.append(partida)
    return [utilidad_bruta,utilidad_operativa,utilidad_neta,utilidad_otros]



def estadoGP(codigo = ''):
    if get_empresa() == 'FUNDO EL PARAISO':
        dfff = connection_api(sp_name='nsp_eeff_json2')
        
        #finanzas_df = etl_bc(dfff)
        #utilidad_bruta = ['Ventas línea film - Colores', 'Ventas línea film - Manual','Ventas línea film - Pre-Estirado',
                        #'Ventas línea film - Automático','Costo de ventas línea film Automático','Costo de ventas línea film Colores',
                        #'Costo de ventas línea film Manual','Costo de ventas línea film Pre-Estirado'   ,'Otros Costos Operacionales',
        #                ]
        #utilidad_operativa = ['Gastos de administración','Otros ingresos','Gastos de distribución y ventas', 'Otros Ingresos Operacionales',]
        #utilidad_neta = ['Gastos financieros','Ingresos financieros','Diferencia de cambio, neto']
    else:
        dfff = connection_api(sp_name='nsp_eeff_json')
        #finanzas_df = etl_bc(dfff)
        #finanzas_df = finanzas_dff.copy()
        #utilidad_bruta = ['Ventas Netas (ingresos operacionales)','Costo de ventas']
        #utilidad_operativa = ['Gastos de Administración','Gastos de Venta','Otros Ingresos','Otros Gastos']
        #utilidad_neta = ['Gastos Financieros','Ingresos Financieros']
    finanzas_df = etl_bc(dfff)
    utilidad_ = tipo_utilidad(lista = finanzas_df['grupo_funcion'].unique())
    year_list = sorted(finanzas_df['Año'].unique())
    
    
    
    

    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Container([
        Modal(id="modal-bar-finanzas-ubruta", size= "85%"),
        Modal(id="modal-bar-finanzas-uoperativa", size= "85%"),
        Modal(id="modal-bar-finanzas-uneta", size= "85%"),
        Row([
                
                Column([
                    Div(id='title'),
                    Entry.chipGroup(id='chipgroup-mes')
                ],size=8),
                Column([
                    Entry.select(id = 'select-anio',
                                 texto = "Año",
                                 size = 'md',
                                 data = [{'label': i, 'value': i} for i in year_list],
                                 value = year_list[-1],
                                 clearable=False
                                 )#,value='2018-Palta'
                ],size=2),
                Column([
                    Entry.select(id = 'select-moneda',
                                 texto = "Moneda",
                                 size = 'md',
                                 data = [{"value": "importe_mof", "label": "PEN"},{"value": "importe_mex", "label": "USD"}],
                                 value = 'importe_mex',
                                 clearable=False
                                 )#,value='2018-Palta'
                ],size=2),
                
        ]),
        Row([
            Column([
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-finanzas-ubruta', id_maximize = 'maximize-bar-finanzas-ubruta',height=250))
            ],size=4),
            Column([
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-finanzas-uoperativa', id_maximize = 'maximize-bar-finanzas-uoperativa',height=250))
            ],size=4),
            Column([
                DataDisplay.loadingOverlay(cardGraph(id_graph = 'bar-finanzas-uneta', id_maximize = 'maximize-bar-finanzas-uneta',height=250))
            ],size=4),
        ]),
        Row([
            Column([
                DataDisplay.loadingOverlay(Div(id='table-utilidad'))
            ],size=12),
            
        ]),
    Div(id='notifications-update-data'),
    Store(id='data-values'),
    ])
    @app.callback(
        Output("chipgroup-mes","children"),
        Output("data-values","data"),
        Output("notifications-update-data","children"),
        Input("select-anio","value")
    )
    def update_data_bc(year):
        df = finanzas_df[finanzas_df['Año'] == year]
        return [
            [dmc.Chip(x,value=x,variant="outline",radius= 'xs',size='xs')for x in order_mes_text(df['Mes'].unique())],
            df.to_dict('series'),
            DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'), 
        ]
    
    @app.callback(
        Output("title","children"),
        Input('select-anio',"value"),
        Input('select-moneda','value')
    )
    def update_title(year,moneda):
            moneda_text = 'Dolares' if moneda == 'importe_mex' else 'Soles'
            return dmc.Title(children=[f'Estado de Ganancias y Pérdidas '],order=2,align='center')
    
    @app.callback(
        
        Output("bar-finanzas-ubruta","figure"),
        Output("bar-finanzas-uoperativa","figure"),
        Output("bar-finanzas-uneta","figure"),
        Output("table-utilidad","children"),
        Input("data-values","data"),
        Input("select-moneda","value"),
        Input("chipgroup-mes","value"),
    )
    def update_graph_bc(*args):
        utilidad_bruta = utilidad_[0]
        utilidad_operativa = utilidad_[1]
        utilidad_neta = utilidad_[2]
        df = pd.DataFrame(args[0])
        moneda = args[1]
        
        meses_list = args[2]
        moneda_text = 'Dolares' if moneda == 'importe_mex' else 'Soles'
        if meses_list != None and len(meses_list)==0:
            dff =df.copy()
        elif meses_list != None:
            dff = df[df['Mes'].isin(meses_list)]
        else:
            dff = df.copy()
            
        dfff =  dff.copy() 
        dfff[moneda] = dfff[moneda]*-1
        bc_df = pd.pivot_table(dfff,index=['Año','Mes','Mes Num','al_periodo'],columns='grupo_funcion',values = moneda,aggfunc='sum').fillna(0).reset_index()
        
        #bc_df['Ingresos Generales'] = bc_df[ingresos].sum(axis=1)
        bc_df['Utilidad Bruta'] = bc_df[utilidad_bruta].sum(axis=1)
        bc_df['Utilidad Operativa'] =  bc_df[['Utilidad Bruta']+utilidad_operativa].sum(axis=1)
        bc_df['Utilidad Neta'] =bc_df[['Utilidad Operativa']+utilidad_neta].sum(axis=1)
        bc_df = bc_df.sort_values('Mes Num')
        def createTableGP(df,moneda):
           
            #selecciono solo las 12 partidas del gfurpo funcion
            df_=df[df['grupo_funcion'].isin(df['grupo_funcion'].unique()[1:])]
            #cambio el signo a los totales por partida funcion
            df_['importe_mex']=df_['importe_mex']*-1
            #agrupo
            df_pg=df_.groupby(['grupo_funcion','Año','Mes','al_periodo'])[[moneda]].sum().reset_index()
            #invierto la tabla por periodo = convierto los periodos en columnas
            df_pg_pivot=df_pg.pivot_table(index=('grupo_funcion'),values=moneda,columns='al_periodo').reset_index()

            #EMPIEZO CREANDO LA TABLA CON EL TOTAL DE LA UTILIDAD BRUTA
            df_utilidad_bruta=df_pg_pivot[df_pg_pivot['grupo_funcion'].isin(utilidad_bruta)]
            #ORDENO POR VENTAS INICIAL
            df_utilidad_bruta=df_utilidad_bruta.sort_values('grupo_funcion',ascending=False)
            #CRETO EL TOTAL QUE SERIA LA UB
            df_utilidad_bruta.loc['UTILIDAD BRUTA',:]= df_utilidad_bruta.sum(numeric_only=True, axis=0)  
            df_utilidad_bruta=df_utilidad_bruta.fillna('UTILIDAD BRUTA')
            #CREO COLUMNA TOTAL
            df_utilidad_bruta.loc[:,'TOTAL']= df_utilidad_bruta.sum(numeric_only=True, axis=1)
            #lista de la fila utilidad bruta
            utilidad_bruta_list=df_utilidad_bruta.values[-1]
            #creto nuevo dataframe que almacenara la utilidad operativa
            df_ff=pd.DataFrame(columns=df_utilidad_bruta.columns)
            df_ff.loc[0]=utilidad_bruta_list
            ###############################UTILIDAD OPERATIVA
            df_utilidad_operativa=df_pg_pivot[df_pg_pivot['grupo_funcion'].isin(utilidad_operativa)]
            df_utilidad_operativa.loc[:,'TOTAL']= df_utilidad_operativa.sum(numeric_only=True, axis=1)
            #CONCATENO EL DATAFRAME DONDE ESTA SOLO LA UTILIDAD BRUTA CON LAS PARTIDAS QUE ME AYUDARAN A CALCULAR LA UTILIDAD OPERATIVA
            df_utilidad_operativa_proc=pd.concat([df_ff, df_utilidad_operativa])
            #CAMBIO EL TIPO DE DATO A FLOAT
            for col in df_utilidad_operativa_proc.columns[1:]:
                df_utilidad_operativa_proc[col]=df_utilidad_operativa_proc[col].astype('float64')
            #CREO LA FILA TOTAL QUE SERIA LA UTILIDAD OPERATIVA
            df_utilidad_operativa_proc.loc['UTILIDAD OPERATIVA',:]= df_utilidad_operativa_proc.sum(numeric_only=True, axis=0)  
            df_utilidad_operativa_proc=df_utilidad_operativa_proc.fillna('UTILIDAD OPERATIVA')

            #ELIMINO LA PRIMERA FILA QUE ES LA UTILIDAD OPERATIVA QUE YA NO SE NECESITA
            df_utilidad_operativa_proc=df_utilidad_operativa_proc.drop([0],axis=0)
            df_utilidad_operativa_proc_list=df_utilidad_operativa_proc.values[-1]
            df_fff=pd.DataFrame(columns=df_utilidad_operativa_proc.columns)
            df_fff.loc[0]=df_utilidad_operativa_proc_list
            ##################################UTILIDAD NETA

            df_utilidad_neta=df_pg_pivot[df_pg_pivot['grupo_funcion'].isin(utilidad_neta)]
            df_utilidad_neta.loc[:,'TOTAL']= df_utilidad_neta.sum(numeric_only=True, axis=1)

            df_utilidad_neta_proc=pd.concat([df_fff, df_utilidad_neta])
            for col in df_utilidad_neta_proc.columns[1:]:
                df_utilidad_neta_proc[col]=df_utilidad_neta_proc[col].astype('float64')
            
            df_utilidad_neta_proc.loc['UTILIDAD NETA',:]= df_utilidad_neta_proc.sum(numeric_only=True, axis=0)  
            df_utilidad_neta_proc=df_utilidad_neta_proc.fillna('UTILIDAD NETA')
            df_utilidad_neta_proc=df_utilidad_neta_proc.drop([0],axis=0)
            #######################DATAFRAME CORE
            df_table_gp=pd.concat([df_utilidad_bruta, df_utilidad_operativa_proc,df_utilidad_neta_proc])
            
            #for periodo_col in df_table_gp.columns[1:]:
            #    print(periodo_col)
            #    df_table_gp[periodo_col] = df_table_gp.apply(lambda x: "{:,.0f}".format(x[periodo_col]), axis=1)
            return df_table_gp.round(1)
        
        utilidad_df=createTableGP(dff,moneda)
        return [
            GraphBarpx.bar_(df = bc_df,x='al_periodo',y='Utilidad Bruta',height=250,left_space=40,title='Utilidad Bruta',yaxis_title=moneda_text, template= 'none'),
            GraphBarpx.bar_(df = bc_df,x='al_periodo',y='Utilidad Operativa',height=250,left_space=40,title='Utilidad Operativa',yaxis_title=moneda_text, template= 'none'),
            GraphBarpx.bar_(df = bc_df,x='al_periodo',y='Utilidad Neta',height=250,left_space=40,title='Utilidad Neta',yaxis_title=moneda_text, template= 'none'),
            dag.AgGrid(
                                    
                                    columnDefs=[{"field": 'grupo_funcion','headerName': '', "minxWidth": 200,"type": "leftAligned"}]+[{"field": i,"minWidth": 110,"type": "leftAligned"} for i in utilidad_df.columns[1:]],
                                    rowData=utilidad_df.to_dict("records"),
                                    #dashGridOptions={"rowSelection": "multiple"},
                                    #columnSize="sizeToFit",
                                    defaultColDef={"resizable": True},
                                    #style={'overflow': "auto"},#'max-height': f'{300}px',
                                    className="ag-theme-balham",
                                    #"['Flavia Mccloskey', 'Lilly Boaz'].includes(params.data.employee)"
                                    rowClassRules={"bg-primary fw-bold": "['UTILIDAD BRUTA', 'UTILIDAD OPERATIVA','UTILIDAD NETA'].includes(params.data.grupo_funcion)"},
                                    columnSize="sizeToFit",
                                    dashGridOptions={"domLayout": "autoHeight"},
                                ),  
        ]
    create_callback_opened_modal(app, modal_id="modal-bar-finanzas-ubruta",children_out_id="bar-finanzas-ubruta", id_button="maximize-bar-finanzas-ubruta",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-bar-finanzas-uoperativa",children_out_id="bar-finanzas-uoperativa", id_button="maximize-bar-finanzas-uoperativa",height_modal=700)
    create_callback_opened_modal(app, modal_id="modal-bar-finanzas-uneta",children_out_id="bar-finanzas-uneta", id_button="maximize-bar-finanzas-uneta",height_modal=700)

def crear_ratio_finanzas(codigo = '',empresa = '',usuario = ''):

    empresa_login = get_empresa()
    if  empresa_login == 'SAMPLAST':
        dfff = connection_api(sp_name='nsp_eeff_json')
        finanzas_df = etl_bc(dfff)
        partidas_df = pivot_data_finanzas(finanzas_df)
        partidas_df = partidas_df.drop(['PATRIMONIO_y'],axis=1)
        partidas_df = partidas_df.rename(columns={'PATRIMONIO_x':'PATRIMONIO'})
        
    elif  empresa_login == 'FUNDO EL PARAISO':
        finanzas_df = finanzas_dff.copy()
        partidas_df = pivot_data_finanzas(finanzas_df)
        partidas_df = partidas_df.drop(['PATRIMONIO_y','Ingresos Financieros_y'],axis=1)
        partidas_df = partidas_df.rename(columns={'PATRIMONIO_x':'PATRIMONIO','Ingresos Financieros_x':'Ingresos Financieros'})
    elif empresa_login == 'SMARTCOLD':
        dfff = connection_api(sp_name='nsp_eeff_json')
        finanzas_df = etl_bc(dfff)
        partidas_df = pivot_data_finanzas(finanzas_df)
        partidas_df = partidas_df.drop(['PATRIMONIO_y'],axis=1)
        partidas_df = partidas_df.rename(columns={'PATRIMONIO_x':'PATRIMONIO'})
    df_bcomprobacion=finanzas_df.copy()
    
    #test_df.columns[3:]
    idind_list=list(TipoIndicador.objects.all().values_list('id',flat=True))
    tipoind_list=list(TipoIndicador.objects.all().values_list('name_tipo_indicador',flat=True))
    
    list_dicts=[]
    for (i,j) in zip(tipoind_list,idind_list):
        list_dicts.append({'label': i, 'value': j})
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Contenedor([
        Modal(id="modal-line-finanzas-mostrar", size= "85%"),
        Row([
            Column([dmc.Title(children=[f'Crear Indicador Financiero'],order=2,align='center')])
        ]),
        Row([
            Column([
                
                Row([
                    Column([
                        Entry.select(id='select-tipo-indicador',texto='Tipo de Indicador', place= 'Seleccione el Tipo de Indicador', data=list_dicts,size='sm',clearable=False, value=idind_list[-1])
                    ],size=6),
                    Column([
                        Entry.textInput(id='input-nombre-indicador', label= 'Nombre del Indicador',place='Ingrese el nombre de su indicador',size='sm')
                    ],size=6)
                ]),
                Row([
                    Column([
                        Entry.select(id='select-partidas',texto='Partidas',size='sm', data=partidas_df.columns[3:])
                    ],size=6),
                    Column([
                        Entry.textInput(id='input-formula-indicador', label= 'Ingrese Fórmula',place='',size='sm')
                    ],size=6)
                ]),
                
                Row([
                    Column([
                        dmc.Center(dmc.Text("Rango Negativo", weight=700,style={'margin-top':30}))
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-negativo-desde',label='Desde')
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-negativo-hasta',label='Hasta')
                    ],size=3),
                    Column([
                        dmc.Center(dbc.Input(type="color",id="colorpicker-negativo",value="#F70808",style={"width": 70, "height": 40,'margin-top':30})),
                        #dmc.Center(dmc.ColorPicker(id='colorpicker-negativo',swatches=["#ff0000","#ffed4a", "#69ff2e"], swatchesPerRow=7, withPicker=False,style={'margin-top':30}))
                    ],size=3),
                    
                ]),
                Row([
                    Column([
                        dmc.Center(dmc.Text("Rango Medio", weight=700,style={'margin-top':30}))
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-medio-desde',label='Desde')
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-medio-hasta',label='Hasta')
                    ],size=3),
                    Column([
                        dmc.Center(dbc.Input(type="color",id="colorpicker-medio",value="#FFF817",style={"width": 70, "height": 40,'margin-top':30})),
                        #dmc.Center(dmc.ColorPicker(id='colorpicker-medio',swatches=["#ff0000","#ffed4a", "#69ff2e"], swatchesPerRow=7, withPicker=False,style={'margin-top':30}))
                    ],size=3),
                    
                ]),
                Row([
                    Column([
                        dmc.Center(dmc.Text("Rango Positivo", weight=700,style={'margin-top':30}))
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-positivo-desde',label='Desde')
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-positivo-hasta',label='Hasta')
                    ],size=3),
                    Column([
                        dmc.Center(
                            dbc.Input(type="color",id="colorpicker-positivo",value="#66FF2E",style={"width": 70, "height": 40,'margin-top':30}),#"width": 45, "height": 40,
                        #dmc.ColorPicker(id='colorpicker-positivo',swatches=["#ff0000","#ffed4a", "#69ff2e"], swatchesPerRow=7, withPicker=False,style={'margin-top':30})
                        )
                    ],size=3),
                    
                ]),
                Row([
                    Column([
                        DataDisplay.loadingOverlay(cardGraph(id_graph = 'line-finanzas-mostrar', id_maximize = 'maximize-line-finanzas-mostrar',height=300))
                    ],size=12),
                    
                ]), 
                Row([
                    Column([
                    Entry.textAreaInput(id = 'textarea-comentario',label='Comentarios')
                    ],size=12),
                ]),
                Row([
                    Column([
                        #dcc.Link(refresh=True,href=f"/{get_nombre_user()}/indicadores/")
                        dcc.Link(Button.button(id = 'btn-guardar', text= 'Guardar',full_width = True, color = 'rgb(81, 207, 102)'),href=f"/{get_nombre_user()}/indicadores/",id='link')
                    ],size=6),
                    Column([
                        Button.button(id = 'btn-mostrar', text= 'Mostrar',full_width = True,color='rgb(32, 201, 151)')
                    ],size=6)
                ]),
                Row([
                    Column([
                        Div(id='alert-respuesta')
                    ],size=12),
                    
                ]), 
                
            
            
            ]),
            
        ]),
        Div(id='update')
        
    ])
    @app.callback(
    Output("line-finanzas-mostrar", "figure"),
   
    
    #Output("alert-respuesta", "children"),
    Input("btn-mostrar","n_clicks"),
    State("select-tipo-indicador","value"),
    State("input-nombre-indicador","value"),
    State("input-formula-indicador","value"),
    State("input-negativo-desde", "value"),
    State("input-negativo-hasta", "value"),
    State("colorpicker-negativo", "value"),
    State("input-medio-desde", "value"),
    State("input-medio-hasta", "value"),
    State("colorpicker-medio", "value"),
    State("input-positivo-desde", "value"),
    State("input-positivo-hasta", "value"),
    State("colorpicker-positivo", "value"),
    
    State("textarea-comentario", "value"),
    #Input("btn-guardar","n_clicks"),
    #State("favorito","value"),

    )
    def update_graph(*args):
        n_clicks_mostrar = args[0]
        tipo_indicador = args[1]
        nombre_indicador = args[2].upper()
        formula_indicador = args[3].upper()
        desde_negativo_indicador = args[4]
        hasta_negativo_indicador = args[5]
        color_negativo_indicador = args[6]
        desde_medio_indicador = args[7]
        hasta_medio_indicador = args[8]
        color_medio_indicador = args[9]
        desde_positivo_indicador = args[10]
        hasta_positivo_indicador = args[11]
        color_positivo_indicador = args[12]
        comentario_indicador = args[13]
        
        
        if n_clicks_mostrar:
            #ratios_df = partidas_df(finanzas_df)
            #print(partidas_df.columns)
            df = pd.DataFrame()
            df['Agrupado']=partidas_df['Trimestre']
            if empresa_login == 'SAMPLAST': 
                df['valor']=formula_samplast(formula = formula_indicador,df = partidas_df)
            elif empresa_login == 'SMARTCOLD':
                df['valor'] = formula_smartcold(formula = formula_indicador,df = partidas_df)
            else:
                
                df['valor']=formula_paraiso(formula = formula_indicador,df = partidas_df)
            
            df['promedio'] = df['valor'].sum()/len(df['Agrupado'].unique())
            
            return figure__line2(df['Agrupado'],df['valor'],df['promedio'],nombre_indicador,'Valor','Promedio',desde_negativo_indicador,hasta_negativo_indicador,color_negativo_indicador,desde_medio_indicador,hasta_medio_indicador,color_medio_indicador,desde_positivo_indicador,hasta_positivo_indicador,color_positivo_indicador)

    @app.callback(
 
    
    Output("alert-respuesta", "children"),
    Output("link", "refresh"),
    Input("btn-guardar","n_clicks"),
    State("select-tipo-indicador","value"),
    State("input-nombre-indicador","value"),
    State("input-formula-indicador","value"),
    State("input-negativo-desde", "value"),
    State("input-negativo-hasta", "value"),
    State("colorpicker-negativo", "value"),
    State("input-medio-desde", "value"),
    State("input-medio-hasta", "value"),
    State("colorpicker-medio", "value"),
    State("input-positivo-desde", "value"),
    State("input-positivo-hasta", "value"),
    State("colorpicker-positivo", "value"),
    
    State("textarea-comentario", "value"),

    )
    def update_guardar(*args):
        
            n_clicks_guardar = args[0]
            tipo_indicador = args[1]
            nombre_indicador = args[2].upper()
            formula_indicador = args[3].upper()
            desde_negativo_indicador = args[4]
            hasta_negativo_indicador = args[5]
            color_negativo_indicador = args[6]
            desde_medio_indicador = args[7]
            hasta_medio_indicador = args[8]
            color_medio_indicador = args[9]
            desde_positivo_indicador = args[10]
            hasta_positivo_indicador = args[11]
            color_positivo_indicador = args[12]
            comentario_indicador = args[13]
            if n_clicks_guardar:
                if (tipo_indicador == None or tipo_indicador == '') or (nombre_indicador == None or nombre_indicador == '')or (formula_indicador == None or formula_indicador == ''):
                    return html.Div([dmc.Alert("No olvide ingresar datos",title="Error :",color="red",duration=5000)]),False
                elif (tipo_indicador != None or tipo_indicador != '') and (nombre_indicador != None or nombre_indicador != '') and (formula_indicador != None or formula_indicador != ''):
                    if nombre_indicador not in get_indicadores_name():
                        RegistrarIndicador(tipo_indicador,nombre_indicador,formula_indicador,desde_negativo_indicador,hasta_negativo_indicador,color_negativo_indicador,desde_medio_indicador,hasta_medio_indicador,color_medio_indicador,desde_positivo_indicador,hasta_positivo_indicador,color_positivo_indicador,comentario_indicador,False,empresa,usuario)
                        return  html.Div([dmc.Alert("Se guardó correctamente",title="Exitoso :",color="green",duration=5000)]),True
                    elif nombre_indicador in get_indicadores_name():
                        return html.Div([dmc.Alert("El nombre del indicador ya existe",title="Error :",color="red",duration=5000)]),False
        
                    
        
        #    return  html.Div([dmc.Alert("Error al intentar guardar",title="Error :",color="red",duration=5000)])
    create_callback_opened_modal(app, modal_id="modal-line-finanzas-mostrar",children_out_id="line-finanzas-mostrar", id_button="maximize-line-finanzas-mostrar",height_modal=700)

def line_fig(x,y,y2,name,namex,namey,rango_desde_1,rango_hasta_1,rango_color_1,rango_desde_2,rango_hasta_2,rango_color_2,rango_desde_3,rango_hasta_3,rango_color_3):#,esperado,permitido,limite
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
    fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    fig.add_hrect(y0=rango_desde_1,y1=rango_hasta_1, line_width=0, fillcolor=rango_color_1, opacity=0.2)
    fig.add_hrect(y0=rango_desde_2,y1=rango_hasta_2, line_width=0, fillcolor=rango_color_2, opacity=0.2)
    fig.add_hrect(y0=rango_desde_3,y1=rango_hasta_3, line_width=0, fillcolor=rango_color_3, opacity=0.2)
    
    return fig

def editar_ratio_finanzas(*args):
    if get_empresa() == 'SAMPLAST':
        dfff = connection_api(sp_name='nsp_eeff_json')
        finanzas_df = etl_bc(dfff)
        partidas_df = pivot_data_finanzas(finanzas_df)
        partidas_df = partidas_df.drop(['PATRIMONIO_y'],axis=1)
        partidas_df = partidas_df.rename(columns={'PATRIMONIO_x':'PATRIMONIO'})
    else:
        finanzas_df = finanzas_dff.copy()
        partidas_df = pivot_data_finanzas(finanzas_df)
        partidas_df = partidas_df.drop(['PATRIMONIO_y','Ingresos Financieros_y'],axis=1)
        partidas_df = partidas_df.rename(columns={'PATRIMONIO_x':'PATRIMONIO','Ingresos Financieros_x':'Ingresos Financieros'})
    tipo_indicador = args[0]
    nombre_indicador_ = args[1].upper()
    formula_indicador = args[2].upper()
    desde_negativo_indicador = args[3]
    hasta_negativo_indicador = args[4]
    color_negativo_indicador = args[5]
    desde_medio_indicador = args[6]
    hasta_medio_indicador = args[7]
    color_medio_indicador = args[8]
    desde_positivo_indicador = args[9]
    hasta_positivo_indicador = args[10]
    color_positivo_indicador = args[11]
    comentario_indicador = args[12]
    indicador_pk = args[13]
    
    
    #test_df.columns[3:]
    idind_list=list(TipoIndicador.objects.all().values_list('id',flat=True))
    tipoind_list=list(TipoIndicador.objects.all().values_list('name_tipo_indicador',flat=True))
    
    list_dicts=[]
    for (i,j) in zip(tipoind_list,idind_list):
        list_dicts.append({'label': i, 'value': j})
    app = DjangoDash(name=args[14],external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Contenedor([
        Modal(id="modal-line-finanzas-mostrar", size= "85%"),
        Row([
            Column([dmc.Title(children=[f'Modificar Indicador Financiero'],order=2,align='center')])
        ]),
        Row([
            Column([
                
                Row([
                    Column([
                        Entry.select(id='select-tipo-indicador',texto='Tipo de Indicador', place= 'Seleccione el Tipo de Indicador', data=list_dicts,size='sm',clearable=False, value=tipo_indicador)
                    ],size=6),
                    Column([
                        Entry.textInput(id='input-nombre-indicador', label= 'Nombre del Indicador',place='Ingrese el nombre de su indicador',size='sm',required=True, value=nombre_indicador_)
                    ],size=6)
                ]),
                Row([
                    Column([
                        Entry.select(id='select-partidas',texto='Partidas',size='sm', data=partidas_df.columns[3:])
                    ],size=6),
                    Column([
                        Entry.textInput(id='input-formula-indicador', label= 'Ingrese Fórmula',place='',size='sm',required=True, value=formula_indicador)
                    ],size=6)
                ]),
                
                Row([
                    Column([
                        dmc.Center(dmc.Text("Rango Negativo", weight=700,style={'margin-top':30}))
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-negativo-desde',label='Desde', value=desde_negativo_indicador)
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-negativo-hasta',label='Hasta', value=hasta_negativo_indicador)
                    ],size=3),
                    Column([
                        dmc.Center(dbc.Input(type="color",id="colorpicker-negativo",value=color_negativo_indicador,style={"width": 70, "height": 40,'margin-top':30})),
                        #dmc.Center(dmc.ColorPicker(id='colorpicker-negativo',swatches=["#ff0000","#ffed4a", "#69ff2e"], swatchesPerRow=7, withPicker=False,style={'margin-top':30}))
                    ],size=3),
                    
                ]),
                Row([
                    Column([
                        dmc.Center(dmc.Text("Rango Medio", weight=700,style={'margin-top':30}))
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-medio-desde',label='Desde',value=desde_medio_indicador)
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-medio-hasta',label='Hasta', value=hasta_medio_indicador)
                    ],size=3),
                    Column([
                        dmc.Center(dbc.Input(type="color",id="colorpicker-medio",value=color_medio_indicador,style={"width": 70, "height": 40,'margin-top':30})),
                        #dmc.Center(dmc.ColorPicker(id='colorpicker-medio',swatches=["#ff0000","#ffed4a", "#69ff2e"], swatchesPerRow=7, withPicker=False,style={'margin-top':30}))
                    ],size=3),
                    
                ]),
                Row([
                    Column([
                        dmc.Center(dmc.Text("Rango Positivo", weight=700,style={'margin-top':30}))
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-positivo-desde',label='Desde', value=desde_positivo_indicador)
                    ],size=3),
                    Column([
                        Entry.numberInput(id = 'input-positivo-hasta',label='Hasta', value=hasta_positivo_indicador)
                    ],size=3),
                    Column([
                        dmc.Center(
                            dbc.Input(type="color",id="colorpicker-positivo",value=color_positivo_indicador,style={"width": 70, "height": 40,'margin-top':30}),#"width": 45, "height": 40,
                        #dmc.ColorPicker(id='colorpicker-positivo',swatches=["#ff0000","#ffed4a", "#69ff2e"], swatchesPerRow=7, withPicker=False,style={'margin-top':30})
                        )
                    ],size=3),
                    
                ]),
                Row([
                    Column([
                    Entry.textAreaInput(id = 'textarea-comentario',label='Comentarios', value=comentario_indicador)
                    ],size=12),
                ]),
                Row([
                    Column([
                        #dcc.Link(refresh=True,href=f"/{get_nombre_user()}/indicadores/")
                        dcc.Link(Button.button(id = 'btn-modificar', text= 'Modificar',full_width = True, color = 'rgb(81, 207, 102)'),href=f"/{get_nombre_user()}/indicadores/",id='link')
                    ],size=6),
                    Column([
                        Button.button(id = 'btn-mostrar', text= 'Mostrar',full_width = True,color='gray')
                    ],size=6)
                ]),
                Row([
                    Column([
                        Div(id='alert-respuesta')
                    ],size=12),
                    
                ]), 
                #Row([
                #    Column([
                #        DataDisplay.loadingOverlay(cardGraph(id_graph = 'line-finanzas-mostrar', id_maximize = 'maximize-line-finanzas-mostrar',height=300))
                #    ],size=12),
                    
                #]), 
            
            
            ]),
            
        ]),
        Div(id='update')
        
    ])
    
    @app.callback(
    Output("update", "children"),
    Input("btn-modificar","n_clicks"),
    State("select-tipo-indicador","value"),
    State("input-nombre-indicador","value"),
    State("input-formula-indicador","value"),
    State("input-negativo-desde", "value"),
    State("input-negativo-hasta", "value"),
    State("colorpicker-negativo", "value"),
    State("input-medio-desde", "value"),
    State("input-medio-hasta", "value"),
    State("colorpicker-medio", "value"),
    State("input-positivo-desde", "value"),
    State("input-positivo-hasta", "value"),
    State("colorpicker-positivo", "value"),
    State("textarea-comentario", "value"),
    )
    def update_data_indicador(*args):
        n_clicks_modificar= args[0]
        tipo_indicador = args[1]
        nombre_indicador = args[2].upper()
        formula_indicador = args[3].upper()
        desde_negativo_indicador = args[4]
        hasta_negativo_indicador = args[5]
        color_negativo_indicador = args[6]
        desde_medio_indicador = args[7]
        hasta_medio_indicador = args[8]
        color_medio_indicador = args[9]
        desde_positivo_indicador = args[10]
        hasta_positivo_indicador = args[11]
        color_positivo_indicador = args[12]
        comentario_indicador = args[13]
        if n_clicks_modificar:
            if (tipo_indicador == None or tipo_indicador == '') or (nombre_indicador == None or nombre_indicador == '')or (formula_indicador == None or formula_indicador == ''):
                return html.Div([dmc.Alert("No olvide ingresar datos",title="Error :",color="red",duration=5000)]),False
            elif (tipo_indicador != None or tipo_indicador != '') and (nombre_indicador != None or nombre_indicador != '') and (formula_indicador != None or formula_indicador != ''):
                if nombre_indicador not in get_indicadores_name() :
                    ActualizarIndicador(tipo_indicador,nombre_indicador,formula_indicador,desde_negativo_indicador,hasta_negativo_indicador,color_negativo_indicador,desde_medio_indicador,hasta_medio_indicador,color_medio_indicador,desde_positivo_indicador,hasta_positivo_indicador,color_positivo_indicador,comentario_indicador,indicador_pk)
                    return  html.Div([dmc.Alert("Se actualizó correctamente",title="Exitoso :",color="green",duration=5000)]),True
                elif nombre_indicador == nombre_indicador_:
                    ActualizarIndicador(tipo_indicador,nombre_indicador,formula_indicador,desde_negativo_indicador,hasta_negativo_indicador,color_negativo_indicador,desde_medio_indicador,hasta_medio_indicador,color_medio_indicador,desde_positivo_indicador,hasta_positivo_indicador,color_positivo_indicador,comentario_indicador,indicador_pk)
                    return  html.Div([dmc.Alert("Se actualizó correctamente",title="Exitoso :",color="green",duration=5000)]),True
                
                elif nombre_indicador in get_indicadores_name():
                    return html.Div([dmc.Alert("El nombre del indicador ya existe",title="Error :",color="red",duration=5000)]),False


def eliminar_ratio_finanzas(*args):
    tipo_indicador = args[0]
    nombre_indicador_ = args[1].upper()
    formula_indicador = args[2].upper()
    indicador_pk = args[3]
    
    
    indicador_tipo_text = TipoIndicador.objects.filter(id = indicador_pk).values_list('name_tipo_indicador',flat=True)
    
    app = DjangoDash(name=args[4],external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout = Contenedor([
        Modal(id="modal-line-finanzas-mostrar", size= "85%"),
        Row([
            Column([dmc.Title(children=['Eliminar Indicador Financiero'],order=2,align='center')])
        ]),
        Row([
            Column([
                
                Row([
                    Column([
                        dmc.TextInput(label="Id Indicador", disabled=True, value= indicador_pk,size = 'sm')
                        #Entry.select(id='select-tipo-indicador',texto='Tipo de Indicador', place= 'Seleccione el Tipo de Indicador', data=list_dicts,size='sm',clearable=False, value=tipo_indicador)
                    ],size=6),
                    Column([
                        dmc.TextInput(label="Tipo de Indicador", disabled=True, value= tipo_indicador,size = 'sm')
                        
                        #Entry.select(id='select-tipo-indicador',texto='Tipo de Indicador', place= 'Sele
                        
                    ],size=6)
                ]),
                Row([
                    Column([
                        dmc.TextInput(label="Nombre del Indicador", disabled=True, value= nombre_indicador_,size = 'sm')
                    ],size=6),
                    Column([
                        dmc.TextInput(label="Fórmula", disabled=True, value= formula_indicador,size = 'sm')
                        
                    ],size=6)
                ]),
                
                Row([
                    Column([
                        #dcc.Link(refresh=True,href=f"/{get_nombre_user()}/indicadores/")
                        html.A(Button.button(id = 'btn-eliminar', text= 'Eliminar',full_width = True, color = "red"),href=f"/{get_nombre_user()}/indicadores/",id='link')
                    ],size=12),
                    
                ]),
                Row([
                    Column([
                        Div(id='alert-respuesta')
                    ],size=12),
                    
                ]), 
                
            
            
            ]),
            
        ]),
        Div(id='update')
        
    ])
    @app.callback(
    Output("update", "children"),
    Input("btn-eliminar","n_clicks"),
    )
    def delete_data_indicador(btn_clicks_eliminar):
        try:
            if btn_clicks_eliminar:
                EliminarIndicador(pk_indicador=indicador_pk)
                return  html.Div([dmc.Alert("Se elimino correctamente",title="Exitoso :",color="green",duration=5000)]),True
        except:
            return  html.Div([dmc.Alert("No se pudo eliminar",title="Error :",color="red",duration=5000)]),True