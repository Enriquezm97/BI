import dash_mantine_components as dmc  
from dash import Input, Output,State,no_update,dcc,html
from datetime import datetime, date, timedelta
from ....constans import COMERCIAL_LOGISTICA
from ...components.components_main import *
from ...functions.functions_filters import *
from ...functions.functions_data import *
from ...functions.functions_figure import *
from ...styles_ import *


def filter_callback(app, filt =[], dataframe = None):
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
               [dmc.Chip(x,value=x,variant="outline",radius= 'xs',styles=styles_chip)for x in order_mes_text(df['Mes_text'].unique())],
               DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),  
        ]  
def graph_log(app):
    @app.callback(
        Output('bar-stock-items','figure'),
        Output('bar-stock-familia','figure'),
        Output('bar-top-producto','figure'),
        Output('bar-stock-abc-ventas','figure'),
        Output('bar-stock-abc-valorizado','figure'),
        Output('pie-stock-antiguedad','figure'),
        Output('pie-items-antiguedad','figure'),
        Input("data-values","data"),
        Input('chipgroup-mes',"value"),
    )
    def update_graph(data, filt_mes):
        df = pd.DataFrame(data)
        if filt_mes != None and len(filt_mes)==0:
            dff = df.copy()
        elif filt_mes != None:
            dff = df[df['Mes_text'].isin(filt_mes)]
        else:
            dff = df.copy()
            
        
        return [
            figure_stock_var_y2(df=dff, height = 380),
            figure_bar_familia(df = dff, height = 380),
            figure_bar_top_producto(df = dff, height = 380),
            figure_bar_relative(df = dff, height = 350, eje_color = 'ABC Ventas', title = '% Stock por el ABC Ventas'),
            figure_bar_relative(df = dff, height = 350, eje_color = 'ABC Stock', title = '% Stock por el ABC de Stock Valorizado'),
            figure_pie_rango_stock(df = dff, height = 350),
            figure_pie_rango_stock_count(df = dff, height = 350)
        ]