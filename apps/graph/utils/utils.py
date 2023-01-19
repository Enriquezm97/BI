import pandas as pd
import numpy as np

## PRODUCCION FUNCTION
def colArea(df):
    df_area_agricola=pd.DataFrame()
    years=sorted(df['AÑO_CAMPAÑA'].unique())
    for year in years:
        df_year=df[df['AÑO_CAMPAÑA']==year]
        df_year=df_year.groupby(['CODCONSUMIDOR','CONSUMIDOR','CULTIVO','VARIEDAD','AREA_CAMPAÑA','AÑO_CAMPAÑA','AREA_PLANIFICADA']).sum().reset_index()
        df_area_agricola=pd.concat([df_area_agricola,df_year])
    return df_area_agricola