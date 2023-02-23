import pandas as pd
import numpy as np

def coordenadas_paises():
        df_coordenadas_all=pd.read_csv('https://raw.githubusercontent.com/Enriquezm97/file/main/COORDENADAS')
        df_coordenadas_all['etiqueta']=df_coordenadas_all['etiqueta'].str.upper()
        df_coordenadas_all.loc[df_coordenadas_all.etiqueta == 'LOS ESTADOS UNIDOS DE AMÉRICA','etiqueta'] ='ESTADOS UNIDOS'
        df_coordenadas_all.loc[df_coordenadas_all.etiqueta == 'LA REPÚBLICA DE COREA','etiqueta'] ='COREA'
        return df_coordenadas_all

def cleanVentas(df_ventas_detalle):
    df_ventas_detalle.loc[df_ventas_detalle.CULTIVO =='','CULTIVO']='NO DEFINIDO'
    df_ventas_detalle.loc[df_ventas_detalle.VARIEDAD =='','VARIEDAD']='SIN VARIEDAD'
    df_ventas_detalle.loc[df_ventas_detalle.PAIS ==None,'PAIS']='PAIS NO DEFINIDO'
    df_ventas_detalle['PAIS']=df_ventas_detalle['PAIS'].fillna('NO ESPECIFICADO')
    df_ventas_detalle['FECHA'] =pd.to_datetime(df_ventas_detalle['FECHA'], format="%Y/%m/%d")
    df_ventas_detalle['DESCRIPCION']=df_ventas_detalle['DESCRIPCION'].apply(lambda x: x.strip())
    df_ventas_detalle['RAZON_SOCIAL']=df_ventas_detalle['RAZON_SOCIAL'].apply(lambda x: x.strip())
    #df_ventas_detalle['FECHA']=pd.to_datetime(df_ventas_detalle['FECHA'], format='%Y-%m-%d %H:%M:%S')
    #df_ventas_detalle['FECHA']=pd.to_datetime(df_ventas_detalle['FECHA'], format='%Y-%m-%d')
    #df_ventas_detalle['FECHA']=df_ventas_detalle['FECHA'].dt.strftime('%Y-%m-%d')
    
    df_ventas_detalle['DAY'] = df_ventas_detalle['FECHA'].dt.day
    df_ventas_detalle['MONTH'] = df_ventas_detalle['FECHA'].dt.month
    df_ventas_detalle['YEAR'] = df_ventas_detalle['FECHA'].dt.year

    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MONTH']

    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(1,'Enero')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(2,'Febrero')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(3,'Marzo')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(4,'Abril')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(5,'Mayo')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(6,'Junio')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(7,'Julio')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(8,'Agosto')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(9,'Setiembre')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(10,'Octubre')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(11,'Noviembre')
    df_ventas_detalle['MES_TEXT']=df_ventas_detalle['MES_TEXT'].replace(12,'Diciembre')

    df_ventas_detalle['SEMANA']=df_ventas_detalle['FECHA'].dt.isocalendar().week 
    df_ventas_detalle['SEMANA']=df_ventas_detalle['SEMANA'].astype("string")

    df_ventas_detalle['TRIM']=df_ventas_detalle['FECHA'].dt.quarter
    #df_ventas_detalle['DESCRIPCION']=df_ventas_detalle['DESCRIPCION'].apply(lambda x: x.split('-')[-1])
    for years in df_ventas_detalle['YEAR'].unique():
        
                df_ventas_detalle['TRIM'].loc[df_ventas_detalle.YEAR==years]=df_ventas_detalle['FECHA'].dt.quarter
                df_ventas_detalle['TRIM'].loc[df_ventas_detalle.YEAR==years]=df_ventas_detalle['TRIM'].replace(1,str(years)+' '+'Trim 1')
                df_ventas_detalle['TRIM'].loc[df_ventas_detalle.YEAR==years]=df_ventas_detalle['TRIM'].replace(2,str(years)+' '+'Trim 2')
                df_ventas_detalle['TRIM'].loc[df_ventas_detalle.YEAR==years]=df_ventas_detalle['TRIM'].replace(3,str(years)+' '+'Trim 3')
                df_ventas_detalle['TRIM'].loc[df_ventas_detalle.YEAR==years]=df_ventas_detalle['TRIM'].replace(4,str(years)+' '+'Trim 4')

    df_ventas_detalle['PAIS']=df_ventas_detalle['PAIS'].str.rstrip()
    df_ventas_detalle.loc[df_ventas_detalle.PAIS == 'COREA, REPÚBLICA DE','PAIS'] ='COREA'
    df_ventas_detalle.loc[df_ventas_detalle.PAIS == 'EL BRASIL','PAIS'] ='BRASIL'

    #df_ventas_detalle.loc[df_ventas_detalle.RAZON_SOCIAL == 'SERVICIOS Y TRANSPORTES FRANCHESS SOCIEDAD COMERCIAL DE RESPONSABILIDAD LIMITADA','RAZON_SOCIAL'] ='SERVICIOS Y TRANSPORTES FRANCHESS SOCIEDAD'
    #df_ventas_detalle.loc[df_ventas_detalle.RAZON_SOCIAL == 'FRUTOS TROPICALES PERU EXPORT SOCIEDAD ANONIMA CERRADA','RAZON_SOCIAL'] ='FRUTOS TROPICALES PERU EXPORT'
            #FRUTOS TROPICALES PERU EXPORT SOCIEDAD ANONIMA CERRADA
    df_coordenadas_all=coordenadas_paises()
    #df_ventas_detalle.loc[df_ventas_detalle.RAZON_SOCIAL == 'CORPORACION MEDIOAMBIENTAL AMPCO PERU SOCIEDAD ANONIMA CERRADA - CM AMPCO PERU S.A.C.','RAZON_SOCIAL'] ='CORPORACION MEDIOAMBIENTAL AMPCO PERU'
    df_ventas_detalle=df_ventas_detalle.merge(df_coordenadas_all,how='left',left_on='PAIS',right_on='etiqueta')
    return df_ventas_detalle

def changeVentasCol(df_ventas_detalle):
        
        df_ventas_detalle_ejes=df_ventas_detalle.rename(columns={
                                                                'SUCURSAL':'Sucursal',
                                                                'RAZON_SOCIAL':'Cliente',
                                                                'TIPOMOVIMIENTO':'Tipo de Movimiento',
                                                                'TIPOVENTA':'Tipo de Venta',
                                                                'PAIS':'Pais',
                                                                'CULTIVO':'Cultivo',
                                                                'VARIEDAD':'Variedad',
                                                                'FORMATO':'Formato',
                                                                'YEAR':'Año',
                                                                'TRIM':'Trimestre',
                                                                'MES_TEXT':'Mes',
                                                                'SEMANA':'Semana',
                                                                'IMPORTEMOF':'Importe en Soles',
                                                                'IMPORTEMEX':'Importe en Dolares',
                                                                'PESONETO_PRODUCTO':'Peso',
                                                                'SEMANA':"Semana",
                                                                'DESCRIPCION':'Producto',
                                                                'GRUPO':'Grupo de Venta'

                                                        })
        return df_ventas_detalle_ejes

def cleanContenedores(df_control_expo):
    if df_control_expo.empty: 
        df_control_expo= pd.DataFrame()
    else:
        df_control_expo['FECHA_FACTEX'] =pd.to_datetime(df_control_expo['FECHA_FACTEX'], format="%Y/%m/%d")
        df_control_expo['DAY'] = df_control_expo['FECHA_FACTEX'].dt.day
        df_control_expo['MONTH'] = df_control_expo['FECHA_FACTEX'].dt.month
        df_control_expo['YEAR'] = df_control_expo['FECHA_FACTEX'].dt.year
    return df_control_expo