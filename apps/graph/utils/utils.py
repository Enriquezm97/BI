import pandas as pd
import numpy as np

## PRODUCCION FUNCTION
def colArea(df):
    df_area_agricola=pd.DataFrame()
    years=sorted(df['AÑO_CAMPAÑA'].unique())
    print("años:")
    print(years)
    for year in years:
        df_year=df[df['AÑO_CAMPAÑA']==year]
        print(df_year)
        df_year=df_year.groupby(['CODCONSUMIDOR','CONSUMIDOR','CULTIVO','VARIEDAD','AREA_CAMPAÑA','AÑO_CAMPAÑA']).sum().reset_index()
        print(df_year.columns)
        df_area_agricola=pd.concat([df_area_agricola,df_year])
        print(df_area_agricola)
    return df_area_agricola