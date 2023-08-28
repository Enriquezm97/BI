import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify
from datetime import datetime, date, timedelta



def datepickerRange(first=datetime.now().date(), last=datetime.now().date() + timedelta(days=5)):
    return html.Div(
                    [
                        dmc.DateRangePicker(
                            id="date-range-picker",
                            label="Date Range",
                            description="You can also provide a description",
                           #minDate=date(2020, 8, 5),
                            #value=[date(2020, 8, 5), date(2020, 8, 5)],
                            locale='es',
                            value=[first,last],
                            style={"width": 330},
                        ),
                        
                    ]
                )
def datePickerRangeId(ids="date-range-picker",text='Fecha inicio y fin - Campaña',value=None,minimo=None,maximo=None):
    return html.Div([
        dmc.DateRangePicker(
                                    id=ids,
                                    label=text,
                                    locale="es",
                                    value=value,
                                    minDate=minimo,
                                    maxDate=maximo
                                    #disabled=True
                                    #minDate=date(2020, 8, 5),
                                    #value=[datetime.now().date(), datetime.now().date() + timedelta(days=5)],
                                    #style={"width": 330},
                                ),
    ])

def datePicker(ids="date-range-picker",text='Desde',value=None,minimo=None,maximo=None):
    return html.Div([
        dmc.DatePicker(
            id=ids,
            label=text,
            #description="You can also provide a description",
            minDate=minimo,
            maxDate=maximo,
            value=value,
            locale="es",
            
            
        ),
    ])