import dash_mantine_components as dmc
from apps.graph.test.utils.components import DataDisplay,Entry
from apps.graph.test.utils.frame import Row,Column,Div


offcanvas_recurso_agricola=DataDisplay.offcanvas(
                            label='Filtros',
                            componentes=[
                                Entry.radioGroup(id="radio-serie-tiempo-ejex-recurso",
                                                texto="Serie de Tiempo",
                                                children=[dmc.Radio(label='Fecha', value='FECHA'),
                                                        dmc.Radio(label='Semana', value='week')],
                                                value='week'
                                ),
                                Entry.radioGroup(
                                                id="radio-serie-tiempo-ejey-recurso",
                                                texto="Serie de Tiempo",
                                                children=[dmc.Radio(label='Por Cantidad', value='cantidad'),
                                                        dmc.Radio(label='Por Hectárea', value='hectarea')],
                                                value='cantidad'
                                ),
                                Entry.checkList(id="checklist-recurso-agricola"),
                            ]
                        
                        )

offcanvas_costos_agricola=DataDisplay.offcanvas(
                        label='Filtros',
                        componentes=[
                               Entry.radioGroup(id="radio-ha-costos-agricola",
                                                texto="Tipo de Costo",
                                                children=[
                                                        dmc.Radio(label='Costos', value='totales'),
                                                        dmc.Radio(label='Costos por Ha', value='por ha')],
                                                value='totales'
                                ),  
                               Entry.radioGroup(id="radio-costos-moneda",
                                                texto="Tipo de Moneda",
                                                children=[
                                                        dmc.Radio(label='PEN', value='SALDO_MOF'),
                                                        dmc.Radio(label='USD', value='SALDO_MEX')],
                                                value='SALDO_MEX'
                                ),
                               Entry.checkList(id="checklist-tipo-costos"),  
                        ]
)


def block_comercial_filters_IV(rubro = 'Agricola', orientation = 'h'):
        select_anio = Entry.select(id = 'select-anio', texto = "Año", size = 'sm',clearable=True)
        select_mes = Entry.select(id = 'select-mes', texto = "Mes", size = 'sm')
        select_cliente = Entry.select(id = 'select-cliente', texto = "Cliente", size = 'sm') 
        select_moneda = Entry.select(
                                        id = 'select-moneda', texto = "Moneda", size = 'sm',
                                        data=[{"value": "Importe Soles", "label": "PEN"},{"value": "Importe Dolares", "label": "USD"}],
                                        value='Importe Dolares',
                                        clearable=False
                        ) 
        if rubro == 'Agricola':
              selector_first = Entry.select(id = 'select-cultivo', texto = "Cultivo", size = 'sm') 
              selector_second = Entry.select(id = 'select-variedad', texto = "Variedad", size = 'sm') 
        else :
              selector_first = Entry.select(id = 'select-tipo-venta', texto = "Tipo de Venta", size = 'sm') 
              selector_second = Entry.select(id = 'select-grupo-producto', texto = "Grupo de Producto", size = 'sm')  
        if  orientation == 'h':
                return Row([
                        Column([
                                select_anio   
                        ],size= 2),
                        #olumn([
                        #        select_mes
                        #],size= 2),
                        Column([
                                select_cliente
                        ],size= 2),
                        Column([
                                selector_first 
                        ],size= 2),
                        Column([
                                selector_second
                        ],size= 2),
                        Column([
                                select_moneda
                        ],size= 2),
                ])
        else:
                return Div([
                        Row([Column([select_anio])]),
                        #Row([Column([select_mes])]),
                        Row([Column([select_cliente])]),
                        Row([Column([selector_first])]),
                        Row([Column([selector_second])]),
                        Row([Column([select_moneda])]),
                        
                ])