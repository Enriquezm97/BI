import pandas as pd
import numpy as np
def create_list_var(*args):
   variables=[]
   for n in args:
      variables.append(n)
   return variables

def convert_to_json(dataframe):
   return dataframe.to_json(date_format='iso', orient='split')

def convert_to_dataframe(json):
   return pd.read_json(json, orient='split')

def order_mes_text(disorder_list = []):
    lista_order_mes_text = ['Enero','Febrero','Marzo', 'Abril', 'Mayo','Junio', 'Julio', 'Agosto','Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    lista_new_order = []
    for mes in lista_order_mes_text:
      if mes in disorder_list:
        lista_new_order.append(mes)
    return lista_new_order

def get_parameters_datepicker(df=pd.DataFrame(),col_inicio='',col_fin=''):
    minimo = str(df[col_inicio].min())
    maximo = str(df[col_fin].max())
    datepicker=[minimo,maximo]
    return [minimo, maximo, datepicker]

def create_stack_np(dataframe = pd.DataFrame(), lista = []):
    return np.stack(tuple(dataframe[elemento] for elemento in lista),axis = -1)

def create_hover_custom(lista = []):
    string_hover = ''
    for i,element in zip(range(len(lista)),lista):
        string_hover = string_hover+'<br><b>'+element+': %{customdata['+str(i)+']}</b>'
    return string_hover

def create_col_for_dataframe(id_components = [],dict_cols_dataframe = {}):
    cols_dataframe = []
    for element in id_components:
        
        if type(dict_cols_dataframe[element]) == list:
            
            cols_dataframe.append(dict_cols_dataframe[element][0])
        else:
            
            cols_dataframe.append(dict_cols_dataframe[element])
    return cols_dataframe

def create_list_dict_outputs(id_components = [],dict_cols_dataframe = {}, dataframe=None):
    outputs_list =[]
    for element in id_components:
        
        if type(dict_cols_dataframe[element]) == list:
            
            outputs_list.append([{'label': i, 'value': i} for i in sorted(dataframe[dict_cols_dataframe[element][0]].unique()) ])
        else:
            
            outputs_list.append([{'label': i, 'value': i} for i in sorted(dataframe[dict_cols_dataframe[element]].unique())])
    return outputs_list

def validar_all_none(variables=()):
    contador = 0
    for i in variables:
        if i == None:
            contador = contador +1
    return True if len(variables) == contador else False

def hoversize_recurso_agricola(recurso = ''):
   if recurso=='Insumos':
        hover='<br><b>Cantidad</b>: %{y:.1f} Kg<br> <b>Unidad/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=13
   elif recurso=='Maquinaria':
        hover='<br><b>Cantidad</b>: %{y:.1f} h<br> <b>Hm/Ha</b>: %{customdata[0]:.1f} <br>'
        size_text=13
   elif recurso=='Mano de Obra':
        hover='<br><b>Cantidad</b>: %{y:.1f} jr<br> <b>Jr/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=13
   elif recurso=='Riego':
        hover='<br><b>Cantidad</b>: %{y:.1f} m3<br> <b>m3/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=13
   else: 
        hover='<br><b>Cantidad</b>: %{y:.1f}<br>{text} <b>-/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=10
   return [hover,size_text]

def order_st_agricola_ejex(df = pd.DataFrame(), ejex = '', var_col =''):
     if ejex == 'week':
                order={ejex : sorted(df[ejex].unique()),var_col : sorted(df[var_col].unique())}
     else: 
                order={}
     return order

def table_agricola_recurso(dataframe = pd.DataFrame(), check = [], recursos = '', col ='CONSUMIDOR'):
     def colArea(df):
            df_area_agricola=pd.DataFrame()
            years=sorted(df['AÑO_CAMPAÑA'].unique())
            for year in years:
                df_year=df[df['AÑO_CAMPAÑA']==year]
                df_year=df_year.groupby(['CODCONSUMIDOR','CONSUMIDOR','CULTIVO','VARIEDAD','AREA_CAMPAÑA','AÑO_CAMPAÑA']).sum().reset_index()
                df_area_agricola=pd.concat([df_area_agricola,df_year])
            return df_area_agricola
     dff_area=colArea(dataframe)
     dff_pt=dff_area.groupby([col]).sum().reset_index()
     dff_pt=dff_pt.rename(columns={
                                        'Nitrógeno':'Nitrogeno',
                                        'Fósforo':'Fosforo',

                                       })
     dff_pt=dff_pt[[col,'AREA_CAMPAÑA']+check]
        ### CONSUMIDORES 
     if col == 'CONSUMIDOR':
          dff_lotes=dff_area.groupby([col]).sum().reset_index()
     else:
          dff_lotes=dff_area.groupby(['CONSUMIDOR',col]).sum().reset_index()
     dff_lotes=dff_lotes.rename(columns={
                                        'Nitrógeno':'Nitrogeno',
                                        'Fósforo':'Fosforo',

                                       })
     dff_lotes=dff_lotes[['CONSUMIDOR','AREA_CAMPAÑA']+check]
     if recursos == 'hectarea':
            columns=dff_pt.columns
            columns_lote=dff_lotes.columns
            dff_pt['AREA_CAMPAÑA']=dff_pt['AREA_CAMPAÑA'].astype('float64')
            dff_lotes['AREA_CAMPAÑA']=dff_lotes['AREA_CAMPAÑA'].astype('float64')
            for recurso in columns[2:]:
                dff_pt[recurso]=dff_pt[recurso]/dff_pt['AREA_CAMPAÑA']
            for recurso2 in columns_lote[2:]:
                dff_lotes[recurso2]=dff_lotes[recurso2]/dff_lotes['AREA_CAMPAÑA']
     dff_lotes=dff_lotes.round(1)
     dff_pt.loc['TOTAL',:]= dff_pt.sum(numeric_only=True, axis=0)      
     dff_pt=dff_pt.fillna('TOTAL')
     dff_pt=dff_pt.round(1)
     return dff_pt
     
def create_dict_of_list(df,col='Ingresos_Generales',dict_color=None,list_partidas=[],pivot=True,col_=''):
     total=df[col].sum()
     lista_diccionario=[]
     for element in list_partidas:
          if pivot==True:
               percent_value=round((df[element].sum()/total)*100)
          else:
               df_filtro=df[df[col_]==element]
               percent_value=round((df_filtro[col].sum()/total)*100)
          dicts={'value': percent_value, 'color': dict_color[element], 'label': f'{percent_value}%', "tooltip": element}
                #print(f"UNA ITERACION:{(df[element].sum()/total)*100}")
          lista_diccionario.append(dicts)
     return lista_diccionario

def create_dataframe_costos_tipo2(df = pd.DataFrame(), col = 'CULTIVO', radio_tipo_costo = ''):
     
     if col == 'CULTIVO':
          list_col_ha = ['CULTIVO','CONSUMIDOR','AREA_CAMPAÑA']  
          list_group_ = ['CULTIVO']
     elif col == 'VARIEDAD':
          list_col_ha = ['VARIEDAD','CONSUMIDOR','AREA_CAMPAÑA'] 
          list_group_ = ['VARIEDAD','CULTIVO']
     elif col == 'CONSUMIDOR':
          list_col_ha = ['CONSUMIDOR','AREA_CAMPAÑA'] 
          list_group_ = ['CONSUMIDOR','CULTIVO']
          
     dff = df.groupby(list_group_).sum().reset_index()
     dff['AREA_CAMPAÑA']=dff['AREA_CAMPAÑA'].astype('object')
     dff.loc[:,'TOTAL']= dff.sum(numeric_only=True, axis=1)
     dff['AREA_CAMPAÑA']=dff['AREA_CAMPAÑA'].astype('float64')
     
            
     if radio_tipo_costo == 'totales':    
          dff  =dff.sort_values('TOTAL',ascending=True)
          #x = dff[col]
          #color = dff['CULTIVO']
          dff['PROMEDIO'] = (dff['TOTAL'].sum())/len(dff[col].unique()) 
          #title=f'Costos {simbolo}. / {ejey}'
          #ejetotal='TOTAL'
     else:
               dff_ha = df.groupby(list_col_ha).sum().reset_index()
               dff['TOTAL'] = dff['TOTAL']/dff_ha['AREA_CAMPAÑA']
               dff = dff.sort_values('TOTAL',ascending=True)
               #x = dff[col]
               #color = dff['CULTIVO']
               dff['PROMEDIO']=(dff['TOTAL'].sum())/len(dff[col].unique())   
               #title=f'Costos {simbolo} / Ha x {ejey}'
               #ejetotal='AH'
     return dff

def create_dataframe_costos_tipo(
     df = pd.DataFrame(), category_col = [], numeric_col = [] ,radio_tipo_costo = ''
):
     if radio_tipo_costo == 'por ha':
          #LOS VALUES DE numeric_col deben ser saldo y luego area
          dff = df.groupby(category_col)[numeric_col].sum().reset_index()#.sort_values(numeric_col[0],ascending=True)
          dff[numeric_col[0]] = dff[numeric_col[0]]/dff[numeric_col[1]]
          return dff.sort_values(numeric_col[0],ascending=True) 
     else: 
          return df.groupby(category_col)[numeric_col].sum().reset_index().sort_values(numeric_col[0],ascending=True) 
          
     