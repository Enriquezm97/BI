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
