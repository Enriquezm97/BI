import dash_mantine_components as dmc  
from dash import Input, Output,State,no_update,dcc,html
from datetime import datetime, date, timedelta
from ....constans import COMERCIAL_LOGISTICA,ALM_LOGISTICA
from ...components.components_main import *
from ...functions.functions_filters import *
from ...functions.functions_data import *
from ...functions.functions_figure import *
from ...figures import GraphPiego
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
               [dmc.Chip(x,value=x,variant="outline",radius= 'xs',styles=styles_chip)for x in order_mes_text(df['Mes'].unique())],
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
        Input('select-moneda','value')
    )
    def update_graph(data, filt_mes,moneda):
        df = pd.DataFrame(data)
        if filt_mes != None and len(filt_mes)==0:
            dff = df.copy()
        elif filt_mes != None:
            dff = df[df['Mes_text'].isin(filt_mes)]
        else:
            dff = df.copy()
           
        
        return [
            figure_stock_var_y2(df=dff, height = 380, moneda = moneda),
            figure_bar_familia(df = dff, height = 380, moneda = moneda),
            figure_bar_top_producto(df = dff, height = 380, moneda = moneda),
            figure_bar_relative(df = dff, height = 380, eje_color = 'ABC Ventas', title = '% Stock por el ABC Ventas', moneda = moneda),
            figure_bar_relative(df = dff, height = 380, eje_color = 'ABC Stock', title = '% Stock por el ABC de Stock Valorizado', moneda = moneda),
            figure_pie_rango_stock(df = dff, height = 380, moneda = moneda),
            figure_pie_rango_stock_count(df = dff, height = 380, moneda = moneda)
        ]
        
def filter_callback_alm(app, filt =[], dataframe = None):
    @app.callback(
        [Output(output_,'data')for output_ in filt]+
        [
         Output("data-values","data"),
         Output("notifications-update-data","children")
        ],
       
        [Input(input_,"value")for input_ in filt]+
         [Input("datepicker-inicio","value"),Input("datepicker-fin","value")]
    )
    def update_filter(*args,**kwargs):
        
        datepicker_inicio = datetime.strptime(args[-2], '%Y-%m-%d').date()
        datepicker_fin = datetime.strptime(args[-1], '%Y-%m-%d').date()
        inputs = args[:-2]
        filter_datepicker_df = dataframe[(dataframe['Última Fecha Ingreso']>=datepicker_inicio)&(dataframe['Última Fecha Ingreso']<=datepicker_fin)]
        if validar_all_none(variables = inputs) == True:
            df = filter_datepicker_df.copy()
        else:
            df = dataframe.query(dataframe_filtro(values=list(inputs),columns_df=create_col_for_dataframe(id_components = filt, dict_cols_dataframe=ALM_LOGISTICA)))

        return create_list_dict_outputs(dataframe = df,id_components = filt, dict_cols_dataframe=ALM_LOGISTICA)+[
               df.to_dict('series'),
               DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),  
        ]  

def graph_alm(app):
    @app.callback(
        [Output('bar-importe-stock','figure'),
        Output('table-status','rowData'),
        Output('table-status','columnDefs'),
        #Output('table-status','getRowStyle'),
        Output('pie-estadoinv','figure'),
        Output('bar-respon','figure')],
        [Input("data-values","data"),
        Input("segmented-col","value"),
        Input('select-moneda','value')]
    )
    def update_graph(data, segmented,moneda):
        df = pd.DataFrame(data)
        #print(df['Última Fecha Salida'].unique())
        dff = df[df['Duracion_Inventario'].notna()]
        
        table_dff = dff[['Sucursal', 'Almacén', 'Tipo','Grupo','Sub Grupo','Producto','Responsable Ingreso','Última Fecha Ingreso', 'Última Fecha Salida','Duracion_Inventario','Stock',moneda]]
        return [
            figure_stock_alm_y2(df = df, height = 300 , moneda = moneda, tipo = segmented),
            table_dff.to_dict("records"),
            [{"field": i,"cellStyle": {'font-size': 11}} for i in table_dff.columns],
            
            figure_pie_estado_inv(df = df),
            figure_bar_responsable(df = df, height = 400)
        ]
"""
{"styleConditions": [
                    {
                        "condition": "params.data.Duracion_Inventario < 0",
                        "style": {"backgroundColor": "grey"},
                    },
                    {
                        "condition": "params.data.Duracion_Inventario >= 0 && params.data.Duracion_Inventario <= 10",
                        "style": {"backgroundColor": "#66f756"},
                    },
                    {
                        "condition": "params.data.Duracion_Inventario > 10 && params.data.Duracion_Inventario <= 50",
                        "style": {"backgroundColor": "yellow"},
                    },
                    {
                        "condition": "params.data.Duracion_Inventario > 50",
                        "style": {"backgroundColor": "#ff4f4f"},
                    },
                ],
                #"defaultStyle": {"backgroundColor": "grey", "color": "white"},
            },
"""