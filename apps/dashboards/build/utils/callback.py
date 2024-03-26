from dash import Input, Output,State,no_update,dcc,html
import pandas as pd
import dash_mantine_components as dmc
import plotly.graph_objects as go
from ..utils.helpers import *
from ..utils.builder import *

def build_inp_out(lista_inputs = []):
    if "moneda" in lista_inputs:
        list_ = list(lista_inputs)
        list_.remove("moneda")
        return [Output(id, "data")for id in lista_inputs],[Input(id, "value")for id in list_],list_
    else:
        return [Output(id, "data")for id in lista_inputs],[Input(id, "value")for id in lista_inputs],list_

def validar_input_moneda(list_inputs = []):
    if "moneda" in list_inputs :
        return [Input("data-values","data"),Input("moneda","value")]
    else:
        return [Input("data-values","data")]
    
def data_filtro(app,dict_ = {},dataframe = None):
    outs,inps,list_no_money = build_inp_out(dict_['id_dash']['compt_input'].keys())
    @app.callback(
        outs+
        [Output("data-values","data"),Output("notifications-update-data","children")],
        inps
    )
    def update_data(*args):
        print(list_no_money)
        if validar_all_none(variables = (args)) == True:
            df = dataframe.copy()
        else:
            df = dataframe.query(dataframe_filtro(values=(args),columns_df=list(dict_['id_dash']['compt_input'].values())[:-1]))
        return [[{'label': i, 'value': i} for i in sorted(df[col].unique())]for col in list(dict_['id_dash']['compt_input'].values())[:-1]]+[['PEN','USD'],df.to_dict('series'),dmc.Notification(title = 'Update',id='noti',action="show",message=f'Se cargaron {len(df)} filas')]
"""
def outputs_func(app,dict_ = {},dataframe = None):
    outputs_id = dict_['id_dash']['compt_output']['id']
    outputs_type = dict_['id_dash']['compt_output']['type']
    outputs_type = list(dict_['id_dash']['compt_input'].keys())
    inputs = validar_input_moneda(list_inputs=outputs_type)
    moneda_soles = dict_['monedas'][0]
    moneda_dolares = dict_['monedas'][1]
    print(moneda_soles,moneda_dolares)
    @app.callback(
        [Output(id, "figure")if type == 1 else Output(id, "children")  for id,type in zip(outputs_id,outputs_type)],
        inputs 
    )
    def update_outs(args*):
        data = pd.DataFrame(args[0])
        if len(args)>1:
            moneda = moneda_soles if args[1] == "PEN" else moneda_dolares
"""
        
            
        