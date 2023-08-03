import pandas as pd

def dataframe_filtro(values=[],columns_df=[]):
   """
   values son los inputs 
   columns_df son las columnas a comparar para el filtro
   """
   query = ""
   for value, col in zip(values,columns_df):
        if value != None:
            if type(value) == int:
                text=f"{col} == {value}"
            elif type(value) == str:
                text=f"{col} == '{value}'"

            query += text + " and "
            
   return query[:-5]



def filter_inputs_agricola_recurso(df=pd.DataFrame(),year_cultivo='',variedad='',lote=''):
    if year_cultivo==None and variedad==None and lote==None:
            options=df
    elif year_cultivo!=None and variedad==None and lote==None:
            options=df[df['AÑO_CULTIVO']==year_cultivo]
    elif year_cultivo!=None and variedad!=None and lote==None:
            options=df[(df['AÑO_CULTIVO']==year_cultivo)&(df['VARIEDAD']==variedad)]
    elif year_cultivo!=None and variedad!=None and lote!=None:
            options=df[(df['AÑO_CULTIVO']==year_cultivo)&(df['VARIEDAD']==variedad)&(df['CONSUMIDOR']==lote)] 
    elif year_cultivo!=None and variedad==None and lote!=None:
            options=df[(df['AÑO_CULTIVO']==year_cultivo)&(df['CONSUMIDOR']==lote)] 
        
    elif year_cultivo==None and variedad!=None and lote!=None:
            options=df[(df['VARIEDAD']==variedad)&(df['CONSUMIDOR']==lote)]
        
    elif year_cultivo==None and variedad!=None and lote==None:
            options=df[(df['VARIEDAD']==variedad)]
    elif year_cultivo==None and variedad==None and lote!=None:
            options=df[(df['CONSUMIDOR']==lote)]
    
    return options






