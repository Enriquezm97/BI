import pandas as pd
from apps.graph.data.gets import getApi

token_greenfruits='0G10O10F10F10Q10T10O10A10D10M10N1lpu0N10O10H10G10T1sgk0Q10D10N10D10O10Z1lpu0q10d10n10d10o10z1lpu0B10m10K10r10z1asd0C1sdf0Z10S10Y10i1qws0u1lpumkimkiertlpuertsdfasdasdlpuertbhgnjhmkimkiloinjhrtgqwsrtgsdfsdfdfg'

api_greenfruits_ventas='http://64.150.180.23:3005/api/consulta/NSP_RPT_VENTAS_DETALLADO'
api_greenfruitss_finanzas='http://64.150.180.23:3005/api/consulta/nsp_eeff_json'
api_greenfruits_contenedores='http://64.150.180.23:3005/api/consulta/NSP_INDICADOR_CTRL_EXPORTACION'
api_greenfruits_pizarra='http://64.150.180.23:3005/api/consulta/BI_PIZARRA_TRACKING_2/?empresa=001&c_finicio=20210101&c_ffin=20221101'
api_greenfruits_consumidores='http://64.150.180.23:3005/api/consulta/nsp_datos_consumidores'
api_greenfruits_variedades='http://64.150.180.23:3005/api/consulta/nsp_datos_variedades_cultivos'
api_greenfruits_cultivos='http://64.150.180.23:3005/api/consulta/nsp_datos_cultivos'
api_greenfruits_fertilizacion='http://64.150.180.23:3005/api/consulta/nsp_datos_plan_fertilizacion'
api_greenfruits_costos='http://64.150.180.23:3005/api/consulta/nsp_datos_detalle_costos_campana'

ventas_lista_greenfruits=getApi(api_greenfruits_ventas,token_greenfruits)
finanzas_lista_greenfruits=getApi(api_greenfruitss_finanzas,token_greenfruits)
contenedores_lista_greenfruits=getApi(api_greenfruits_contenedores,token_greenfruits)
pizarra_lista_greenfruits=getApi(api_greenfruits_pizarra,token_greenfruits)

consumidores_lista_greenfruits=getApi(api_greenfruits_consumidores,token_greenfruits)
variedades_lista_greenfruits=getApi(api_greenfruits_variedades,token_greenfruits)
cultivos_lista_greenfruits=getApi(api_greenfruits_cultivos,token_greenfruits)
fertilizacion_lista_greenfruits=getApi(api_greenfruits_fertilizacion,token_greenfruits)
costos_lista_greenfruits=getApi(api_greenfruits_costos,token_greenfruits)


#DATAFRAME VENTAS
df_ventas_greenfruits=pd.DataFrame(ventas_lista_greenfruits)

#DATAFRAME BALANCE DE COMPROBACION
df_bcomprobacion_greenfruits=pd.DataFrame(finanzas_lista_greenfruits)

#DATAFRAME CONTENEDORES
df_contenedores_greenfruits=pd.DataFrame(contenedores_lista_greenfruits)

#DATAFRAME PIZARRA
df_pizarra_greenfruits=pd.DataFrame(pizarra_lista_greenfruits)

#DATAFRAME VARIABLES AGRICOLAS Y COSTOS
df_consumidores_greenfruits=pd.DataFrame(consumidores_lista_greenfruits)#,dtype={'CODCULTIVO':str,'CODVARIEDAD':str}
df_variedad_greenfruits=pd.DataFrame(variedades_lista_greenfruits)#,dtype={'CODCULTIVO':str,'CODVARIEDAD':str}
df_cultivo_greenfruits=pd.DataFrame(cultivos_lista_greenfruits)#,dtype={'CODCULTIVO':str}
df_fertilizacion_greenfruits=pd.DataFrame(fertilizacion_lista_greenfruits)
df_costos_greenfruits=pd.DataFrame(costos_lista_greenfruits)