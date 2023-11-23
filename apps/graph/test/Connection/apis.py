import pandas as pd
from datetime import datetime
from apps.graph.test.utils.crum import get_data_connection
from apps.graph.test.Connection.read_api import getApi


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