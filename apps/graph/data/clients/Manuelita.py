import pandas as pd
from apps.graph.data.gets import getApi
"""
token_manuelita='0Q10D10N10D10O10Z1qwsmkiertertlpu0N10H10O10I10Y10Z10M10Z1lpu0n10a10i1lpuert0s10i10c123d0q10m123d0x1ertmki0q1qwsmkiqwsertlpumkimkiertlpuertsdfasdasdlpuertbhgnjhmkiertqwsnjhsdfnjhrtgloiqwsmki'

api_manuelita_ventas='http://209.45.79.42:3005/api/consulta/NSP_RPT_VENTAS_DETALLADO'
api_manuelita_finanzas='http://209.45.79.42:3005/api/consulta/nsp_eeff_json'
api_manuelita_contenedores='http://209.45.79.42:3005/api/consulta/NSP_INDICADOR_CTRL_EXPORTACION'
api_manuelita_pizarra='http://209.45.79.42:3005/api/consulta/BI_PIZARRA_TRACKING1/?empresa=001&c_finicio=20210101&c_ffin=20221101'
api_manuelita_consumidores='http://209.45.79.42:3005/api/consulta/nsp_datos_consumidores'
api_manuelita_variedades='http://209.45.79.42:3005/api/consulta/nsp_datos_variedades_cultivos'
api_manuelita_cultivos='http://209.45.79.42:3005/api/consulta/nsp_datos_cultivos'
api_manuelita_fertilizacion='http://209.45.79.42:3005/api/consulta/nsp_datos_plan_fertilizacion'
api_manuelita_costos='http://209.45.79.42:3005/api/consulta/nsp_datos_detalle_costos_campana'

ventas_lista_manuelita=getApi(api_manuelita_ventas,token_manuelita)
finanzas_lista_manuelita=getApi(api_manuelita_finanzas,token_manuelita)
contenedores_lista_manuelita=getApi(api_manuelita_contenedores,token_manuelita)
pizarra_lista_manuelita=getApi(api_manuelita_pizarra,token_manuelita)

consumidores_lista_manuelita=getApi(api_manuelita_consumidores,token_manuelita)
variedades_lista_manuelita=getApi(api_manuelita_variedades,token_manuelita)
cultivos_lista_manuelita=getApi(api_manuelita_cultivos,token_manuelita)
fertilizacion_lista_manuelita=getApi(api_manuelita_fertilizacion,token_manuelita)
costos_lista_manuelita=getApi(api_manuelita_costos,token_manuelita)

#DATAFRAME VENTAS
df_ventas_manuelita=pd.DataFrame(ventas_lista_manuelita)

#DATAFRAME BALANCE DE COMPROBACION
df_bcomprobacion_manuelita=pd.DataFrame(finanzas_lista_manuelita)

#DATAFRAME CONTENEDORES
df_contenedores_manuelita=pd.DataFrame(contenedores_lista_manuelita)

#DATAFRAME PIZARRA
df_pizarra_manuelita=pd.DataFrame(pizarra_lista_manuelita)

#DATAFRAME VARIABLES AGRICOLAS Y COSTOS
df_consumidores_manuelita=pd.DataFrame(consumidores_lista_manuelita)#,dtype={'CODCULTIVO':str,'CODVARIEDAD':str}
df_variedad_manuelita=pd.DataFrame(variedades_lista_manuelita)#,dtype={'CODCULTIVO':str,'CODVARIEDAD':str}
df_cultivo_manuelita=pd.DataFrame(cultivos_lista_manuelita)#,dtype={'CODCULTIVO':str}
df_fertilizacion_manuelita=pd.DataFrame(fertilizacion_lista_manuelita)
df_costos_manuelita=pd.DataFrame(costos_lista_manuelita)
"""