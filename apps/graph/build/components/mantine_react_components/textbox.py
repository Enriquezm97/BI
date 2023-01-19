import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify

def textInput(label="",ids=None,required=False,size="sm",error=False):
    return html.Div([dmc.TextInput(label=label,id=ids,required=required,size=size,error=error),]) 

def numberInput(label="",ids=None,value=0,precision=2,minimo=-10,step=0.01):
    return  html.Div([dmc.NumberInput(
                        label=label,
                        value=value,
                        precision=precision,
                        min=minimo,
                        step=step,
                        id=ids,
                        #max=1,
                        #style={"width": 250},
                    ),])
        
def textAreaInput(label="",place="",autosize=True,minimorow=2,ids=None):
    return html.Div([dmc.Textarea(
            id=ids,
            label=label,
            placeholder=place,
            
            autosize=autosize,
            minRows=minimorow,
        ),
        ])