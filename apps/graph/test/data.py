import pandas as pd
import numpy as np
import requests
from apps.graph.test.utils.functions.functions_transform import *
from ..test.Connection.apis import connection_api

df_var_agricolas_default=pd.read_parquet('agricola.parquet', engine='pyarrow')
df_costos_agricola_default=pd.read_parquet('costos.parquet', engine='pyarrow')







#################
def getApi(api,token):
    response = requests.get(api, headers={'Authorization': "Bearer {}".format(token)})
    objeto=response.json()
    list_objetos=objeto['objeto']
    return list_objetos


token_paraiso = '0I10Z10O10Z10D10N10E1lpu0Q10D10N10D10O10Z10I10Z10O10Z10D10N10E1sgk0Q10D10N10D10O10Z1lpu0q10d10n10n10f10o10h10d10x10f1lpu0v10h10p10m10W10v10I10Z10G10y10y10e1lpumkimkiertlpuertsdfasdasdlpuertbhgloiasdsdfrtgmkiertasddfgasdertrtg'
api_paraiso = 'http://190.117.112.27:3005/api/consulta/nsp_rpt_ventas_detallado'

#consumidores = pd.DataFrame(getApi(api='http://190.117.112.27:3005/api/consulta/nsp_datos_consumidores',token = token_paraiso))

#variedades = pd.DataFrame(getApi(api='http://190.117.112.27:3005/api/consulta/nsp_datos_variedades_cultivos',token = token_paraiso))

#cultivos = pd.DataFrame(getApi(api='http://190.117.112.27:3005/api/consulta/nsp_datos_cultivos',token = token_paraiso))

#fertilizantes = pd.DataFrame(getApi(api='http://190.117.112.27:3005/api/consulta/nsp_datos_plan_fertilizacion',token = token_paraiso))

#costos = pd.DataFrame(getApi(api='http://190.117.112.27:3005/api/consulta/nsp_datos_detalle_costos_campana',token = token_paraiso))

#ventas = pd.DataFrame(getApi(api='http://190.117.112.27:3005/api/consulta/nsp_rpt_ventas_detallado',token = token_paraiso))

#ventas_paraiso_df = etl_comercial(ventas)

#agricola_df = cleanVariablesAgricolas(df_consumidores=consumidores,df_variedad=variedades,df_cultivos=cultivos,df_fertilizacion= fertilizantes)
#costos_agricola_df = costosAgricolas(df_costos_campana = costos,df_consumidores = consumidores,df_cultivos = cultivos,df_variedad = variedades)




#bc_df = pd.read_parquet('bc_paraiso.parquet', engine='pyarrow')
#finanzas_dff = etl_bc(bc_df)


def data_agricola(empresa = ''):
    if empresa == 'FUNDO EL PARAISO':
        return df_var_agricolas_default,df_costos_agricola_default
    #agricola_df,costos_agricola_df
    else:
        return df_var_agricolas_default,df_costos_agricola_default
    
def data_comercial(empresa = ''):
    if empresa == 'FUNDO EL PARAISO':
        print("data el paraiso")
        return df_ventas_detalle
    else:
        print("data nisira")
        return df_ventas_detalle
    

def data_finanzas(empresa = ''):
    if empresa == 'FUNDO EL PARAISO':
        print("data el paraiso")
        return finanzas_dff
    elif empresa == 'SAMPLAST':
        return None
    else:
        
        return finanzas_dff


        