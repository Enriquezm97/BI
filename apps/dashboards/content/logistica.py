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

filt = ['select-anio','select-grupo','select-rango']
dict_almacen = {
            'IDALMACEN':['001','002','003','004','005','006','007','008'],
            'ALMACEN':['ALMACEN CENTRAL','ALMACEN EN PROCESO','ALMACEN PRODUCTO TERMINADO','ALMACEN EXTERIOR TEMPORAL','ALMACEN TERCEROS','ALMACEN DE AJUSTE DE INVENTARIO','ALMACEN TEMPORAL LATAM','ALMACEN AVERIADOS']
}

dict_sucursal = {
    'IDSUCURSAL':['001','002','003'],
    'SUCURSAL':['LIMA','ICA','ALMACEN TERCEROS']
}

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



def dashboard_gestion_stock(codigo = '',empresa = ''):#filtros = ['select-anio','select-grupo','select-rango']
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    #print(connect_saldos_alm())
    
    app.layout =  gestion_stock(data_almacen=['ALMACEN CENTRAL','ALMACEN EN PROCESO','ALMACEN PRODUCTO TERMINADO','ALMACEN EXTERIOR TEMPORAL','ALMACEN TERCEROS','ALMACEN DE AJUSTE DE INVENTARIO','ALMACEN TEMPORAL LATAM','ALMACEN AVERIADOS'])
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
        consumo_alm_df = consumo_alm_df.merge(pd.DataFrame(dict_almacen), how='left', left_on=["IDALMACEN"], right_on=["IDALMACEN"])
        consumo_alm_df = consumo_alm_df.merge(pd.DataFrame(dict_sucursal), how='left', left_on=["IDSUCURSAL"], right_on=["IDSUCURSAL"])
        #consumo_alm_df.to_excel('alm_suc.xlsx')
        if almacen == None or len(almacen) == 0:#(len(almacen)==0 or cultivo==None):
            df = consumo_alm_df.copy()
        else:
            df = consumo_alm_df[consumo_alm_df['ALMACEN'].isin(almacen)]
        
        return [
            [{'label': i, 'value': i} for i in df['ALMACEN'].unique()],
            df.to_dict('series')
        ]

    @app.callback(
        [
            Output('select-grupo','data'),
            Output('select-subgrupo','data'),
            Output('select-marca','data'),
            Output('range-slider-cpm','max'),
            Output('range-slider-cpm','value'),
            Output('select-sucursal','data'),
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
        if sucursal != None:
            consumo_alm_df = consumo_alm_df[consumo_alm_df['SUCURSAL']==sucursal]
        precio_ = 'PU_S' if moneda == 'soles' else 'PU_D'
        
        saldos_alm_df = connect_saldos_alm()
        #stock_producto = saldos_alm_df.groupby(['COD_PRODUCTO'])[['STOCK']].sum().reset_index()
        saldos_alm_df.loc[saldos_alm_df.MARCA =='','MARCA']='NO ESPECIFICADO'
        
        #stock_promedio_= saldos_alm_df.groupby(['COD_PRODUCTO'])[[precio_]].mean().reset_index()
        precio_unit = saldos_alm_df.groupby(['COD_PRODUCTO'])[[precio_]].mean().reset_index()
        precio_unit = precio_unit.rename(columns={precio_:'Precio Unitario'})
        cantidad_almacen_ = consumo_alm_df.groupby(['IDPRODUCTO'])[['CANTIDAD']].sum().reset_index()
        
        if validate_inputs(variables = (grupo,subgrupo,marca)) == True:
            productos_dff = saldos_alm_df.copy()
        else:
            productos_dff = saldos_alm_df.query(dataframe_filtro(values=list((grupo,subgrupo,marca)),columns_df = ['DSC_GRUPO','DSC_SUBGRUPO','MARCA']))
    
        productos_cols_df = productos_dff.groupby(['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA'])[['PU_S', 'PU_D', 'STOCK', 'INV_VALMOF', 'INV_VALMEX']].sum().reset_index()
        productos_cant_df = productos_cols_df.merge(cantidad_almacen_, how='left', left_on=["COD_PRODUCTO"], right_on=["IDPRODUCTO"])
        ##ADD PRECIO UNIT PROM
        productos_cant_df = productos_cant_df.merge(precio_unit,how='left',left_on=['COD_PRODUCTO'],right_on=['COD_PRODUCTO'])
        #productos_cant_stock_df = productos_cant_df.merge(stock_producto, how='left', left_on=["COD_PRODUCTO"], right_on=["COD_PRODUCTO"])
        #dff = productos_cant_df.merge(stock_promedio_, how='left', left_on=["COD_PRODUCTO"], right_on=["COD_PRODUCTO"])
        dff = productos_cant_df.copy()
        
        #print('here')
        #print(dff)
        #dff.to_excel('productos_alm.xlsx')
        dff['CANTIDAD'] = dff['CANTIDAD'].fillna(0)
        dff['STOCK'] = dff['STOCK'].fillna(0)
        dff[precio_] = dff[precio_].fillna(0)
        dff['CANTIDAD'] = dff['CANTIDAD']/mes_back
        dff['CANTIDAD'] = dff['CANTIDAD'].round(2)
        dff['Meses Inventario'] = dff.apply(lambda x: meses_inventario(x['CANTIDAD'],x['STOCK']),axis=1)
        dff['Inventario Valorizado'] = dff[precio_] * dff['STOCK']
        dff = dff.sort_values('Inventario Valorizado',ascending =  False)
        dff['TI'] = 1/dff['CANTIDAD']
        dff['TI'] = dff['TI'].replace([np.inf],0)
        if input_text != None:
            
            dff = dff[(dff['COD_PRODUCTO'].str.contains(input_text))|(dff['DESCRIPCION'].str.contains(input_text))]
            
        
        cpm_max = round(dff['CANTIDAD'].max())
        print(len(dff['MARCA'].unique()))
        return [
            [{'label': i, 'value': i} for i in sorted(dff['DSC_GRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(dff['DSC_SUBGRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(dff['MARCA'].unique())],
            cpm_max+1,
            
            [0,cpm_max+1],
            [{'label': i, 'value': i} for i in sorted(consumo_alm_df['SUCURSAL'].unique())],
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
        Input('range-slider-cpm','value'),
        Input('num-meses','value'),
    )
    def update_outs(data,moneda,slider_cpm,meses_back):
        df = pd.DataFrame(data)
        df = df[(df['CANTIDAD']>=slider_cpm[0])&(df['CANTIDAD']<=(slider_cpm[1]+1))]
        sig = 'S/.' if moneda == 'soles' else '$'
        moneda_ = 'PU_S' if moneda == 'soles' else 'PU_D'
        inv_val_moneda = 'INV_VALMOF' if moneda == 'soles' else 'INV_VALMEX'
        cpm = round(df['CANTIDAD'].mean(),2)
        invval = f"{sig} {(int(round(df['Inventario Valorizado'].sum(),0))):,}"
        meses_invet_prom = df[df['Meses Inventario']!='NO ROTA']
        stock = round(meses_invet_prom['Meses Inventario'].mean(),2)
        consumo = round(df['TI'].mean(),2)
        mi_dff = df[(df['Meses Inventario']!='NO ROTA')]
       
        df_mi_ =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario']].sum().sort_values('Meses Inventario').reset_index().tail(30)
        df_mi_iv =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario','Inventario Valorizado']].sum().sort_values('Inventario Valorizado').reset_index().tail(30)
        
        #df['CANTIDAD']=df.apply(lambda x: "{:,.2f}".format(x['CANTIDAD']), axis=1)
        #df['STOCK']=df.apply(lambda x: "{:,.2f}".format(x['STOCK']), axis=1)
        #df[moneda_]=df.apply(lambda x: "{:,.2f}".format(x[moneda_]), axis=1)
        #df['Meses Inventario']=df.apply(lambda x: "{:,.2f}".format(x['Meses Inventario']), axis=1)
        #df['Inventario Valorizado']=df.apply(lambda x: "{:,.2f}".format(x['Inventario Valorizado']), axis=1)
        #df['TI']=df.apply(lambda x: "{:,.2f}".format(x['TI']), axis=1)
        print(df.columns)
        df = df[['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA','Precio Unitario', 'STOCK', inv_val_moneda,'IDPRODUCTO', 'CANTIDAD', 'Meses Inventario', 'Inventario Valorizado','TI']]
        df = df.drop(['IDPRODUCTO'], axis=1)
        #{'CANTIDAD':'CPM','moneda':'Precio Unitario','Meses Inventario':'Meses de Inventario'}
        for col_numeric in  ['STOCK', inv_val_moneda,'Precio Unitario', 'CANTIDAD', 'Inventario Valorizado','TI']:
            df[col_numeric]=df.apply(lambda x: "{:,.2f}".format(x[col_numeric]), axis=1)
        df = df.rename(columns = {
                'DSC_GRUPO':'GRUPO', 
                'DSC_SUBGRUPO':'SUBGRUPO', 
                'COD_PRODUCTO':'CODIGO', 
                'DESCRIPCION':'DESCRIPCION', 
                'UM':'UMD',
                'MARCA':'MARCA', 
                'STOCK':'STOCK', 
                inv_val_moneda:f'Inventario Valorizado {moneda}', 
                
                'CANTIDAD': f'Consumo Prom Mensual({meses_back}meses)', 
                'Meses Inventario':'Meses de Inventario', 
                'Inventario Valorizado':'Inventario Valorizado', 
                'TI':'TI'
            })
        
        return [
            cpm, invval, stock, consumo,
            #bar_(df = df_mi_,x = 'DESCRIPCION', y = 'Meses Inventario', orientation= 'v',height = 380,title = 'Meses de Inventario Promedio',text='Meses Inventario',
            #     xaxis_title = 'Descripción', yaxis_title = 'Meses de Inventario'),
            bar_logistica_y1(df = df_mi_,height = 350),
            bar_logistica_y2(df = df_mi_iv,height = 350 ),
            df.to_dict("records"),
            fields_columns(columns = df.columns),
            df.to_dict("series"),
            
        ]
    download_data(app,input_id_data='data-table',name_file = 'stocks_producto.xlsx')
    opened_modal(app, id="bar-minv-prom",height_modal=900)
    opened_modal(app, id="bar-inv-val",height_modal=900)
    return app
