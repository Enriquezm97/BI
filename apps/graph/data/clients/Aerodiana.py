import pandas as pd
from apps.graph.data.gets import getApi

token_aerodina='0Z10F10O10E10Y10D10Z10Q10Z1lpu0N10O10H1T890Z10F10O10E10Y10D10Z10Q10Z1sgk0Q10D10N10D10O10Z1lpu0q10d10n10d10o10z1lpu0Q10d10n10d10o10z1poiqwsmkiqwsert23dlpumkimkiertlpuertsdfasdasdlpuertbhgnjhmkiertmkiqwssdfsdfsdfloisdfqws'

api_aerodiana_ventas='http://69.64.92.156:3005/api/consulta/NSP_RPT_VENTAS_DETALLADO'
api_aerodiana_finanzas='http://69.64.92.156:3005/api/consulta/nsp_eeff_json'
api_aerodiana_contenedores='http://69.64.92.156:3005/api/consulta/NSP_INDICADOR_CTRL_EXPORTACION'
api_aerodiana_pizarra='http://69.64.92.156:3005/api/consulta/BI_PIZARRA_TRACKING/?empresa=001&c_finicio=20210101&c_ffin=20221101'
api_aerodiana_consumidores='http://69.64.92.156:3005/api/consulta/nsp_datos_consumidores'
api_aerodiana_variedades='http://69.64.92.156:3005/api/consulta/nsp_datos_variedades_cultivos'
api_aerodiana_cultivos='http://69.64.92.156:3005/api/consulta/nsp_datos_cultivos'
api_aerodiana_fertilizacion='http://69.64.92.156:3005/api/consulta/nsp_datos_plan_fertilizacion'
api_aerodiana_costos='http://69.64.92.156:3005/api/consulta/nsp_datos_detalle_costos_campana'

ventas_lista_aerodiana=getApi(api_aerodiana_ventas,token_aerodina)
finanzas_lista_aerodiana=getApi(api_aerodiana_finanzas,token_aerodina)
contenedores_lista_aerodiana=getApi(api_aerodiana_contenedores,token_aerodina)
pizarra_lista_aerodiana=getApi(api_aerodiana_pizarra,token_aerodina)

#DATAFRAME VENTAS
df_ventas_aerodiana=pd.DataFrame(ventas_lista_aerodiana)

#DATAFRAME BALANCE DE COMPROBACION
df_bcomprobacion_aerodiana=pd.DataFrame(finanzas_lista_aerodiana)

#DATAFRAME CONTENEDORES
df_contenedores_aerodiana=pd.DataFrame(contenedores_lista_aerodiana)

#DATAFRAME PIZARRA
df_pizarra_aerodiana=pd.DataFrame(pizarra_lista_aerodiana)

#DATAFRAME VARIABLES AGRICOLAS Y COSTOS
#df_consumidores_aerodiana=pd.DataFrame(consumidores_lista_aerodiana,dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
#df_variedad_aerodiana=pd.DataFrame(variedades_lista_aerodiana,dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
#df_cultivo_aerodiana=pd.DataFrame(cultivos_lista_aerodiana,dtype={'CODCULTIVO':str})
#df_fertilizacion_aerodiana=pd.DataFrame(fertilizacion_lista_aerodiana)
#df_costos_aerodiana=pd.DataFrame(costos_lista_aerodiana)