
import dash_mantine_components as dmc
import pandas as pd
from datetime import datetime, date, timedelta
from apps.graph.test.utils.components.components_main import DataDisplay,Entry
from apps.graph.test.utils.frame import Row,Column,Div

def dict_components_comercial():
    select_anio = Entry.select(id = 'select-anio', texto = "Año", size = 'sm',clearable=True, value = 2020)
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
    select_moneda = Entry.select(
                                id = 'select-moneda', texto = "Moneda", size = 'sm',
                                data=[
                                     {"value": "Importe Soles", "label": "PEN"},
                                    {"value": "Importe Dolares", "label": "USD"}
                                    ],
                                value='Importe Dolares',
                                clearable=False
                            )
   
    """
    dict_principal={
    'Año' : {'select':{'id':'select-anio','componente':1},'multiselect':{'id':'multiselect-anio','componente':1}},
    'Cliente' : {'select':{'id':'select-cliente','componente':2},'multiselect':{'id':'multiselect-cliente','componente':2}},
    'Cultivo' : {'select':{'id':'select-cultivo','componente':3},'multiselect':{'id':'multiselect-cultivo','componente':3}},
    'Variedad' : {'select':{'id':'select-variedad','componente':4},'multiselect':{'id':'multiselect-variedad','componente':4}},
    'Grupo Producto' : {'select':{'id':'select-grupo-producto','componente':5},'multiselect':{'id':'multiselect-grupo-producto','componente':5}},
}'select':{},'multiselect':{}
    """
    
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
                    #'Fecha':{'datepicker-inicio':{'id':'datepicker-inicio','componente':'owo'},'datepicker-fin':{'id':'datepicker-fin','componente':'uwu'}}
                    
            }
def datepicker_(dataframe = pd.DataFrame(),name_fecha = '', name_anio ='', tipo = 'Inicio'):
    fecha_minima=str(dataframe[name_fecha].min())
    fecha_maxima=str(dataframe[name_fecha].max())
    print(fecha_minima,fecha_maxima)
    df=dataframe[dataframe[name_anio]==sorted(dataframe[name_anio].unique())[-1]]
    if tipo == 'Inicio' or tipo == 'inicio':
        return  Entry.datePicker(id='datepicker-inicio',
                                 text='Desde',
                                 value=df[name_fecha].min(),
                                 minimo=date(int(fecha_minima[:4]),int(fecha_minima[-5:-3]),int(fecha_minima[-2:])),
                                 maximo=date(int(fecha_maxima[:4]),int(fecha_maxima[-5:-3]),int(fecha_maxima[-2:])),
                                 )
    elif tipo == 'Fin' or tipo == 'fin':
        return  Entry.datePicker(id='datepicker-fin',
                                 text='Hasta',
                                 value=df[name_fecha].max(),
                                 minimo=date(int(fecha_minima[:4]),int(fecha_minima[-5:-3]),int(fecha_minima[-2:])),
                                 maximo=date(int(fecha_maxima[:4]),int(fecha_maxima[-5:-3]),int(fecha_maxima[-2:])),
                                 )