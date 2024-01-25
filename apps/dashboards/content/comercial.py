from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS,DASH_CSS_FILE,COMERCIAL_SELECTS_COLUMNS
from ..build.layout.error.dashboard_error import ERROR
from ..build.api.get_connect import connect_api
from ..build.layout.layout_comercial import *
from ..build.utils.transform.t_comercial import *

##
from dash import Input, Output,State,no_update
from ..build.components.figure_comp import *
from ..build.utils.global_callback import *
dara_colores= ["#3AA99B","#EFA54F","#DE5886","#5175C7","#FFFFFF","#366996","#304E64","#004576","#3599B8","#DFBFBF","#4AC5BB","#5F6B6D","#FB8281","#F4D25A","#7F898A","#A4DDEE","#FDAB89","#B687AC","#28738A","#A78F8F","#168980","#293537","#BB4A4A","#B59525","#475052","#6A9FB0","#BD7150","#7B4F71","#1B4D5C","#706060","#0F5C55","#1C2325"]
inputs_={
    'Producto':{'tipo_componente':'select'},
    'Vendedor':{'tipo_componente':'select'},
    'Subgrupo Producto':{'tipo_componente':'select'},
    'Pais':{'tipo_componente':'select'},
    'Tipo de Movimiento':{'tipo_componente':'select'},
}


def dashboard_inf_ventas(codigo = '',empresa_rubro = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    app.layout =  informe_comercial(rubro_empresa = empresa_rubro)
    
    return app

def dashboard_seguimiento_comercial(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    app.layout =  seguimiento_comercial(filtros={})
    
    return app

def dashboard_ventas_clientes(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    try:
        app.layout =  ventas_clientes(filtros={}, dataframe = None)
    except:
        app.layout = ERROR
    
    return app


def dashboard_ventas_productos(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    try:
        app.layout =  ventas_productos(filtros={}, dataframe = None)
    except:
        app.layout = ERROR
    
    return app

def dashboard_ventas_cultivos(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    try:
        app.layout =  ventas_cultivos(filtros={}, dataframe = None)
    except:
        app.layout = ERROR
    
    return app


def dashboard_ventas_agricola(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    dff = clean_comercial_detallado(dataframe=connect_api(sp_name ='nsp_rpt_ventas_detallado'))
    
    #try:
    app.layout =  ventas_exportacion_agro(dict_data = dict_dataframe(dataframe = dff))#ventas_cultivos(filtros={}, dataframe = None)
    #except:
    #    app.layout = ERROR
    offcanvas_filters(app)
    @app.callback(
        [Output(output_,'data')for output_ in ['select-grupo-producto','select-grupo-cliente','select-producto','select-cliente']]+
        [Output('data-values','data'),Output('notifications-update-data','children')],
        [Input('id_year','value'),Input('id_tipo_venta','value')]+
        [Input(input_,"value")for input_ in ['select-grupo-producto','select-grupo-cliente','select-producto','select-cliente']]
    )
    
    def update_data(*args):
        print(args)
        #year,tipo_v
        #anio =int(args[0])
        if validar_all_none(variables = args) == True:#(anio,tipo_v)
            df = dff.copy()
        else:   
            if args[0] != None:
                year_mod = int(args[0])
                args = tuple(year_mod if i == 0 else elemento for i, elemento in enumerate(args))
            #df = dff.query(dataframe_filtro(values=(anio,tipo_v),columns_df=['Año','Tipo de Venta'])) 
            df = dff.query(dataframe_filtro(values=args,columns_df=['Año','Tipo de Venta','Grupo Producto','Grupo Cliente','Producto','Cliente']))   
        print(df)
        return list_dict_outputs(dataframe=df, id_components=['select-grupo-producto','select-grupo-cliente','select-producto','select-cliente'],dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)+[
          df.to_dict('series'),  
          DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update')
        ]
    @app.callback(
        Output('pie_tipo_venta','figure'),
        Output('bar_gp','figure'),
        Output('bar_gc','figure'),
        Output('bar_cliente_top','figure'),
        Output('bar_producto_top','figure'),
        Output('bar_mes','figure'),
        Input('data-values','data'),
        Input('id_moneda','value'),
    )
    def update_build_dashboard(data, moneda):
        
        df = pd.DataFrame(data)
        tv_df = df.groupby(['Tipo de Venta'])[[moneda]].sum().reset_index()
        tv_df = tv_df[tv_df['Tipo de Venta'].isin(list(tv_df['Tipo de Venta'].values))]
        
        gp_df = df.groupby(['Grupo Producto'])[[moneda]].sum().sort_values(moneda).reset_index()
        gc_df = df.groupby(['Grupo Cliente'])[[moneda]].sum().sort_values(moneda).reset_index()
        
        client_top_df = df.groupby(['Cliente'])[[moneda]].sum().sort_values(moneda).tail(20).reset_index()
        product_top_df = df.groupby(['Producto'])[[moneda]].sum().sort_values(moneda).tail(20).reset_index()
        
        meses_df = dff.groupby(['Mes','Mes Num'])[[moneda]].sum().reset_index().sort_values('Mes Num',ascending=True).reset_index()
        meses_df['Porcentaje']=(meses_df[moneda]/meses_df[moneda].sum())*100
        meses_df['Porcentaje']=meses_df['Porcentaje'].map('{:,.1f}%'.format)
        return [ 
            GraphPiego.pie_(
            df = tv_df, 
            label_col = 'Tipo de Venta', 
            value_col = moneda, 
            title = 'Ventas por Tipo',
            height=380,
            showlegend = False,
            color_list= dara_colores,
            hole = .8
            ),
            bar_chart(df = gp_df, x = moneda, y = 'Grupo Producto', height=380, titulo = 'Ventas por Grupo Producto',color ='#3AA99b', orientacion = 'h'),
            bar_chart(df = gc_df, x = moneda, y = 'Grupo Cliente', height=380, titulo = 'Ventas por Grupo Cliente',color ='#5175C7', orientacion = 'h'),
            bar_chart(df = client_top_df, x = moneda, y = 'Cliente', height=380, titulo = 'Top 20 Ventas por Cliente',color ='#706060', orientacion = 'h'),
            bar_chart(df = product_top_df, x = moneda, y = 'Producto', height=380, titulo = 'Top 20 Ventas por Producto',color ='#A4DDEE', orientacion = 'h'),
            bar_chart(df = meses_df, x = 'Mes', y = moneda, height=380, titulo = 'Ventas por Mes',color ='#F4D25A', orientacion = 'v'),
        ]
    opened_modal(app, id="pie_tipo_venta", height_modal=900)
    opened_modal(app, id="bar_cliente_top", height_modal=900)
    opened_modal(app, id="bar_producto_top",height_modal=900)
    opened_modal(app, id="bar_mes", height_modal=900)
    opened_modal(app, id="bar_gp", height_modal=900)
    opened_modal(app, id="bar_gc", height_modal=900)
    
    return app