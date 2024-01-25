from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *
from ..utils.builder import *
from ..utils.helpers import *

def comercial_block_filt(rubro = 'Agricola', orientation = 'h'):
        select_anio = Entry.select(id = 'select-anio', texto = "Año", size = 'sm',clearable=True)
        select_cliente = Entry.select(id = 'select-cliente', texto = "Cliente", size = 'sm',searchable=True) 
        select_grupo_cliente = Entry.select(id = 'select-grupo-cliente', texto = "Grupo Cliente", size = 'sm') 
        select_producto = Entry.select(id = 'select-producto', texto = "Producto", size = 'sm') 
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
                        Column([select_anio],size= 2),
                        Column([select_cliente],size= 2),
                        Column([selector_first],size= 2),
                        Column([selector_second],size= 2),
                        Column([select_moneda],size= 2),
                ])
        else:
                return Div([
                        Row([Column([select_anio])]),
                        Row([Column([select_cliente])]),
                        Row([Column([selector_first])]),
                        Row([Column([selector_second])]),
                        Row([Column([select_grupo_cliente])]),
                        Row([Column([select_producto])]),
                        Row([Column([select_moneda])]),
   
                ])


def comercial_offcanvas_filt(dict_filt = {}, dict_comp = {}, add_filter = []):
        # extraer_list_value_dict con el value = componente nos traer objetos inputs-selects
        if len(add_filter) == 0:
                lista_componentes = get_list_values(
                                                    dict_input = dict_filt, 
                                                    dict_componentes = dict_comp, 
                                                    tipe_value ='componente'
                                                    )
        else:
                lista_componentes = get_list_values(
                                                    dict_input = dict_filt, 
                                                    dict_componentes = dict_comp, 
                                                    tipe_value ='componente'
                                                    ) + add_filter
        
        return DataDisplay.offcanvas(componentes= lista_componentes,label='Filtros')

def agricola_offcanvas_filt():
        return DataDisplay.offcanvas(
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
        
def block_offcanvas_comercial_filter(dict_filtros = {}, diccionario_componentes = {}, add_filter = []):
        # extraer_list_value_dict con el value = componente nos traer objetos inputs-selects
        if len(add_filter) == 0:
                lista_componentes = extraer_list_value_dict(dict_input = dict_filtros, dict_componentes = diccionario_componentes, tipe_value ='componente')
        else:
                lista_componentes = extraer_list_value_dict(dict_input = dict_filtros, dict_componentes = diccionario_componentes, tipe_value ='componente') + add_filter
        
        return DataDisplay.offcanvas(componentes= lista_componentes,label='Filtros')