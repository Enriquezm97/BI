import pandas as pd
from datetime import datetime, timedelta
import requests as r
"""
def data_agricola(ip):
        df_consumidores = pd.read_json(f"http://{ip}:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
        df_costos_campana = pd.read_json(f"http://{ip}:3000/api/consulta/nsp_datos_detalle_costos_campana")
        df_variedad = pd.read_json(f"http://{ip}:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
        df_fertilizacion = pd.read_json(f"http://{ip}:3000/api/consulta/nsp_datos_plan_fertilizacion")
        df_cultivos = pd.read_json(f"http://{ip}:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
        #68.168.108.184
        #df_consumidores = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_consumidores",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
        #df_costos_campana = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_detalle_costos_campana")
        #df_variedad = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_variedades_cultivos",dtype={'CODCULTIVO':str,'CODVARIEDAD':str})
        #df_fertilizacion = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_plan_fertilizacion")
        #df_cultivos = pd.read_json(f"http://68.168.108.184:3000/api/consulta/nsp_datos_cultivos",dtype={'CODCULTIVO':str})
        return df_consumidores,df_costos_campana,df_variedad,df_fertilizacion,df_cultivos

def data_balance_comprobacion(ip):
    df_bcomprobacion = pd.read_json(f"http://{ip}:3000/api/consulta/nsp_eeff_json/")#(p.nsp_eeff_json)
    return df_bcomprobacion
"""