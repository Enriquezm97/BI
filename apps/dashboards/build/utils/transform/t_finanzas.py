import pandas as pd
from ..helpers import	*

def clean_bcomprobacion(df =  None):
        df['al_periodo'] = df['al_periodo'].fillna('')
        df = df[df['al_periodo'] != '']
        df['Periodo']=df['al_periodo']+'01'
        df['Periodo']=pd.to_datetime(df['Periodo'])
        df['importe_mof']=df['mov_cargo_mof']-df['mov_abono_mof']
        df['importe_mex']=df['mov_cargo_mex']-df['mov_abono_mex']
        df['grupo1']=df['grupo1'].str.strip()
        df['grupo2'].loc[df.grupo1=='ACTIVO']=df['grupo2'].replace('PASIVO CORRIENTE','ACTIVO CORRIENTE')
        df['grupo2'].loc[df.grupo1=='PASIVO']=df['grupo2'].replace('ACTIVO NO CORRIENTE','PASIVO NO CORRIENTE')
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
        return df
    
def pivot_bcomprobacion(df = pd.DataFrame() ,etapa = 'Trimestre', moneda = 'soles'):
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
    merge_1 = grupo1_df_pivot.merge(grupo2_df_pivot,how ='inner',on = group)
    merge_2 = merge_1.merge(grupo3_df_pivot,how ='inner',on = group)
    merge_3 = merge_2.merge(grupo_funcion_df_pivot,how ='inner',on = group)
    merge_4 = merge_3.merge(grupo_naturaleza_df_pivot,how ='left',on = group)
    return merge_4.fillna(0)    


def clean_bg(df = None):
    df['periodo'] = df['periodo'].fillna('')
    df = df[df['periodo'] != '']
    df['titulo1']=df['titulo1'].str.strip()
    df['titulo2']=df['titulo2'].str.strip()
    df['titulo3']=df['titulo3'].str.strip()
    df['titulo4']=df['titulo4'].str.strip()
    df['Año']=df['periodo'].str[:4]
    df['Mes']=df['periodo'].str[4:]
    df['Mes_num']= df['Mes'].astype('int')
    df['Mes_'] = df.apply(lambda x: mes_short(x['Mes_num']),axis=1) 
    df['Trimestre'] = df.apply(lambda x: cal_trim(x['Mes_num']),axis=1)
    return df

    
