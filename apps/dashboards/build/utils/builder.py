import pandas as pd
import numpy as np

def get_list_values(dict_input = {}, dict_componentes ={}, tipe_value = 'componente', for_title = False):
        lista_values= []
        if for_title == False:
            if tipe_value == 'id':
                for key, value in dict_input.items():
                    if key != 'Moneda':
                        lista_values.append(dict_componentes[key][value['tipo_componente']][tipe_value])
            else :
                for key, value in dict_input.items():
                        lista_values.append(dict_componentes[key][value['tipo_componente']][tipe_value])
        else :
            for key, value in dict_input.items():
                        lista_values.append(dict_componentes[key][value['tipo_componente']][tipe_value])
        return lista_values

def validate_inputs(variables=()):
    contador = 0
    for i in variables:
        if i == None:
            contador = contador +1
    return True if len(variables) == contador else False

def dataframe_filtro(values=[],columns_df=[]):
   """
   values son los inputs 
   columns_df son las columnas a comparar para el filtro
   """
   query = ""
   for value, col in zip(values,columns_df):
        if value != None:
            if type(value) == int:
                text=f"`{col}` == {value}"
            elif type(value) == str:
                text=f"`{col}` == '{value}'"
            elif type(value) == list:
                text=f"`{col}` in {value}"
            query += text + " and "
            
   return query[:-5]

def create_col_for_dataframe(id_components = [],dict_cols_dataframe = {}):
    cols_dataframe = []
    for element in id_components:
        
        if type(dict_cols_dataframe[element]) == list:
            
            cols_dataframe.append(dict_cols_dataframe[element][0])
        else:
            
            cols_dataframe.append(dict_cols_dataframe[element])
    return cols_dataframe