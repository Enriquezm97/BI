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
    id_inputs = ['select-anio','select-cliente','select-cultivo','select-variedad','select-grupo-cliente','select-producto'], 
    id_outputs = ['select-anio','select-cliente','select-cultivo','select-variedad','select-grupo-cliente','select-producto']
    ):
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

        return create_list_dict_outputs(dataframe = df,id_components = id_inputs, dict_cols_dataframe=COMERCIAL_SELECTS_COLUMNS)+[
               #[{'label': i, 'value': i} for i in sorted(df['Tipo de Venta'].unique())],
               #sorted(df['Tipo de Venta'].unique()),
               df.to_dict('series'),
               [dmc.Chip(x,value=x,variant="outline",radius= 'xs',styles=styles_chip)for x in order_mes_text(df['Mes'].unique())],
               DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update'),  
        ]   


def create_title_comercial_informe(app, title ='', rubro_empresa = '',id_inputs = ['select-anio','select-cliente','select-cultivo','select-variedad','select-moneda']):
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
        
        
        return[
            GraphBargo.bar_(df=productos_df_20, x= importe, y= 'Producto',orientation= 'h', height = 400, 
               title= 'Los 20 Productos más Vendidos', customdata=['Grupo Producto','Subgrupo Producto'],space_ticked= 280, text= importe,
               showticklabel_y=True, 
               xaxis_title = importe, template= 'none', list_or_color=   lista_colores,size_tickfont=size_ticked#px.colors.qualitative.Alphabet
            ),
            GraphBargo.bar_(df=meses_df_12, x= 'Mes', y= importe,orientation= 'v', height = 320, 
                title= 'Ventas por Mes', customdata=['Porcentaje'],space_ticked= 50, text= importe, yaxis_title= importe,xaxis_title= 'Mes',
                template='none',list_or_color=   lista_colores,size_tickfont=size_ticked#px.colors.qualitative.Set3
            ),
            GraphFunnelgo.funnel_(df = grupo_producto_df, x = importe, y = 'Grupo Producto', height = 400,xaxis_title = importe, yaxis_title = 'Grupo Producto', title = 'Grupo Producto mas vendido',list_or_color=lista_colores,size_tickfont=size_ticked),
            GraphPiego.pie_(df = pais_df, title = 'Ventas - País',label_col = 'Pais', value_col = importe, height = 310, showlegend=False, color_list=lista_colores,#px.colors.qualitative.Set3, 
                            textfont_size = 10),
            GraphPiego.pie_(df = vendedor_df, title = 'Ventas - Vendedor',label_col = 'Vendedor', value_col = importe, height = 310, showlegend=False, color_list=lista_colores,#px.colors.qualitative.Set3, 
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

def create_graph_comercial_bar(app):
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
        
        num = round(len(df['Cliente'].unique())*(int(value_slider)/100))
        print(num)
        bar_df = df.groupby(['Cliente'])[[importe]].sum().sort_values(importe,ascending=True).reset_index().tail(num)#tail(num)
        return GraphBargo.bar_(df=bar_df,x=importe,y='Cliente',orientation='h',text=importe,title=f'Clientes Top ({value_slider}%)',height=800,clickmode=True,color_dataframe='#0d6efd')
            #f"{sig} {(round(importe_total,0)):,}",clientes_total
            
        
#px.colors.diverging.Portland+px.colors.diverging.Earth+px.colors.diverging.balance+px.colors.diverging.Tealrose
def create_graph_comercial_crossfiltering(app):
    @app.callback(
       
        Output('bar-secundario-comercial',"figure"),
        Output('line-comercial-st',"figure"),
        Output('card-total',"children"),
        Output('card-clientes',"children"),
        Output('card-pais',"children"),
        Output('card-vendedor',"children"),
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
            importe_total = df[importe].sum()
            clientes_total=len(df['Cliente'].unique())
            pais_total = len(df['Pais'].unique())
            vendedor_total = len(df['Vendedor'].unique())
            
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
            cliente = dict_cliente['points'][0]['y']
            bar_filter_df = df[df['Cliente']==cliente]
            importe_total = dict_cliente['points'][0]['value']
            clientes_total=len(bar_filter_df['Cliente'].unique())
            pais_total = len(bar_filter_df['Pais'].unique())
            vendedor_total = len(bar_filter_df['Vendedor'].unique())
            
            bar_df= bar_filter_df.groupby([col_segmented_categoria])[[importe]].sum().sort_values(importe,ascending=True) .reset_index()
            title = f'{col_segmented_categoria}({cliente})'
            
            if col_segmented_st == 'Mes':
                serie_time_df = bar_filter_df.groupby([col_segmented_st,'Mes Num',col_segmented_categoria])[[importe]].sum().reset_index().sort_values('Mes Num',ascending=True)
            else:
                serie_time_df = bar_filter_df.groupby([col_segmented_st,col_segmented_categoria])[[importe]].sum().reset_index()

            lista_ejey = bar_df[col_segmented_categoria].unique()
            dict_colors = dict(zip(lista_ejey, LISTA_COLORES_BAR[:len(lista_ejey)]))
            
            figure_line_st = GraphLinepx.line_(df = serie_time_df, x = col_segmented_st, y = importe, color= col_segmented_categoria,height=300, y_title = importe,x_title=col_segmented_st,title = f'Ventas por {col_segmented_st} por{col_segmented_categoria} ({cliente})',markers = True, hover_template= '<br>'+col_segmented_st+': <b>%{x}</b><br>'+importe+':<b> %{y:,.2f}</b>',size_text=15,legend_orizontal=False,legend_font_size = 9,
                                               order={col_segmented_st : sorted(df[col_segmented_st].unique()),col_segmented_categoria :sorted(df [col_segmented_categoria])}if col_segmented_st != 'Mes'else {'Mes' : MESES_ORDER,col_segmented_categoria :sorted(df [col_segmented_categoria])},discrete_color=dict_colors)
            #f"{sig} {(round(importe_total,0)):,}",clientes_total
        

        return [
            GraphBargo.bar_(df=bar_df,x=importe,y=col_segmented_categoria,orientation='h',text=importe,title=title,height=300, xaxis_title=importe,title_font_size=15, list_or_color=dict_colors),
            figure_line_st,
            f"{sig} {(round(importe_total,0)):,}",clientes_total,pais_total,vendedor_total
        ]