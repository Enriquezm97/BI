import pandas as pd
import numpy as np
from ..estructura_data import columns_drop_nsp_rpt_ventas_detallado,columns_nsp_rpt_ventas_detallado
from ..helpers import	*

def clean_comercial_detallado(dataframe = pd.DataFrame()):
    dataframe = dataframe.drop(columns_drop_nsp_rpt_ventas_detallado, axis=1)
    dataframe = dataframe.rename(columns = columns_nsp_rpt_ventas_detallado)
    dataframe['Sucursal'] = dataframe['Sucursal'].str[4:]
    dataframe['Vendedor'] = dataframe['Vendedor'].str[4:]
    dataframe['Tipo de Movimiento'] = dataframe['Tipo de Movimiento'].str[5:]
    dataframe['Tipo de Venta'] = dataframe['Tipo de Venta'].str[4:]
    dataframe['Tipo de Condicion'] = dataframe['Tipo de Condicion'].str[4:]
    dataframe['Grupo Producto'] = dataframe['Grupo Producto'].str[5:]
    dataframe['Subgrupo Producto'] = dataframe['Subgrupo Producto'].str[4:]
    dataframe['Grupo Cliente'] = dataframe['Grupo Cliente'].str[3:]
    dataframe['Fecha'] = pd.to_datetime(dataframe['Fecha'].str[:-14], format="%Y-%m-%d")
    dataframe['Sucursal'] = dataframe['Sucursal'].fillna('NO ESPECIFICADO')
    dataframe['Vendedor'] = dataframe['Vendedor'].fillna('NO ESPECIFICADO')
    dataframe['Tipo de Movimiento'] = dataframe['Tipo de Movimiento'].fillna('NO ESPECIFICADO')
    dataframe['Tipo de Venta'] = dataframe['Tipo de Venta'].fillna('NO ESPECIFICADO')
    dataframe['Tipo de Condicion'] = dataframe['Tipo de Condicion'].fillna('NO ESPECIFICADO')
    dataframe['Grupo Producto'] = dataframe['Grupo Producto'].fillna('NO ESPECIFICADO')
    dataframe['Subgrupo Producto'] = dataframe['Subgrupo Producto'].fillna('NO ESPECIFICADO')
    dataframe['Producto'] = dataframe['Producto'].apply(lambda x: x.strip())
    dataframe['Cliente'] = dataframe['Cliente'].apply(lambda x: x.strip())
    dataframe['Grupo Producto'] = dataframe['Grupo Producto'].apply(lambda x: x.strip())
    dataframe['Pais'] = dataframe['Pais'].str.rstrip()
    dataframe['Dia'] = dataframe['Fecha'].dt.day
    dataframe['Mes Num'] = dataframe['Fecha'].dt.month
    dataframe['Mes']=dataframe['Mes Num']
    dataframe['Mes']=dataframe['Mes'].replace(1,'Enero')
    dataframe['Mes']=dataframe['Mes'].replace(2,'Febrero')
    dataframe['Mes']=dataframe['Mes'].replace(3,'Marzo')
    dataframe['Mes']=dataframe['Mes'].replace(4,'Abril')
    dataframe['Mes']=dataframe['Mes'].replace(5,'Mayo')
    dataframe['Mes']=dataframe['Mes'].replace(6,'Junio')
    dataframe['Mes']=dataframe['Mes'].replace(7,'Julio')
    dataframe['Mes']=dataframe['Mes'].replace(8,'Agosto')
    dataframe['Mes']=dataframe['Mes'].replace(9,'Setiembre')
    dataframe['Mes']=dataframe['Mes'].replace(10,'Octubre')
    dataframe['Mes']=dataframe['Mes'].replace(11,'Noviembre')
    dataframe['Mes']=dataframe['Mes'].replace(12,'Diciembre')
    dataframe['Año'] =dataframe['Fecha'].dt.year
    dataframe['Año'] =dataframe['Fecha'].dt.year
    dataframe['Semana_'] = dataframe['Fecha'].dt.isocalendar().week.astype(int)
    dataframe['Semana'] = dataframe.apply(lambda x: semana_text(x['Año'], x['Semana_']),axis=1)
    dataframe['Trimestre_'] =dataframe['Fecha'].dt.quarter
    dataframe['Trimestre'] = dataframe.apply(lambda x: trimestre_text(x['Año'], x['Trimestre_']),axis=1)
    dataframe['Pais'] = dataframe['Pais'].replace([np.nan],['NO ESPECIFICADO'])
    dataframe['Cultivo'] = dataframe['Cultivo'].replace([''],['NO ESPECIFICADO'])
    dataframe['Variedad'] = dataframe['Variedad'].replace([''],['NO ESPECIFICADO'])
    return dataframe