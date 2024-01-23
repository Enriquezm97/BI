import dash_bootstrap_components as dbc
import plotly.express as px

# MODIFICA EL IDIOMA POR DEFECTO DE UN DATAPICKER dmc
EXTERNAL_SCRIPTS = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/es.min.js",
    "https://cdn.plot.ly/plotly-locale-de-latest.js"
]

EXTERNAL_STYLESHEETS =  [
                            dbc.themes.BOOTSTRAP,
                            "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css",
                            dbc.icons.BOOTSTRAP
                        ]
DICT_CULTIVOS_COLOR={'Arandano':'#7A325A',
               'Esparrago':'#87AA6C',
               'Uva':'#AF799F',
               'Palta':'#527E03',
               'Compost':'#5F524B',
               'Mandarina':'#F74628',
               'Frambuesa':'#DE194D',
               'Algodon':"#ccddb8",
               'Quinua':"#E3C08C",
                'Granada':"#D77477",
                'Ensayos':"#000000",
               'Naranja':"#ffbf75",
               'Palto':"#527E03",
               'Zarzamora':"#ff35c2",
               'Duraznos':"#e4c5c4",                
               'Maiz':"#f4ff91",
               'Ninguno':"#1d3d33",
               'Ciruelo':"#ff5f7c",
               'Manzano':"#9dc09d",
               'Kaki':"#e6a15c",
               'Arandanos':"#b93af8",
               'Tangelo':"#fd971c",
               'Lima':"#97db51",
               'Citrico':"#a0fb0e",
               'Granada':"#d35d1d",
               'Palto p roduccion':"#527E03",
               'Zapallo':"#cbe03d",
               'Limon':"#93EE59",
               'Pecana':"#b16d57",
               'Mango': "#bb2328"

              }
DIC_RECURSOS_AGRICOLA = {
    
    'Metros cúbicos':"#00B6FF",
    'Horas máquina':"#000000",
    'Jornales':"#740000",
    'Potasio':"#1F77B4",
    'Calcio':"#FF7F0E",
    'Fosforo':"#2CA02C",
    'Magnesio':"#9467BD",
    'Nitrogeno':"#8C564B",
    'Zinc':"#BCBD22",

}

DICT_TIPO_COSTO={
    'Insumos':'lightcyan',
    'Mano de obra':'#575d6d',
    'Depreciación':'royalblue',
    'Otros':'darkblue',
    'Maquinaria':'#123570',
    'Riego':'cyan'
}
COLORS_G10 = px.colors.qualitative.G10

COMERCIAL_SELECTS_COLUMNS ={
    'select-anio' : 'Año',
    'select-mes' : ['Mes','Mes Num'],
    'select-cliente' : 'Cliente',
    'select-cultivo' : 'Cultivo',
    'select-variedad' : 'Variedad',
    'select-moneda' : ['Importe Soles','Importe dolares'],
    'select-tipo-venta' : 'Tipo de Venta',
    'select-grupo-producto' : 'Grupo Producto',
    'select-grupo-cliente' : 'Grupo Cliente',
    'select-producto':'Producto',
}

MESES_ORDER = ['Enero','Febrero','Marzo', 'Abril', 'Mayo','Junio', 'Julio', 'Agosto','Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
LISTA_COLORES_BAR = px.colors.diverging.Portland+px.colors.diverging.Earth+px.colors.diverging.balance+px.colors.diverging.Tealrose+px.colors.qualitative.Plotly+px.colors.qualitative.Dark24+px.colors.qualitative.Light24+px.colors.qualitative.Alphabet

COMERCIAL_LOGISTICA ={
    'select-anio' : 'Año',
    'select-grupo' : 'Grupo Producto',
    'select-rango' : 'Rango antigüedad del stock',
}

ALM_LOGISTICA ={
        'select-sucursal'   : 'Sucursal',
        'select-almacen'    : 'Almacén',
        'select-tipo'       : 'Tipo',
        'select-grupo'      : 'Grupo',
        'select-subgrupo'   : 'Sub Grupo',
        'select-producto'   : 'Producto',
        'select-grupo2'     : 'Grupo 2',
        'select-respon-en'  : 'Responsable Ingreso',
        'select-respon-sal' : 'Responsable Salida',
        'select-um'         : 'Unidad de Medida',
        'select-estado'     : 'Estado',
        
}