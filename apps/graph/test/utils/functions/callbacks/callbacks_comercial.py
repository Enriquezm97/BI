from dash import Input, Output,State,no_update,dcc,html
from apps.graph.test.constans import COMERCIAL_SELECTS_COLUMNS
from apps.graph.test.utils.functions.functions_filters import *
from apps.graph.test.utils.functions.functions_data import *
from apps.graph.test.utils.components import DataDisplay,Button
from apps.graph.test.utils.figures import *
from apps.graph.test.utils.frame import Graph
from apps.graph.test.utils.tables import tableDag
from apps.graph.test.utils.blocks.block_card import cardDivider
from apps.graph.test.utils.styles_ import *
import dash_mantine_components as dmc  

def create_callback_filter_comercial_informe(
    app, dataframe=pd.DataFrame(), 
    id_inputs = ['select-anio','select-cliente','select-cultivo','select-variedad'], 
    id_outputs = ['select-anio','select-cliente','select-cultivo','select-variedad']
    ):
    @app.callback(
                 [Output(output_,'data')for output_ in id_outputs]+
                 [
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
    )
    def update_graph_informe_comercial(*args):
        simbolo = "S/" if args[1] == 'Importe Soles' else "$"
        importe = args[1]#"IMPORTEMOF" if args[1] == 'Soles' else "IMPORTEMOF"
        df = pd.DataFrame(args[0])
        if args[2] != None and len(args[2])==0:
            df = df.copy()
        elif args[2] != None:
            df = df[df['Mes'].isin(args[2])]
        else:
            df = df.copy()
            
        productos_df_20=df.groupby(['Producto','Grupo Producto','Subgrupo Producto'])[[importe]].sum().sort_values(importe,ascending=True).tail(20).reset_index()
        productos_df_20['Producto']=productos_df_20['Producto'].str.capitalize()
        
        
        grupo_producto_df = df.groupby(['Grupo Producto'])[[importe]].sum().reset_index().round(2)
        grupo_producto_df=grupo_producto_df[grupo_producto_df[importe]>0].sort_values(importe, ascending = False)
        fig = go.Figure(go.Funnel(
        y = grupo_producto_df['Grupo Producto'],
        x = grupo_producto_df[importe],
        textposition = "outside",
        textinfo = "value+percent total",
        marker_color=px.colors.qualitative.Dark24,
        #marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
        #"line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
        #connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}}
        )
        )
        fig.update_xaxes(tickfont=dict(size=8),color='black',showticklabels = True)#,showgrid=True, gridwidth=1, gridcolor='black',
        fig.update_yaxes(tickfont=dict(size=8),color='black',showticklabels = True)  
        fig.update_layout(margin=dict(l = 50, r = 40, b= 30, t = 40, pad = 1))
        fig.update_layout(
                template='plotly_white',
                title={'text': f"<b>Grupo Producto mas vendido</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                #title_font_color="#145f82",
                xaxis_title='<b>'+importe+'</b>',
                yaxis_title='<b>Grupo</b>',
                legend_title="",
                font=dict(size=11,color="black"),
                height = 400, 
        )
        
        
        
        
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
               xaxis_title = importe, template= 'none', list_or_color=   px.colors.qualitative.Alphabet
            ),
            GraphBargo.bar_(df=meses_df_12, x= 'Mes', y= importe,orientation= 'v', height = 320, 
                title= 'Ventas por Mes', customdata=['Porcentaje'],space_ticked= 50, text= importe, yaxis_title= importe,xaxis_title= 'Mes',
                template='none',list_or_color=   px.colors.qualitative.Set3
            ),
            fig,
            GraphPiego.pie_(df = pais_df, title = 'Ventas - País',label_col = 'Pais', value_col = importe, height = 310, showlegend=False, color_list=px.colors.qualitative.Set3, textfont_size = 10),
            GraphPiego.pie_(df = vendedor_df, title = 'Ventas - Vendedor',label_col = 'Vendedor', value_col = importe, height = 310, showlegend=False, color_list=px.colors.qualitative.Set3, textfont_size = 10),
        ]
           
        
        
