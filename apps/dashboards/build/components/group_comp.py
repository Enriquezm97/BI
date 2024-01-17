import pandas as pd
from datetime import datetime, date
from ..components.display_comp import * 
from ..components.layout_comp import *
from ..components.card_comp import *
from ..utils.builder import *


def slider_percent(value = None):
    return Entry.slider(
                        id = 'slider-percet',
                        value = value,
                        marks = [
                            {"value": 20, "label": "20%"},
                            {"value": 50, "label": "50%"},
                            {"value": 80, "label": "80%"}
                        ],
                        label_tick = False,
                        step = 10,
                        minimo = 10,
                        maximo = 100
    )

def datepicker_range_comercial(dataframe = pd.DataFrame(),name_fecha = 'Fecha', name_anio ='Año', tipo = 'Inicio'):
    dataframe['Fecha'] = dataframe['Fecha'].apply(lambda a: pd.to_datetime(a).date())
    fecha_minima = str(dataframe[name_fecha].min())
    fecha_maxima = str(dataframe[name_fecha].max())
    df = dataframe[dataframe[name_anio]==sorted(dataframe[name_anio].unique())[-1]]
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
