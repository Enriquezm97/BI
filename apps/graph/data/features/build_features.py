import requests
import pandas as pd


def getApi(api,token):
    response = requests.get(api, headers={'Authorization': "Bearer {}".format(token)})
    objeto=response.json()
    list_objetos=objeto['objeto']
    return list_objetos

class DataFinanzas:

    def createTrimestre(df):
        df['importe_mof']=df['mov_cargo_mof']-df['mov_abono_mof']
        df['importe_mex']=df['mov_cargo_mex']-df['mov_abono_mex']
        df['grupo1']=df['grupo1'].str.strip()
        #PARTIDAS PASIVO CORRIENTE Y ACTIVO NO CORRIENTE MODIFICADOS
        df['grupo2'].loc[df.grupo1=='ACTIVO']=df['grupo2'].replace('PASIVO CORRIENTE','ACTIVO CORRIENTE')
        df['grupo2'].loc[df.grupo1=='PASIVO']=df['grupo2'].replace('ACTIVO NO CORRIENTE','PASIVO NO CORRIENTE')
        #
    
        df['al_periodo']=df['al_periodo'].astype("str")
        df['Año']=df['al_periodo'].str[:4]
        df['month']=df['al_periodo'].str[4:]
        df['TRIM']=df['trimestre']
        for anio in df['Año'].unique():
                    df['TRIM'].loc[df.Año==anio]=df['trimestre']
                    df['TRIM'].loc[df.Año==anio]=df['TRIM'].replace(1,str(anio)+' '+'Trim 1')
                    df['TRIM'].loc[df.Año==anio]=df['TRIM'].replace(2,str(anio)+' '+'Trim 2')
                    df['TRIM'].loc[df.Año==anio]=df['TRIM'].replace(3,str(anio)+' '+'Trim 3')
                    df['TRIM'].loc[df.Año==anio]=df['TRIM'].replace(4,str(anio)+' '+'Trim 4')
        df['Mes']=df['month']
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
        df['trimestre']=df['trimestre'].replace(1,'Trim 1')
        df['trimestre']=df['trimestre'].replace(2,'Trim 2')
        df['trimestre']=df['trimestre'].replace(3,'Trim 3')
        df['trimestre']=df['trimestre'].replace(4,'Trim 4')

        return df

    def separateItems(df_bcomprobacion,ejex='Periodo Mensual',tipo_moneda='dolares',tipo_importe=['saldo_cargo_mof','saldo_cargo_mex']):
            if ejex =='Periodo Trimestral':
                group=['Año','trimestre','TRIM']
                eje='TRIM'
            elif ejex =='Periodo Mensual':
                group=['Año','Mes','month','al_periodo']
                eje='al_periodo'
            df_niv1_trim=df_bcomprobacion.groupby(group+['grupo1'])[[tipo_importe[0],tipo_importe[1]]].sum().reset_index()
            df_niv2_trim=df_bcomprobacion.groupby(group+['grupo2'])[[tipo_importe[0],tipo_importe[1]]].sum().reset_index()
            df_niv3_trim=df_bcomprobacion.groupby(group+['grupo3'])[[tipo_importe[0],tipo_importe[1]]].sum().reset_index()
            if tipo_moneda == 'soles':
                tipo=tipo_importe[0]
            elif tipo_moneda == 'dolares':
                tipo=tipo_importe[1]
            df_niv1_pivot_trim=pd.pivot_table(df_niv1_trim,index=group,columns='grupo1',values=tipo)
            df_niv1_pivot_trim=df_niv1_pivot_trim.reset_index()
            df_niv2_pivot_trim=pd.pivot_table(df_niv2_trim,index=group,columns='grupo2',values=tipo)
            df_niv2_pivot_trim=df_niv2_pivot_trim.reset_index()
            df_niv3_pivot_trim=pd.pivot_table(df_niv3_trim,index=group,columns='grupo3',values=tipo)
            df_niv3_pivot_trim=df_niv3_pivot_trim.reset_index()
            df_ratios_first_trim=df_niv1_pivot_trim.merge(df_niv2_pivot_trim,how='inner',left_on=eje,right_on=eje)
            df_ratios_first_trim=df_ratios_first_trim.merge(df_niv3_pivot_trim,how='inner',left_on=eje,right_on=eje)
            df_ratios_first_trim=df_ratios_first_trim.drop(['PATRIMONIO_y'], axis=1)
            #agregando columnas del grupo funcion
            df_pivot_funcion=pd.pivot_table(df_bcomprobacion,index=group,columns='grupo_funcion',values=tipo)
            df_pivot_funcion=df_pivot_funcion.reset_index()
            df_pivot_funcion=df_pivot_funcion.fillna(0)
            for partida_funcion in df_pivot_funcion.columns[4:]:
                df_ratios_first_trim[partida_funcion]=df_pivot_funcion[partida_funcion]
            
            return df_ratios_first_trim

    ###PARA EL ESTADO DE SITUACION FINANCIERA
    def dataframeBalanceAPP(df_bc,partida_grupo_1='ACTIVO',importe='saldo_cargo_mex',partida_grupo_2='ACTIVO CORRIENTE',label_total=''):
        if importe =='saldo_cargo_mex':
            simbolo='$'
        elif importe == 'saldo_cargo_mof':
            simbolo='S/'
        
        total_grupo1=df_bc[df_bc['grupo1']==partida_grupo_1][importe].sum()
        df=df_bc[df_bc['grupo2']==partida_grupo_2].groupby(['grupo3']).sum().reset_index()
        df.loc['Total',:]= df.sum(numeric_only=True, axis=0)
        df=df.fillna(label_total) 
        df['porcentaje']=df[importe]/total_grupo1
        df['porcentaje']=df['porcentaje'].apply('{:.1%}'.format)
        df[importe] = df.apply(lambda x: "{:,.2f}".format(x[importe]), axis=1)#.round(0)
        
        df=df.rename(columns={'grupo3':partida_grupo_2,importe:simbolo,'porcentaje':'%'})
        #df[simbolo]=df[simbolo].round(decimals = 3)
        return df

"""
df_pronostico=pd.read_excel('pronostico_partidas_dolares.xlsx')
df_pronostico=df_pronostico.rename(columns={'Unnamed: 0':'al_periodo'})
df_pronostico=df_pronostico.round(2)
def trash(df,list_partida=[],periodo_list=['2023-11-01','2022-12-01']):
    #RECORDAR QUE EL FORMATO DEL PERIODO VA A VARIAR DEPENDDIENDO DEL OTRO DATA FRAME QUE SE VA A USAR
        df_invertir=pd.DataFrame()
        for periodo in periodo_list:
            name_periodo=f'predict_{periodo}'
            df_pivot_balance=df[df['al_periodo']==periodo]
            
            df_invertir['grupo']=list_partida
            df_invertir[name_periodo]=0
            df_invertir[name_periodo]=df_invertir[name_periodo].astype('float')
            for partida in list_partida:
                df_invertir[name_periodo].loc[df_invertir.grupo==partida]=float(df_pivot_balance[partida])
        return df_invertir

def dataframeTestPronostico(df_bc,partida_grupo_1='ACTIVO',importe='saldo_cargo_mex',partida_grupo_2='ACTIVO CORRIENTE',label_total=''):
    if importe =='saldo_cargo_mex':
         simbolo='$'
    elif importe == 'saldo_cargo_mof':
         simbolo='S/'
    
    total_grupo1=df_bc[df_bc['grupo1']==partida_grupo_1][importe].sum()
    df=df_bc[df_bc['grupo2']==partida_grupo_2].groupby(['grupo3']).sum().reset_index()
    #df.loc['Total',:]= df.sum(numeric_only=True, axis=0)
    #df=df.fillna(label_total) 
    #df['porcentaje']=df[importe]/total_grupo1
    #df['porcentaje']=df['porcentaje'].apply('{:.1%}'.format)
    #df[importe] = df.apply(lambda x: "{:,.2f}".format(x[importe]), axis=1)#.round(0)
    
    df=df.rename(columns={'grupo3':partida_grupo_2,importe:simbolo,'porcentaje':'%'})

    
    periodo_list=['2022-11-01','2022-12-01']

    
        
    df_table_partida_pronosticos=trash(df_pronostico,list_partida=df[partida_grupo_2].unique(),periodo_list=['2023-11-01','2022-12-01'])

        #df_cultivo_variedad = df_cultivos.merge(df_variedad, how='inner', left_on=["CODCULTIVO"], right_on=["CODCULTIVO"])
    df_last=df.merge(df_table_partida_pronosticos, how='inner', left_on=[partida_grupo_2], right_on=['grupo'])

    df_last=df_last.drop(['grupo'], axis=1)
    df_last.loc['Total',:]= df_last.sum(numeric_only=True, axis=0)
    df_last=df_last.fillna(label_total)
    for columna in df_last.columns[1:]:
        df_last[columna] = df_last.apply(lambda x: "{:,.2f}".format(x[columna]), axis=1)#.round(0)

    #df[simbolo]=df[simbolo].round(decimals = 3)
    return df_last

"""
