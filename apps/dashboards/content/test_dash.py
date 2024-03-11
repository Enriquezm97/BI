from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS, DASH_CSS_FILE
from ..build.layout.error.dashboard_error import ERROR
from ..build.api.get_connect import connect_api
from ..build.layout.layout_test import test_dashboard,resize_dashboard
from ..build.utils.transform.t_logistica import *
#####
from dash import Input, Output,State,dcc
from ..build.utils.builder import *
from ...dashboards.build.components.display_comp import DataDisplay
from ..build.utils.global_callback import *

########
stockxalmacen_df = pd.read_parquet("stockxalmacen.parquet", engine="pyarrow")
stockxalmacen_df['SUCURSAL'] = stockxalmacen_df['SUCURSAL'].str.strip()
stockxalmacen_df['ALMACEN'] = stockxalmacen_df['ALMACEN'].str.strip()
stockxalmacen_df['DSC_GRUPO'] = stockxalmacen_df['DSC_GRUPO'].str.strip()
stockxalmacen_df['DSC_SUBGRUPO'] = stockxalmacen_df['DSC_SUBGRUPO'].str.strip()
stockxalmacen_df['SEDE'] = stockxalmacen_df['SEDE'].str.strip()
#####
det_consumidor_df = pd.read_parquet("detalle_consumidor.parquet", engine="pyarrow")
det_consumidor_df['GRUPO'] = det_consumidor_df['GRUPO'].str.strip()
det_consumidor_df['SUBGRUPO'] = det_consumidor_df['SUBGRUPO'].str.strip()
det_consumidor_df['DSC_PRODUCTO'] = det_consumidor_df['DSC_PRODUCTO'].str.strip()
#####
productos_df = pd.read_parquet("productos.parquet", engine="pyarrow")
productos_df['GRUPO']=productos_df['GRUPO'].str.strip()
productos_df['SUBGRUPO']=productos_df['SUBGRUPO'].str.strip()
productos_df['DESCRIPCION']=productos_df['DESCRIPCION'].str.strip()
productos_df['UMD']=productos_df['UMD'].str.strip()
productos_df['MARCA']=productos_df['MARCA'].str.strip()
productos_df.loc[productos_df.MARCA =='','MARCA']='NO ESPECIFICADO'

DICT_CULTIVOS_COLOR={}
def meses_inventario(cpm,stock):
    if cpm == 0:
        return 'NO ROTA'
    else:
        return round(stock/cpm,2)

def create_stack_np(dataframe = pd.DataFrame(), lista = []):
    return np.stack(tuple(dataframe[elemento] for elemento in lista),axis = -1)

def create_hover_custom(lista = []):
    string_hover = ''
    for i,element in zip(range(len(lista)),lista):
         if element == 'AREA_CAMPAÑA' or element == 'AREA' or element == 'Area':
               string_hover = string_hover+'<br>'+element+': <b>%{customdata['+str(i)+']:,.2f}</b>'
         else:
               string_hover = string_hover+'<br>'+element+': <b>%{customdata['+str(i)+']}</b>'   
    return string_hover

import plotly.express as px
import plotly.graph_objs as go
def bar_(df = pd.DataFrame(), x = '', y = '', text = '', orientation = 'v', height = 400 ,
        title = '', space_ticked = 40, xaxis_title = '',yaxis_title = '', showticklabel_x = False, 
        showticklabel_y = True , color_dataframe= '#228be6',list_or_color = None, customdata = [],
        template = 'plotly_white', size_tickfont = 11, title_font_size = 20, clickmode = False
    ):  
        #print(df)
        figure = go.Figure()
        if len(customdata)>0:
            custom = create_stack_np(dataframe = df, lista = customdata)
            hover_aditional_datacustom = create_hover_custom(lista = customdata)
        else:
            custom = []
            hover_aditional_datacustom = ""
            
        if orientation == 'h':
            value_left = space_ticked
            value_bottom = 40
            hover = '<br>'+y+': <b>%{y}</b><br>'+x+': <b>%{x:,.2f}</b>'+hover_aditional_datacustom
        elif orientation == 'v': 
            value_left = 60
            value_bottom = space_ticked
            hover = '<br>'+x+': <b>%{x}</b><br>'+y+': <b>%{y:,.2f}</b>'+hover_aditional_datacustom
            
        if  type(list_or_color) == list:
                value_colors =  list_or_color  

        elif type(list_or_color) == dict:

                try :
                    value_colors = [list_or_color[i] for i in df[x]]
                except:
                    value_colors = [list_or_color[i] for i in df[y]]
        else :
            value_colors = color_dataframe
        figure.add_trace(
            go.Bar(y = df[y],
                   x = df[x],   
                   text = df[text],
                   
                   orientation = orientation,
                   textposition = 'outside',
                   texttemplate =' %{text:.2s}',
                   marker_color = color_dataframe,    
                  # marker_color = value_colors,
                   opacity=0.9,
                   name = '',
                   customdata = custom,
                   hovertemplate=hover,
                   #hoverinfo='none',
                   hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'),
                   cliponaxis=False,
            )
        )
        
        figure.update_layout(
                template = template,
                title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                #title_font_color="#145f82",
                xaxis_title='<b>'+xaxis_title+'</b>',
                yaxis_title='<b>'+yaxis_title+'</b>',
                legend_title="",
                #font=dict(size=15,color="black"),
                title_font_family="sans-serif", 
                title_font_size = title_font_size,
                title_font_color = "rgba(0, 0, 0, 0.7)",
                height = height, 
                
        )
        if clickmode == True:
            figure.update_layout(clickmode='event+select')
        size_list = len(df[x].unique()) if orientation == 'v' else len(df[y].unique())
        figure.update_xaxes(tickfont=dict(size=size_tickfont),color='rgba(0, 0, 0, 0.7)',showticklabels = showticklabel_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
        figure.update_yaxes(tickfont=dict(size=size_tickfont),color='rgba(0, 0, 0, 0.7)',showticklabels = showticklabel_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
        figure.update_layout(margin=dict(l = value_left, r = 40, b= value_bottom, t = 40, pad = 1))
        
        if  size_list== 1:
            figure.update_layout(bargap=0.7)
        elif size_list== 2:
            figure.update_layout(bargap=0.4)
        elif size_list== 3:
            figure.update_layout(bargap=0.3)

        return figure
    
def bar_y1(df = None, height = 450 , moneda = 'Soles'):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df['DESCRIPCION'],
    y = df['Meses Inventario'],
    name = "Meses Inventario",
    cliponaxis=False,
    marker=dict(color="#3aa99b"),
    hovertemplate ='<br>'+'Descripción'+': <b>%{x}</b><br>'+'Meses Inventario'+': <b>%{y}</b>',hoverlabel=dict(font_size=13,bgcolor="white")
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+'Meses Inventario'+'</b>'),
            side="left",
            range=[0, df['Meses Inventario'].max()]
        ),
        
        template= 'none',
        xaxis_title='<b>'+'Descripción'+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>Meses de Inventario Promedio</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template = 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=13),color='black',showticklabels = False,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 40, b = 40))
    return fig

def bar_y2(df = None, height = 450 , moneda = 'Soles'):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df['DESCRIPCION'],
    y = df['Inventario Valorizado'],
    name = "Inventario Valorizado",
    cliponaxis=False,
    marker=dict(color="#5175c7"),
    hovertemplate ='<br>'+'Descripción'+': <b>%{x}</b><br>'+'Inventario Valorizado'+': <b>%{y:,.2f}</b>',hoverlabel=dict(font_size=13,bgcolor="white")
    ))
    fig.add_trace(
        go.Scatter(
            x= df['DESCRIPCION'],
            y= df['Meses Inventario'],
            yaxis="y2",
            name="Meses de Inventario",
            marker=dict(color="#3aa99b"),
            cliponaxis=False,
            hovertemplate ='<br>'+'Descripción'+': <b>%{x}</b><br>'+'Meses de Inventario'+': <b>%{y}</b>',hoverlabel=dict(font_size=13,bgcolor="white")
        )
    )
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+'Inventario Valorizado'+'</b>'),
            side="left",
            range=[0, df['Inventario Valorizado'].max()]
        ),
        yaxis2=dict(
            title=dict(text='<b>'+'Meses Inventario'+'</b>'),
            side="right",
            range=[0, df['Meses Inventario'].max()],
            overlaying="y",
            tickmode="auto",
        ),
        template= 'none',
        xaxis_title='<b>'+'Descripción'+'</b>',
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        title = f"<b>Variación de Inventario Valorizado</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template = 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=13),color='black',showticklabels = False,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(b = 40))
    
    return fig

def opened_modal(
    app,
    modal_id ='',
    children_out_id = '', 
    id_button = '', 
    height_modal = 500, 
    type_children = 'Figure'
): 
    @app.callback(
        [Output(modal_id, "opened"),
         Output(modal_id, "children")],
        [Input(id_button, "n_clicks")],
        [State(children_out_id,'figure'),
        State(modal_id, "opened")],
        prevent_initial_call=True,
    )
    #if type_children == 'Figure':
    def toggle_modal(n_clicks,figure, opened):
        
            fig=go.Figure(figure)
            fig.update_layout(margin=dict(b = 150))
            fig.update_layout(height = height_modal,
                              
                              title_font_size = 30)
            
            fig.update_xaxes(
                             tickfont=dict(size=15),
                             color='black',
                             showticklabels = True,
                             title_font_family="sans-serif",
                             title_font_size = 25,
                             automargin=False
                            )
            fig.update_yaxes(
                             tickfont=dict(size=20),
                             color='black',
                             showticklabels = True,
                             title_font_family="sans-serif",
                             title_font_size = 30,
                             automargin=False
                            )  
            fig.update_layout(
                legend=dict(
                    
                    title_font_family="sans-serif",
                    font=dict(
                        family="sans-serif",
                        size=25,
                        color="black"
                    ),
                    
                )
            ),
            
            try:
                fig.update_traces(hoverinfo='label+percent+value', textfont_size = 20,marker=dict(line=dict(color='#000000', width=1)))
            except:
                pass
        
            if n_clicks:
                return True,dcc.Graph(figure=fig)
            else:
                return not opened

def fields_columns(columns = []):
    list_ = []
    for col in columns:
        if col =='CPM' or col == 'STOCK':
            
            list_.append({"field": col,"cellStyle": {'font-size': 12},"type": "rightAligned",'cellStyle':{"styleConditions": [{"condition": "params.value > 0 ","style": {"backgroundColor": "#C6EFCE"}}],"defaultStyle": {"backgroundColor": "white"}}})
        else :
            list_.append({"field": col,"cellStyle": {'font-size': 12},"type": "rightAligned"})
    return list_
#################








def dashboard_test(codigo = '',empresa = ''):#filtros = ['select-anio','select-grupo','select-rango']
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    app.layout =  test_dashboard(data_almacen = stockxalmacen_df['ALMACEN'].unique())
    @app.callback(
        #Output('multiselect-almacen','data'),
        Output("data-stock","data"),
        Input('multiselect-almacen','value'),
    )
    def update_data_stock(almacen):
        if almacen == None or len(almacen) == 0:#(len(almacen)==0 or cultivo==None):
            df = stockxalmacen_df.copy()
        else:
            df = stockxalmacen_df[stockxalmacen_df['ALMACEN'].isin(almacen)]
        return df.to_dict('series')
        
    
    @app.callback(
        [
            Output('select-grupo','data'),
            Output('select-subgrupo','data'),
            Output('select-marca','data'),
            Output('range-slider-cpm','max'),
            Output('range-slider-cpm','value'),
            #Output('slider-rango-cpm','marks'),
            #Output('slider-rango-cpm','value'),
            #Output('slider-rango-mi','marks'),
            #Output('slider-rango-mi','value'),
        ]+
        [
         Output("data-values","data"),
         Output("notifications-update-data","children")
        ],
        [
            Input('select-grupo','value'),
            Input('select-subgrupo','value'),
            Input('select-marca','value'),
            #Input('slider-rango-cpm','value'),
            #Input('slider-rango-mi','value'),
            Input('select-moneda','value'),
            Input('text-input-find','value'),
            
            Input('data-stock','data'),
            
        ]
    )
    def update_filter_(*args):
        
        grupo = args[0]
        subgrupo = args[1]
        marca = args[2]
        #rango_cpm = args[3]
        #rango_mi = args[4]
        moneda = args[3]
        input_text = args[4]
        stockxalmacen_df = pd.DataFrame(args[5])
        
        
        
        
        stock_x_producto_df = stockxalmacen_df.groupby(['IDPRODUCTO'])[['STOCK']].sum().reset_index()
        stock_promediomof_df = stockxalmacen_df.groupby(['IDPRODUCTO'])[[moneda]].mean().reset_index()
        cant_almacen_df = det_consumidor_df.groupby(['IDPRODUCTO'])[['CANT']].sum().reset_index()
        if validate_inputs(variables = (grupo,subgrupo,marca)) == True:    
            productos_dff = productos_df.copy()
        else:
            productos_dff = productos_df.query(dataframe_filtro(values=list((grupo,subgrupo,marca)),columns_df = ['GRUPO','SUBGRUPO','MARCA']))
        
        productos_cols_df = productos_dff.groupby(['GRUPO', 'SUBGRUPO', 'CODIGO', 'DESCRIPCION', 'UMD', 'MARCA'])[['FILTRO']].sum().reset_index()
        productos_cant_df = productos_cols_df.merge(cant_almacen_df, how='left', left_on=["CODIGO"], right_on=["IDPRODUCTO"])
        productos_cant_stock_df = productos_cant_df.merge(stock_x_producto_df, how='left', left_on=["CODIGO"], right_on=["IDPRODUCTO"])
        dff = productos_cant_stock_df.merge(stock_promediomof_df, how='left', left_on=["CODIGO"], right_on=["IDPRODUCTO"])
        dff['CANT'] = dff['CANT'].fillna(0)
        dff['STOCK'] = dff['STOCK'].fillna(0)
        dff[moneda] = dff[moneda].fillna(0)
        dff = dff.drop(['IDPRODUCTO_x','IDPRODUCTO_y','IDPRODUCTO'], axis=1)
        dff['CANT'] = dff['CANT']/6
        dff['Meses Inventario'] = dff.apply(lambda x: meses_inventario(x['CANT'],x['STOCK']),axis=1)
        dff['Inventario Valorizado'] = dff[moneda] * dff['STOCK']
        dff = dff.sort_values('Inventario Valorizado',ascending =  False)
        dff['TI'] = 1/dff['CANT']
        dff['TI'] = dff['TI'].replace([np.inf],0)
        if input_text != None:
            
            dff = dff[(dff['CODIGO'].str.contains(input_text))|(dff['DESCRIPCION'].str.contains(input_text))]
        
            
        
        #cpm_max = dff['CPM'].max()
        #print(cpm_max)
        #df['CANT'].mean()
        #dff.to_excel('dash.xlsx')
        print(dff['CANT'].max())
        cpm_max = round(dff['CANT'].max())
        return [
            [{'label': i, 'value': i} for i in sorted(dff['GRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(dff['SUBGRUPO'].unique())],
            [{'label': i, 'value': i} for i in sorted(dff['MARCA'].unique())],
            cpm_max,
            
            [0,cpm_max],
            dff.to_dict('series'),
            DataDisplay.notification(text=f'Se cargaron {len(dff)} filas',title='Update')
        ]
    @app.callback(
        #Output('multiselect-almacen','data'),
        Output("card-cpm","children"),
        Output("card-invval","children"),
        Output("card-stock","children"),
        Output("card-consumo","children"),
        Output("bar-minv-prom","figure"),
        Output("bar-inv-val","figure"),
        Output("table","rowData"),
        Output("table","columnDefs"),
        Output("data-table","data"),
        #Output("line-inv-val","value"),
        Input("data-values","data"),
        Input("select-moneda","value"),
        Input('range-slider-cpm','value'),
    )
    def update_outs(data,moneda,slider_cpm):
        df = pd.DataFrame(data)
        df = df[(df['CANT']>=slider_cpm[0])&(df['CANT']<=(slider_cpm[1]+1))]
        sig = 'S/.' if moneda == 'PROMEDIOMOF' else '$'
        cpm = round(df['CANT'].mean(),2)
        invval = f"{sig} {(round(df['Inventario Valorizado'].sum(),2)):,}"
        meses_invet_prom = df[df['Meses Inventario']!='NO ROTA']
        stock = round(meses_invet_prom['Meses Inventario'].mean(),2)
        consumo = round(df['TI'].mean(),2)
        mi_dff = df[(df['Meses Inventario']!='NO ROTA')]
        df_mi_ =mi_dff.groupby(['CODIGO','DESCRIPCION'])[['Meses Inventario']].sum().sort_values('Meses Inventario').reset_index().tail(30)
        df_mi_iv =mi_dff.groupby(['CODIGO','DESCRIPCION'])[['Meses Inventario','Inventario Valorizado']].sum().sort_values('Inventario Valorizado').reset_index().tail(30)
        df['CANT']=df.apply(lambda x: "{:,.2f}".format(x['CANT']), axis=1)
        df['STOCK']=df.apply(lambda x: "{:,.2f}".format(x['STOCK']), axis=1)
        df[moneda]=df.apply(lambda x: "{:,.2f}".format(x[moneda]), axis=1)
        #df['Meses Inventario']=df.apply(lambda x: "{:,.2f}".format(x['Meses Inventario']), axis=1)
        df['Inventario Valorizado']=df.apply(lambda x: "{:,.2f}".format(x['Inventario Valorizado']), axis=1)
        df['TI']=df.apply(lambda x: "{:,.2f}".format(x['TI']), axis=1)
        
        df = df.drop(['FILTRO'], axis=1)
        df = df.rename(columns = {'CANT':'CPM','moneda':'Precio Unitario','Meses Inventario':'Meses de Inventario'})
        
        return [
            cpm, invval, stock, consumo,
            #bar_(df = df_mi_,x = 'DESCRIPCION', y = 'Meses Inventario', orientation= 'v',height = 380,title = 'Meses de Inventario Promedio',text='Meses Inventario',
            #     xaxis_title = 'Descripción', yaxis_title = 'Meses de Inventario'),
            bar_y1(df = df_mi_,height = 350),
            bar_y2(df = df_mi_iv,height = 350 ),
            df.to_dict("records"),
            fields_columns(columns = df.columns),
            df.to_dict("series"),
            
        ]
    download_data(app,input_id_data='data-table',name_file = 'stocks_producto.xlsx')
    opened_modal(app, modal_id="modal-bar-minv-prom",children_out_id="bar-minv-prom", id_button="maximize-bar-minv-prom",height_modal=900)
    opened_modal(app, modal_id="modal-bar-inv-val",children_out_id="bar-inv-val", id_button="maximize-bar-inv-val",height_modal=900)
    return app


def dashboard_resize(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    #try:
    app.layout =  resize_dashboard()
    #except:
    #    app.layout = ERROR
    
    return app

"""
 @app.callback(
        [
            Output('select-grupo','data'),
            Output('select-subgrupo','data'),
            Output('select-marca','data'),
            Output('multiselect-almacen','data'),
            Output('slider-rango-cpm','marks'),
            Output('slider-rango-cpm','value'),
            Output('slider-rango-mi','marks'),
            Output('slider-rango-mi','value'),
        ]+
        [
         Output("data-values","data"),
         Output('chipgroup-mes','children'),
         Output("notifications-update-data","children")
        ],
        [
            Input('select-grupo','value'),
            Input('select-subgrupo','value'),
            Input('select-marca','value'),
            Input('multiselect-almacen','value'),
            Input('slider-rango-cpm','value'),
            Input('slider-rango-mi','value'),
            Input('select-moneda','value'),
        ]
    )
    def update_filter_(*args):
        if validate_inputs(variables = args[:-1]) == True:
"""