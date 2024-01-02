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
        
def inicio_build(dataframe = None, dataframe_ventas = None):
    productos_df_20=dataframe_ventas.groupby(['Producto','Grupo Producto','Subgrupo Producto'])[["Importe Dolares"]].sum().sort_values("Importe Dolares",ascending=True).tail(20).reset_index()
    productos_df_20['Producto']=productos_df_20['Producto'].str.capitalize()
    return Container([
        Row([
            Column([
                Title.title(text = 'Inicio')  
            ],size=12), 
        ]),
        Row([
            Column([
            card_l(title_card='Almacen',child=[
                DataDisplay.loadingOverlay(
                        dcc.Graph(figure = figure_stock_var_y2(df=dataframe, height = 300, moneda = 'Dolares'),)
                        
                )  
            ])  
            ],size=4), 
             Column([
                card_l(title_card='Ventas',child=[
                    DataDisplay.loadingOverlay(
                            dcc.Graph(figure = GraphBargo.bar_(df=productos_df_20, x= "Importe Dolares", y= 'Producto',orientation= 'h', height = 300, 
                                    title= 'Top 10 Productos Vendidos', customdata=['Grupo Producto','Subgrupo Producto'],space_ticked= 280, text= "Importe Dolares",
                                    showticklabel_y=True, 
                                    xaxis_title = "Importe Dolares", template= 'none',size_tickfont=13#px.colors.qualitative.Alphabet
                                    ),
                            )
                            
                    )  
                ])  
            ],size=4), 
            Column([
                card_tc()
            ],size=4), 
        ]),
    
    ])
   