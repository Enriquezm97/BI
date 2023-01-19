import pandas as pd

#CREAR RATIOS ADICONALES
def createRatios(df_ratios):
    try:
        df_ratios['PATRIMONIO NETO']=df_ratios['ACTIVO    ']-df_ratios['PASIVO    ']
    except:
        df_ratios['PATRIMONIO NETO']=0
    try:
        df_ratios['ACTIVO CORRIENTE']=df_ratios['ACTIVO    ']-df_ratios['ACTIVO NO CORRIENTE']
    except:
        df_ratios['ACTIVO CORRIENTE']=0
    try:
        df_ratios['PASIVO NO CORRIENTE']=df_ratios['PASIVO CORRIENTE']-df_ratios['PASIVO    ']
    except:
        df_ratios['PASIVO NO CORRIENTE']=0
    try:
        df_ratios['INVENTARIOS']=df_ratios['Existencias (Neto)']+df_ratios['Activos Biologicos']#(['Parte Corriente de Activo Biológico'])
    except:
        df_ratios['INVENTARIOS']=0
    try:
        df_ratios['GASTO EN CAPITAL']=df_ratios['ACTIVO CORRIENTE']-df_ratios['PASIVO CORRIENTE']
    except:
        df_ratios['GASTO EN CAPITAL']=0
    try:
        df_ratios['ACTIVO FIJO']=df_ratios['Activo Fijo (neto)']
    except:
        df_ratios['ACTIVO FIJO']=0
    
    try:
        df_ratios['CASH']=df_ratios['Efectivo y Equivalentes de Efectivo']
    except:
        df_ratios['CASH']=0
    try:
        df_ratios['DEUDA TOTAL']=df_ratios['Sobregiros Bancarios']+df_ratios['Obligaciones Financieras']
    except:
        df_ratios['DEUDA TOTAL']=0
    
    try:
        df_ratios['ratio_liquidez'] = df_ratios['ACTIVO CORRIENTE']/df_ratios['PASIVO CORRIENTE']
    except:
        df_ratios['ratio_liquidez'] = 0
    try:
        df_ratios['ratio_rapido'] = (df_ratios['ACTIVO CORRIENTE']-df_ratios['INVENTARIOS'])/df_ratios['PASIVO CORRIENTE']
    except:
        df_ratios['ratio_rapido'] = 0
        
    try:
        df_ratios['ratio_cash'] = df_ratios['CASH']/df_ratios['PASIVO CORRIENTE']
    except:
        df_ratios['ratio_cash'] = 0
        
    try:
        df_ratios['deuda_activos']=df_ratios['DEUDA TOTAL']/df_ratios['ACTIVO    ']
    except:
        df_ratios['deuda_activos']=0
    try:
        df_ratios['deuda_patrimonio'] = df_ratios['DEUDA TOTAL']/df_ratios['PATRIMONIO_x']
    except:
        df_ratios['deuda_patrimonio'] = 0
    try:
        df_ratios['apalancamiento'] = df_ratios['ACTIVO    ']/df_ratios['PATRIMONIO NETO']
    except:
        df_ratios['apalancamiento']=0
    
    try:
         df_ratios['DEUDA_ESTR']= df_ratios['PASIVO    '] - df_ratios['ACTIVO CORRIENTE'] 
    except:
        df_ratios['DEUDA_ESTR']= 0
    
    try:
        df_ratios['CUENTAS POR COBRAR']=df_ratios['Cuentas Por Cobrar Diversas -  Relacionadas']+df_ratios['Cuentas por Cobrar Comerciales - Relacionadas Contenido']+df_ratios['Cuentas por Cobrar Comerciales - Terceros']+df_ratios['Cuentas por Cobrar Diversas -Terceros']+df_ratios['Cuentas por Cobrar al Personal a los Accionistas ( Socios) Directores y Gerentes']
    except:
        df_ratios['CUENTAS POR COBRAR']=0
    
    try:
        df_ratios['CUENTAS POR PAGAR']=df_ratios['Cuentas por Pagar Comerciales - Relacionadas']+df_ratios['Cuentas por Pagar Comerciales - Terceros']+df_ratios['Cuentas por Pagar Diversas - Relacionadas']+df_ratios['Cuentas por Pagar Diversas - Terceros']+df_ratios['Cuentas por Pagar a los Accionistas (Socios), Directores y Gerentes']
    except:
        df_ratios['CUENTAS POR PAGAR']=0
    

    return df_ratios

####CREAR COLUMNAS TRIMESTRE MES ETC
def cleanBalanceComprobacion(df_bcomprobacion):
    df_bcomprobacion['al_periodo']=df_bcomprobacion['al_periodo'].astype("str")
    df_bcomprobacion['year']=df_bcomprobacion['al_periodo'].str[:4]
    df_bcomprobacion['month']=df_bcomprobacion['al_periodo'].str[4:]
    df_bcomprobacion['year2']=df_bcomprobacion['year']+'-'
    df_bcomprobacion['year']=df_bcomprobacion['year'].astype("str")#.astype(object)
    df_bcomprobacion['TRIM']=df_bcomprobacion['trimestre']
    df_bcomprobacion['al_periodo']=df_bcomprobacion['al_periodo']+'-'
    for anio in df_bcomprobacion['year'].unique():
                df_bcomprobacion['TRIM'].loc[df_bcomprobacion.year==anio]=df_bcomprobacion['trimestre']
                df_bcomprobacion['TRIM'].loc[df_bcomprobacion.year==anio]=df_bcomprobacion['TRIM'].replace(1,str(anio)+' '+'Trim 1')
                df_bcomprobacion['TRIM'].loc[df_bcomprobacion.year==anio]=df_bcomprobacion['TRIM'].replace(2,str(anio)+' '+'Trim 2')
                df_bcomprobacion['TRIM'].loc[df_bcomprobacion.year==anio]=df_bcomprobacion['TRIM'].replace(3,str(anio)+' '+'Trim 3')
                df_bcomprobacion['TRIM'].loc[df_bcomprobacion.year==anio]=df_bcomprobacion['TRIM'].replace(4,str(anio)+' '+'Trim 4')
    df_bcomprobacion['Mes']=df_bcomprobacion['month']
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('01','Enero')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('02','Febrero')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('03','Marzo')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('04','Abril')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('05','Mayo')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('06','Junio')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('07','Julio')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('08','Agosto')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('09','Setiembre')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('10','Octubre')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('11','Noviembre')
    df_bcomprobacion['Mes']=df_bcomprobacion['Mes'].replace('12','Diciembre')
    df_bcomprobacion['trimestre']=df_bcomprobacion['trimestre'].replace(1,'Trim 1')
    df_bcomprobacion['trimestre']=df_bcomprobacion['trimestre'].replace(2,'Trim 2')
    df_bcomprobacion['trimestre']=df_bcomprobacion['trimestre'].replace(3,'Trim 3')
    df_bcomprobacion['trimestre']=df_bcomprobacion['trimestre'].replace(4,'Trim 4')
    return df_bcomprobacion
###
def balancePivot(ejex,moneda,df_bcomprobacion):

        if ejex =='Trimestre':
            group=['year','trimestre','TRIM']
            eje='TRIM'
        elif ejex =='Periodo':
            group=['year','Mes','month','al_periodo']
            eje='al_periodo'

        df_niv1_trim=df_bcomprobacion.groupby(group+['grupo1'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        df_niv2_trim=df_bcomprobacion.groupby(group+['grupo2'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        df_niv3_trim=df_bcomprobacion.groupby(group+['grupo3'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        df_niv4_trim=df_bcomprobacion.groupby(group+['grupo_funcion'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        df_niv5_trim=df_bcomprobacion.groupby(group+['grupo_naturaleza'])[['saldo_cargo_mof','saldo_cargo_mex']].sum().reset_index()
        if moneda == 'soles':
            tipo='saldo_cargo_mof'
        elif moneda == 'dolares':
            tipo='saldo_cargo_mex'
        df_niv1_pivot_trim=pd.pivot_table(df_niv1_trim,index=group,columns='grupo1',values=tipo)
        df_niv1_pivot_trim=df_niv1_pivot_trim.reset_index()

        df_niv2_pivot_trim=pd.pivot_table(df_niv2_trim,index=group,columns='grupo2',values=tipo)
        df_niv2_pivot_trim=df_niv2_pivot_trim.reset_index()

        df_niv3_pivot_trim=pd.pivot_table(df_niv3_trim,index=group,columns='grupo3',values=tipo)
        df_niv3_pivot_trim=df_niv3_pivot_trim.reset_index()

        df_niv4_pivot_trim=pd.pivot_table(df_niv4_trim,index=group,columns='grupo_funcion',values=tipo)
        df_niv4_pivot_trim=df_niv4_pivot_trim.reset_index()

        df_niv5_pivot_trim=pd.pivot_table(df_niv5_trim,index=group,columns='grupo_naturaleza',values=tipo)
        df_niv5_pivot_trim=df_niv5_pivot_trim.reset_index()

        df_ratios_first_trim=df_niv1_pivot_trim.merge(df_niv2_pivot_trim,how='inner',left_on=eje,right_on=eje)
        df_ratios_first_trim=df_ratios_first_trim.merge(df_niv3_pivot_trim,how='inner',left_on=eje,right_on=eje)
        createRatios(df_ratios_first_trim)
        
        return df_ratios_first_trim

def balancePivotRename(moneda,df):
        if moneda=='saldo_cargo_mof':
            df_bcomprobacion_123=balancePivot('Periodo','soles',df)
        elif moneda=='saldo_cargo_mex':
            df_bcomprobacion_123=balancePivot('Periodo','dolares',df)
        
        df_bcomprobacion_123=df_bcomprobacion_123[['al_periodo','year','ACTIVO    ','PASIVO    ', 'PATRIMONIO_x','ACTIVO NO CORRIENTE', 'PASIVO CORRIENTE']]
        df_bcomprobacion_123=df_bcomprobacion_123.rename(columns={'ACTIVO    ':'ACTIVO','PASIVO    ':'PASIVO','PATRIMONIO_x':'PATRIMONIO'})
        return df_bcomprobacion_123
#bc_uti
def createBc_uti(moneda,df_bcomprobacion):
        df_bcomprobacion_123=df_bcomprobacion#dfCompuesto(moneda)
        
        df_bc_uti=df_bcomprobacion_123.groupby(['grupo_funcion','year','month','al_periodo'])[[moneda]].sum().reset_index()
        df_bc_uti_pivot=df_bc_uti.pivot_table(index=('year','month','al_periodo'),values=moneda,columns='grupo_funcion').reset_index()
        df_bc_uti_pivot=df_bc_uti_pivot.fillna(0)
        df_bc_uti_pivot['UTILIDAD BRUTA']=df_bc_uti_pivot['VENTAS']-df_bc_uti_pivot['COSTO DE VENTAS']
        df_bc_uti_pivot['GASTOS DE OPERACION']=df_bc_uti_pivot['GASTOS DE ADMINISTRACION']+df_bc_uti_pivot['GASTOS DE VENTA']
        df_bc_uti_pivot['UTILIDAD OPERATIVA']=df_bc_uti_pivot['UTILIDAD BRUTA']-df_bc_uti_pivot['GASTOS DE OPERACION']
        df_bc_uti_pivot['OTROS INGRESOS Y GASTOS']=(df_bc_uti_pivot['CAMBIOS EN EL VALOR RAZONABLE DE LOS ACTIVOS BIOLOGICOS']+
                                                    df_bc_uti_pivot['DIFERENCIA DE CAMBIO, NETA']+
                                                    df_bc_uti_pivot['FLUCTUACION DE INVERSIONES EN SUBSIDIARIAS']+
                                                    df_bc_uti_pivot['GASTOS - CONTRATO DE COLABORACION']+
                                                    df_bc_uti_pivot['GASTOS FINANCIEROS, NETO']+
                                                    df_bc_uti_pivot['RECUPERACION DRAWBACK']+
                                                    df_bc_uti_pivot['OTROS INGRESOS, NETO'])
        df_bc_uti_pivot['UTILIDAD ANTES DE IMPUESTOS']=df_bc_uti_pivot['UTILIDAD OPERATIVA']+df_bc_uti_pivot['OTROS INGRESOS Y GASTOS']
        df_bc_uti_pivot['UTILIDAD NETA']=df_bc_uti_pivot['UTILIDAD OPERATIVA']+df_bc_uti_pivot['OTROS INGRESOS Y GASTOS']-df_bc_uti_pivot['(-) IMPUESTO A LAS GANACIAS']
        df_bc_uti_pivot['EBIT']=df_bc_uti_pivot['VENTAS']-df_bc_uti_pivot['GASTOS DE OPERACION']
        return df_bc_uti_pivot

################################# VENTAS
