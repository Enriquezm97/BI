import pandas as pd
import numpy as np
import datetime

def cleanVariablesAgricolas(df_consumidores,df_variedad,df_cultivos,df_fertilizacion):
    
    df_variedad['VARIEDAD']=df_variedad['VARIEDAD'].str.capitalize()
    df_fertilizacion['DSCVARIABLE']=df_fertilizacion['DSCVARIABLE'].str.capitalize()
    df_fertilizacion['TIPO']=df_fertilizacion['TIPO'].str.capitalize()
    df_cultivos['CULTIVO']=df_cultivos['CULTIVO'].str.capitalize()
    df_consumidores['FECHAINICIO_CAMPAÑA'] =pd.to_datetime(df_consumidores['FECHAINICIO_CAMPAÑA'], format="%Y/%m/%d")
    df_consumidores['FECHAFIN_CAMPAÑA'] =pd.to_datetime(df_consumidores['FECHAFIN_CAMPAÑA'], format="%Y/%m/%d")
    df_consumidores['AÑO_CAMPAÑA']=df_consumidores['AÑO_CAMPAÑA'].astype(object)
    df_fertilizacion['FECHA'] =pd.to_datetime(df_fertilizacion['FECHA'], format="%Y/%m/%d")
    df_fertilizacion['FECHA']=df_fertilizacion['FECHA'].apply(lambda a: pd.to_datetime(a).date()) 
    df_consumidores['FECHAINICIO_CAMPAÑA'] =df_consumidores['FECHAINICIO_CAMPAÑA'].apply(lambda a: pd.to_datetime(a).date())
    df_consumidores['FECHAFIN_CAMPAÑA'] =df_consumidores['FECHAFIN_CAMPAÑA'].apply(lambda a: pd.to_datetime(a).date())
    df_fertilizacion['SEMANA']=pd.DatetimeIndex(df_fertilizacion['FECHA']).week 
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
    return df_campaña_ccc