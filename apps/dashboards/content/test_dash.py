from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS, DASH_CSS_FILE, DASH_JS_FILE_1,DASH_JS_FILE_2
from ..build.layout.error.dashboard_error import ERROR
from ..build.api.get_connect import connect_api
from ..build.layout.layout_test import test_dashboard,resize_dashboard
from ..build.utils.transform.t_logistica import *
#####
from dash import Input, Output,State,dcc, clientside_callback, ClientsideFunction
from ..build.utils.builder import *
from ...dashboards.build.components.display_comp import DataDisplay
from ..build.utils.global_callback import *


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
import dash_mantine_components as dmc 

tradeData = [{'year': 2006,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 63716214,
  'weight_kg': 115629234.0,
  'quantity': 115629234.0},
 {'year': 2006,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 430748553,
  'weight_kg': 2346450775.0,
  'quantity': 2346450775.0},
 {'year': 2006,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 1253785288,
  'weight_kg': 5024869572.0,
  'quantity': 5024869572.0},
 {'year': 2007,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 91229464,
  'weight_kg': 136514750.0,
  'quantity': 136514750.0},
 {'year': 2007,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 684278862,
  'weight_kg': 3038566363.0,
  'quantity': 3038566363.0},
 {'year': 2007,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 1808139555,
  'weight_kg': 5876042474.0,
  'quantity': 5876042474.0},
 {'year': 2008,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 186805290,
  'weight_kg': 202116608.0,
  'quantity': 202116608.0},
 {'year': 2008,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 955438637,
  'weight_kg': 3187626879.0,
  'quantity': 3187626879.0},
 {'year': 2008,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2957377727,
  'weight_kg': 11187339048.0,
  'quantity': 11187339048.0},
 {'year': 2009,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 200173126,
  'weight_kg': 207601221.0,
  'quantity': 207601221.0},
 {'year': 2009,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 731037503,
  'weight_kg': 2511883912.0,
  'quantity': 2511883912.0},
 {'year': 2009,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2187165737,
  'weight_kg': 5845789247.0,
  'quantity': 5845789247.0},
 {'year': 2010,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 194488373,
  'weight_kg': 197969326.0,
  'quantity': 197969326.0},
 {'year': 2010,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 688543192,
  'weight_kg': 2084921052.0,
  'quantity': 2084921052.0},
 {'year': 2010,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 1989199221,
  'weight_kg': 5410192249.0,
  'quantity': 5410192249.0},
 {'year': 2011,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 171090533,
  'weight_kg': 166577289.0,
  'quantity': 166577289.0},
 {'year': 2011,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 706041630,
  'weight_kg': 1601805508.0,
  'quantity': 1601805508.0},
 {'year': 2011,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2318505417,
  'weight_kg': 5246030143.0,
  'quantity': 5246030143.0},
 {'year': 2012,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 154979602,
  'weight_kg': 144000498.0,
  'quantity': 144000498.0},
 {'year': 2012,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 689334863,
  'weight_kg': 1147480258.0,
  'quantity': 1147480258.0},
 {'year': 2012,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 3320471158,
  'weight_kg': 7343723240.0,
  'quantity': 7343723240.0},
 {'year': 2013,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 170559183,
  'weight_kg': 152319200.0,
  'quantity': 152319200.0},
 {'year': 2013,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 716892707,
  'weight_kg': 1100256655.0,
  'quantity': 1100256655.0},
 {'year': 2013,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 4361816392,
  'weight_kg': 9694455603.0,
  'quantity': 9694455603.0},
 {'year': 2014,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 196371046,
  'weight_kg': 171237022.0,
  'quantity': 171237022.0},
 {'year': 2014,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 883248862,
  'weight_kg': 1666338102.0,
  'quantity': 1666338102.0},
 {'year': 2014,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 3458934816,
  'weight_kg': 7648066482.0,
  'quantity': 7648066482.0},
 {'year': 2015,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 162978086,
  'weight_kg': 164851991.0,
  'quantity': 164851991.0},
 {'year': 2015,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 825058622,
  'weight_kg': 2179033032.0,
  'quantity': 2179033032.0},
 {'year': 2015,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2800409503,
  'weight_kg': 6895217307.0,
  'quantity': 6895217307.0},
 {'year': 2016,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 149905907,
  'weight_kg': 175307330.0,
  'quantity': 175307330.0},
 {'year': 2016,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 702756213,
  'weight_kg': 1930607068.0,
  'quantity': 1930607068.0},
 {'year': 2016,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2333001754,
  'weight_kg': 6612951940.0,
  'quantity': 6612951940.0}]

trade = [{'year': 2006,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 3448330729,
  'weight_kg': 27886740602.0,
  'quantity': 27886740602.0},
 {'year': 2006,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 1814093905,
  'weight_kg': 885616837.0,
  'quantity': 885616837.0},
 {'year': 2006,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 63716214,
  'weight_kg': 115629234.0,
  'quantity': 115629234.0},
 {'year': 2006,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 323295053,
  'weight_kg': 109478468.0,
  'quantity': 109478468.0},
 {'year': 2006,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 3887949437,
  'weight_kg': 22455057235.0,
  'quantity': 22455057235.0},
 {'year': 2006,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 271600990,
  'weight_kg': 132982575.0,
  'quantity': 132982575.0},
 {'year': 2006,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 430748553,
  'weight_kg': 2346450775.0,
  'quantity': 2346450775.0},
 {'year': 2006,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 404904348,
  'weight_kg': 179733880.0,
  'quantity': 179733880.0},
 {'year': 2006,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 13525652374,
  'weight_kg': 90322441986.0,
  'quantity': 90322441986.0},
 {'year': 2006,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 1253785288,
  'weight_kg': 5024869572.0,
  'quantity': 5024869572.0},
 {'year': 2007,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 2238694233,
  'weight_kg': 17108258841.0,
  'quantity': 17108258841.0},
 {'year': 2007,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 2035795080,
  'weight_kg': 740609996.0,
  'quantity': 740609996.0},
 {'year': 2007,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 91229464,
  'weight_kg': 136514750.0,
  'quantity': 136514750.0},
 {'year': 2007,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 395020258,
  'weight_kg': 116496174.0,
  'quantity': 116496174.0},
 {'year': 2007,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 5518128317,
  'weight_kg': 22500904857.0,
  'quantity': 22500904857.0},
 {'year': 2007,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 294094881,
  'weight_kg': 136547323.0,
  'quantity': 136547323.0},
 {'year': 2007,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 684278862,
  'weight_kg': 3038566363.0,
  'quantity': 3038566363.0},
 {'year': 2007,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 504945760,
  'weight_kg': 214040227.0,
  'quantity': 214040227.0},
 {'year': 2007,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 21119589167,
  'weight_kg': 99994118088.0,
  'quantity': 99994118088.0},
 {'year': 2007,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 1808139555,
  'weight_kg': 5876042474.0,
  'quantity': 5876042474.0},
 {'year': 2008,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 4383983777,
  'weight_kg': 27302371391.0,
  'quantity': 27302371391.0},
 {'year': 2008,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 2238222249,
  'weight_kg': 659404338.0,
  'quantity': 659404338.0},
 {'year': 2008,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 186805290,
  'weight_kg': 202116608.0,
  'quantity': 202116608.0},
 {'year': 2008,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 586650903,
  'weight_kg': 140734051.0,
  'quantity': 140734051.0},
 {'year': 2008,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 8277663788,
  'weight_kg': 33491627334.0,
  'quantity': 33491627334.0},
 {'year': 2008,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 306039146,
  'weight_kg': 104734120.0,
  'quantity': 104734120.0},
 {'year': 2008,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 955438637,
  'weight_kg': 3187626879.0,
  'quantity': 3187626879.0},
 {'year': 2008,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 523957112,
  'weight_kg': 219248950.0,
  'quantity': 219248950.0},
 {'year': 2008,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 28948701392,
  'weight_kg': 95639789213.0,
  'quantity': 95639789213.0},
 {'year': 2008,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2957377727,
  'weight_kg': 11187339048.0,
  'quantity': 11187339048.0},
 {'year': 2009,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 4426237299,
  'weight_kg': 24319297872.0,
  'quantity': 24319297872.0},
 {'year': 2009,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 1684922166,
  'weight_kg': 752462328.0,
  'quantity': 752462328.0},
 {'year': 2009,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 200173126,
  'weight_kg': 207601221.0,
  'quantity': 207601221.0},
 {'year': 2009,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 432990775,
  'weight_kg': 139751328.0,
  'quantity': 139751328.0},
 {'year': 2009,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 6223889821,
  'weight_kg': 23009940345.0,
  'quantity': 23009940345.0},
 {'year': 2009,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 232702341,
  'weight_kg': 100078088.0,
  'quantity': 100078088.0},
 {'year': 2009,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 731037503,
  'weight_kg': 2511883912.0,
  'quantity': 2511883912.0},
 {'year': 2009,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 423482621,
  'weight_kg': 307696035.0,
  'quantity': 307696035.0},
 {'year': 2009,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 17419347206,
  'weight_kg': 77211366952.0,
  'quantity': 77211366952.0},
 {'year': 2009,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2187165737,
  'weight_kg': 5845789247.0,
  'quantity': 5845789247.0},
 {'year': 2010,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 4705078783,
  'weight_kg': 20155724438.0,
  'quantity': 20155724438.0},
 {'year': 2010,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 1987959643,
  'weight_kg': 639703269.0,
  'quantity': 639703269.0},
 {'year': 2010,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 194488373,
  'weight_kg': 197969326.0,
  'quantity': 197969326.0},
 {'year': 2010,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 610376904,
  'weight_kg': 155224300.0,
  'quantity': 155224300.0},
 {'year': 2010,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 5577340847,
  'weight_kg': 22500574085.0,
  'quantity': 22500574085.0},
 {'year': 2010,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 277174255,
  'weight_kg': 113283274.0,
  'quantity': 113283274.0},
 {'year': 2010,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 688543192,
  'weight_kg': 2084921052.0,
  'quantity': 2084921052.0},
 {'year': 2010,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 474974221,
  'weight_kg': 268327651.0,
  'quantity': 268327651.0},
 {'year': 2010,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 20036820271,
  'weight_kg': 86902693226.0,
  'quantity': 86902693226.0},
 {'year': 2010,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 1989199221,
  'weight_kg': 5410192249.0,
  'quantity': 5410192249.0},
 {'year': 2011,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 8065036042,
  'weight_kg': 25489041804.0,
  'quantity': 25489041804.0},
 {'year': 2011,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 2242088426,
  'weight_kg': 636660294.0,
  'quantity': 636660294.0},
 {'year': 2011,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 171090533,
  'weight_kg': 166577289.0,
  'quantity': 166577289.0},
 {'year': 2011,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 664356778,
  'weight_kg': 153463407.0,
  'quantity': 153463407.0},
 {'year': 2011,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 7046180964,
  'weight_kg': 20518070901.0,
  'quantity': 20518070901.0},
 {'year': 2011,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 285934111,
  'weight_kg': 107176482.0,
  'quantity': 107176482.0},
 {'year': 2011,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 706041630,
  'weight_kg': 1601805508.0,
  'quantity': 1601805508.0},
 {'year': 2011,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 525241705,
  'weight_kg': 137875435.0,
  'quantity': 137875435.0},
 {'year': 2011,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 28347941016,
  'weight_kg': 86069184301.0,
  'quantity': 86069184301.0},
 {'year': 2011,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2318505417,
  'weight_kg': 5246030143.0,
  'quantity': 5246030143.0},
 {'year': 2012,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 8619740515,
  'weight_kg': 29620404061.0,
  'quantity': 29620404061.0},
 {'year': 2012,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 2245517239,
  'weight_kg': 689211238.0,
  'quantity': 689211238.0},
 {'year': 2012,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 154979602,
  'weight_kg': 144000498.0,
  'quantity': 144000498.0},
 {'year': 2012,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 639098163,
  'weight_kg': 149012010.0,
  'quantity': 149012010.0},
 {'year': 2012,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 7522699240,
  'weight_kg': 22074643166.0,
  'quantity': 22074643166.0},
 {'year': 2012,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 325169296,
  'weight_kg': 102625243.0,
  'quantity': 102625243.0},
 {'year': 2012,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 689334863,
  'weight_kg': 1147480258.0,
  'quantity': 1147480258.0},
 {'year': 2012,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 516435008,
  'weight_kg': 143361846.0,
  'quantity': 143361846.0},
 {'year': 2012,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 20616227140,
  'weight_kg': 63118806829.0,
  'quantity': 63118806829.0},
 {'year': 2012,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 3320471158,
  'weight_kg': 7343723240.0,
  'quantity': 7343723240.0},
 {'year': 2013,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 8047797638,
  'weight_kg': 24568845965.0,
  'quantity': 24568845965.0},
 {'year': 2013,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 2232513214,
  'weight_kg': 626633379.0,
  'quantity': 626633379.0},
 {'year': 2013,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 170559183,
  'weight_kg': 152319200.0,
  'quantity': 152319200.0},
 {'year': 2013,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 684300276,
  'weight_kg': 154926775.0,
  'quantity': 154926775.0},
 {'year': 2013,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 8072446255,
  'weight_kg': 24423734164.0,
  'quantity': 24423734164.0},
 {'year': 2013,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 360269276,
  'weight_kg': 111332757.0,
  'quantity': 111332757.0},
 {'year': 2013,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 716892707,
  'weight_kg': 1100256655.0,
  'quantity': 1100256655.0},
 {'year': 2013,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 575521748,
  'weight_kg': 181040361.0,
  'quantity': 181040361.0},
 {'year': 2013,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 20300976057,
  'weight_kg': 63353710059.0,
  'quantity': 63353710059.0},
 {'year': 2013,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 4361816392,
  'weight_kg': 9694455603.0,
  'quantity': 9694455603.0},
 {'year': 2014,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 7427763728,
  'weight_kg': 25281653416.0,
  'quantity': 25281653416.0},
 {'year': 2014,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 2318777372,
  'weight_kg': 684125731.0,
  'quantity': 684125731.0},
 {'year': 2014,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 196371046,
  'weight_kg': 171237022.0,
  'quantity': 171237022.0},
 {'year': 2014,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 786255979,
  'weight_kg': 172900377.0,
  'quantity': 172900377.0},
 {'year': 2014,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 8753949988,
  'weight_kg': 29586443967.0,
  'quantity': 29586443967.0},
 {'year': 2014,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 367130518,
  'weight_kg': 119581175.0,
  'quantity': 119581175.0},
 {'year': 2014,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 883248862,
  'weight_kg': 1666338102.0,
  'quantity': 1666338102.0},
 {'year': 2014,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 667300268,
  'weight_kg': 242303660.0,
  'quantity': 242303660.0},
 {'year': 2014,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 22850742210,
  'weight_kg': 69549077430.0,
  'quantity': 69549077430.0},
 {'year': 2014,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 3458934816,
  'weight_kg': 7648066482.0,
  'quantity': 7648066482.0},
 {'year': 2015,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 6427636897,
  'weight_kg': 24199617522.0,
  'quantity': 24199617522.0},
 {'year': 2015,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 1819189579,
  'weight_kg': 734274446.0,
  'quantity': 734274446.0},
 {'year': 2015,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 162978086,
  'weight_kg': 164851991.0,
  'quantity': 164851991.0},
 {'year': 2015,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 725379927,
  'weight_kg': 188275151.0,
  'quantity': 188275151.0},
 {'year': 2015,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 7336350608,
  'weight_kg': 27592979130.0,
  'quantity': 27592979130.0},
 {'year': 2015,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 293134974,
  'weight_kg': 115937294.0,
  'quantity': 115937294.0},
 {'year': 2015,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 825058622,
  'weight_kg': 2179033032.0,
  'quantity': 2179033032.0},
 {'year': 2015,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 644048214,
  'weight_kg': 247731662.0,
  'quantity': 247731662.0},
 {'year': 2015,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 18799966274,
  'weight_kg': 80051768667.0,
  'quantity': 80051768667.0},
 {'year': 2015,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2800409503,
  'weight_kg': 6895217307.0,
  'quantity': 6895217307.0},
 {'year': 2016,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 5097736255,
  'weight_kg': 23020418603.0,
  'quantity': 23020418603.0},
 {'year': 2016,
  'country': 'Australia',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 1665225962,
  'weight_kg': 745989971.0,
  'quantity': 745989971.0},
 {'year': 2016,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 149905907,
  'weight_kg': 175307330.0,
  'quantity': 175307330.0},
 {'year': 2016,
  'country': 'Australia',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 795465400,
  'weight_kg': 217360115.0,
  'quantity': 217360115.0},
 {'year': 2016,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 5623477260,
  'weight_kg': 24637615695.0,
  'quantity': 24637615695.0},
 {'year': 2016,
  'country': 'Canada',
  'flow': 'Export',
  'category': 'dairy',
  'trade_usd': 296991486,
  'weight_kg': 133724372.0,
  'quantity': 133724372.0},
 {'year': 2016,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 702756213,
  'weight_kg': 1930607068.0,
  'quantity': 1930607068.0},
 {'year': 2016,
  'country': 'Canada',
  'flow': 'Import',
  'category': 'dairy',
  'trade_usd': 608669404,
  'weight_kg': 207771321.0,
  'quantity': 207771321.0},
 {'year': 2016,
  'country': 'USA',
  'flow': 'Export',
  'category': 'cereals',
  'trade_usd': 19109878912,
  'weight_kg': 91377729660.0,
  'quantity': 91377729660.0},
 {'year': 2016,
  'country': 'USA',
  'flow': 'Import',
  'category': 'cereals',
  'trade_usd': 2333001754,
  'weight_kg': 6612951940.0,
  'quantity': 6612951940.0}]
def dashboard_resize(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=['/static/css/dashstyles.css'],external_scripts=['https://cdn.jsdelivr.net/npm/apexcharts','/static/css/herpers.js'])
    
    #app.css.append_css(DASH_CSS_FILE)
    #resize_dashboard()
    
    app.layout = html.Div(
        children=[
            dcc.Store(id='ApexchartsSampleData', data=tradeData),
            html.H1("Javascript Charts Test"),
            dmc.Center(
                dmc.Paper(
                    shadow="sm",
                    style={'height':'600px', 'width':'800px', 'marginTop':'100px'},
                    children=[
                        html.Div(id='apexAreaChart'),
                        dmc.Center(
                            children=[
                                dmc.SegmentedControl(
                                    id="selectCountryChip",
                                    value="Canada",
                                    data=['Canada', 'USA', 'Australia'],
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )
    app.clientside_callback(
    #ClientsideFunction(
    #        namespace='apexCharts',
    #        function_name='areaChart'
    #    ),
    
    """

    function (tradeData, selectedCountry) {

            console.log(selectedCountry)
            document.getElementById("apexAreaChart").innerHTML = "";
            data = tradeData.filter(item=>  item.country===selectedCountry) 
            var options = {
                series: [
                    {
                        name: 'USD',
                        type: 'column',
                        data: data.map( (item) => item.trade_usd)
                    }, 
                    {
                        name: 'Weight',
                        type: 'area',
                        data: data.map( (item) => item.weight_kg)
                    },
                 
                ],
                labels: [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016],
                xaxis: { type: 'category'},
                yaxis: [
                    { 
                        labels: { formatter:  BillionFormatter},
                        title: { text: "Billions (USD) "},
                    },
                    {
                        opposite: true,
                        labels: { formatter: GigatonneFormatter},
                        title: { text: 'Gigatonne'}
                    }
                ],
                fill: {
                    opacity: [0.85, 0.25, 1],
                    gradient: {
                        inverseColors: false,
                        shade: 'light',
                        type: "vertical",
                        opacityFrom: 0.85,
                        opacityTo: 0.55,
                        stops: [0, 100, 100, 100]
                    }
                },
                chart: { height: '85%'},
                stroke: { width: [0, 4],  curve: 'smooth'},
                title: {
                    text: "Global Import of Cereals",
                    align: 'center',
                    style: {
                        fontSize:  '22px',
                        fontWeight:  'bold',
                    },
                },
                dataLabels: {
                    enabled: true,
                    enabledOnSeries: [1],
                    formatter: GigatonneFormatter
                },
            };
            var chart = new ApexCharts(document.getElementById('apexAreaChart'), options);


            chart.render();

        return window.dash_clientside.no_update
    }
        
    """,
        Output("apexAreaChart", "children"),
        Input("ApexchartsSampleData", "data"),
        Input("selectCountryChip", "value"),
    )
    #    app.layout = ERROR
    
    return app


def dashboard_resize_test(codigo = ''):
    app = DjangoDash(
        name = codigo,
        external_stylesheets=['/static/css/dashstyles.css'],
        external_scripts=[
            "https://code.highcharts.com/highcharts.js",
            "https://code.highcharts.com/stock/highstock.js"
        ]
    )
    app.layout = html.Div([
        dcc.Store(id='highChartsData', data=tradeData),
            html.H1("HighCharts Test"),
            dmc.Center(
                dmc.Paper(
                    shadow="sm",
                    style={'height':'600px', 'width':'800px', 'marginTop':'100px'},
                    children=[
                        html.Div(id='highcharts'),
                        dmc.Center(
                            children=[
                                dmc.SegmentedControl(
                                    id="selectCountryChip",
                                    value="Canada",
                                    data=['Canada', 'USA', 'Australia'],
                                )
                            ]
                        )
                    ]
                )
            )
    ])
    app.clientside_callback(
    #ClientsideFunction(
    #        namespace='apexCharts',
    #        function_name='areaChart'
    #    ),
    
    """
    function crearGrafico() {
        document.getElementById("highcharts").innerHTML = "";
        Highcharts.chart('container', {
            title: {
                text: 'U.S Solar Employment Growth',
                align: 'left'
            },
            subtitle: {
                text: 'By Job Category. Source: <a href="https://irecusa.org/programs/solar-jobs-census/" target="_blank">IREC</a>.',
                align: 'left'
            },
            yAxis: {
                title: {
                    text: 'Number of Employees'
                }
            },
            xAxis: {
                accessibility: {
                    rangeDescription: 'Range: 2010 to 2020'
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
            plotOptions: {
                series: {
                    label: {
                        connectorAllowed: false
                    },
                    pointStart: 2010
                }
            },
            series: [{
                name: 'Installation & Developers',
                data: [43934, 48656, 65165, 81827, 112143, 142383,
                    171533, 165174, 155157, 161454, 154610]
            }, {
                name: 'Manufacturing',
                data: [24916, 37941, 29742, 29851, 32490, 30282,
                    38121, 36885, 33726, 34243, 31050]
            }, {
                name: 'Sales & Distribution',
                data: [11744, 30000, 16005, 19771, 20185, 24377,
                    32147, 30912, 29243, 29213, 25663]
            }, {
                name: 'Operations & Maintenance',
                data: [null, null, null, null, null, null, null,
                    null, 11164, 11218, 10077]
            }, {
                name: 'Other',
                data: [21908, 5548, 8105, 11248, 8989, 11816, 18274,
                    17300, 13053, 11906, 10073]
            }],
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        });
        return window.dash_clientside.no_update
    }
        
    """,
        Output("highcharts", "children"),
        Input("highChartsData", "data"),
    )

















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