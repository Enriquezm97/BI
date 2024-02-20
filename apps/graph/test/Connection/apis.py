import pandas as pd
import requests
import json
from datetime import datetime
from apps.graph.test.utils.crum import get_data_connection
from apps.graph.test.Connection.read_api import getApi
from ..utils.functions.functions_transform import *


def connection_api(sp_name = 'nsp_rpt_ventas_detallado', test = 'no'):
    if test == 'no':
        ip, token_ =get_data_connection()
        dataframe = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/{sp_name}',token = token_))
    else:
        df_ventas_detalle=pd.read_parquet('comercial_new_etl.parquet', engine='pyarrow')
        df_ventas_detalle['Tipo de Movimiento'] = df_ventas_detalle['Tipo de Movimiento'].astype(object)
        df_ventas_detalle['Tipo de Venta'] = df_ventas_detalle['Tipo de Venta'].astype(object)
        df_ventas_detalle['Tipo de Condicion'] = df_ventas_detalle['Tipo de Condicion'].astype(object)
        df_ventas_detalle['Grupo Producto'] = df_ventas_detalle['Grupo Producto'].astype(object)
        df_ventas_detalle['Subgrupo Producto'] = df_ventas_detalle['Subgrupo Producto'].astype(object)
        df_ventas_detalle['Vendedor'] = df_ventas_detalle['Vendedor'].astype(object)

        df_ventas_detalle['Tipo de Movimiento'] = df_ventas_detalle['Tipo de Movimiento'].fillna('NO ESPECIFICADO')
        df_ventas_detalle['Tipo de Venta'] = df_ventas_detalle['Tipo de Venta'].fillna('NO ESPECIFICADO')
        df_ventas_detalle['Tipo de Condicion'] = df_ventas_detalle['Tipo de Condicion'].fillna('NO ESPECIFICADO')
        df_ventas_detalle['Grupo Producto'] = df_ventas_detalle['Grupo Producto'].fillna('NO ESPECIFICADO')
        df_ventas_detalle['Subgrupo Producto'] = df_ventas_detalle['Subgrupo Producto'].fillna('NO ESPECIFICADO')
        df_ventas_detalle['Vendedor'] = df_ventas_detalle['Vendedor'].fillna('NO ESPECIFICADO')

        df_ventas_detalle['Cliente']=df_ventas_detalle['Cliente'].str[:30]
        df_ventas_detalle['Producto']=df_ventas_detalle['Producto'].str[:30]
        df_ventas_detalle['Fecha']=df_ventas_detalle['Fecha'].apply(lambda a: pd.to_datetime(a).date())
        dataframe = df_ventas_detalle.copy()
    return dataframe
from celery import shared_task
#@shared_task()
def connection_api_almstock():
    
    ip, token_ =get_data_connection()
    fecha_now = (str(datetime.now())[:10].replace('-', ""))
    dataframe = pd.DataFrame(getApi(api=f"http://{ip}:3005/api/consulta/STOCKALMVAL?EMPRESA=001&SUCURSAL=&ALMACEN&FECHA={fecha_now}&IDGRUPO&SUBGRUPO&DESCRIPCION&IDPRODUCTO",token = token_))
    
    return dataframe

def connection_api_agricola(tipo = 'fertilizantes'):
    print('consulta api owo')
    ip, token_ =get_data_connection()
    if tipo ==  'fertilizantes':
        consumidores = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/nsp_datos_consumidores',token = token_))
        variedades = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/nsp_datos_variedades_cultivos',token = token_))
        cultivos = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/nsp_datos_cultivos',token = token_))
        fertilizantes = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/nsp_datos_plan_fertilizacion',token = token_))
       
        dataframe = cleanVariablesAgricolas(df_consumidores=consumidores,df_variedad=variedades,df_cultivos=cultivos,df_fertilizacion= fertilizantes)
    elif tipo ==  'costos':
        consumidores = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/nsp_datos_consumidores',token = token_))
        variedades = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/nsp_datos_variedades_cultivos',token = token_))
        cultivos = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/nsp_datos_cultivos',token = token_))
        costos = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/nsp_datos_detalle_costos_campana',token = token_))
        dataframe = costosAgricolas(df_costos_campana = costos,df_consumidores = consumidores,df_cultivos = cultivos,df_variedad = variedades)
    return dataframe

def conecction_data_tc():
    iter_data= pd.DataFrame(columns=['compra','venta','origen','moneda','fecha'])
    fecha_now =datetime.now()
    for mes  in range(1,fecha_now.month+1):
        r = requests.get(f"https://api.apis.net.pe/v1/tipo-cambio-sunat?month={mes}&year={fecha_now.year}")
        data = json.loads(r.text)
        iter_data=pd.concat([iter_data,pd.DataFrame(data)])
    return iter_data.rename(columns = {'compra':'Compra','venta': 'Venta','fecha': 'Fecha'})