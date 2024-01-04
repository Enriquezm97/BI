import pandas as pd
import numpy as np

def semana_text(year, week):
        if len(str(week)) == 1:
            semana = '0'+ str(week)
        else:
            semana = str(week)
        return str(year)+'-'+'Sem'+''+str(semana)
                                          
def trimestre_text(year,trimestre):
        return str(year)+' '+'Trim '+str(trimestre)  

def etl_comercial(dataframe = pd.DataFrame()):

    columns_drop = [
        'DOCUMENTO','IDCLIEPROV','MONEDA','TCAMBIO','PROYECTO','TCMONEDA','IDPRODUCTO','IDMEDIDA','VENTANA','IDCOBRARPAGARDOC', 
        'IDSERIE', 'UNDEX', 'EQUIVALENCIA','idtipocontenedor', 'idtipoprecio', 'DSC_PUERTODESTINO', 'DUA', 'glosa','IDCANAL',
        'CANAL', 'Lotep', 'ocompra','nro_contenedor','idconsumidor', 'IDCAMPANA', 'CONTADO', 'vencimiento'
    ]
    dataframe = dataframe.drop(columns_drop, axis=1)
    dataframe = dataframe.rename(columns = {
                                'SUCURSAL': 'Sucursal',
                                'FECHA': 'Fecha',
                                'RAZON_SOCIAL': 'Cliente',
                                'VENDEDOR':'Vendedor',
                                'TIPOMOVIMIENTO':'Tipo de Movimiento',
                                'TIPOVENTA': 'Tipo de Venta',
                                'CONDICION': 'Tipo de Condicion',
                                'DESCRIPCION': 'Producto',
                                'GRUPO': 'Grupo Producto',
                                'SUBGRUPO': 'Subgrupo Producto',
                                'MARCA': 'Marca Producto',
                                'CANTIDAD': 'Cantidad',
                                'PRECIOMOF':'P.U Soles',
                                'PRECIOMEX':'P.U Dolares',
                                'VVENTAMOF': 'Subtotal Soles',
                                'VVENTAMEX': 'Subtotal Dolares',
                                'IMPORTEMOF': 'Importe Soles',
                                'IMPORTEMEX': 'Importe Dolares',
                                'NroEmbarque': 'Número de Embarque',
                                'FechaEmbarque': 'Fecha de Embarque',
                                'PESONETO_PRODUCTO': 'Peso Producto', 
                                'DEPARTAMENTO': 'Departamento',
                                'PROVINCIA': 'Provincia', 
                                'DISTRITO': 'Distrito', 
                                'PAIS': 'Pais',
                                'CULTIVO': 'Cultivo', 
                                'VARIEDAD': 'Variedad', 
                                'FORMATO': 'Formato', 
                                'GRUPOCLIENTE': 'Grupo Cliente'
                                }
    )
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
    
    
    
    
    #dataframe['Mes'] = pd.to_datetime(dataframe['Fecha'], format='%Y.%m.%d', errors="coerce").dt.month_name(locale='es_ES.utf8')
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

def cleanVariablesAgricolas(df_consumidores,df_variedad,df_cultivos,df_fertilizacion):
    #print(df_consumidores['FECHAINICIO_CAMPAÑA'].unique())
    df_variedad['VARIEDAD']=df_variedad['VARIEDAD'].str.capitalize()
    df_fertilizacion['DSCVARIABLE']=df_fertilizacion['DSCVARIABLE'].str.capitalize()
    df_fertilizacion['TIPO']=df_fertilizacion['TIPO'].str.capitalize()
    df_cultivos['CULTIVO']=df_cultivos['CULTIVO'].str.capitalize()
    #df_consumidores['FECHAINICIO_CAMPAÑA'] =pd.to_datetime(df_consumidores['FECHAINICIO_CAMPAÑA'], format="%Y-%m-%d")
    #df_consumidores['FECHAFIN_CAMPAÑA'] =pd.to_datetime(df_consumidores['FECHAFIN_CAMPAÑA'], format="%Y-%m-%d")
    df_consumidores['AÑO_CAMPAÑA']=df_consumidores['AÑO_CAMPAÑA'].astype(object)
    
    df_fertilizacion['FECHA'] =pd.to_datetime(df_fertilizacion['FECHA'].str[:10], format="%Y-%m-%d")#, format="%Y-%m-%d"
  
    #df_fertilizacion['FECHA']=df_fertilizacion['FECHA'].apply(lambda a: pd.to_datetime(a).date()) 
    df_consumidores['FECHAINICIO_CAMPAÑA'] =df_consumidores['FECHAINICIO_CAMPAÑA'].apply(lambda a: pd.to_datetime(a).date())
    df_consumidores['FECHAFIN_CAMPAÑA'] =df_consumidores['FECHAFIN_CAMPAÑA'].apply(lambda a: pd.to_datetime(a).date())
    
    df_fertilizacion['SEMANA']=df_fertilizacion['FECHA'].dt.strftime("%U")
    df_fertilizacion['SEMANA']=df_fertilizacion['SEMANA'].astype(object)
   
            #JOINS DATA
    df_cultivo_variedad = df_cultivos.merge(df_variedad, how='inner', left_on=["CODCULTIVO"], right_on=["CODCULTIVO"])
    df_consumidor_cultivo_variedad = df_consumidores.merge(df_cultivo_variedad, how='inner', left_on=["CODCULTIVO","CODVARIEDAD"], right_on=["CODCULTIVO","CODVARIEDAD"])
    df_general=df_fertilizacion.merge(df_consumidor_cultivo_variedad, how='inner', left_on=["CODCONSUMIDOR","CODSIEMBRA","CODCAMPAÑA"], right_on=["CODCONSUMIDOR","CODSIEMBRA","CODCAMPAÑA"])
    #df_general=df_fertilizacion.merge(df_consumidor_cultivo_variedad, how='inner', left_on=["CODCONSUMIDOR"], right_on=["CODCONSUMIDOR"])
            #TABLE GENERAL
    
    #df_general=df_general.drop(['NCULTIVO', 'FECHAINICIO_CAMPAÑA', 'FECHAFIN_CAMPAÑA','NCULTIVO'], axis=1)
    df_general=df_general[df_general["CULTIVO"]!='COMPOST']
    df_general['DSCVARIABLE']=df_general['DSCVARIABLE'].str.strip()
    ## crear semana caracter
    df_general['AÑO_FECHA'] = pd.DatetimeIndex(df_general['FECHA']).year#df_general['FECHA'].datetime
    df_general['SEM']=df_general['SEMANA'].astype('string')
    df_general['SEM']=df_general['SEM'].replace('1','01')
    df_general['SEM']=df_general['SEM'].replace('2','02')
    df_general['SEM']=df_general['SEM'].replace('3','03')
    df_general['SEM']=df_general['SEM'].replace('4','04')
    df_general['SEM']=df_general['SEM'].replace('5','05')
    df_general['SEM']=df_general['SEM'].replace('6','06')
    df_general['SEM']=df_general['SEM'].replace('7','07')
    df_general['SEM']=df_general['SEM'].replace('8','08')
    df_general['SEM']=df_general['SEM'].replace('9','09')
    df_general['week']=df_general['SEM']
    df_general['AÑO_CULTIVO']=df_general['CULTIVO']

    semanas=sorted(df_general['SEM'].unique())
    for anio in df_general['AÑO_FECHA'].unique():
        for i in semanas:
            df_general['week'].loc[df_general['AÑO_FECHA']==anio]=df_general['week'].replace(i,str(anio)+'-'+'Sem'+''+str(i))

    cultivo=sorted(df_general['CULTIVO'].unique())
    for anio in df_general['AÑO_CAMPAÑA'].unique():
        for i in cultivo:
            df_general['AÑO_CULTIVO'].loc[df_general['AÑO_CAMPAÑA']==anio]=df_general['AÑO_CULTIVO'].replace(i,str(anio)+'-'+str(i))    
    print(df_general.columns)    
    return df_general

def variablesAgricolasPivot(df_general):
    df_general_pivot=df_general.pivot_table(index=('CULTIVO','VARIEDAD','CODCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','FECHA','AÑO_CAMPAÑA','AREA_CAMPAÑA','AREA_PLANIFICADA','week','AÑO_FECHA','SEMANA','AÑO_CULTIVO'),values=('CANTIDAD'),columns=('DSCVARIABLE'))
    df_general_pivot.reset_index()
    df_general_pivot=pd.DataFrame(df_general_pivot.to_records())
    df_general_pivot=df_general_pivot.fillna(0)
    df_general_pivot['AÑO_CAMPAÑA']=df_general_pivot['AÑO_CAMPAÑA'].astype(object)
    return df_general_pivot


def costosAgricolas(df_costos_campana,df_consumidores,df_cultivos,df_variedad):
    if df_costos_campana.empty: 
        df_campaña_ccc= pd.DataFrame()
    else:
        
        df_costos_campana['TIPO']=df_costos_campana['TIPO'].str.capitalize()
        df_campaña_cc=df_costos_campana.merge(df_consumidores, how='inner', left_on=["IDCONSUMIDOR","CODSIEMBRA","CODCAMPAÑA"], right_on=["CODCONSUMIDOR","CODSIEMBRA","CODCAMPAÑA"])
        df_campaña_ccc=df_campaña_cc.merge(df_cultivos, how='inner', left_on=["CODCULTIVO"], right_on=["CODCULTIVO"])
        df_campaña_ccc=df_campaña_ccc.merge(df_variedad, how='inner', left_on=["CODCULTIVO","CODVARIEDAD"], right_on=["CODCULTIVO","CODVARIEDAD"])
        df_campaña_ccc['FECHAINICIO_CAMPAÑA']=df_campaña_ccc['FECHAINICIO_CAMPAÑA'].apply(lambda a: pd.to_datetime(a).date()) 
        df_campaña_ccc['FECHAFIN_CAMPAÑA']=df_campaña_ccc['FECHAFIN_CAMPAÑA'].apply(lambda a: pd.to_datetime(a).date()) 
        df_campaña_ccc.sort_values('FECHAINICIO_CAMPAÑA',ascending=True)
        df_campaña_ccc=df_campaña_ccc[df_campaña_ccc["CULTIVO"]!='Compost']
        conditionlist = [(df_campaña_ccc['NCONSUMIDOR']=='            '),
                                (df_campaña_ccc['NCONSUMIDOR']!='            ')]
        choicelist_1 = [df_campaña_ccc['CODCONSUMIDOR'],df_campaña_ccc['NCONSUMIDOR']]
        df_campaña_ccc['NCONSUMIDOR'] = np.select(conditionlist, choicelist_1,default='Not Specified')
        df_campaña_ccc['CULTIVO']=df_campaña_ccc['CULTIVO'].str.capitalize()
    return df_campaña_ccc

def etl_bc(df):
        df['al_periodo'] = df['al_periodo'].fillna('')
        df = df[df['al_periodo'] != '']
        df['Periodo']=df['al_periodo']+'01'
        df['Periodo']=pd.to_datetime(df['Periodo'])
        df['importe_mof']=df['mov_cargo_mof']-df['mov_abono_mof']
        df['importe_mex']=df['mov_cargo_mex']-df['mov_abono_mex']
        df['grupo1']=df['grupo1'].str.strip()
        df['grupo2'].loc[df.grupo1=='ACTIVO']=df['grupo2'].replace('PASIVO CORRIENTE','ACTIVO CORRIENTE')
        df['grupo2'].loc[df.grupo1=='PASIVO']=df['grupo2'].replace('ACTIVO NO CORRIENTE','PASIVO NO CORRIENTE')
        #
    
        df['al_periodo']=df['al_periodo'].astype("str")
        df['Año']=df['al_periodo'].str[:4]
        df['Mes Num']=df['al_periodo'].str[4:]
        df['Trimestre']=df['trimestre']
        for anio in df['Año'].unique():
            df['Trimestre'].loc[df.Año==anio]=df['trimestre']
            df['Trimestre'].loc[df.Año==anio]=df['Trimestre'].replace(1,str(anio)+' '+'Trim 1')
            df['Trimestre'].loc[df.Año==anio]=df['Trimestre'].replace(2,str(anio)+' '+'Trim 2')
            df['Trimestre'].loc[df.Año==anio]=df['Trimestre'].replace(3,str(anio)+' '+'Trim 3')
            df['Trimestre'].loc[df.Año==anio]=df['Trimestre'].replace(4,str(anio)+' '+'Trim 4')
        df['Mes']=df['Mes Num']
        df['Mes']=df['Mes'].replace('01','Enero')
        df['Mes']=df['Mes'].replace('02','Febrero')
        df['Mes']=df['Mes'].replace('03','Marzo')
        df['Mes']=df['Mes'].replace('04','Abril')
        df['Mes']=df['Mes'].replace('05','Mayo')
        df['Mes']=df['Mes'].replace('06','Junio')
        df['Mes']=df['Mes'].replace('07','Julio')
        df['Mes']=df['Mes'].replace('08','Agosto')
        df['Mes']=df['Mes'].replace('09','Setiembre')
        df['Mes']=df['Mes'].replace('10','Octubre')
        df['Mes']=df['Mes'].replace('11','Noviembre')
        df['Mes']=df['Mes'].replace('12','Diciembre')
        df['trimestre']=df['trimestre'].astype('int')
        #df['trimestre']=df['trimestre'].replace(1,'Trim 1')
        #df['trimestre']=df['trimestre'].replace(2,'Trim 2')
        #df['trimestre']=df['trimestre'].replace(3,'Trim 3')
        #df['trimestre']=df['trimestre'].replace(4,'Trim 4')

        return df

def pivot_data_finanzas(df = pd.DataFrame() ,etapa = 'Trimestre', moneda = 'soles'):
    group = ['Año','trimestre','Trimestre'] if etapa =='Trimestre' else ['Año','Mes','Mes Num','Periodo']
    eje ='Trimestre'  if etapa =='Trimestre' else 'Periodo'
    tipo_moneda = 'saldo_cargo_mof' if moneda == 'soles' else 'saldo_cargo_mex'
    grupo1_df =df.groupby(group+['grupo1'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
    grupo1_df_pivot=pd.pivot_table(grupo1_df,index = group, columns = 'grupo1',values = tipo_moneda).reset_index()
    
    grupo2_df =df.groupby(group+['grupo2'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
    grupo2_df_pivot = pd.pivot_table(grupo2_df,index = group,columns = 'grupo2', values = tipo_moneda).reset_index()
    
    grupo3_df =df.groupby(group+['grupo3'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
    grupo3_df_pivot = pd.pivot_table(grupo3_df,index = group,columns = 'grupo3', values = tipo_moneda).reset_index()
    
    grupo_funcion_df =df.groupby(group+['grupo_funcion'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
    grupo_funcion_df_pivot = pd.pivot_table(grupo_funcion_df,index=group,columns='grupo_funcion',values = tipo_moneda).reset_index()
    
    grupo_naturaleza_df = df.groupby(group+['grupo_naturaleza'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
    grupo_naturaleza_df_pivot = pd.pivot_table(grupo_naturaleza_df, index = group,columns='grupo_naturaleza',values = tipo_moneda).reset_index()
    #df_niv1_pivot_trim.merge(df_niv2_pivot_trim,how='inner',left_on=eje,right_on=eje)
    
    merge_1 = grupo1_df_pivot.merge(grupo2_df_pivot,how ='inner',on = group)
    merge_2 = merge_1.merge(grupo3_df_pivot,how ='inner',on = group)
    merge_3 = merge_2.merge(grupo_funcion_df_pivot,how ='inner',on = group)
    merge_4 = merge_3.merge(grupo_naturaleza_df_pivot,how ='left',on = group)
    #return pd.merge(right = [grupo1_df_pivot, grupo2_df_pivot, grupo3_df_pivot,grupo_funcion_df_pivot,grupo_naturaleza_df_pivot],how='inner',left_on = eje,right_on = eje )
    return merge_4.fillna(0)#.reset_index()

def mes_short(x):
    if x == 1:
        return 'Ene'
    elif x == 2:
        return 'Feb'
    elif x == 3:
        return 'Mar'
    elif x == 4:
        return 'Abr'
    elif x == 5:
        return 'May'
    elif x == 6:
        return 'Jun'
    elif x == 7:
        return 'Jul'
    elif x == 8:
        return 'Ago'
    elif x == 9:
        return 'Set'
    elif x == 10:
        return 'Oct'
    elif x == 11:
        return 'Nov'
    elif x == 12:
        return 'Dic'
    

        
def clean_inventarios(df = None):
    
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
    df = df.rename(columns = {
                     'dsc_producto':'Producto',
                     'dsc_grupo': 'Grupo Producto',
                     'dsc_subgrupo': 'Sub Grupo Producto',
                     'unid_medida': 'Unidad de medida',
                     'stock_unidades':'Stock en unidades',
                     'costo_unitario_mof':'Costo Unitario Soles',
                     'costo_unitario_mex':'Costo Unitario Dolares',
                     'stock_valorizado_mof':'Stock Valorizado Soles',
                     'stock_valorizado_mex':'Stock Valorizado Dolares',
                     'año':'Año',
                     'mes':'Mes_',
                     'venta_prom_unidades':'Venta prom 12 meses en UN',
                     'venta_prom_mof':'Venta prom 12 meses en monto Soles',
                     'venta_prom_mex':'Venta prom 12 meses en monto Dolares',
                     'costo_venta_prom_mof':'Costo de Venta prom 12 meses en monto Soles',
                     'costo_venta_prom_mex':'Costo de Venta prom 12 meses en monto Dolares',
                     'ABC_ventas':'ABC Ventas',
                     'ABC_stock':'ABC Stock',
                     'rango_antiguedad_stock':'Rango antigüedad del stock',
                     'rotacion':'Rotación',
                     'meses_stock': 'Meses de stock',
                     
          }
    )
    return df


def new_col_salidas(x):
    if x == '':
        return 'Sin Salida'
    else:
        return 'Tuvo Salida'
    
    
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
    dff = df.rename(columns = {
        'CODSUCURSAL': 'Código Sucursal', 
        'SUCURSAL'   : 'Sucursal',
        'CODALMACEN' : 'Código Almacén',
        'ALMACEN'    : 'Almacén',
        'codtipo'    : 'Código Tipo',
        'tipo'       : 'Tipo',
        'CODGRUPO'   : 'Código Grupo',
        'GRUPO'      : 'Grupo',
        'CODSUBGRUPO': 'Código Sub Grupo',
        'SUBGRUPO'   : 'Sub Grupo',
        'CODPRODUCTO': 'Código Producto',
        'PRODUCTO'   : 'Producto',
        'GRUPO2'     : 'Grupo 2',
        'RESPONSABLEINGRESO' : 'Responsable Ingreso',
        'RESPONSABLESALIDA'  : 'Responsable Salida',
        'MEDIDA'     : 'Unidad de Medida',
        'ESTADO'     : 'Estado',
        'STOCK'      : 'Stock',
        'IMPORTETOTALMOF' : 'Importe Soles',
        'IMPORTETOTALMEX' : 'Importe Dolares',
        'UBICACION'  : 'Ubicación',
        'ULTFECHAINGRESO' : 'Última Fecha Ingreso',
        'ULTFECHASALIDA'  : 'Última Fecha Salida',
        'MARCA'      : 'Marca',
        'TIPOMATERIAL': 'Tipo de Material',
        'desde'      : 'Desde',
        'hasta'      : 'Hasta'
    })
    return dff