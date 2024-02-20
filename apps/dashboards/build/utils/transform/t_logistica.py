import pandas as pd
import numpy as np
from ..helpers import mes_short,new_col_salidas
from ...utils.estructura_data import *

def clean_stocks(df = None):
    df['mes'] = df['mes'].astype('int')
    df['Mes'] = df.apply(lambda x: mes_short(x['mes']),axis=1)
    df['Mes_text']=df['mes']
    df['Mes_text']=df['Mes_text'].replace(1,'Enero')
    df['Mes_text']=df['Mes_text'].replace(2,'Febrero')
    df['Mes_text']=df['Mes_text'].replace(3,'Marzo')
    df['Mes_text']=df['Mes_text'].replace(4,'Abril')
    df['Mes_text']=df['Mes_text'].replace(5,'Mayo')
    df['Mes_text']=df['Mes_text'].replace(6,'Junio')
    df['Mes_text']=df['Mes_text'].replace(7,'Julio')
    df['Mes_text']=df['Mes_text'].replace(8,'Agosto')
    df['Mes_text']=df['Mes_text'].replace(9,'Setiembre')
    df['Mes_text']=df['Mes_text'].replace(10,'Octubre')
    df['Mes_text']=df['Mes_text'].replace(11,'Noviembre')
    df['Mes_text']=df['Mes_text'].replace(12,'Diciembre')
    df = df.rename(columns = columns_nsp_stocks)
    return df

def clean_stock_alm(df = None):
    df['ALMACEN'] = df['ALMACEN'].apply(lambda x: x.strip())
    df['tipo'] = df['tipo'].fillna('No Especificado')
    df['tipo'] = df['tipo'].apply(lambda x: x.strip())
    df['SUCURSAL'] = df['SUCURSAL'].apply(lambda x: x.strip())
    df['GRUPO'] = df['GRUPO'].apply(lambda x: x.strip())
    df['SUBGRUPO'] = df['SUBGRUPO'].apply(lambda x: x.strip())
    df['PRODUCTO'] = df['PRODUCTO'].apply(lambda x: x.strip())
    df['GRUPO2'] = df['GRUPO2'].fillna('')
    df['GRUPO2'] = df['GRUPO2'].apply(lambda x: x.strip())
    df['RESPONSABLEINGRESO'] = df['RESPONSABLEINGRESO'].fillna('No Especificado')
    df['RESPONSABLEINGRESO'] = df['RESPONSABLEINGRESO'].apply(lambda x: x.strip())
    df['RESPONSABLESALIDA'] = df['RESPONSABLESALIDA'].fillna('No Especificado')
    df['RESPONSABLESALIDA'] = df['RESPONSABLESALIDA'].apply(lambda x: x.strip())
    df['ULTFECHAINGRESO'] = pd.to_datetime(df['ULTFECHAINGRESO'].str[:-14], format="%Y-%m-%d")
    df['ULTFECHASALIDA'] = pd.to_datetime(df['ULTFECHASALIDA'].str[:-14], format="%Y-%m-%d")
    df['Duracion_Inventario'] = df['ULTFECHASALIDA']-df['ULTFECHAINGRESO']
    df['Duracion_Inventario'] = (df['Duracion_Inventario'].dt.days)
    df= df[df["ULTFECHAINGRESO"].notna()]
    df['Estado Inventario'] = df['ULTFECHASALIDA'].astype('string')
    df['Estado Inventario'] = df['Estado Inventario'].replace([np.nan],[''])
    df['Estado Inventario'] = df.apply(lambda x: new_col_salidas(x['Estado Inventario']),axis=1)
    df = df.drop(['codmodelo','modelo'], axis=1)
    dff = df.rename(columns = columns_nsp_stockalmval)
    return dff

def transform_saldos_alm(df = None):
    df['COD_PRODUCTO'] = df['COD_PRODUCTO'].str.strip()
    df.loc[df.MARCA =='','MARCA']='NO ESPECIFICADO'
    df = df.rename(columns = columns_nsp_saldosalmacen)
    return df

def transform_consumos_alm(df = None):
    df['IDPRODUCTO'] = df['IDPRODUCTO'].str.strip()
    df.loc[df.LLEVADOPOR =='','LLEVADOPOR']='NO ESPECIFICADO'
    df = df.rename(columns = columns_nsp_consumosalmacen)
    return df