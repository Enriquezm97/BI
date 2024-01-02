from dash import Input, Output,State,no_update,dcc,html
from datetime import datetime, date, timedelta
from apps.graph.test.constans import COMERCIAL_SELECTS_COLUMNS,MESES_ORDER,LISTA_COLORES_BAR
from apps.graph.test.utils.functions.functions_filters import *
from apps.graph.test.utils.functions.functions_data import *
from apps.graph.test.utils.components.components_main import DataDisplay,Button
from apps.graph.test.utils.figures import *
from apps.graph.test.utils.frame import Graph
from apps.graph.test.utils.tables import tableDag
from apps.graph.test.utils.blocks.block_card import cardDivider
from apps.graph.test.utils.styles_ import *
import dash_mantine_components as dmc  


def create_callback_download_data(
    app,input_id_data="data-values",input_id_btn="btn-download",output="download", name_file="comercial.xlsx"
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
            return dcc.send_data_frame(df.to_excel, name_file, sheet_name="Sheet_name_1",index =False)




def  create_callback_filter_comercial_informe(
    app, dataframe=pd.DataFrame(), 
    rubro = ''
    ):
    if rubro =='Agricola':
        inp_out = ['select-anio','select-cliente','select-cultivo','select-variedad','select-grupo-cliente','select-producto']
    else:
        inp_out = ['select-anio','select-cliente','select-tipo-venta','select-grupo-producto','select-grupo-cliente','select-producto']
        
    @app.callback(
                 [Output(output_,'data')for output_ in inp_out]+
                 [
                  #Output('checklist-comercial-tipoventa','options'),
                  #Output('checklist-comercial-tipoventa','value'),   
                  Output("data-values","data"),
                  Output('chipgroup-mes','children'),
                  Output("notifications-update-data","children")],
                 [Input(input_,"value")for input_ in inp_out]  
                 )
    def update_filter_comercial_informe(*args):
        if validar_all_none(variables = args) == True:
            df=dataframe.copy()
        else:
            df=dataframe.query(dataframe_filtro(values=list(args),columns_df=create_col_for_dataframe(id_components = inp_out, dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)))
        print('here')
        print(df.columns)
        return create_list_dict_outputs(dataframe = df,id_components = inp_out, dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)+[
               #[{'label': i, 'value': i} for i in sorted(df['Tipo de Venta'].unique())],
               #sorted(df['Tipo de Venta'].unique()),
               df.to_dict('series'),
               [dmc.Chip(x,value=x,variant="outline",radius= 'xs',styles=styles_chip)for x in order_mes_text(df['Mes'].unique())],
               DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),  
        ]   


def create_title_comercial_informe(app, title ='', rubro = '',id_inputs = ['select-anio','select-cliente','select-cultivo','select-variedad','select-moneda']):
    if rubro =='Agricola':
        id_inputs = ['select-anio','select-cliente','select-cultivo','select-variedad','select-grupo-cliente','select-producto','select-moneda']
    else:
        id_inputs = ['select-anio','select-cliente','select-tipo-venta','select-grupo-producto','select-grupo-cliente','select-producto','select-moneda']
        
    @app.callback(
        Output("title","children"),
        [Input(input_,"value")for input_ in id_inputs]
          
    )
    def update_title(*args):
        
        if validar_all_none(variables = args) == True:
            return dmc.Title(children=[title],order=2,align='center')
        else:
            badges=[]
            for i in args:
                if i != None:
                    badges.append(dmc.Badge(i,variant='dot',color='blue', size='lg',radius="lg"))
            return dmc.Title(children=[title]+badges,order=2,align='center')#,style={"margin-left":"35px"}
    
def create_graph_informe_comercial(app):
    @app.callback(
        #Output('pie-comercial-selector_first','figure'),
        #Output('pie-comercial-selector_second','figure'),
        Output('bar-comercial-productos','figure'),
        Output('bar-comercial-mes','figure'),
        Output('funnel-comercial-selector_second','figure'),
        Output('pie-comercial-pais','figure'),
        Output('pie-comercial-vendedor','figure'),
        
        #bar-comercial-mes
        Input("data-values","data"),
        Input('select-moneda',"value"),
        Input('chipgroup-mes',"value"),
        Input('radio-paleta-color','value'),
        Input('slider-size-tickfont','value'),
        Input('first-pie','n_clicks'),
        Input('first-bar','n_clicks'),
        
        #Input('checklist-comercial-tipoventa','value'),
    )
    def update_graph_informe_comercial(*args):
        size_ticked = int(args[4])
        simbolo = "S/" if args[1] == 'Importe Soles' else "$"
        importe = args[1]#"IMPORTEMOF" if args[1] == 'Soles' else "IMPORTEMOF"
        df = pd.DataFrame(args[0])
        #df = df[df['Tipo de Venta'].isin(args[5])]
        
        
        
        if args[2] != None and len(args[2])==0:
            df = df.copy()
        elif args[2] != None:
            df = df[df['Mes'].isin(args[2])]
        else:
            df = df.copy()
        
        if args[3] == 'Plotly':
            lista_colores = px.colors.diverging.Portland+px.colors.diverging.Earth+px.colors.diverging.balance+px.colors.diverging.Tealrose#px.colors.diverging.Portland#px.colors.qualitative.Alphabet
            
        elif args[3] == 'G10':
            lista_colores = px.colors.qualitative.Dark24
        elif args[3] == 'Bold':
            lista_colores = px.colors.qualitative.Light24
        
        productos_df_20=df.groupby(['Producto','Grupo Producto','Subgrupo Producto'])[[importe]].sum().sort_values(importe,ascending=True).tail(20).reset_index()
        productos_df_20['Producto']=productos_df_20['Producto'].str.capitalize()
        
        
        grupo_producto_df = df.groupby(['Grupo Producto'])[[importe]].sum().reset_index().round(2)
        grupo_producto_df=grupo_producto_df[grupo_producto_df[importe]>0].sort_values(importe, ascending = False)
        
        meses_df_12 = df.groupby(['Mes','Mes Num'])[[importe]].sum().reset_index().sort_values('Mes Num',ascending=True).reset_index()
        meses_df_12['Porcentaje']=(meses_df_12[importe]/meses_df_12[importe].sum())*100
        meses_df_12['Porcentaje']=meses_df_12['Porcentaje'].map('{:,.1f}%'.format)
        #df[importe].map('{:,.1f}%'.format)
        pais_df = df.groupby(['Pais'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
        vendedor_df = df.groupby(['Vendedor'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
        if args[6] == 0:
            graph1_ =GraphBargo.bar_(df=productos_df_20, x= importe, y= 'Producto',orientation= 'h', height = 400, 
               title= 'Los 20 Productos más Vendidos', customdata=['Grupo Producto','Subgrupo Producto'],space_ticked= 280, text= importe,
               showticklabel_y=True, 
               xaxis_title = importe, template= 'none', list_or_color=   lista_colores,size_tickfont=size_ticked#px.colors.qualitative.Alphabet
            )
        elif args[5]:
            graph1_ = GraphPiego.pie_(df = productos_df_20, title = 'Los 20 Productos más Vendidos',label_col = 'Producto', value_col = importe, height = 400, showlegend=False, color_list=lista_colores,#px.colors.qualitative.Set3, 
                            textfont_size = 10)
        return[
            graph1_,
            GraphBargo.bar_(df=meses_df_12, x= 'Mes', y= importe,orientation= 'v', height = 400, 
                title= 'Ventas por Mes', customdata=['Porcentaje'],space_ticked= 50, text= importe, yaxis_title= importe,xaxis_title= 'Mes',
                template='none',list_or_color=   lista_colores,size_tickfont=size_ticked#px.colors.qualitative.Set3
            ),
            GraphFunnelgo.funnel_(df = grupo_producto_df, x = importe, y = 'Grupo Producto', height = 400,xaxis_title = importe, yaxis_title = 'Grupo Producto', title = 'Grupo Producto mas vendido',list_or_color=lista_colores,size_tickfont=size_ticked),
            GraphPiego.pie_(df = pais_df, title = 'Ventas - País',label_col = 'Pais', value_col = importe, height = 400, showlegend=False, color_list=lista_colores,#px.colors.qualitative.Set3, 
                            textfont_size = 10),
            GraphPiego.pie_(df = vendedor_df, title = 'Ventas - Vendedor',label_col = 'Vendedor', value_col = importe, height = 400, showlegend=False, color_list=lista_colores,#px.colors.qualitative.Set3, 
                            textfont_size = 10),
        ]
           
        
        
################### DASHBOARD SEGMENTED
#['Año','Cliente','Cultivo','Variedad','Grupo Producto','Moneda']
def  create_callback_filter_comercial_segmented(app, dataframe=pd.DataFrame(), id_inputs = [],id_outputs = []):
        @app.callback(
                    [Output(output_,'data')for output_ in id_outputs]+
                    [
                    #Output('checklist-comercial-tipoventa','options'),
                    #Output('checklist-comercial-tipoventa','value'),   
                    Output("data-values","data"),
                    Output('chipgroup-mes','children'),
                    Output("notifications-update-data","children")],
                    [Input(input_,"value")for input_ in id_inputs]  
                    )
        def update_filter_comercial_informe(*args):
            if validar_all_none(variables = args) == True:
                df=dataframe.copy()
            else:
                df=dataframe.query(dataframe_filtro(values=list(args),columns_df=create_col_for_dataframe(id_components = id_inputs, dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)))
            
            test_outs= create_list_dict_outputs(dataframe = df,id_components = id_inputs, dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)
            
            return test_outs+[
                #[{'label': i, 'value': i} for i in sorted(df['Tipo de Venta'].unique())],
                #sorted(df['Tipo de Venta'].unique()),
                df.to_dict('series'),
                [dmc.Chip(x,value=x,variant="outline",radius= 'xs',styles=styles_chip)for x in order_mes_text(df['Mes'].unique())],
                DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),  
            ]   
        
def create_graph_comercial_segmented(app):
    @app.callback(
        #Output('pie-comercial-selector_first','figure'),
        #Output('pie-comercial-selector_second','figure'),
        Output('line-comercial-st','figure'),
        Output('pie-comercial','figure'),
        Output('bar-comercial','figure'),
       
        
        #bar-comercial-mes
        Input("data-values","data"),
        Input('select-moneda',"value"),
        Input('chipgroup-mes',"value"),
        Input('segmented-st',"value"),
        Input('segmented-pie',"value"),
        Input('segmented-bar',"value"),
        
        Input('checkbox-ticked',"checked"),
        Input('slider-percent',"value"),
        #Input('radio-paleta-color','value'),
        #Input('slider-size-tickfont','value'),
        #Input('checklist-comercial-tipoventa','value'),
    )
    def update_graph_comercial_segmented(*args):
        df = pd.DataFrame(args[0])
        importe = args[1]
        list_meses= args[2]
        segmented_st = args[3]
        segmented_pie = args[4]
        segmented_bar = args[5]
        checkedbox_ticked = args[6]
        porcentaje_value = args[7]
        
        if  list_meses!= None and len(list_meses)==0:
            df = df.copy()
        elif list_meses != None:
            df = df[df['Mes'].isin(list_meses)]
        else:
            df = df.copy()

        if segmented_st == 'Mes':
            serie_time_df = df.groupby([segmented_st,'Mes Num'])[[importe]].sum().reset_index().sort_values('Mes Num',ascending=True)
        else:
            serie_time_df = df.groupby([segmented_st])[[importe]].sum().reset_index()
        
        pie_df = df .groupby([segmented_pie])[[importe]].sum().round(1).reset_index()
        
        bar_df = df .groupby([segmented_bar])[[importe]].sum().sort_values(importe,ascending=False).reset_index()
        bar_dfoW=bar_df.copy()
        bar_df['Porcentaje %']=bar_df[importe]/bar_df[importe].sum()
        bar_df['Porcentaje Acumulado']=bar_df['Porcentaje %'].cumsum(axis = 0, skipna = True) 
        bar_df['Porcentaje %'] = bar_df['Porcentaje %']*100
        bar_df['Porcentaje Acumulado'] = bar_df['Porcentaje Acumulado'] *100
        bar_df=bar_df[bar_df['Porcentaje Acumulado']<=porcentaje_value]
        bar_df['Porcentaje %'] = bar_df['Porcentaje %'].round(1)
        size_bottom_bar = 130 if checkedbox_ticked ==  True else 30
        return [
            GraphLinepx.line_(df = serie_time_df, x = segmented_st, y = importe, height=300, y_title = importe,title = f'Serie de Tiempo - {segmented_st}',markers = True, hover_template= '<br>'+segmented_st+': <b>%{x}</b><br>'+importe+':<b> %{y:,.2f}</b>',size_text=15),
            GraphPiego.pie_(df = pie_df, label_col= segmented_pie, value_col= importe, title = segmented_pie),
            GraphBargo.bar_(df = bar_df,x = segmented_bar, y= importe,text= importe, height=400, title = segmented_bar, yaxis_title=importe,showticklabel_x = checkedbox_ticked,space_ticked = size_bottom_bar, customdata=['Porcentaje %'])
        ]
    
            
        

def  create_callback_filter_comercial_ventas(app, dataframe=pd.DataFrame(), id_inputs = [],id_outputs = []):
        @app.callback(
                    [Output(output_,'data')for output_ in id_outputs]+
                    [
                    
                    Output("data-values","data"),
                    
                    Output("notifications-update-data","children")],
                    [Input(input_,"value")for input_ in id_inputs]+
                    [Input('datepicker-inicio',"value"),Input('datepicker-fin',"value")]
                    )
        def update_filter_comercial_informe(*args):
            
            datepicker_inicio = datetime.strptime(args[-2], '%Y-%m-%d').date()
            datepicker_fin = datetime.strptime(args[-1], '%Y-%m-%d').date()
            inputs = args[:-2]
            filter_datepicker_df = dataframe[(dataframe['Fecha']>=datepicker_inicio)&(dataframe['Fecha']<=datepicker_fin)]
            if validar_all_none(variables = inputs) == True:
                df=filter_datepicker_df.copy()
            else:
                df=filter_datepicker_df.query(dataframe_filtro(values=list(inputs),columns_df=create_col_for_dataframe(id_components = id_inputs, dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)))
            
            test_outs= create_list_dict_outputs(dataframe = df,id_components = id_inputs, dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)
            
            return test_outs+[
                df.to_dict('series'),
                DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),  
            ]   

def create_graph_comercial_bar(app, columns_top = 'Cliente'):
    @app.callback(
        Output('bar-comercial','figure'),
        
        Input("data-values","data"),
        Input('select-moneda',"value"),
        Input("slider-percent",'value')
        
    )
    def update_graph_comercial(*args):
        df = pd.DataFrame(args[0])
        importe = args[1]
        value_slider = args[2]
        
        num = round(len(df[columns_top].unique())*(int(value_slider)/100))
        
        bar_df = df.groupby([columns_top])[[importe]].sum().sort_values(importe,ascending=True).reset_index().tail(num)#tail(num)
        return GraphBargo.bar_(df=bar_df,x=importe,y=columns_top,orientation='h',text=importe,title=f'{columns_top}s Top ({value_slider}%)',height=800,clickmode=True,color_dataframe='#0d6efd')
            #f"{sig} {(round(importe_total,0)):,}",clientes_total
            
        
#px.colors.diverging.Portland+px.colors.diverging.Earth+px.colors.diverging.balance+px.colors.diverging.Tealrose
def create_graph_comercial_crossfiltering(app,column = 'Cliente'):
    @app.callback(
       
        Output('bar-secundario-comercial',"figure"),
        Output('line-comercial-st',"figure"),
        Output('card-1',"children"),
        Output('card-2',"children"),
        Output('card-3',"children"),
        Output('card-4',"children"),
        #Output('card-total',"children"),
        Input("data-values","data"),
        Input('select-moneda',"value"),
        Input('bar-comercial','selectedData'),
        Input('segmented-bar-categoria','value'),
        Input('segmented-st','value'),
    )
    def update_graph_comercial(*args):
        df = pd.DataFrame(args[0])
        importe = args[1]
        dict_cliente = args[2]#['points'][0]['y']
        col_segmented_categoria= args[3]
        col_segmented_st = args[4]
        
        sig="$"if importe =='Importe Dolares' else "S/"
        
        if dict_cliente == None:
            card_1 = df[importe].sum()
            card_2=len(df[column].unique())
            card_3 = len(df['Pais'].unique())
            card_4 = len(df['Vendedor'].unique())
            
            bar_df = df.groupby([col_segmented_categoria])[[importe]].sum().sort_values(importe,ascending=True).reset_index().tail(10)
            title = f'Top 10 - {col_segmented_categoria}'
            if col_segmented_st == 'Mes':
                serie_time_df = df.groupby([col_segmented_st,'Mes Num'])[[importe]].sum().reset_index().sort_values('Mes Num',ascending=True)
            else:
                serie_time_df = df.groupby([col_segmented_st])[[importe]].sum().reset_index()
            
            #LISTA_COLORES_BAR
            lista_ejey = bar_df[col_segmented_categoria].unique()
            dict_colors = dict(zip(lista_ejey, LISTA_COLORES_BAR[:len(lista_ejey)]))
            figure_line_st = GraphLinepx.line_(df = serie_time_df, x = col_segmented_st, y = importe, height=300, y_title = importe,x_title=col_segmented_st,title = f'Serie de Tiempo - {col_segmented_st}',markers = True, hover_template= '<br>'+col_segmented_st+': <b>%{x}</b><br>'+importe+':<b> %{y:,.2f}</b>',size_text=15)
        else:
            column_obj = dict_cliente['points'][0]['y']
            bar_filter_df = df[df[column]==column_obj]
            card_1 = dict_cliente['points'][0]['value']
            card_2=len(bar_filter_df[column].unique())
            card_3 = len(bar_filter_df['Pais'].unique())
            card_4 = len(bar_filter_df['Vendedor'].unique())
            
            bar_df= bar_filter_df.groupby([col_segmented_categoria])[[importe]].sum().sort_values(importe,ascending=True) .reset_index()
            title = f'{col_segmented_categoria}({column_obj})'
            
            if col_segmented_st == 'Mes':
                serie_time_df = bar_filter_df.groupby([col_segmented_st,'Mes Num',col_segmented_categoria])[[importe]].sum().reset_index().sort_values('Mes Num',ascending=True)
            else:
                serie_time_df = bar_filter_df.groupby([col_segmented_st,col_segmented_categoria])[[importe]].sum().reset_index()

            lista_ejey = bar_df[col_segmented_categoria].unique()
            dict_colors = dict(zip(lista_ejey, LISTA_COLORES_BAR[:len(lista_ejey)]))
            
            figure_line_st = GraphLinepx.line_(df = serie_time_df, x = col_segmented_st, y = importe, color= col_segmented_categoria,height=300, y_title = importe,x_title=col_segmented_st,title = f'Ventas por {col_segmented_st} por {col_segmented_categoria} ({column_obj})',markers = True, hover_template= '<br>'+col_segmented_st+': <b>%{x}</b><br>'+importe+':<b> %{y:,.2f}</b>',size_text=15,legend_orizontal=False,legend_font_size = 9,
                                               order={col_segmented_st : sorted(df[col_segmented_st].unique()),col_segmented_categoria :sorted(df [col_segmented_categoria])}if col_segmented_st != 'Mes'else {'Mes' : MESES_ORDER,col_segmented_categoria :sorted(df [col_segmented_categoria])},discrete_color=dict_colors)
            #f"{sig} {(round(importe_total,0)):,}",clientes_total
        

        return [
            GraphBargo.bar_(df=bar_df,x=importe,y=col_segmented_categoria,orientation='h',text=importe,title=title,height=300, xaxis_title=importe,title_font_size=15, list_or_color=dict_colors),
            figure_line_st,
            f"{sig} {(round(card_1,0)):,}",card_2,card_3,card_4
        ]

def  create_callback_filter_comercial_simple(
    app, dataframe=pd.DataFrame(), 
    id_inputs = ['select-anio','select-cliente','select-cultivo','select-variedad','select-grupo-cliente','select-producto'], 
    id_outputs = ['select-anio','select-cliente','select-cultivo','select-variedad','select-grupo-cliente','select-producto']
    ):
    @app.callback(
                 [Output(output_,'data')for output_ in id_outputs]+
                 [
                  #Output('checklist-comercial-tipoventa','options'),
                  #Output('checklist-comercial-tipoventa','value'),   
                  Output("data-values","data"),
                  Output("notifications-update-data","children")],
                 [Input(input_,"value")for input_ in id_inputs]  
                 )
    def update_filter_comercial_informe(*args):
        if validar_all_none(variables = args) == True:
            df=dataframe.copy()
        else:
            df=dataframe.query(dataframe_filtro(values=list(args),columns_df=create_col_for_dataframe(id_components = id_inputs, dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)))

        return create_list_dict_outputs(dataframe = df,id_components = id_inputs, dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)+[
               df.to_dict('series'),
               DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),  
        ]   
        
def callback_table_interactive(app,list_empty = [],dict_year = {}):
        @app.callback(
                Output("tabla-interactiva","rowData"),
                Output("tabla-interactiva","columnDefs"),
                Output("pie-year-comparativo","figure"),
                Input("data-values","data"),
                Input("multiselect-year","value"),
                #Input("segmented-st","value"),
                Input('select-moneda',"value"),
                Input("tabla-interactiva", "selectedRows"),

            )
        def update_ventas(*args):
            df=pd.DataFrame(args[0])
            year_list = args[1]
            #segmented_st = args[2]
            moneda = args[2]
            year_selected = args[3]
            
            
            df['Año']=df['Año'].astype("string")
            
            
            if year_list == [] or year_list == None:
                dff=df[df['Año'].isin(year_list[-1])]
            #elif year_list == []:
            #    df=options[options['Año'].isin(years[-1])]
            elif year_list != None:
                dff=df[df['Año'].isin(year_list)]
            
            table_df = dff.groupby(['Año'])[[moneda]].sum().reset_index()
            pie_df = dff.groupby(['Año'])[[moneda]].sum().reset_index()
            table_df[moneda] = table_df[moneda].round(1)
            table_df[moneda] = table_df.apply(lambda x: "{:,}".format(x[moneda]), axis=1)
            
            year_selected_list = [s["Año"] for s in year_selected] if year_selected!=None else []
            
            if year_selected_list == []:
                list_empty.clear()
                columnsdef=[{"field": 'Año',"checkboxSelection": True},{"field": moneda}]
            elif year_selected_list!=[]:
                value_seleccionado=valueSelectElementTable(selected=year_selected_list,list_add=list_empty)
                columnsdef=[{"field": 'Año', "type": "rightAligned","checkboxSelection": True, "cellClassRules":{"bg-primary": f"params.value == '{value_seleccionado}'"} },{"field": moneda, "type": "rightAligned"}]                    
            
            
            
            return [table_df.to_dict("records"),columnsdef,
                    GraphPiego.pie_(df = pie_df, title = 'Ventas por Año',label_col = 'Año', value_col = moneda, height = 350, showlegend=False, dict_color= dict_year,textfont_size = 10),
                    
            ]
        

def graphPinta2(df,element_seleccionado,lista_iteracion,lista_order_year,ejex,importe,selected_list,dict_year):
    if ejex == 'Mes Num':
        name_eje = 'Mes'
        hover_selected_bar='<br><b>Mes </b>:%{x}'+'<br><b>Importe</b>: %{y:$,.0f}<br>'
        hover_selected_linea ='<br><b>Mes </b>:%{x}'+'<br><b>Cremimiento </b>: %{y}%<br>'
    elif ejex == 'Trimestre_':
        name_eje = 'Trimestre'
        hover_selected_bar='<br><b>Trimestre </b>:%{x}'+'<br><b>Importe</b>: %{y:$,.0f}<br>'
        hover_selected_linea ='<br><b>Trimestre </b>:%{x}'+'<br><b>Cremimiento </b>: %{y}%<br>'
    elif ejex == 'Semana_': 
        name_eje = 'Semana'
        hover_selected_bar='<br><b>Semana </b>:%{x}'+'<br><b>Importe</b>: %{y:$,.0f}<br>'
        hover_selected_linea ='<br><b>Semana </b>:%{x}'+'<br><b>Cremimiento </b>: %{y}%<br>'
    
    num_opacidad= 0.9 if selected_list!=[] else 1
    fig = go.Figure()
    if selected_list !=[]:
        fig.add_trace(go.Bar(x=df[ejex],
                                y=df[element_seleccionado],
                                name=element_seleccionado,
                                marker_color=dict_year[element_seleccionado],
                                #customdata=dict_year['year']==selected_list[-1],
                                text=df[element_seleccionado],
                                textposition="outside",
                                texttemplate='%{text:,.0f}',
                                hovertemplate =hover_selected_bar,
                                textfont=dict(size=16),
                                cliponaxis=False,
                                )) 
        fig.update_traces(marker_line_width=2, marker_line_color='black')#,marker_pattern_shape="+"
    for year in lista_iteracion:
        fig.add_trace(
                go.Bar(
                        x=df[ejex],
                        y=df[year],
                        name=year,
                        marker_color=dict_year[year],
                        text=df[year],
                        textposition="outside",
                        texttemplate='%{text:,.0f}',
                        hovertemplate =hover_selected_bar,#'<br><b>Mes </b>:%{x}'+'<br><b>Importe</b>: %{y:$,.0f}<br>',
                        textfont=dict(size=16),
                        opacity=num_opacidad,
                        cliponaxis=False,
                        )
                    )
    fig.update_layout(
            title=f'<b>Comparativo {name_eje} por año</b>',
            title_font_family="sans-serif", 
            xaxis_tickfont_size=15,
            yaxis=dict(
                title='<b>'+importe+'</b>',
                titlefont_size=16,
                tickfont_size=14,
                title_font_family="sans-serif"
            ),
            xaxis=dict(
                title='<b>'+name_eje+'</b>',
                titlefont_size=16,
                tickfont_size=14,
                title_font_family="sans-serif"
            ),
            legend=dict(orientation="h",yanchor="bottom",xanchor="right",y=1.02,x=1),
            barmode='group',
            bargap=0.15, # gap between bars of adjacent location coordinates.0.15
            bargroupgap=0.1, # gap between bars of the same location coordinate.
            template='plotly_white',
            margin=dict(l=40,r=40,b=40,t=40),
            height=380
        )
    fig.update_xaxes(type='category')
    fig.update_layout(
                yaxis2=dict(
                    title="%",
                    overlaying="y",
                    side="right",
                    titlefont_size=16,
                    tickfont_size=14,
                )
    )
    #### trazo de linea
    if selected_list ==[]:
        print("condicion line 1")
        fig.add_trace(
            go.Scatter(
                x=df[ejex], 
                y=df[f'% - {lista_order_year[0]}'], 
                name=f"Crecimiento-{lista_order_year[0]}", 
                yaxis="y2",
                text=df[f'% - {lista_order_year[0]}'],
                textposition="bottom center",
                marker_color=px.colors.qualitative.Prism[1],
                hovertemplate =hover_selected_linea,
                mode='lines+markers',
                cliponaxis=False,
                ))
    elif len(selected_list)==1:
        print("condicion line 2")
        lista_rango_=deleteElementList(selected_list,element_seleccionado)
        for year_percents,i in zip(lista_rango_,range(len(lista_rango_))):
            fig.add_trace(
                 go.Scatter(
                    x=df[ejex], 
                    y=df[f'% - {year_percents}'], 
                    name=f"Crecimiento-{year_percents}", 
                    yaxis="y2",
                    text=df[f'% - {year_percents}'],
                    cliponaxis=False,
                    textposition="bottom center",
                    marker_color=px.colors.qualitative.Dark2[i],
                    hovertemplate =hover_selected_linea,
                    mode='lines+markers',line=dict(color=px.colors.qualitative.Dark2[i], width=3)
                    ))
    

    elif selected_list !=[] and len(selected_list)>1:
        print("condicion line 3")
        lista_rango_=deleteElementList(selected_list,element_seleccionado)
        for year_percents,i in zip(lista_rango_,range(len(lista_rango_))):
            fig.add_trace(
                 go.Scatter(
                    x=df[ejex], 
                    y=df[f'% - {year_percents}'], 
                    name=f"Crecimiento-{year_percents}", 
                    yaxis="y2",
                    text=df[f'% - {year_percents}'],
                    textposition="bottom center",
                    cliponaxis=False,
                    marker_color=px.colors.qualitative.Dark2[i],
                    hovertemplate =hover_selected_linea,
                    mode='lines+markers',line=dict(color=px.colors.qualitative.Dark2[i], width=3)
                    ))
    return fig
    
 
def callback_table_resultado(app, list_for_graph = [], dict_colors = {}):
        @app.callback(
                Output("tabla-resultado","columnDefs"),
                Output("tabla-resultado","rowData"),
                Output("tabla-resultado","defaultColDef"),
                Output("bar-st-comparativo","figure"),
                Input("data-values","data"),
                Input("multiselect-year","value"),
                Input("segmented-st","value"),
                Input('select-moneda',"value"),
                Input("tabla-interactiva", "selectedRows"),

            )
        def update_ventas(*args):
            df=pd.DataFrame(args[0])
            year_list = args[1]
            segmented_st = args[2]
            print(segmented_st)
            moneda = args[3]
            year_selected = args[4]
            df['Año']=df['Año'].astype("string")
            if year_list == [] or year_list == None:
                dff=df[df['Año'].isin(year_list[-1])]
            elif year_list != None:
                dff=df[df['Año'].isin(year_list)]
                
            # lista con los elementos seleccionados de la tabla interactiva    
            year_selected_list = [s["Año"] for s in year_selected] if year_selected!=None else []
            
            print(segmented_st)#puede ser mes,trimestral o semanal
            principal_df = dff.groupby(['Año',segmented_st])[[moneda]].sum().reset_index()
            year_list_sorted = sorted(year_list)# ordena los valorews de entrada del multiselect
        
            principal_pivot_df = pd.pivot_table(principal_df, values=moneda, index=[segmented_st], columns=['Año']).fillna(0).reset_index()
            
            
            columnas_years_table=list(principal_pivot_df.columns[1:len(year_list)+1])
            print(columnas_years_table)
            
            try:
                first_year_multiselect = year_list_sorted[0]# primer elemento del multiselect ordenado de menor a mayor
                last_year_multiselect = year_list_sorted[-1]# ultimo elemento del multiselect ordenado de menor a mayor
                size_year_selected = len(year_selected_list)# tamaño de la lista de la tabla principal
            except:
                pass
            
            if year_selected_list == []:
                list_for_graph.clear()
                lista_iteracion = columnas_years_table
                principal_pivot_df[f"dif - {first_year_multiselect}"] = principal_pivot_df[last_year_multiselect] - principal_pivot_df[first_year_multiselect]
                principal_pivot_df[f"% - {first_year_multiselect}"] = (principal_pivot_df[f"dif - {first_year_multiselect}"]/principal_pivot_df[first_year_multiselect])*100
                principal_pivot_df[f"% - {first_year_multiselect}"] = principal_pivot_df[f"% - {first_year_multiselect}"].round(1)
                pinta_columna_year_select = last_year_multiselect
            elif  size_year_selected == 1:
                value_seleccionado = valueSelectElementTable(selected=year_selected_list,list_add=list_for_graph)
                lista_iteracion = deleteElementList(lista =columnas_years_table,elemento_eliminar= value_seleccionado)##
                principal_pivot_df[f"dif - {first_year_multiselect}"] = principal_pivot_df[last_year_multiselect] - principal_pivot_df[first_year_multiselect]
                principal_pivot_df[f"% - {first_year_multiselect}"] = (principal_pivot_df[f"dif - {first_year_multiselect}"]/principal_pivot_df[first_year_multiselect])*100
                principal_pivot_df[f"% - {first_year_multiselect}"] = principal_pivot_df[f"% - {first_year_multiselect}"].round(1)
                pinta_columna_year_select = value_seleccionado
            elif  size_year_selected == 2:
                value_seleccionado = valueSelectElementTable(selected=year_selected_list,list_add=list_for_graph)
                lista_iteracion = deleteElementList(lista =year_selected_list,elemento_eliminar= value_seleccionado)##
                primer_elemento_lista_iteracion = lista_iteracion[0]
                principal_pivot_df[f"dif - {primer_elemento_lista_iteracion}"] = principal_pivot_df[value_seleccionado] - principal_pivot_df[primer_elemento_lista_iteracion]
                principal_pivot_df[f"% - {primer_elemento_lista_iteracion}"] = (principal_pivot_df[f"dif - {primer_elemento_lista_iteracion}"]/ principal_pivot_df[primer_elemento_lista_iteracion])*100
                principal_pivot_df[f"% - {primer_elemento_lista_iteracion}"] =  principal_pivot_df[f"% - {primer_elemento_lista_iteracion}"].round(1)
                pinta_columna_year_select = value_seleccionado
            
            elif  year_selected_list != [] and size_year_selected>2:
                value_seleccionado = valueSelectElementTable(selected=year_selected_list,list_add=list_for_graph)
                lista_iteracion = deleteElementList(lista =year_selected_list,elemento_eliminar= value_seleccionado)##
                for year_iteracion in lista_iteracion:
                    year_iteracion = str(year_iteracion)
                    principal_pivot_df[f"dif - {year_iteracion}"] = principal_pivot_df[value_seleccionado] - principal_pivot_df[year_iteracion]
                    principal_pivot_df[f"% - {year_iteracion}"] = (principal_pivot_df[f"dif - {year_iteracion}"]/ principal_pivot_df[year_iteracion])*100
                    principal_pivot_df[f"% - {year_iteracion}"] =  principal_pivot_df[f"% - {year_iteracion}"].round(1)
                pinta_columna_year_select = value_seleccionado
            principal_pivot_df = principal_pivot_df.replace([np.inf, -np.inf], 0)
            defaultColDef=dict(resizable=True,sortable= True, filter = True,cellStyle={"styleConditions": [{"condition": f"params.colDef.field == {pinta_columna_year_select}","style": {"backgroundColor": f"#1f77b4", "color": "white"}}]})
            table_df = principal_pivot_df.copy()
            for columns in table_df.columns[1:]:
                table_df[columns]=table_df[columns].round(1)
                table_df[columns] = table_df.apply(lambda x: "{:,}".format(x[columns]), axis=1)
           
            return [[{"field": i,"maxWidth": 130, "type": "rightAligned"} for i in table_df.columns],
                    table_df.to_dict("records"),defaultColDef,
                    graphPinta2(df = principal_pivot_df,
                                element_seleccionado = pinta_columna_year_select,
                                lista_iteracion = lista_iteracion,
                                lista_order_year = year_list_sorted,
                                ejex = segmented_st,
                                importe = moneda,
                                selected_list = year_selected_list,
                                dict_year =dict_colors
                    )
            ]