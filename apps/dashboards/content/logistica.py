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


from concurrent.futures import ThreadPoolExecutor
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
    with ThreadPoolExecutor(max_workers=2) as executor:
        consumos_api_alm_df = executor.submit(api.send_get_dataframe,"NSP_OBJREPORTES_CONSUMOSALM_DET_BI",dict_CONSUMOSALM).result()
        saldos_api_alm_df = executor.submit(api.send_get_dataframe,"NSP_OBJREPORTES_SALDOSALMACEN_BI",dict_SALDOSALM).result()
    
    saldos_api_alm_df = change_cols_saldosalm(saldos_api_alm_df)
    print(datetime.now())
    #consumos_api_alm_df = api.send_get_dataframe(endpoint="NSP_OBJREPORTES_CONSUMOSALM_DET_BI",params=dict_CONSUMOSALM)
    
    #saldos_api_alm_df = change_cols_saldosalm(api.send_get_dataframe(endpoint="NSP_OBJREPORTES_SALDOSALMACEN_BI",params=dict_SALDOSALM))
    
    
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
        
        Output("bar-inv_val-first","figure"),
        Output("bar-inv_val-second","figure"),
        Output("bar-inv_val-thrid","figure"),
        
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
        
        if cpm_min != None and cpm_max != None:
            dff = dff[(dff['CANTIDAD']>=cpm_min)&(dff['CANTIDAD']<=cpm_max)]
            
        cpm = round(dff['CANTIDAD'].mean(),2)
        invval = f"{sig}{(int(round(dff[inv_val_moneda].sum(),0))):,}"
        meses_invet_prom = dff[dff['Meses Inventario']!='NO ROTA']
        stock = round(meses_invet_prom['Meses Inventario'].mean(),2)
        consumo = round(dff['TI'].mean(),2)
        total_stock = f"{(int(round(dff['STOCK'].sum(),0))):,}"
        
        #GRAPHS
        mi_dff = dff[(dff['Meses Inventario']!='NO ROTA')]
        mi_dff = mi_dff[mi_dff['Meses Inventario']>0]
        
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
        sucursal_df = saldos_alm_df.groupby(['SUCURSAL'])[[inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index()
        almacen_df = saldos_alm_df.groupby(['ALMACEN'])[[inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index()
        grupo_df = saldos_alm_df.groupby(['DSC_GRUPO'])[[inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index()
        #print(df_table['STOCK'].sum())
        return [
            [{'label': i, 'value': i} for i in sorted(input_df['SUCURSAL'].unique())],
            [{'label': i, 'value': i} for i in sorted(input_df['ALMACEN'].unique())],
            [{'label': i, 'value': i} for i in sorted(input_df['DSC_GRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(input_df['DSC_SUBGRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(input_df['MARCA'].unique())],
            cpm,invval,stock,consumo,total_stock,
            bar_logistica_y1(df = df_mi_,height = 320),
            bar_logistica_y2(df = df_mi_iv,height = 320,y_col=inv_val_moneda ),
            bar_horizontal(df = sucursal_df, height = 350, x= inv_val_moneda, y = 'SUCURSAL', name_x='Inventario Valorizado', name_y='Sucursal',title = 'Sucursal por Inventario Valorizado',color = 'rgb(95, 70, 144)'),
            bar_horizontal(df = almacen_df, height = 350, x= inv_val_moneda, y = 'ALMACEN', name_x='Inventario Valorizado', name_y='Almacen',title = 'Almacen por Inventario Valorizado',color ='rgb(29, 105, 150)'),
            bar_horizontal(df = grupo_df, height = 350, x= inv_val_moneda, y = 'DSC_GRUPO', name_x='Inventario Valorizado', name_y='Grupo Producto',title = 'Grupo Producto por Inventario Valorizado',color = 'rgb(56, 166, 165)'),
            df_table.to_dict("records"),
            fields_columns(columns = df_table.columns),
            df_table.to_dict("series"),
            DataDisplay.notification(text=f'Se cargaron {len(dff)} filas',title='Update')
        ]

    download_data(app,input_id_data='data-table',name_file = 'stocks_producto.xlsx')
    opened_modal(app, id="bar-minv-prom",height_modal=900)
    opened_modal(app, id="bar-inv-val",height_modal=900)
    opened_modal(app, id="bar-inv_val-first",height_modal=900)
    opened_modal(app, id="bar-inv_val-second",height_modal=900)
    opened_modal(app, id="bar-inv_val-thrid",height_modal=900)
    return app
   
#LAST CALLBACK     
