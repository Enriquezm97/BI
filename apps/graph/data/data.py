
import pandas as pd
import numpy as np
import DateTime as dt
from datetime import datetime, timedelta

from apps.graph.data.transform_finanzas import *
from apps.graph.data.transform_comercial import *
from apps.graph.data.transform_produccion import *

import apps.graph.data.clients.Aerodiana as aero
import apps.graph.data.clients.Greenfruits as green
import apps.graph.data.clients.Manuelita as manu
import apps.graph.data.clients.Arona as aro
import apps.graph.data.clients.Nisira as nisira





############################################################################
##NISIRA TEST
df_bcomprobacion_default = pd.read_json("http://68.168.108.184:3000/api/consulta/nsp_eeff_json/")#pd.read_json("http://68.168.108.184:3000/api/consulta/nsp_eeff_json/")
#df_bcomprobacion=df_bcomprobacion_default
"""
##GREENFRUITS
df_bcomprobacion_greenfruits=pd.DataFrame(finanzas_lista_greenfruits)#pd.read_json("http://64.150.180.23:3000/api/consulta/nsp_eeff_json")
##AERODIANA
df_bcomprobacion_aerodiana=pd.DataFrame(finanzas_lista_aerodiana)#pd.read_json("http://69.64.92.156:3000/api/consulta/nsp_eeff_json")
##ARONA
df_bcomprobacion_arona=pd.DataFrame(finanzas_lista_arona)#'owo'

## MANUELITA
df_bcomprobacion_manuelita=pd.DataFrame(finanzas_lista_manuelita)
##NISIRA
df_bcomprobacion_nisira='owo'
"""


df_bc_default=cleanBalanceComprobacion(df_bcomprobacion_default)
df_bc_greenfruits=cleanBalanceComprobacion(green.df_bcomprobacion_greenfruits)
df_bc_aerodiana=cleanBalanceComprobacion(aero.df_bcomprobacion_aerodiana)
df_bc_nisira=cleanBalanceComprobacion(nisira.df_bcomprobacion_nisira)
#df_bc_manuelita=cleanBalanceComprobacion(manu.df_bcomprobacion_manuelita)
df_bc_arona=cleanBalanceComprobacion(aro.df_bcomprobacion_arona)

def dataBcEmpresa(empresa):
    #if empresa == 'Nisira':
    #    df_bcomprobacion=df_bc
    if empresa =='ARONA':
        df_bcomprobacion=df_bc_arona
        #df_bcomprobacion=df_bc_default
    elif empresa =='GREENFRUITS':
        df_bcomprobacion=df_bc_greenfruits
        #df_bcomprobacion=df_bc_default
    elif empresa =='AERODIANA':
        df_bcomprobacion=df_bc_aerodiana
    #elif empresa =='NISIRA':
    #    df_bcomprobacion=df_bc
    elif empresa =='MANUELITA':
        #df_bcomprobacion=df_bc_manuelita[df_bc_manuelita['year'].isin(df_bc_manuelita['year'].unique()[-5:])]
        df_bcomprobacion=df_bc_default
    else:
        df_bcomprobacion=df_bc_nisira
        #df_bcomprobacion=df_bc_default
    
    return df_bcomprobacion
    

    

#def data_consumidor(ip):
#        df_consumidores = pd.read_json("http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
        #df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
        #df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
        #df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
        #df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
        #df_consumidores = data[0]
#        return  df_consumidores

df_consumidores = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})


df_var_agricolas_default=cleanVariablesAgricolas(df_consumidores,
                                                  df_variedad,
                                                  df_cultivos,
                                                  df_fertilizacion)
df_var_agricolas_arona=cleanVariablesAgricolas(aro.df_consumidores_arona,
                                               aro.df_variedad_arona,
                                               aro.df_cultivo_arona,
                                              aro.df_fertilizacion_arona)
df_var_agricolas_greenfruits=cleanVariablesAgricolas(green.df_consumidores_greenfruits,
                                                    green.df_variedad_greenfruits,
                                                    green.df_cultivo_greenfruits,
                                                    green.df_fertilizacion_greenfruits           
                                                   )
df_var_agricolas_aerodiana=cleanVariablesAgricolas(df_consumidores,
                                                  df_variedad,
                                                  df_cultivos,
                                                  df_fertilizacion)
#df_var_agricolas_manuelita=cleanVariablesAgricolas(manu.df_consumidores_manuelita,
#                                                   manu.df_variedad_manuelita,
#                                                   manu.df_cultivo_manuelita,
#                                                   manu.df_fertilizacion_manuelita
#                                                   )

df_var_agricolas_pivot_default=variablesAgricolasPivot(df_var_agricolas_default)
df_var_agricolas_pivot_arona=variablesAgricolasPivot(df_var_agricolas_default)
df_var_agricolas_pivot_greenfruits=variablesAgricolasPivot(df_var_agricolas_greenfruits)
df_var_agricolas_pivot_aerodiana=variablesAgricolasPivot(df_var_agricolas_aerodiana)
#df_var_agricolas_pivot_manuelita=variablesAgricolasPivot(df_var_agricolas_manuelita)

df_costos_agricola_default=costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad)
df_costos_agricola_arona=costosAgricolas(aro.df_costos_arona,aro.df_consumidores_arona,aro.df_cultivo_arona,aro.df_variedad_arona)
df_costos_agricola_greenfruits=costosAgricolas(green.df_costos_greenfruits,green.df_consumidores_greenfruits,green.df_cultivo_greenfruits,green.df_variedad_greenfruits)
df_costos_agricola_aerodiana=costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad)
#df_costos_agricola_manuelita=costosAgricolas(manu.df_costos_manuelita,manu.df_consumidores_manuelita,manu.df_cultivo_manuelita,manu.df_variedad_manuelita)

def dataAgricolaEmpresa(empresa):
    if empresa =='ARONA':
        df_general=df_var_agricolas_arona
        df_general_pivot=df_var_agricolas_pivot_arona
        df_general_costos=df_costos_agricola_arona
        consumidores=aro.df_consumidores_arona
        #df_general=df_var_agricolas_default
        #df_general_pivot=df_var_agricolas_pivot_default
        #df_general_costos=df_costos_agricola_default
        #consumidores=df_consumidores
    elif empresa =='GREENFRUITS':
        df_general=df_var_agricolas_greenfruits
        df_general_pivot=df_var_agricolas_pivot_greenfruits
        df_general_costos=df_costos_agricola_greenfruits
        consumidores=green.df_consumidores_greenfruits
        #df_general=df_var_agricolas_default
        #df_general_pivot=df_var_agricolas_pivot_default
        #df_general_costos=df_costos_agricola_default
        #consumidores=df_consumidores
    elif empresa =='AERODIANA':
        df_general=df_var_agricolas_aerodiana
        df_general_pivot=df_var_agricolas_pivot_aerodiana
        df_general_costos=df_costos_agricola_aerodiana
        consumidores=df_consumidores
    elif empresa =='MANUELITA':
        #df_general=df_var_agricolas_manuelita
        #df_general_pivot=df_var_agricolas_pivot_manuelita
        #df_general_costos=df_costos_agricola_manuelita
        #consumidores=manu.df_consumidores_manuelita
        df_general=df_var_agricolas_default
        df_general_pivot=df_var_agricolas_pivot_default
        df_general_costos=df_costos_agricola_default
        consumidores=df_consumidores
    else:
        df_general=df_var_agricolas_default
        df_general_pivot=df_var_agricolas_pivot_default
        df_general_costos=df_costos_agricola_default
        consumidores=df_consumidores
    
    return df_general,df_general_pivot,df_general_costos,consumidores

#df_general['week']=df_general['SEMANA']
#semanas=sorted(df_general['SEMANA'].unique())
#for anio in df_general['AÑO_CAMPAÑA'].unique():
#    for i in semanas:
#        df_general['week'].loc[df_general['AÑO_CAMPAÑA']==anio]=df_general['week'].replace(i,str(anio)+'-'+str(i))









###############################################################VENTAS

##NISIRA TEST
df_ventas_default= pd.read_json(f"http://68.168.108.184:3000/api/consulta/NSP_RPT_VENTAS_DETALLADO_nisira")#http://68.168.108.184:3000/api/consulta/NSP_RPT_VENTAS_DETALLADO_nisira

 



df_ventas_detalle=cleanVentas(df_ventas_default)
df_ventas_detalle_arona=cleanVentas(aro.df_ventas_arona)
df_ventas_detalle_greenfruits=cleanVentas(green.df_ventas_greenfruits)
df_ventas_detalle_aerodiana=cleanVentas(aero.df_ventas_aerodiana)
df_ventas_detalle_nisira=cleanVentas(nisira.df_ventas_nisira)
#df_ventas_detalle_manuelita=cleanVentas(manu.df_ventas_manuelita)

def dataVentasEmpresa(empresa):
    if empresa =='ARONA':
        #f_ventas_expo=df_ventas_detalle_greenfruits
        df_ventas_expo=df_ventas_detalle_arona
    elif empresa =='GREENFRUITS':
        df_ventas_expo=df_ventas_detalle_greenfruits
        #df_ventas_expo=df_ventas_detalle_arona
    elif empresa =='AERODIANA':
        df_ventas_expo=df_ventas_detalle_aerodiana
    elif empresa =='MANUELITA':
        #df_ventas_expo=df_ventas_detalle_manuelita

        #df_ventas_expo=df_ventas_detalle_greenfruits
        df_ventas_expo=df_ventas_detalle_arona
    else:
        df_ventas_expo=df_ventas_detalle_nisira
        #df_ventas_expo=df_ventas_detalle_greenfruits
    return df_ventas_expo

################ last dashboards




##ARONA
df_control_expo_arona = pd.read_csv("https://raw.githubusercontent.com/Enriquezm97/file/main/exportacion_arona.csv")
##NISIRA TEST

##GREENFRUITS

##AERODIANA

##NISIRA



df_control_contenedores_default=cleanContenedores(df_control_expo_arona)
df_control_contenedores_greenfruits=cleanContenedores(green.df_contenedores_greenfruits)
df_control_contenedores_arona=cleanContenedores(aro.df_contenedores_arona)
df_control_contenedores_aerodiana=cleanContenedores(aero.df_contenedores_aerodiana)
#df_control_contenedores_manuelita=cleanContenedores(manu.df_contenedores_manuelita)

def dataContenedoresEmpresa(empresa):
    if empresa =='ARONA':
        #df_contenedores=df_control_contenedores_default
        df_contenedores=df_control_contenedores_arona
    elif empresa =='GREENFRUITS':
        df_contenedores=df_control_contenedores_greenfruits
        #df_contenedores=df_control_contenedores_arona
    elif empresa =='AERODIANA':
        df_contenedores=df_control_contenedores_aerodiana
    elif empresa =='MANUELITA':
        #df_contenedores=df_control_contenedores_manuelita
        df_contenedores=df_control_contenedores_default
    else:
        df_contenedores=df_control_contenedores_default

    return df_contenedores