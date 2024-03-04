from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS,DASH_CSS_FILE
from ..build.layout.error.dashboard_error import ERROR
from ..build.api.get_connect import connect_api,connect_saldos_alm, connect_consumo_alm
from ..build.layout.layout_logistica import almacen_stock,gestion_stock
from ..build.utils.transform.t_logistica import *
###

from dash import Input, Output,State,no_update,dcc,html
import dash_mantine_components as dmc
from ..build.components.display_comp import *
from ..build.utils.builder import *
from ..build.utils.global_callback import * 
from ..build.utils.figure import *
from ..build.utils.crum import get_data_connect
from ..build.api.connector import  APIConnector

from datetime import datetime,timedelta



filt = ['select-anio','select-grupo','select-rango']


def validar_all_none(variables=()):
    contador = 0
    for i in variables:
        if i == None:
            contador = contador +1
    return True if len(variables) == contador else False

def dataframe_filtro(values=[],columns_df=[]):
   """
   values son los inputs 
   columns_df son las columnas a comparar para el filtro
   """
   query = ""
   for value, col in zip(values,columns_df):
        if value != None:
            if type(value) == int:
                text=f"`{col}` == {value}"
            elif type(value) == str:
                text=f"`{col}` == '{value}'"
            elif type(value) == list:
                text=f"`{col}` in {value}"
            query += text + " and "
            
   return query[:-5]

def create_list_dict_outputs(id_components = [],dict_cols_dataframe = {}, dataframe=None):
    outputs_list =[]
    for element in id_components:
        
        if type(dict_cols_dataframe[element]) == list:
            
            outputs_list.append([{'label': i, 'value': i} for i in sorted(dataframe[dict_cols_dataframe[element][0]].unique()) ])
        else:
           
            outputs_list.append([{'label': i, 'value': i} for i in sorted(dataframe[dict_cols_dataframe[element]].unique())])
    return outputs_list

def create_col_for_dataframe(id_components = [],dict_cols_dataframe = {}):
    cols_dataframe = []
    for element in id_components:
        
        if type(dict_cols_dataframe[element]) == list:
            
            cols_dataframe.append(dict_cols_dataframe[element][0])
        else:
            
            cols_dataframe.append(dict_cols_dataframe[element])
    return cols_dataframe

def order_mes_text(disorder_list = []):
    lista_order_mes_text = ['Enero','Febrero','Marzo', 'Abril', 'Mayo','Junio', 'Julio', 'Agosto','Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    lista_new_order = []
    for mes in lista_order_mes_text:
      if mes in disorder_list:
        lista_new_order.append(mes)
    return lista_new_order



def dashboard_stocks(codigo = '',empresa = ''):#filtros = ['select-anio','select-grupo','select-rango']
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout =  almacen_stock() 
    try:
        if empresa == 'SAMPLAST':
            dff  = connect_api(sp_name = 'nsp_stocks_bi_samplast')
        else :
            dff  = connect_api(sp_name = 'nsp_stocks')
        dataframe = clean_stocks(df = dff)
        print(dataframe)
        #app.layout =  logistica_build()   
    except:
        app.layout = ERROR
    #def filter_callback(app, filt =[], dataframe = None):
    @app.callback(
        [Output(output_,'data')for output_ in filt]+
        [
         Output("data-values","data"),
         Output('chipgroup-mes','children'),
         Output("notifications-update-data","children")
        ],
        [Input(input_,"value")for input_ in filt]
    )
    def update_filter(*args):
        
        if validar_all_none(variables = args) == True:
            df=dataframe.copy()
        else:
            df=dataframe.query(dataframe_filtro(values=list(args),columns_df=create_col_for_dataframe(id_components = filt, dict_cols_dataframe=COMERCIAL_LOGISTICA)))

        return create_list_dict_outputs(dataframe = df,id_components = filt, dict_cols_dataframe=COMERCIAL_LOGISTICA)+[
               df.to_dict('series'),
               [dmc.Chip(x,value=x,variant="outline",radius= 'xs')for x in order_mes_text(df['Mes'].unique())],
               DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),
        ]  
    #app.layout =  logistica_build() 
    #dff  = connect_api(sp_name = 'nsp_stocks_bi_samplast')
    #stocks_df = clean_stocks(df = dff)
    #print(stocks_df)
    return app



def dashboard_gestion_stock(codigo = '',empresa = ''):
    ip, token_ =get_data_connect()
    api = APIConnector(ip, token_)
    dict_CONSUMOSALM = {
                'C_EMP':'001','C_SUC':'','C_ALM': '',
                'C_FECINI':str(datetime.now()- timedelta(days = 6 * 30))[:8].replace('-', "")+str('01')  ,
                'C_FECFIN':str(datetime.now())[:10].replace('-', ""),
                'C_VALOR':'1','C_GRUPO':'','C_SUBGRUPO':'','C_TEXTO':'','C_IDPRODUCTO':'','LOTEP':'','C_CONSUMIDOR':''
            }

    dict_SALDOSALM = {
                    'EMPRESA':'001','SUCURSAL':'','ALMACEN': '','FECHA':str(datetime.now())[:10].replace('-', ""),
                    'IDGRUPO':'','SUBGRUPO':'','DESCRIPCION':'','IDPRODUCTO':'','LOTEP':'',
            }
    
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout =  gestion_stock()
    app.css.append_css(DASH_CSS_FILE)
    print(datetime.now())
    consumos_api_alm_df = api.send_get_dataframe(endpoint="NSP_OBJREPORTES_CONSUMOSALM_DET_BI",params=dict_CONSUMOSALM)
    print(datetime.now())
    saldos_api_alm_df = change_cols_saldosalm(api.send_get_dataframe(endpoint="NSP_OBJREPORTES_SALDOSALMACEN_BI",params=dict_SALDOSALM))
    print(datetime.now())
    
    @app.callback(
        [
        Output('select-sucursal','data'),   
        Output('select-almacen','data'),
        Output('select-grupo','data'),
        Output('select-subgrupo','data'),
        Output('select-marca','data'),
        Output("card-cpm","children"),
        Output("card-invval","children"),
        Output("card-stock","children"),
        Output("card-consumo","children"),
         
        Output("card-total-stock","children"),
        
        Output("bar-minv-prom","figure"),
        Output("bar-inv-val","figure"),
        Output("table","rowData"),
        Output("table","columnDefs"),
        Output("data-table","data"),
         #Output("data-values","data"),
        Output("notifications-update-data","children")
         
        ],
        [Input('btn-filtrar','n_clicks')],
        [
         State('select-sucursal','value'),   
         State('select-almacen','value'),
         State('select-grupo','value'),
         State('select-subgrupo','value'),
         State('select-marca','value'),
         #State('num-meses','value'),
         State('text-input-find','value'),
         
         State('cpm-min','value'),
         State('cpm-max','value'),
         State('select-moneda','value'),
        ]
        
    )
    def update_data_stock(*args):
        n_clicks = args[0]
        sucursal =  args[1] 
        almacen =  args[2]
        grupo =  args[3]
        subgrupo =  args[4]
        marca = args[5]
        #meses_back = args[6]# if args[6] != None or args[6] == 0 else '1'
        find_text = args[6]
        cpm_min = args[7] if args[7] != '' else None
        cpm_max = args[8] if args[8] != '' else None
        moneda = args[9]
        print(args)
        col_pu = 'PU_S' if moneda == 'soles' else 'PU_D'
        inv_val_moneda = 'INV_VALMOF' if moneda == 'soles' else 'INV_VALMEX'
        sig = 'S/.' if moneda == 'soles' else '$'
        #dataframe.query(dataframe_filtro(values=list(args),columns_df=[]))
        
        if n_clicks == None:
            consumos_alm_df = consumos_api_alm_df.copy()
            saldos_alm_df = saldos_api_alm_df.copy()
        else:
            if validar_all_none(variables = (sucursal,almacen,grupo,subgrupo,marca)) == True:
                consumos_alm_df = consumos_api_alm_df.copy()
                saldos_alm_df = saldos_api_alm_df.copy()
            else:
                if sucursal == None and almacen == None and grupo == None and subgrupo == None and marca != None:
                    consumos_alm_df = consumos_api_alm_df.copy()
                else :
                    consumos_alm_df = consumos_api_alm_df.query(dataframe_filtro(values=[sucursal,almacen,grupo,subgrupo],columns_df=['SUCURSAL','ALMACEN','DSC_GRUPO','DSC_SUBGRUPO']))
                saldos_alm_df = saldos_api_alm_df.query(dataframe_filtro(values=[sucursal,almacen,grupo,subgrupo,marca],columns_df=['SUCURSAL','ALMACEN','DSC_GRUPO','DSC_SUBGRUPO','MARCA']))

        
        input_df = saldos_alm_df.groupby(['SUCURSAL','ALMACEN','DSC_GRUPO','DSC_SUBGRUPO','MARCA'])[['STOCK']].sum().reset_index()
        ###
        
        #PRECIO UNITARIO PROM
        precio_unit_prom = saldos_alm_df.groupby(['COD_PRODUCTO'])[[col_pu]].mean().reset_index()
        precio_unit_prom = precio_unit_prom.rename(columns = {col_pu:'Precio Unitario Promedio'})
        precio_unit_prom['Precio Unitario Promedio'] = precio_unit_prom['Precio Unitario Promedio'].fillna(0).round(2)
        #
        consumos_alm_df = consumos_alm_df.groupby(['IDPRODUCTO'])[['CANTIDAD']].sum().reset_index()
        saldos_alm_group_df = saldos_alm_df.groupby(['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA'])[['PU_S','PU_D', 'STOCK', 'INV_VALMOF', 'INV_VALMEX']].sum().reset_index()
        dff = saldos_alm_group_df.merge(consumos_alm_df, how='left', left_on=["COD_PRODUCTO"], right_on=["IDPRODUCTO"])
        dff = dff.merge(precio_unit_prom,how='left', left_on=["COD_PRODUCTO"], right_on=["COD_PRODUCTO"])
        dff.loc[dff.MARCA =='','MARCA']='NO ESPECIFICADO'
        if find_text != None:
            dff = dff[(dff['COD_PRODUCTO'].str.contains(find_text))|(dff['DESCRIPCION'].str.contains(find_text))]
        
        
            
        dff['CANTIDAD'] = dff['CANTIDAD'].fillna(0)
        dff['STOCK'] = dff['STOCK'].fillna(0)
        dff['Precio Unitario'] = dff[col_pu].fillna(0)
        dff['CANTIDAD'] = dff['CANTIDAD']/6
        dff['CANTIDAD'] = dff['CANTIDAD'].round(2)
        dff['Meses Inventario'] = dff.apply(lambda x: meses_inventario(x['CANTIDAD'],x['STOCK']),axis=1)
        dff['TI'] = 1/dff['CANTIDAD']
        dff['TI'] = dff['TI'].replace([np.inf],0)
        #CARDS
        print(cpm_min,cpm_max)
        if cpm_min != None and cpm_max != None:
            dff = dff[(dff['CANTIDAD']>=cpm_min)&(dff['CANTIDAD']<=cpm_max)]
            
        cpm = round(dff['CANTIDAD'].mean(),2)
        invval = f"{sig} {(int(round(dff[inv_val_moneda].sum(),0))):,}"
        meses_invet_prom = dff[dff['Meses Inventario']!='NO ROTA']
        stock = round(meses_invet_prom['Meses Inventario'].mean(),2)
        consumo = round(dff['TI'].mean(),2)
        total_stock = f"{(int(round(dff['STOCK'].sum(),0))):,}"
        
        #GRAPHS
        mi_dff = dff[(dff['Meses Inventario']!='NO ROTA')]
        df_mi_ =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario']].sum().sort_values('Meses Inventario').reset_index().tail(30)
        df_mi_iv =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario',inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index().tail(30)
        ##table
        df_table = dff[['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA','Precio Unitario Promedio', 'STOCK', inv_val_moneda,'IDPRODUCTO', 'CANTIDAD', 'Meses Inventario','TI']]
        df_table = df_table.drop(['IDPRODUCTO'], axis=1)
        

        
        #{'CANTIDAD':'CPM','moneda':'Precio Unitario','Meses Inventario':'Meses de Inventario'}
        #for col_numeric in  ['STOCK', inv_val_moneda,'Precio Unitario', 'CANTIDAD', 'Inventario Valorizado','TI']:
        #    df[col_numeric]=df.apply(lambda x: "{:,.2f}".format(x[col_numeric]), axis=1)
        df_table = df_table.rename(columns = {
                'DSC_GRUPO':'GRUPO', 
                'DSC_SUBGRUPO':'SUBGRUPO', 
                'COD_PRODUCTO':'CODIGO', 
                'DESCRIPCION':'DESCRIPCION', 
                'UM':'UMD',
                'MARCA':'MARCA', 
                'STOCK':'STOCK', 
                inv_val_moneda:f'Inventario Valorizado {moneda}', 
                
                'CANTIDAD': f'Consumo Promedio Mensual', 
                'Meses Inventario':'Meses de Inventario', 
                #'Inventario Valorizado':'Inventario Valorizado', 
                'TI':'TI'
            })
        #print(df_table['STOCK'].sum())
        return [
            [{'label': i, 'value': i} for i in sorted(input_df['SUCURSAL'].unique())],
            [{'label': i, 'value': i} for i in sorted(input_df['ALMACEN'].unique())],
            [{'label': i, 'value': i} for i in sorted(input_df['DSC_GRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(input_df['DSC_SUBGRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(input_df['MARCA'].unique())],
            cpm,invval,stock,consumo,total_stock,
            bar_logistica_y1(df = df_mi_,height = 350),
            bar_logistica_y2(df = df_mi_iv,height = 350,y_col=inv_val_moneda ),
            df_table.to_dict("records"),
            fields_columns(columns = df_table.columns),
            df_table.to_dict("series"),
            DataDisplay.notification(text=f'Se cargaron {len(dff)} filas',title='Update')
        ]

    download_data(app,input_id_data='data-table',name_file = 'stocks_producto.xlsx')
    opened_modal(app, id="bar-minv-prom",height_modal=900)
    opened_modal(app, id="bar-inv-val",height_modal=900)
    return app
   
#LAST CALLBACK     
"""
@app.callback(
        [Output(output_,'data')for output_ in filt]+
        [
         Output("data-values","data"),
         Output('chipgroup-mes','children'),
         Output("notifications-update-data","children")
        ],
        [Input(input_,"value")for input_ in filt]
    )
    def update_filter(*args):
        
        if validar_all_none(variables = args) == True:
            df=dataframe.copy()
        else:
            df=dataframe.query(dataframe_filtro(values=list(args),columns_df=create_col_for_dataframe(id_components = filt, dict_cols_dataframe=COMERCIAL_LOGISTICA)))

        return create_list_dict_outputs(dataframe = df,id_components = filt, dict_cols_dataframe=COMERCIAL_LOGISTICA)+[
               df.to_dict('series'),
               [dmc.Chip(x,value=x,variant="outline",radius= 'xs')for x in order_mes_text(df['Mes'].unique())],
               DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),
        ]  
    #app.layout =  logistica_build() 
    #dff  = connect_api(sp_name = 'nsp_stocks_bi_samplast')
    #stocks_df = clean_stocks(df = dff)
    #print(stocks_df)
    return app



def dashboard_gestion_stock(codigo = '',empresa = ''):
    ip, token_ =get_data_connect()
    api = APIConnector(ip, token_)
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout =  gestion_stock()
    app.css.append_css(DASH_CSS_FILE)
    
    @app.callback(
        [
        Output('select-sucursal','data'),   
        Output('select-almacen','data'),
        Output('select-grupo','data'),
        Output('select-subgrupo','data'),
        Output('select-marca','data'),
        Output("card-cpm","children"),
        Output("card-invval","children"),
        Output("card-stock","children"),
        Output("card-consumo","children"),
        Output("bar-minv-prom","figure"),
        Output("bar-inv-val","figure"),
        Output("table","rowData"),
        Output("table","columnDefs"),
        Output("data-table","data"),
         #Output("data-values","data"),
        Output("notifications-update-data","children")
         
        ],
        [Input('btn-filtrar','n_clicks')],
        [
         State('select-sucursal','value'),   
         State('select-almacen','value'),
         State('select-grupo','value'),
         State('select-subgrupo','value'),
         State('select-marca','value'),
         State('num-meses','value'),
         State('text-input-find','value'),
         
         State('cpm-min','value'),
         State('cpm-max','value'),
         State('select-moneda','value'),
        ]
        
    )
    def update_data_stock(*args):
        n_clicks = args[0]
        sucursal =  args[1] if args[1] != None else ''
        almacen =  args[2] if args[2] != None else ''
        grupo =  args[3] if args[3] != None else ''
        subgrupo =  args[4] if args[4] != None else ''
        marca = args[5]
        meses_back = args[6]# if args[6] != None or args[6] == 0 else '1'
        find_text = args[7]
        cpm_min = args[8] if args[8] != '' else None
        cpm_max = args[9] if args[9] != '' else None
        moneda = args[10]
        print(args)
        col_pu = 'PU_S' if moneda == 'soles' else 'PU_D'
        inv_val_moneda = 'INV_VALMOF' if moneda == 'soles' else 'INV_VALMEX'
        sig = 'S/.' if moneda == 'soles' else '$'

        if n_clicks == None:
            
            dict_CONSUMOSALM = {
                'C_EMP':'001','C_SUC':'','C_ALM': '',
                'C_FECINI':str(datetime.now()- timedelta(days = meses_back * 30))[:8].replace('-', "")+str(datetime.now().day)  ,
                'C_FECFIN':str(datetime.now())[:10].replace('-', ""),
                'C_VALOR':'1','C_GRUPO':'','C_SUBGRUPO':'','C_TEXTO':'','C_IDPRODUCTO':'','LOTEP':'','C_CONSUMIDOR':''
            }

            dict_SALDOSALM = {
                    'EMPRESA':'001','SUCURSAL':'','ALMACEN': '','FECHA':str(datetime.now())[:10].replace('-', ""),
                    'IDGRUPO':'','SUBGRUPO':'','DESCRIPCION':'','IDPRODUCTO':'','LOTEP':'',
            }
        else:
            dict_CONSUMOSALM = {
                'C_EMP':'001','C_SUC':sucursal,'C_ALM': almacen,
                'C_FECINI':str(datetime.now()- timedelta(days = meses_back * 30))[:8].replace('-', "")+str(datetime.now().day)  ,
                'C_FECFIN':str(datetime.now())[:10].replace('-', ""),
                'C_VALOR':'1','C_GRUPO':grupo,'C_SUBGRUPO':subgrupo,'C_TEXTO':'','C_IDPRODUCTO':'','LOTEP':'','C_CONSUMIDOR':''
            }

            dict_SALDOSALM = {
                    'EMPRESA':'001','SUCURSAL':sucursal,'ALMACEN': almacen,'FECHA':str(datetime.now())[:10].replace('-', ""),
                    'IDGRUPO':grupo,'SUBGRUPO':subgrupo,'DESCRIPCION':'','IDPRODUCTO':'','LOTEP':'',
            }
        print(datetime.now())
        consumos_alm_df = api.send_get_dataframe(endpoint="NSP_OBJREPORTES_CONSUMOSALM_DET_BI",params=dict_CONSUMOSALM)
        print(datetime.now())
        saldos_alm_df = change_cols_saldosalm(api.send_get_dataframe(endpoint="NSP_OBJREPORTES_SALDOSALMACEN_BI",params=dict_SALDOSALM))
        print(datetime.now())
        if marca != None:
            saldos_alm_df = saldos_alm_df[saldos_alm_df['MARCA']==marca]
        ##FILTROS 
        input_df = saldos_alm_df.groupby(['codsucursal', 'SUCURSAL', 'codalmacen', 'ALMACEN', 'codgrupo','DSC_GRUPO', 'codsubgrupo', 'DSC_SUBGRUPO','MARCA'])[['STOCK']].sum().reset_index()
        ###
        consumos_alm_df = consumos_alm_df.groupby(['IDPRODUCTO'])[['CANTIDAD']].sum().reset_index()
        saldos_alm_group_df = saldos_alm_df.groupby(['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA'])[['PU_S','PU_D', 'STOCK', 'INV_VALMOF', 'INV_VALMEX']].sum().reset_index()
        dff = saldos_alm_group_df.merge(consumos_alm_df, how='left', left_on=["COD_PRODUCTO"], right_on=["IDPRODUCTO"])
        dff.loc[dff.MARCA =='','MARCA']='NO ESPECIFICADO'
        if find_text != None:
            dff = dff[(dff['COD_PRODUCTO'].str.contains(find_text))|(dff['DESCRIPCION'].str.contains(find_text))]
        
        
            
        dff['CANTIDAD'] = dff['CANTIDAD'].fillna(0)
        dff['STOCK'] = dff['STOCK'].fillna(0)
        dff['Precio Unitario'] = dff[col_pu].fillna(0)
        dff['CANTIDAD'] = dff['CANTIDAD']/meses_back
        dff['CANTIDAD'] = dff['CANTIDAD'].round(2)
        dff['Meses Inventario'] = dff.apply(lambda x: meses_inventario(x['CANTIDAD'],x['STOCK']),axis=1)
        dff['TI'] = 1/dff['CANTIDAD']
        dff['TI'] = dff['TI'].replace([np.inf],0)
        #CARDS
        print(cpm_min,cpm_max)
        if cpm_min != None and cpm_max != None:
            dff = dff[(dff['CANTIDAD']>=cpm_min)&(dff['CANTIDAD']<=cpm_max)]
            
        cpm = round(dff['CANTIDAD'].mean(),2)
        invval = f"{sig} {(int(round(dff[inv_val_moneda].sum(),0))):,}"
        meses_invet_prom = dff[dff['Meses Inventario']!='NO ROTA']
        stock = round(meses_invet_prom['Meses Inventario'].mean(),2)
        consumo = round(dff['TI'].mean(),2)
        #GRAPHS
        mi_dff = dff[(dff['Meses Inventario']!='NO ROTA')]
        df_mi_ =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario']].sum().sort_values('Meses Inventario').reset_index().tail(30)
        df_mi_iv =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario',inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index().tail(30)
        ##table
        df_table = dff[['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA','Precio Unitario', 'STOCK', inv_val_moneda,'IDPRODUCTO', 'CANTIDAD', 'Meses Inventario','TI']]
        df_table = df_table.drop(['IDPRODUCTO'], axis=1)
        #{'CANTIDAD':'CPM','moneda':'Precio Unitario','Meses Inventario':'Meses de Inventario'}
        #for col_numeric in  ['STOCK', inv_val_moneda,'Precio Unitario', 'CANTIDAD', 'Inventario Valorizado','TI']:
        #    df[col_numeric]=df.apply(lambda x: "{:,.2f}".format(x[col_numeric]), axis=1)
        df_table = df_table.rename(columns = {
                'DSC_GRUPO':'GRUPO', 
                'DSC_SUBGRUPO':'SUBGRUPO', 
                'COD_PRODUCTO':'CODIGO', 
                'DESCRIPCION':'DESCRIPCION', 
                'UM':'UMD',
                'MARCA':'MARCA', 
                'STOCK':'STOCK', 
                inv_val_moneda:f'Inventario Valorizado {moneda}', 
                
                'CANTIDAD': f'Consumo Promedio Mensual', 
                'Meses Inventario':'Meses de Inventario', 
                #'Inventario Valorizado':'Inventario Valorizado', 
                'TI':'TI'
            })
        
        return [
           
            [{'value': i[0], 'label': i[1]} for i in input_df.groupby(['codsucursal','SUCURSAL'])[['STOCK']].sum().reset_index()[['codsucursal','SUCURSAL']].values],
            [{'value': i[0], 'label': i[1]} for i in input_df.groupby(['codalmacen','ALMACEN'])[['STOCK']].sum().reset_index()[['codalmacen','ALMACEN']].values],
            [{'value': i[0], 'label': i[1]} for i in input_df.groupby(['codgrupo','DSC_GRUPO'])[['STOCK']].sum().reset_index()[['codgrupo','DSC_GRUPO']].values],
            [{'value': i[0], 'label': i[1]} for i in input_df.groupby(['codsubgrupo','DSC_SUBGRUPO'])[['STOCK']].sum().reset_index()[['codsubgrupo','DSC_SUBGRUPO']].values], 
            [{'label': i, 'value': i} for i in sorted(input_df['MARCA'].unique())],
            cpm,invval,stock,consumo,
            bar_logistica_y1(df = df_mi_,height = 350),
            bar_logistica_y2(df = df_mi_iv,height = 350,y_col=inv_val_moneda ),
            df_table.to_dict("records"),
            fields_columns(columns = df_table.columns),
            df_table.to_dict("series"),
            #dff.to_dict('series'),
            DataDisplay.notification(text=f'Se cargaron {len(dff)} filas',title='Update')
        ]
"""
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
            

"""
@app.callback(
        #Output('multiselect-almacen','data'),
        Output("multiselect-almacen","data"),
        Output("data-stock","data"),
        Input('multiselect-almacen','value'),
        Input('select-tipo-val','value'),
        Input('num-meses','value')
    )
    def update_data_stock(almacen,tipo_val,meses_back):
        meses_back_ = 1 if meses_back == 0 or meses_back == None else meses_back
        consumo_alm_df = connect_consumo_alm(mes_back = meses_back_,tipo_val= tipo_val)
        if almacen == None or len(almacen) == 0:#(len(almacen)==0 or cultivo==None):
            df = consumo_alm_df.copy()
        else:
            df = consumo_alm_df[consumo_alm_df['ALMACEN']==almacen]
        
        return [
            [{'label': i, 'value': i} for i in df['ALMACEN'].unique()],
            df.to_dict('series')
        ]
    
    @app.callback(
        [
            Output('select-grupo','data'),
            Output('select-subgrupo','data'),
            Output('select-marca','data'),
            #Output('range-slider-cpm','max'),
            #Output('range-slider-cpm','value'),
            Output('select-sucursal','data'),
            #Output('inv_val_total','data'),
        ]+
        [
         Output("data-values","data"),
         Output("notifications-update-data","children")
        ],
        [
            Input('select-grupo','value'),
            Input('select-subgrupo','value'),
            Input('select-marca','value'),
            Input('select-moneda','value'),
            Input('text-input-find','value'),
            Input('num-meses','value'),
            Input('data-stock','data'),
            Input('select-sucursal','value'),
            Input('multiselect-almacen','value'),
        ]
    )
    def update_filter_(*args):
        grupo = args[0]
        subgrupo = args[1]
        marca = args[2]
        moneda = args[3]
        input_text = args[4]
        mes_back = args[5]
        consumo_alm_df = pd.DataFrame(args[6])
        sucursal = args[7]
        almacen = args[8]
        if sucursal != None:
            consumo_alm_df = consumo_alm_df[consumo_alm_df['SUCURSAL']==sucursal]
        precio_ = 'PU_S' if moneda == 'soles' else 'PU_D'
        inv_val_moneda = 'INV_VALMOF' if moneda == 'soles' else 'INV_VALMEX'
        #sucursal_ = sucursal if sucursal != None else ''
        #almacen_ = almacen if almacen != None else ''
        
        saldos_alm_df = change_cols_saldosalm(df = connect_saldos_alm())
        if sucursal == None and almacen == None:
            saldos_alm_df = saldos_alm_df.copy()
        elif sucursal != None and almacen == None:
            saldos_alm_df=saldos_alm_df[saldos_alm_df['SUCURSAL']==sucursal]
        elif sucursal == None and almacen != None:
            saldos_alm_df=saldos_alm_df[saldos_alm_df['ALMACEN']==almacen]
        elif sucursal != None and almacen != None:
            saldos_alm_df=saldos_alm_df[(saldos_alm_df['ALMACEN']==almacen)&(saldos_alm_df['SUCURSAL']==sucursal)]
        #stock_producto = saldos_alm_df.groupby(['COD_PRODUCTO'])[['STOCK']].sum().reset_index()
        saldos_alm_df.loc[saldos_alm_df.MARCA =='','MARCA']='NO ESPECIFICADO'
        #saldos_alm_df.to_excel('saldos_alm_.xlsx')
        #stock_promedio_= saldos_alm_df.groupby(['COD_PRODUCTO'])[[precio_]].mean().reset_index()
        #precio_unit = saldos_alm_df.groupby(['COD_PRODUCTO'])[[precio_]].mean().reset_index()
        #precio_unit = precio_unit.rename(columns={precio_:'Precio Unitario'})
        cantidad_almacen_ = consumo_alm_df.groupby(['IDPRODUCTO'])[['CANTIDAD']].sum().reset_index()
        
        if validate_inputs(variables = (grupo,subgrupo,marca)) == True:
            productos_dff = saldos_alm_df.copy()
        else:
            productos_dff = saldos_alm_df.query(dataframe_filtro(values=list((grupo,subgrupo,marca)),columns_df = ['DSC_GRUPO','DSC_SUBGRUPO','MARCA']))
    
        productos_cols_df = productos_dff.groupby(['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA'])[[precio_, 'STOCK', 'INV_VALMOF', 'INV_VALMEX']].sum().reset_index()
        productos_cols_df = productos_cols_df.rename(columns={precio_:'Precio Unitario'})
        #val_inv_valorizado
        
        productos_cant_df = productos_cols_df.merge(cantidad_almacen_, how='left', left_on=["COD_PRODUCTO"], right_on=["IDPRODUCTO"])
        
        ##ADD PRECIO UNIT PROM
        #productos_cant_df = productos_cant_df.merge(precio_unit,how='left',left_on=['COD_PRODUCTO'],right_on=['COD_PRODUCTO'])
        #productos_cant_stock_df = productos_cant_df.merge(stock_producto, how='left', left_on=["COD_PRODUCTO"], right_on=["COD_PRODUCTO"])
        #dff = productos_cant_df.merge(stock_promedio_, how='left', left_on=["COD_PRODUCTO"], right_on=["COD_PRODUCTO"])
        dff = productos_cant_df.copy()
        
        #print('here')
        #print(dff)
        #dff.to_excel('productos_alm.xlsx')
        dff['CANTIDAD'] = dff['CANTIDAD'].fillna(0)
        dff['STOCK'] = dff['STOCK'].fillna(0)
        dff['Precio Unitario'] = dff['Precio Unitario'].fillna(0)
        dff['CANTIDAD'] = dff['CANTIDAD']/mes_back
        dff['CANTIDAD'] = dff['CANTIDAD'].round(2)
        dff['Meses Inventario'] = dff.apply(lambda x: meses_inventario(x['CANTIDAD'],x['STOCK']),axis=1)
        #dff['Inventario Valorizado'] = dff[precio_] * dff['STOCK']
        #dff = dff.sort_values('Inventario Valorizado',ascending =  False)
        dff['TI'] = 1/dff['CANTIDAD']
        dff['TI'] = dff['TI'].replace([np.inf],0)
        if input_text != None:
            
            dff = dff[(dff['COD_PRODUCTO'].str.contains(input_text))|(dff['DESCRIPCION'].str.contains(input_text))]
            
        
        
        
        return [
            [{'label': i, 'value': i} for i in sorted(dff['DSC_GRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(dff['DSC_SUBGRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(dff['MARCA'].unique())],
            #
            
            
            [{'label': i, 'value': i} for i in sorted(consumo_alm_df['SUCURSAL'].unique())],
            #valor_inv_val,
            dff.to_dict('series'),
            DataDisplay.notification(text=f'Se cargaron {len(dff)} filas',title='Update')
        ]
    
    @app.callback(
        #Output('multiselect-almacen','data'),
        Output("card-cpm","children"),
        Output("card-invval","children"),
        Output("card-stock","children"),
        Output("card-consumo","children"),
        Output("bar-minv-prom","figure"),
        Output("bar-inv-val","figure"),
        Output("table","rowData"),
        Output("table","columnDefs"),
        Output("data-table","data"),
        #Output("line-inv-val","value"),
        Input("data-values","data"),
        Input("select-moneda","value"),
        #Input('range-slider-cpm','value'),
        Input('num-meses','value'),
        
    )
    def update_outs(data,moneda,meses_back,):#,slider_cpm
        
        inv_val_moneda = 'INV_VALMOF' if moneda == 'soles' else 'INV_VALMEX'
        df = pd.DataFrame(data)

        #df = df[(df['CANTIDAD']>=slider_cpm[0])&(df['CANTIDAD']<=(slider_cpm[1]+1))]
        
        
        sig = 'S/.' if moneda == 'soles' else '$'
        moneda_ = 'PU_S' if moneda == 'soles' else 'PU_D'
        
        cpm = round(df['CANTIDAD'].mean(),2)
        invval = f"{sig} {(int(round(df[inv_val_moneda].sum(),0))):,}"
        
        meses_invet_prom = df[df['Meses Inventario']!='NO ROTA']
        stock = round(meses_invet_prom['Meses Inventario'].mean(),2)
        consumo = round(df['TI'].mean(),2)
        mi_dff = df[(df['Meses Inventario']!='NO ROTA')]
       
        df_mi_ =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario']].sum().sort_values('Meses Inventario').reset_index().tail(30)
        df_mi_iv =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario',inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index().tail(30)
        

        df = df[['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA','Precio Unitario', 'STOCK', inv_val_moneda,'IDPRODUCTO', 'CANTIDAD', 'Meses Inventario','TI']]
        df = df.drop(['IDPRODUCTO'], axis=1)
        #{'CANTIDAD':'CPM','moneda':'Precio Unitario','Meses Inventario':'Meses de Inventario'}
        #for col_numeric in  ['STOCK', inv_val_moneda,'Precio Unitario', 'CANTIDAD', 'Inventario Valorizado','TI']:
        #    df[col_numeric]=df.apply(lambda x: "{:,.2f}".format(x[col_numeric]), axis=1)
        df = df.rename(columns = {
                'DSC_GRUPO':'GRUPO', 
                'DSC_SUBGRUPO':'SUBGRUPO', 
                'COD_PRODUCTO':'CODIGO', 
                'DESCRIPCION':'DESCRIPCION', 
                'UM':'UMD',
                'MARCA':'MARCA', 
                'STOCK':'STOCK', 
                inv_val_moneda:f'Inventario Valorizado {moneda}', 
                
                'CANTIDAD': f'Consumo Promedio Mensual', 
                'Meses Inventario':'Meses de Inventario', 
                #'Inventario Valorizado':'Inventario Valorizado', 
                'TI':'TI'
            })
        
        return [
            cpm, invval, stock, consumo,
            #bar_(df = df_mi_,x = 'DESCRIPCION', y = 'Meses Inventario', orientation= 'v',height = 380,title = 'Meses de Inventario Promedio',text='Meses Inventario',
            #     xaxis_title = 'Descripción', yaxis_title = 'Meses de Inventario'),
            bar_logistica_y1(df = df_mi_,height = 350),
            bar_logistica_y2(df = df_mi_iv,height = 350,y_col=inv_val_moneda ),
            df.to_dict("records"),
            fields_columns(columns = df.columns),
            df.to_dict("series"),
            
        ]
    download_data(app,input_id_data='data-table',name_file = 'stocks_producto.xlsx')
    opened_modal(app, id="bar-minv-prom",height_modal=900)
    opened_modal(app, id="bar-inv-val",height_modal=900)
    return app
"""