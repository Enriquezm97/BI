import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback,dcc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc


def checkbox(ids=None,label=""):
    return html.Div([dmc.Checkbox(id=ids, label=label, mb=10),])
    

def checkboxGroup(ids,texto,value=[],orientacion="horizontal",size="xs",requerido=False,offset="sm",space="xs",child=[]):
    return html.Div(
                [
                    dmc.CheckboxGroup(
                        id=ids,
                        label=texto,
                        value=value,
                        size=size,
                        #description="This is anonymous",
                        orientation=orientacion,
                        withAsterisk=requerido,
                        offset=offset,
                        mb=1,
                        spacing=space,
                        children=child,
                    ),
                ]
            )


def checkboxChild(list):
    #dmc.Checkbox(label="React", value="react"),
    return [dmc.Checkbox(label=i, value=i) for i in list]


############### DCC.CHECKLIST HASTA QUE DMC CHECKBOX FUNCIONE CORRECTAMENTE
def checkList(ids,texto,options=[],value=[],inline=False):
    return dbc.Checklist(  
                                    id=ids,
                                    options=options,
                                    value=value,
                                    inline=inline,
                                    #label_checked_style={"color": "red"},
                                    input_checked_style={
                                        "backgroundColor": "rgb(34, 139, 230)",
                                        "borderColor": "rgb(34, 139, 230)",
                                    },     
                            ),
                
            
