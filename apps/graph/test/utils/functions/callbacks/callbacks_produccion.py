from dash import Input, Output,State,no_update,dcc,html
from apps.graph.test.constans import DIC_RECURSOS_AGRICOLA,COLORS_G10,DICT_TIPO_COSTO,DICT_CULTIVOS_COLOR
from apps.graph.test.utils.functions.functions_filters import *
from apps.graph.test.utils.functions.functions_data import *
from apps.graph.test.utils.components import DataDisplay,Button
from apps.graph.test.utils.figures import *
from apps.graph.test.utils.frame import Graph
from apps.graph.test.utils.tables import tableDag
from apps.graph.test.utils.blocks.block_card import cardDivider

import sys


##############################
def create_callback_offcanvas_filters(app):
    @app.callback(
        Output("offcanvas-placement", "is_open"),
        Input("btn-filter", "n_clicks"),
        State("offcanvas-placement", "is_open"),
    )
    def toggle_offcanvas_scrollable(n1, is_open):
        if n1:
            return not is_open
        return is_open
    
def create_callback_download_data(
    app,input_id_data="data-values",input_id_btn="btn-download",output="download", name_file="source.xlsx"
):
    @app.callback(
            Output(output, "data"),
            
            Input(input_id_btn, "n_clicks"),
            State(input_id_data,"data"),
            prevent_initial_call=True,
            
            )
    def update_download(n_clicks_download,data):
        if n_clicks_download:
            df = pd.DataFrame(data)
            return dcc.send_data_frame(df.to_excel, name_file, sheet_name="Sheet_name_1")

def create_callback_change_theme(app):
    @app.callback(Output("mantine-provider", "theme"),
                  Output("container", "style"),
                  Input("switch","checked"))
    def change_theme(switch):
        #, style={'backgroundColor':'blue'}
        value= "light " if switch else "dark"
        back_color= "rgb(255, 255, 255)" if switch else "rgb(26, 27, 30)"
        #rgb(26, 27, 30)
        return {"colorScheme": value},{'backgroundColor': back_color}
    
def create_callback_filter_agricola_recurso(app,dataframe=pd.DataFrame()):
    @app.callback(
                  Output('select-variedad','data'),
                  Output('select-lote','data'),
                  Output('checklist-recurso-agricola','options'),
                  Output('checklist-recurso-agricola','value'),  
                  Output('label-range-inicio-campania','children'), 
                  Output('label-range-fin-campania','children'), 
                  Output("data-values","data"),
                  Output("segmented-recurso",'data'),
                  Output("segmented-recurso",'value'),
                  Output("notifications-update-data","children"),
                  Input('select-campania','value'),
                  Input('select-variedad','value'),
                  Input('select-lote','value'),
                 )
    def update_filter_agricola_recurso(select_campania,select_variedad,select_lote):
    
        list_variables=create_list_var(select_campania,select_variedad,select_lote)
        df=dataframe.query(dataframe_filtro(values=list_variables,columns_df=['AÑO_CULTIVO','VARIEDAD','CONSUMIDOR']))
        """convirtiendo el dataframe a json"""
        select_out_variedad = [{'label': i, 'value': i} for i in sorted(df['VARIEDAD'].unique())]
        select_out_lote = [{'label': i, 'value': i} for i in df['CONSUMIDOR'].unique()]
        out_check_recurso = [{'label': i, 'value': i} for i in sorted(df['DSCVARIABLE'].unique())]
        values_out_check_recurso = sorted(df['DSCVARIABLE'].unique())
        
        segmented_recurso=df['TIPO'].unique()
        value_segmented_recurso=segmented_recurso[0]
        
        parametros_datepicker = get_parameters_datepicker(df=df,col_inicio='FECHAINICIO_CAMPAÑA',col_fin='FECHAFIN_CAMPAÑA')
        return [
                select_out_variedad, select_out_lote, 
                out_check_recurso,values_out_check_recurso,
                dmc.Badge(f"Inicio de Campaña: {parametros_datepicker[0]}",variant='dot',color='gray', size='lg',radius="lg"),
                dmc.Badge(f"Fin de Campaña: {parametros_datepicker[1]}",variant='dot',color='gray', size='lg',radius="lg"),
                #DataDisplay.text(id='inicio',text=),
                #DataDisplay.text(id='fin',text=),
                df.to_dict('series'),
                segmented_recurso,value_segmented_recurso,
                DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),
               ]

def create_callback_filter_agricola_costos(app,dataframe=pd.DataFrame()):
    @app.callback(
                  Output('select-cultivo','data'),
                  Output('select-variedad','data'),
                  Output('checklist-tipo-costos','options'),
                  Output('checklist-tipo-costos','value'),   
                  Output("data-values","data"),
                  Output("notifications-update-data","children"),
                  
                  Input('select-anio','value'),
                  Input('select-cultivo','value'),
                  Input('select-variedad','value'),
                 )
    
    def update_filter_agricola_recurso(select_anio,select_cultivo,select_variedad):
        list_variables=create_list_var(select_anio,select_cultivo,select_variedad)
        df=dataframe.query(dataframe_filtro(values=list_variables,columns_df=['AÑO_CAMPAÑA','CULTIVO','VARIEDAD']))
        #select_out_variedad

        select_out_cultivo=[{'label': i, 'value': i} for i in df['CULTIVO'].unique()]
        select_out_variedad=[{'label': i, 'value': i} for i in df['VARIEDAD'].unique()]
        out_check=[{'label': i, 'value': i} for i in df['TIPO'].unique()]
        value_out_check = df['TIPO'].unique()

        
        return [
            select_out_cultivo,select_out_variedad,out_check,value_out_check,
            df.to_dict('series'),
            DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),
        ]

def create_callback_recurso_agricola(app):
    @app.callback(
        Output('line-recurso-agricola','figure'),
        Output('table-variedad','children'),
        Output('table-lote','children'),
        Input("data-values","data"),
        Input("radio-serie-tiempo-ejex-recurso","value"),
        Input("radio-serie-tiempo-ejey-recurso","value"),
        Input("checklist-recurso-agricola","value"),
        Input("segmented-recurso","value"),
        
        
    )
    def update_graph_recurso_agricola(data,radio_ejex,radio_ejey,checklist_recursos,segmented_recurso):
        df = pd.DataFrame(data)
        df_ha_sembrado=df.groupby(['CONSUMIDOR',radio_ejex,'SEMANA','CULTIVO','VARIEDAD','AÑO_FECHA','AÑO_CAMPAÑA','AREA_CAMPAÑA','AÑO_CULTIVO'])[['CANTIDAD']].sum().reset_index()
        df_ha_total=df_ha_sembrado.groupby(['CONSUMIDOR',radio_ejex,'SEMANA','VARIEDAD','AÑO_FECHA','AÑO_CAMPAÑA','AÑO_CULTIVO'])[['AREA_CAMPAÑA']].sum().reset_index()
        df_ha_st=df_ha_total.groupby([radio_ejex,'SEMANA','AÑO_FECHA','AÑO_CAMPAÑA','AÑO_CULTIVO'])[['AREA_CAMPAÑA']].sum().reset_index()
        df_ha_st=df_ha_st[[radio_ejex,'AREA_CAMPAÑA']]
        
        

        df_graph=df.groupby(['DSCVARIABLE','TIPO',radio_ejex,'AÑO_FECHA','SEMANA'])[['CANTIDAD']].sum().reset_index()
        df_graph=df_graph.merge(df_ha_st, how='inner', left_on=[radio_ejex], right_on=[radio_ejex])


        df_graph.loc[df_graph.DSCVARIABLE == 'Nitrógeno','DSCVARIABLE'] =  'Nitrogeno'  
        df_graph.loc[df_graph.DSCVARIABLE == 'Fósforo','DSCVARIABLE'] =  'Fosforo'  
        #df_graph=df_graph[df_graph['DSCVARIABLE'].isin(check)]
        df_graph['CANTXHA']=df_graph['CANTIDAD']/df_graph['AREA_CAMPAÑA']
        if radio_ejey == 'hectarea':
              df_graph['CANTIDAD']=df_graph['CANTIDAD']/df_graph['AREA_CAMPAÑA']
              
        df_segmented = df_graph[df_graph['TIPO'] == segmented_recurso]
        df_segmented = df_segmented[df_segmented['DSCVARIABLE'].isin(checklist_recursos)]
        df_segmented = df_segmented.sort_values(by=[radio_ejex,'AÑO_FECHA','SEMANA'],ascending=True)
        print(df_segmented.info())
        print(segmented_recurso)
        hover_size = hoversize_recurso_agricola(recurso = segmented_recurso)
        ############################################
        df_pivot=df.pivot_table(index=('CULTIVO','VARIEDAD','CODCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','FECHA','AÑO_CAMPAÑA','AREA_CAMPAÑA','AREA_PLANIFICADA','week','AÑO_FECHA','SEMANA','AÑO_CULTIVO'),values=('CANTIDAD'),columns=('DSCVARIABLE'),aggfunc='sum').fillna(0).reset_index()
        #df_pivot['AÑO_CAMPAÑA']=df_pivot['AÑO_CAMPAÑA'].astype(object)
        variedad_table=table_agricola_recurso(dataframe= df_pivot,check = checklist_recursos,recursos  = radio_ejey,col = 'VARIEDAD')
        lote_table=table_agricola_recurso(dataframe= df_pivot,check = checklist_recursos,recursos = radio_ejey,col = 'CONSUMIDOR')
        def orderX(x,df):
            if x == 'week':
                order={'week':sorted(df['week'].unique()),'DSCVARIABLE': sorted(df['DSCVARIABLE'].unique())}
            else: 
                order={}
            return order
        return[GraphLinepx.line_(
                df = df_segmented, x = radio_ejex, y = "CANTIDAD", color="DSCVARIABLE", height = 400,
                y_title = '',title_legend = '', order = orderX(x=radio_ejex,df=df_segmented ),#order_st_agricola_ejex(df = df_segmented, ejex = radio_ejex, var_col = "DSCVARIABLE")
                title = segmented_recurso, discrete_color = DIC_RECURSOS_AGRICOLA, custom_data = ["CANTXHA"], hover_template = hover_size[0], size_text = hover_size[1]
                ),
                tableDag(id='variedad', 
                 columnDefs=[{"field": i, "type": "rightAligned"} for i in variedad_table.columns],
                 dataframe= variedad_table,
                 rules_col=['TOTAL','VARIEDAD']
                ),
                tableDag(id='lote', 
                 columnDefs=[{"field": i, "type": "rightAligned"} for i in lote_table.columns],
                 dataframe= lote_table,
                 rules_col=['TOTAL','CONSUMIDOR']
                ),
        ] 


def create_callback_modal_graph(app, id_modal = '', id_btn_modal = '', id_figure = ''):
    @app.callback(
    Output(id_modal, "children"),
    Output(id_modal, "is_open"),
    
    Input(id_btn_modal, "n_clicks"),
    Input(id_figure,'figure'),
    #prevent_initial_call=True,
    )
    def update_modal_(n_clicks, figure):
        #if n_clicks:
        #    return not is_open
        #return is_open,DataDisplay.modalMaximize(Graph(figure = convert_dict_to_graph(figure)))
        
        if n_clicks:#True, 
            return DataDisplay.modalMaximize(Graph(figure = convert_dict_to_graph(figure))),True
        else:#False,
            return  no_update
        
import dash_mantine_components as dmc     
def create_title_ejecucion_campania(app, title =''):
    @app.callback(
        Output("title","children"),
        Input('select-campania',"value"),
        Input('select-variedad',"value"),
        Input('select-lote',"value"),
        Input('radio-serie-tiempo-ejey-recurso',"value")
         
    )
    def update_title(recurso,campania,variedad,lote):
        
        lista_variables=create_list_var(recurso,campania,variedad,lote)
        badges=[]
        for i in lista_variables:
            if i != None:
                badges.append(dmc.Badge(i,variant='dot',color='blue', size='md',radius="lg"))
        
        return dmc.Title(children=[title]+badges,order=2, align='center')
    
def create_title_costos_campania(app, title =''):
    @app.callback(
        Output("title","children"),
        Input('select-anio',"value"),
        Input('select-cultivo',"value"),
        Input('select-variedad',"value"),
        Input('radio-ha-costos-agricola',"value"),
        Input('radio-costos-moneda',"value"),
         
    )
    def update_title(select_anio,select_cultivo,select_variedad,radio_tipocosto,radio_moneda):
        
        lista_variables=create_list_var(select_anio,select_cultivo,select_variedad,radio_tipocosto,"Soles" if radio_moneda=='SALDO_MOF' else "Dolares")
        badges=[]
        for i in lista_variables:
            if i != None:
                badges.append(dmc.Badge(i,variant='dot',color='blue', size='md',radius="lg"))
        
        return dmc.Title(children=[title]+badges,order=2,align='initial',style={"margin-left":"35px"})
import plotly.graph_objects as go     
def create_callback_costos_agricola(app):
    @app.callback(
        Output('card-costos-total','children'),
        Output('card-costos-ha','children'),
        Output('card-costos-cultivo','children'),
        Output('bar-costos-cultivo','figure'),
        Output('bar-costos-variedad','figure'),
        Output('pie-costos-tipo','figure'),
        Output('map-costos-lt','figure'),
        Output('bar-costos-lote','figure'),
        Input("data-values","data"),
        Input("radio-ha-costos-agricola","value"),
        Input("radio-costos-moneda","value"),
        Input("checklist-tipo-costos","value"),
        
    )
    def update_graph_recurso_agricola(data, radio_ha_costos, radio_moneda, checklist_tipo_costos):
        simbolo = "S/" if radio_moneda == 'SALDO_MOF' else "$"
        df = pd.DataFrame(data)
        costos_df=df[df['TIPO'].isin(checklist_tipo_costos)]
        
        costos_distribuido_df = costos_df.groupby(['IDCONSUMIDOR','CONSUMIDOR','CULTIVO','VARIEDAD','AREA_CAMPAÑA'])[[radio_moneda]].sum().reset_index()
        #costos_df_pivot = costos_df.pivot_table(index = ['CODCULTIVO','CULTIVO','VARIEDAD','AREA_CAMPAÑA','IDCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA'], values = radio_moneda, columns = 'TIPO',aggfunc='sum').fillna(0).reset_index()

        #costos_cultivo_df = costos_df.groupby(['CULTIVO'])[[radio_moneda]].sum().reset_index()
        total_card_1 = "{:,.2f}".format(costos_distribuido_df[radio_moneda].sum())
        list_cultivo = costos_distribuido_df['CULTIVO'].unique()
        total_costos_dict = create_dict_of_list(costos_distribuido_df,col=radio_moneda,dict_color = DICT_CULTIVOS_COLOR,list_partidas=list_cultivo,pivot=False,col_='CULTIVO')
        ################
        #ha_cultivo_df = costos_df_pivot.groupby(['CULTIVO'])[['AREA_CAMPAÑA']].sum().reset_index()
        total_card_2 = "{:,.2f}".format(costos_distribuido_df['AREA_CAMPAÑA'].sum())
        list_cultivo_ha=costos_distribuido_df['CULTIVO'].unique()
        total_dict_ha = create_dict_of_list(costos_distribuido_df,col='AREA_CAMPAÑA',dict_color = DICT_CULTIVOS_COLOR,list_partidas=list_cultivo_ha,pivot=False,col_='CULTIVO')
        ###########
        cotos_por_ha = "{:,.2f}".format((costos_distribuido_df[radio_moneda].sum())/(costos_distribuido_df['AREA_CAMPAÑA'].sum()))
        
        
        cultivo_df = create_dataframe_costos_tipo(df = costos_distribuido_df, category_col = ['CULTIVO'], numeric_col = [radio_moneda,'AREA_CAMPAÑA'], radio_tipo_costo = radio_ha_costos)
        variedad_df = create_dataframe_costos_tipo(df = costos_distribuido_df, category_col = ['VARIEDAD','CULTIVO'], numeric_col = [radio_moneda,'AREA_CAMPAÑA'], radio_tipo_costo = radio_ha_costos)
        lote_df = create_dataframe_costos_tipo(df = costos_distribuido_df, category_col = ['CONSUMIDOR','CULTIVO'], numeric_col = [radio_moneda,'AREA_CAMPAÑA'], radio_tipo_costo = radio_ha_costos)
      
        pie_tipo_gasto = costos_df.groupby('TIPO')[[radio_moneda]].sum().reset_index()
        if radio_ha_costos == 'por ha':
            pie_tipo_gasto[radio_moneda] = pie_tipo_gasto[radio_moneda]/costos_distribuido_df['AREA_CAMPAÑA'].sum()
            pie_tipo_gasto[radio_moneda] = pie_tipo_gasto[radio_moneda].round(2)
        df_map=costos_df[costos_df['POLYGON'].notnull()]
        df_map_polygon=df_map.groupby(['CONSUMIDOR','CULTIVO','VARIEDAD','POLYGON'])[['AREA_CAMPAÑA',radio_moneda]].sum().reset_index()
        
        return [
            cardDivider(value = f"{simbolo} {total_card_1}",text='Costos Totales',list_element=total_costos_dict),
            cardDivider(value = f"{total_card_2} ha",text='Hectáreas Sembradas',list_element=total_dict_ha),
            cardDivider(value = f"{simbolo} {cotos_por_ha}",text='Costo por Hectárea',list_element=[{'value': 100, 'color': "rgb(51, 102, 204)", 'label': '100%', "tooltip": "Costo por Hectárea"}]),
            GraphBargo.bar_(df = cultivo_df, x = radio_moneda , y = 'CULTIVO', text= radio_moneda, orientation = 'h', height = 485, title = 'Costos por Cultivo', space_ticked = 100,xaxis_title = simbolo,yaxis_title = 'CULTIVO',color_dataframe='CULTIVO',customdata=['AREA_CAMPAÑA']),
            GraphBargo.bar_(df = variedad_df, x = radio_moneda, y = 'VARIEDAD', text= radio_moneda, orientation = 'h', height = 485, title = 'Costos por Variedad', space_ticked = 100,xaxis_title = simbolo,yaxis_title = 'VARIEDAD',color_dataframe='CULTIVO',customdata=['AREA_CAMPAÑA']),
            GraphPiego.pie_(df = pie_tipo_gasto, title = 'Tipo de Costo',label_col = 'TIPO', value_col = radio_moneda, height = 280, dict_color = DICT_TIPO_COSTO),
            GraphMapgo.map_agricola_scatter(df = df_map_polygon, height = 300, importe = radio_moneda),
            GraphBargo.bar_(df = lote_df, x = 'CONSUMIDOR', y = radio_moneda, text= radio_moneda, orientation = 'v', height = 300, title = 'Costos por Lote', space_ticked = 30,xaxis_title = 'Lotes',yaxis_title = simbolo, showticklabel_x=False,color_dataframe='CULTIVO',customdata=['AREA_CAMPAÑA']),
        ]



"""
def create_title_ejecucion_campania(app, title ='',arg=None,variables=None):
    @app.callback(
        [Output("title","children")],
        [Input(filters,"value")for filters in arg]
    )
    def update_title(variables):
        #lista_variables=create_list_var(campania,variedad,lote)
        badges=[]
        for i in variables:
            if i != None:
                badges.append(dmc.Badge(i,variant='filled',color='gray', size='lg'))

        return dmc.Title(children=[title]+badges,order=2, align='center')    
            
"""