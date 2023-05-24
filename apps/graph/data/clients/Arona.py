import pandas as pd
from apps.graph.data.gets import getApi



"""
token_arona="0Z10O10E10Q10Z1qwsmkiqwsmki0D10Q10X10D10Y10F10Q10X10D10Z1lpubhgrtgpoiertbhgrtgpoiertmkiqwspoiqwsqwsbhglpu0q10d10n10d10o10z10c10z10w10e10o10z10c1lpu0z10y10s10d10q1qwsmkiertloipoi0o10z10o1lpumkimkiertlpuertsdfasdasdlpuertbhgnjhmkimkirtgmkibhgasdnjhbhgbhgrtg"
api_arona_ventas='http://68.168.102.226:3005/api/consulta/NSP_RPT_VENTAS_DETALLADO'
api_arona_finanzas='http://68.168.102.226:3005/api/consulta/nsp_eeff_json'
api_arona_contenedores='http://68.168.102.226:3005/api/consulta/NSP_INDICADOR_CTRL_EXPORTACION'
api_arona_pizarra='http://68.168.102.226:3005/api/consulta/BI_PIZARRA_TRACKING/?empresa=001&c_finicio=20210101&c_ffin=20221101'
api_arona_consumidores='http://68.168.102.226:3005/api/consulta/nsp_datos_consumidores'
api_arona_variedades='http://68.168.102.226:3005/api/consulta/nsp_datos_variedades_cultivos'
api_arona_cultivos='http://68.168.102.226:3005/api/consulta/nsp_datos_cultivos'
api_arona_fertilizacion='http://68.168.102.226:3005/api/consulta/nsp_datos_plan_fertilizacion'
api_arona_costos='http://68.168.102.226:3005/api/consulta/nsp_datos_detalle_costos_campana'

ventas_lista_arona=getApi(api_arona_ventas,token_arona)
finanzas_lista_arona=getApi(api_arona_finanzas,token_arona)
contenedores_lista_arona=getApi(api_arona_contenedores,token_arona)
pizarra_lista_arona=getApi(api_arona_pizarra,token_arona)

consumidores_lista_arona=getApi(api_arona_consumidores,token_arona)
variedades_lista_arona=getApi(api_arona_variedades,token_arona)
cultivos_lista_arona=getApi(api_arona_cultivos,token_arona)
fertilizacion_lista_arona=getApi(api_arona_fertilizacion,token_arona)
costos_lista_arona=getApi(api_arona_costos,token_arona)

#DATAFRAME VENTAS
df_ventas_arona=pd.DataFrame(ventas_lista_arona)

#DATAFRAME BALANCE DE COMPROBACION
df_bcomprobacion_arona=pd.DataFrame(finanzas_lista_arona)

#DATAFRAME CONTENEDORES
df_contenedores_arona=pd.DataFrame(contenedores_lista_arona)

#DATAFRAME PIZARRA
df_pizarra_arona=pd.DataFrame(pizarra_lista_arona)

#DATAFRAME VARIABLES AGRICOLAS Y COSTOS
df_consumidores_arona=pd.DataFrame(consumidores_lista_arona)#,dtype={'CODCULTIVO':str,'CODVARIEDAD':str}
df_variedad_arona=pd.DataFrame(variedades_lista_arona)#,dtype={'CODCULTIVO':str,'CODVARIEDAD':str}
df_cultivo_arona=pd.DataFrame(cultivos_lista_arona)#,dtype={'CODCULTIVO':str}
df_fertilizacion_arona=pd.DataFrame(fertilizacion_lista_arona)
df_costos_arona=pd.DataFrame(costos_lista_arona)

"""


