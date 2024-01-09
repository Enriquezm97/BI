import pandas as pd
from datetime import datetime
from ..api.read_api import get_api
from ..utils.crum import get_data_connect
from ..utils.transform.t_produccion import *

def connect_api(sp_name =''):
    ip, token_ =get_data_connect()
    dataframe = pd.DataFrame(get_api(api=f'http://{ip}:3005/api/consulta/{sp_name}',token = token_))
    return dataframe

def connect_api_stock():
    ip, token_ =get_data_connect()
    fecha_now = (str(datetime.now())[:10].replace('-', ""))
    dataframe = pd.DataFrame(get_api(api=f"http://{ip}:3005/api/consulta/STOCKALMVAL?EMPRESA=001&SUCURSAL=&ALMACEN&FECHA={fecha_now}&IDGRUPO&SUBGRUPO&DESCRIPCION&IDPRODUCTO",token = token_))
    return dataframe

def connect_api_agricola(tipo = 'fertilizantes'):
    ip, token_ =get_data_connect()
    
    if tipo ==  'fertilizantes':
        consumidores = pd.DataFrame(get_api(api=f'http://{ip}:3005/api/consulta/nsp_datos_consumidores',token = token_))
        variedades = pd.DataFrame(get_api(api=f'http://{ip}:3005/api/consulta/nsp_datos_variedades_cultivos',token = token_))
        cultivos = pd.DataFrame(get_api(api=f'http://{ip}:3005/api/consulta/nsp_datos_cultivos',token = token_))
        fertilizantes = pd.DataFrame(get_api(api=f'http://{ip}:3005/api/consulta/nsp_datos_plan_fertilizacion',token = token_))
        dataframe = clean_agricola_ejecucion(df_consumidores=consumidores,df_variedad=variedades,df_cultivos=cultivos,df_fertilizacion= fertilizantes)
    elif tipo ==  'costos':
        consumidores = pd.DataFrame(get_api(api=f'http://{ip}:3005/api/consulta/nsp_datos_consumidores',token = token_))
        variedades = pd.DataFrame(get_api(api=f'http://{ip}:3005/api/consulta/nsp_datos_variedades_cultivos',token = token_))
        cultivos = pd.DataFrame(get_api(api=f'http://{ip}:3005/api/consulta/nsp_datos_cultivos',token = token_))
        costos = pd.DataFrame(get_api(api=f'http://{ip}:3005/api/consulta/nsp_datos_detalle_costos_campana',token = token_))
        dataframe = clean_agricola_costos(df_costos_campana = costos,df_consumidores = consumidores,df_cultivos = cultivos,df_variedad = variedades)
    return dataframe

