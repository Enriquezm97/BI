from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS,COMERCIAL_LOGISTICA
from ..build.layout.error.dashboard_error import ERROR
from ..build.api.get_connect import connect_api
from ..build.layout.layout_logistica import almacen_stock
from ..build.utils.transform.t_logistica import *
###

from dash import Input, Output,State,no_update,dcc,html
import dash_mantine_components as dmc
from ..build.components.display_comp import *

filt = ['select-anio','select-grupo','select-rango']

def validar_all_none(variables=()):
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

def create_list_dict_outputs(id_components = [],dict_cols_dataframe = {}, dataframe=None):
    outputs_list =[]
    for element in id_components:
        
        if type(dict_cols_dataframe[element]) == list:
            
            outputs_list.append([{'label': i, 'value': i} for i in sorted(dataframe[dict_cols_dataframe[element][0]].unique()) ])
        else:
           
            outputs_list.append([{'label': i, 'value': i} for i in sorted(dataframe[dict_cols_dataframe[element]].unique())])
    return outputs_list

def create_col_for_dataframe(id_components = [],dict_cols_dataframe = {}):
    cols_dataframe = []
    for element in id_components:
        
        if type(dict_cols_dataframe[element]) == list:
            
            cols_dataframe.append(dict_cols_dataframe[element][0])
        else:
            
            cols_dataframe.append(dict_cols_dataframe[element])
    return cols_dataframe

def order_mes_text(disorder_list = []):
    lista_order_mes_text = ['Enero','Febrero','Marzo', 'Abril', 'Mayo','Junio', 'Julio', 'Agosto','Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    lista_new_order = []
    for mes in lista_order_mes_text:
      if mes in disorder_list:
        lista_new_order.append(mes)
    return lista_new_order






def dashboard_stocks(codigo = '',empresa = ''):#filtros = ['select-anio','select-grupo','select-rango']
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    app.layout =  almacen_stock() 
    try:
        if empresa == 'SAMPLAST':
            dff  = connect_api(sp_name = 'nsp_stocks_bi_samplast')
        else :
            dff  = connect_api(sp_name = 'nsp_stocks')
        dataframe = clean_stocks(df = dff)
        print(dataframe)
        #app.layout =  logistica_build()   
    except:
        app.layout = ERROR
    #def filter_callback(app, filt =[], dataframe = None):
    @app.callback(
        [Output(output_,'data')for output_ in filt]+
        [
         Output("data-values","data"),
         Output('chipgroup-mes','children'),
         Output("notifications-update-data","children")
        ],
        [Input(input_,"value")for input_ in filt]
    )
    def update_filter(*args):
        
        if validar_all_none(variables = args) == True:
            df=dataframe.copy()
        else:
            df=dataframe.query(dataframe_filtro(values=list(args),columns_df=create_col_for_dataframe(id_components = filt, dict_cols_dataframe=COMERCIAL_LOGISTICA)))

        return create_list_dict_outputs(dataframe = df,id_components = filt, dict_cols_dataframe=COMERCIAL_LOGISTICA)+[
               df.to_dict('series'),
               [dmc.Chip(x,value=x,variant="outline",radius= 'xs')for x in order_mes_text(df['Mes'].unique())],
               DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),
        ]  
    #app.layout =  logistica_build() 
    #dff  = connect_api(sp_name = 'nsp_stocks_bi_samplast')
    #stocks_df = clean_stocks(df = dff)
    #print(stocks_df)
    return app