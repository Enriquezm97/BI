from ..utils.theme import Container
from ..utils.frame import *
from ..utils.components.components_main import *
from ..utils.blocks.block_card import *
from ..utils.components.components_filters import *
from ...test.utils.functions.functions_data import * 
from ...test.utils.functions.functions_figure import *
from apps.graph.test.utils.crum import get_empresa,get_nombre_user,get_rubro_empresa
from apps.graph.test.utils.figures import *
import requests
from bs4 import BeautifulSoup
from lxml import etree
#
serie_list = ['PN01792AM','PN01714AM','PN01720AM','PN01724AM','PN01725AM','PN01777AM',
            'PN01779AM','PN01780AM','PN01781AM','PN01783AM','PN01788AM','PN01793AM','PN01791AM','PN01795AM']
def get_bcrp(series = serie_list,start_period = '2019-01', end_period = '2024-01'):
    def get_api(api):
        response = requests.get(api)
        objeto=response.json()
        return objeto
    def data_clean(dff = None):
        list_month_text=['Ene','Feb', 'Mar', 'Abr','May', 'Jun', 'Jul','Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        dff['month_text']=dff['name'].str[:3]
        dff['year']=dff['name'].str[4:]
        dff['month_number']=dff['month_text']
        for mes_text,i in zip(list_month_text,range(12)):

            dff['month_number'].loc[dff.month_text==mes_text]=dff['month_text']

            dff['month_number'].loc[dff.month_text==mes_text]=dff['month_text'].replace(mes_text,i+1)
        dff['year']=dff['year'].astype("string")
        dff['month_number']=dff['month_number'].astype("string")
        dff['periodo']=dff['year']+'-'+dff['month_number']+'-01'
        dff['periodo']=pd.to_datetime(dff['periodo'])
        return dff
    for code_ in series:
        api_csv=f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{code_}/json/{start_period}/{end_period}/esp"
        data = get_api(api_csv)
        name = data['config']['series'][0]['name']
        df_ = pd.DataFrame(data['periods'])
        df_ = df_.rename(columns={'values': name})
        df_[name] = df_[name].apply(lambda x: x[0])
        df_[name] = df_[name].astype(float)
        df_[name] = df_[name].round(1)
        if series[0] == code_:
            dataframe = df_.copy()
        else:
            dataframe = dataframe.merge(df_, how='inner', left_on=["name"], right_on=["name"])
    return data_clean(dff = dataframe)


def card_l(title_card = '', description = '', url = '',child = []):
    return Div([dmc.Card(
        children=[
            dmc.CardSection(
                child
            ),
            dmc.Group(
                [
                    dmc.Text(title_card, weight=400,size="lg"),
                    dmc.Badge("habilitado", color="green", variant="light"),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                description ,
                size="sm",
                color="dimmed",
            ),
        html.A(
            dmc.Button(
                "Ingresar",
                variant="light",
                color="blue",
                fullWidth=True,
                mt="md",
                radius="md",
            ),
            href=f"/{get_nombre_user()}/{url}"
        )
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        
    )])
    
    
def card_tc(title_card = '', description = '', url = '',child = []):
    url='https://cuantoestaeldolar.pe/'
    page= requests.get(url)
    s = BeautifulSoup(page.text,'lxml')
    dom=etree.HTML(str(s))
    comprasunat=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[1]/div[2]/div/div[1]/p')[0].text)
    ventasunat=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[1]/div[2]/div/div[2]/p')[0].text)
   

    compradolar=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[2]/div[2]/div/div[1]/p')[0].text)

    ventadolar=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[2]/div[2]/div/div[2]/p')[0].text)


    compraeuro=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[3]/div[2]/div/div[1]/p')[0].text)
    ventaeuro=float(dom.xpath('//*[@id="converter"]/div/div[2]/div[3]/div[2]/div/div[2]/p')[0].text)
    #https://cuantoestaeldolar.pe/icons/bbva.svg

    return Div([dmc.Card(
        children=[
            dmc.Text(children =[dmc.Center(children=[DashIconify(icon='', width=25,className="me-1"),'Tipo de Cambio'])] , weight=600, color='black'),
            dmc.Divider(variant="solid"),
            dmc.SimpleGrid(
                cols=3,
                children=[
                    dmc.Text(children ='Cotización', weight=700,size="lg"),
                    dmc.Text('Compra', weight=500,size="lg"),
                    dmc.Text('Venta' , weight=500,size="lg"),
                    
                    dmc.Text(children ='Sunat', weight=500, color='black'),
                    dmc.Text(comprasunat, weight=500,size="lg"),
                    dmc.Text(ventasunat , weight=500,size="lg"),
                    
                    dmc.Text(children ='Dólar', weight=500, color='black'),
                    dmc.Text(compradolar, weight=500,size="lg"),
                    dmc.Text(ventadolar , weight=500,size="lg"),
                   
                    dmc.Text(children ='Euro', weight=500, color='black'),
                    dmc.Text(compraeuro, weight=500,size="lg"),
                    dmc.Text(ventaeuro , weight=500,size="lg"),
                    
                ]
            )
            #dmc.Group(
            #    [
            #        dmc.Text(comprasunat, weight=500,size="lg"),
                    #dmc.Badge("habilitado", color="green", variant="light"),
            #    ],
            #    position="apart",
            #    mt="md",
            #    mb="xs",
            #),
            #dmc.Text(
            #    ventasunat ,
            #    size="sm",
            #    color="dimmed",
            #),
        
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        
        
        
    )])
def card_status_service():
    return Div([dmc.Card(
        children=[
            dmc.Text(children =[dmc.Center(children=['Servicios ON'])] , weight=600, color='black', size="xl"),
            dmc.Divider(variant="solid"),
            
        
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        
        
        
    )])

def line_2trace(df = None, height = 380, title = 'test',x = '', y = '',y2='',x_title = '',y_title = ''):

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
                mode = "number+delta",
                value = list(df[y])[-1],
                delta = {"reference": list(df[y])[-2], "valueformat": ".2f"},
                number = {'valueformat':'.3f'},
                title = {"text": "HOY"},
                domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )
    fig.add_trace(go.Scatter(
        x = df[x],
        y = df[y],
        name = y,
        cliponaxis=False,
        marker=dict(color="#3aa99b"),
        hoverlabel=dict(font_size=13,bgcolor="white"),
        mode='lines'
    ))
    fig.add_trace(go.Scatter(
        x = df[x],
        y = df[y2],
        name = y2,
        cliponaxis=False,
        marker=dict(color="#228be6"),
        hoverlabel=dict(font_size=13,bgcolor="white"),
        mode='lines'
    ))
    fig.update_layout(

        yaxis=dict(
            title=dict(text='<b>'+y_title+'</b>'),
            side="left",

        ),
        xaxis_title='<b>'+x_title+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template = 'plotly_white'
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_xaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 40, b = 90 ,t = 40, l = 40 ))
    fig.update_layout(hovermode="x unified")
    return fig

def fillarea_(df = None, height = 380, title = 'test',x = '', y = [],x_title = '',y_title = '',tipo = 'PBI', color_list = px.colors.qualitative.Set3,legend_site ='over' ):

    fig = go.Figure()
    for ejey,color in zip(y,color_list):
        if tipo == 'PBI':
            fig.add_trace(go.Scatter(
                x = df[x],
                y = df[ejey],
                name = ejey[82:],
                cliponaxis=False,
                marker=dict(color = color),
                hoverlabel=dict(font_size=13,bgcolor="white"),
                mode='lines',
                stackgroup='one'
            ))
        else:
            fig.add_trace(go.Scatter(
                x = df[x],
                y = df[ejey],
                name = ejey[47:],
                cliponaxis=False,
                marker=dict(color = color),
                hoverlabel=dict(font_size=13,bgcolor="white"),
                mode='lines',
                stackgroup='one'
            ))
    
    fig.update_layout(

        yaxis=dict(
            title=dict(text='<b>'+y_title+'</b>'),
            side="left",

        ),
        xaxis_title='<b>'+x_title+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template = 'plotly_white'
    )
    if legend_site == 'over':
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    fig.update_xaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 40, b = 90 ,t = 40, l = 40 ))
    fig.update_layout(hovermode="x unified")
    return fig

def bar_iter(df = None, height = 380, title = 'test',x = '', y = [],x_title = '',y_title = '', color_list = px.colors.qualitative.Set3,legend_site ='over' ):

    fig = go.Figure()
    for ejey,color in zip(y,color_list):
            fig.add_trace(go.Bar(
                x = df[x],
                y = df[ejey],
                name = ejey[47:],
                cliponaxis=False,
                marker=dict(color = color),
                hoverlabel=dict(font_size=13,bgcolor="white"),
                hovertemplate='<br>'+ejey[47:]+': <b>%{y:,.0f}</b><br>'+'Año'+': <b>%{x}</b>'
                
            ))
    
    fig.update_layout(

        yaxis=dict(
            title=dict(text='<b>'+y_title+'</b>'),
            side="left",

        ),
        xaxis_title='<b>'+x_title+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template = 'plotly_white'
    )
    if legend_site == 'over':
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    fig.update_xaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=13),color='black',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 40, b = 90 ,t = 40, l = 40 ))
    fig.update_layout( barmode='group',bargap=0.15, bargroupgap=0.1 )
    return fig
"""
                    #BBVA
                    dmc.Image(src = 'https://cuantoestaeldolar.pe/icons/bbva.svg',height=25,width=80),
                    dmc.Text(0 , weight=500,size="lg"),
                    dmc.Text(0 , weight=500,size="lg"),
                    #BCP
                    dmc.Image(src = 'https://cuantoestaeldolar.pe/icons/bcp.svg',height=25,width=90),
                    dmc.Text(0 , weight=500,size="lg"),
                    dmc.Text(0 , weight=500,size="lg"),
                    #INTERBANK
                    dmc.Image(src = 'https://cuantoestaeldolar.pe/icons/interbank.svg',height=25,width=130),
                    dmc.Text(0 , weight=500,size="lg"),
                    dmc.Text(0 , weight=500,size="lg"),
                    """   
        
def inicio_build(dataframe_tc = None):#dataframe = None, dataframe_ventas = None, 
    #productos_df_20=dataframe_ventas.groupby(['Producto','Grupo Producto','Subgrupo Producto'])[["Importe Dolares"]].sum().sort_values("Importe Dolares",ascending=True).tail(20).reset_index()
    #productos_df_20['Producto']=productos_df_20['Producto'].str.capitalize()
    PBI_=['Producto bruto interno y demanda interna (variaciones porcentuales anualizadas) - Agropecuario - Agrícola',
       'Producto bruto interno y demanda interna (variaciones porcentuales anualizadas) - Manufactura',
       'Producto bruto interno y demanda interna (variaciones porcentuales anualizadas) - Construcción',
       'Producto bruto interno y demanda interna (variaciones porcentuales anualizadas) - Comercio']
    PRODUCCION_=['Producción agropecuaria (miles de toneladas) - Agrícola - Espárrago',
     'Producción agropecuaria (miles de toneladas) - Agrícola - Papa',
       'Producción agropecuaria (miles de toneladas) - Agrícola - Cebolla',
       'Producción agropecuaria (miles de toneladas) - Agrícola - Mandarina',
       'Producción agropecuaria (miles de toneladas) - Agrícola - Naranja',
       'Producción agropecuaria (miles de toneladas) - Agrícola - Tomate',
       'Producción agropecuaria (miles de toneladas) - Agrícola - Limón',
       'Producción agropecuaria (miles de toneladas) - Agrícola - Uva',
       'Producción agropecuaria (miles de toneladas) - Agrícola - Maíz Amarillo Duro',
       'Producción agropecuaria (miles de toneladas) - Agrícola - Mango']
    dff = get_bcrp()
    print(dff)
    print(dff.columns)
    produccion_ton_df = dff.groupby(['year'])[PRODUCCION_].sum().reset_index()
    print(produccion_ton_df)
    return Container([
        #Row([
        #    Column([
        #        Title.title(text = 'Inicio')  
        #    ],size=12), 
        #]),
        Row([
            Column([
            
                card_graph_(title = 'TIPO DE CAMBIO (SUNAT)',height=380,with_id=False,fig=line_2trace(df = dataframe_tc, height = 380, title = '',x = 'Fecha', y = 'Compra',y2 = 'Venta',x_title='Fecha', y_title = 'Soles'))  
            ],size=5), 
             Column([
                card_graph_(title = 'PBI Y DEMANDA INTERNA (VAR% ANUAL) - PERÚ',height=380,with_id=False,fig=fillarea_(df=dff,height = 380, title = '',x = 'periodo', y = PBI_,x_title = '',y_title = '%'))  
            ],size=7), 
            
        ]),
        Row([
            Column([
                card_graph_(title = 'PRODUCCIÓN (MILES-TONELADAS) - PERÚ',height=380,with_id=False,fig=bar_iter(df=produccion_ton_df,height = 380, title = '',x = 'year', y = PRODUCCION_,x_title = '',y_title = 'Toneladas', color_list = px.colors.qualitative.Pastel, legend_site='under'))  
            ],size=12), 
        ]),
    ])
   #    card_l(title_card='Ventas',child=[
            #        DataDisplay.loadingOverlay(
            #                dcc.Graph(figure = GraphBargo.bar_(df=productos_df_20, x= "Importe Dolares", y= 'Producto',orientation= 'h', height = 300, 
            #                        title= 'Top 10 Productos Vendidos', customdata=['Grupo Producto','Subgrupo Producto'], text= "Importe Dolares",
            #                        showticklabel_y=True, 
            #                        xaxis_title = "Importe Dolares", template= 'none',size_tickfont=13#px.colors.qualitative.Alphabet
            #                        ),
            #                )
                            
            #        )  
            #    ],url='informe-ventas')  
    #card_l(title_card='Almacen',child=[
            #    DataDisplay.loadingOverlay(
            #            dcc.Graph(figure = figure_stock_var_y2(df=dataframe, height = 300, moneda = 'Dolares'),)
            #            
            #    )  
            #],url='inventario')