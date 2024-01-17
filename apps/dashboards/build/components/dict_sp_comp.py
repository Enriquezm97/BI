from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *
from ..utils.builder import *

def nsp_rpt_ventas_detallado_comp():
    select_anio = Entry.select(id = 'select-anio', texto = "Año", size = 'sm',clearable=True, value = 2023)
    select_cliente = Entry.select(id = 'select-cliente', texto = "Cliente", size = 'sm',searchable=True) 
    select_grupo_cliente = Entry.select(id = 'select-grupo-cliente', texto = "Grupo Cliente", size = 'sm',searchable=True) 
    select_producto = Entry.select(id = 'select-producto', texto = "Producto", size = 'sm',searchable=True) 
    select_sucursal = Entry.select(id = 'select-sucursal', texto = "Sucursal", size = 'sm',clearable=True)
    select_vendedor = Entry.select(id = 'select-vendedor', texto = "Vendedor", size = 'sm',clearable=True)
    select_tipo_movimiento = Entry.select(id = 'select-tipo-movimiento', texto = "Tipo de Movimiento", size = 'sm',clearable=True)
    select_tipo_venta = Entry.select(id = 'select-tipo-venta', texto = "Tipo de Venta", size = 'sm',clearable=True)
    select_tipo_condicion = Entry.select(id = 'select-tipo-condicion', texto = "Tipo de Condición", size = 'sm',clearable=True)
    select_grupo_producto = Entry.select(id = 'select-grupo-producto', texto = "Grupo de Producto", size = 'sm',searchable=True)
    select_subgrupo_producto = Entry.select(id = 'select-subgrupo-producto', texto = "Subgrupo de Producto", size = 'sm',searchable=True)
    select_marca_producto = Entry.select(id = 'select-marca-producto', texto = "Marca de Producto", size = 'sm',searchable=True)
    select_pais = Entry.select(id = 'select-pais', texto = "País", size = 'sm',searchable=True)
    select_cultivo = Entry.select(id = 'select-cultivo', texto = "Cultivo", size = 'sm',searchable=True) 
    select_variedad = Entry.select(id = 'select-variedad', texto = "Variedad", size = 'sm',searchable=True) 
    select_formato = Entry.select(id = 'select-formato', texto = "Formato", size = 'sm',searchable=True) 
    select_moneda = Entry.select(id = 'select-moneda', texto = "Moneda", size = 'sm',
                                data=[{"value": "Importe Dolares", "label": "USD"},{"value": "Importe Soles", "label": "PEN"}],
                                value='Importe Dolares',
                                clearable=False
                    )
   
    return  {       'Año' : {'select':{'id':'select-anio','componente':select_anio},'multiselect':{}},
                    'Cliente' : {'select':{'id':'select-cliente','componente':select_cliente},'multiselect':{}},
                    'Grupo Cliente' : {'select':{'id':'select-grupo-cliente','componente':select_grupo_cliente},'multiselect':{}},
                    'Producto' : {'select':{'id':'select-producto','componente':select_producto},'multiselect':{}},
                    'Sucursal' : {'select':{'id':'select-sucursal','componente':select_sucursal},'multiselect':{}},
                    'Vendedor' : {'select':{'id':'select-vendedor','componente':select_vendedor},'multiselect':{}},
                    'Tipo de Movimiento' : {'select':{'id':'select-tipo-movimiento','componente':select_tipo_movimiento},'multiselect':{}},
                    'Tipo de Venta' : {'select':{'id':'select-tipo-venta','componente':select_tipo_venta},'multiselect':{}},
                    'Tipo de Condicion' : {'select':{'id':'select-tipo-condicion','componente':select_tipo_condicion},'multiselect':{}},
                    'Grupo Producto' : {'select':{'id':'select-grupo-producto','componente':select_grupo_producto},'multiselect':{}},
                    'Subgrupo Producto' : {'select':{'id':'select-subgrupo','componente':select_subgrupo_producto},'multiselect':{}},
                    'Marca Producto': {'select':{'id':'select-marca-producto','componente':select_marca_producto},'multiselect':{}},
                    'Pais' : {'select':{'id':'select-pais','componente':select_pais},'multiselect':{}},
                    'Cultivo' : {'select':{'id':'select-cultivo','componente':select_cultivo},'multiselect':{}},
                    'Variedad' : {'select':{'id':'select-variedad','componente':select_variedad},'multiselect':{}},
                    'Formato' : {'select':{'id':'select-formato','componente':select_formato},'multiselect':{}},
                    'Moneda' : {'select':{'id':'select-moneda','componente': select_moneda},'multiselect':{}},
                    
                    
            }