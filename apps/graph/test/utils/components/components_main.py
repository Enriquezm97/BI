import dash_mantine_components as dmc
from dash import html,dcc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
from datetime import datetime, date, timedelta

class DataDisplay():
    def accordion(
       children=[], texto='accordion',value='accordion',variant="default"
    ):
        return html.Div(
            dmc.Accordion(
                variant=variant,
                children=[
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(children=[dmc.Text(texto, weight=700),]),
                            dmc.AccordionPanel(children=children),
                        ],
                        value=value,
                    ), 
                ],
            )
        )
    
    def alert(
        ids=None,text="This alert will dismiss itself after 3 seconds!",title="Alerta", duration=3000,color="green"
    ):
        return html.Div(
            [
                dmc.Alert(
                    text,
                    title=title,
                    id=ids,
                    color=color,
                    duration=duration,
                ),
            ]
        )
    def drawer(componentes=[]):
        return html.Div(dmc.Drawer(
                            title="Filtros",
                            id="drawer",
                            padding="md",
                            children=componentes,
                            closeOnClickOutside=False,
                            closeOnEscape=True,
                            lockScroll=False,
                            withOverlay=False,
                            size="250px",
                            style={'position': 'absolute','z-index': '999'}
                        ),
                    )
    def offcanvas(
        componentes=[], label='', size_width=250, placement = "start"
    ):
        return html.Div(
            dbc.Offcanvas(
                        scrollable=True,
                        id="offcanvas-placement",
                        title=label,
                        is_open=False,
                        backdrop=False,
                        style={"width": size_width},
                        children =componentes,
                        placement = placement
                        )
        )
        
    def loadingOverlay(
        component,type="bars",colors="#01414b",size="xl"
    ):
        return html.Div(dmc.LoadingOverlay(component,
                            loaderProps={"variant": type, "color": colors, "size": size},
                            loader=dmc.Image(
                                src="https://i.imgur.com/KIj15up.gif", alt="", caption="", width=70,height=70#
                                ),
        ))
    def spoiler(text=""):
        return html.Div([
                dmc.Spoiler(
                    #id=ids,
                    showLabel="Mostrar más",
                    hideLabel="Hide",
                    maxHeight=50,
                    children=[
                        dmc.Text(children=text)
                    ],
                )
        ])
    def switchTheme():
        return html.Div([
                dmc.Switch(
                            id='switch',
                            offLabel=DashIconify(icon="radix-icons:moon", width=20),
                            onLabel=DashIconify(icon="radix-icons:sun", width=20),
                            size="lg",
                            checked=True,
                            color="blue",
                        )
        ])
    def notification(id='',text='',title=''):
        return dmc.Notification(
            id=id,
            title=title,
            message=[text],
            disallowClose=False,
            radius="xl",
            icon=[DashIconify(icon="feather:database", width=128)],
            action="show",
        )
    
    def modalMaximize(content=[]):
            return html.Div(
                [
                    dbc.ModalHeader(close_button=True),
                    dbc.ModalBody([content]),
                ],
            )
    
    def Tabs(content = [], value = None,):
            return html.Div(
                dmc.Tabs([dmc.TabsList(content)],value = value,)
            )
    
    def Tab(label = '', value = ''):
            return dmc.Tab(label, value = value)
    
    def TabsPanel(content = [], value = ''):
            return dmc.TabsPanel(children=content, value=value),
    def TabsList(content = []):
            return dmc.TabsList(children=[content]),
        
    def tabss( content=[], value = ''):
        return dmc.Tabs(children=content,value= value)
    def text(id = '', text = '',weight = 800, align = "center"):
        return dmc.Text(text, weight=weight,align=align),
            
                                    

class Button():
    def btnFilter(
        variant="default",color="blue",style={}
    ):
        return html.Div(
                dmc.ActionIcon(
                                DashIconify(icon="feather:filter"), 
                                color=color, 
                                variant=variant,
                                id="btn-filter",
                                n_clicks=0,
                                mb=10,
                                style = style
                            ),
            )
        
    def btnCollapse(
        variant="default",color="blue"
    ):
        return html.Div(
                dmc.ActionIcon(
                                DashIconify(icon="feather:chevron-up"), 
                                color=color, 
                                variant=variant,
                                id="btn-collapse",
                                n_clicks=0,
                                mb=10,
                            ),
            )
        
    def btnDownload(
        variant="default",color="blue"
    ):
        return html.Div(
                dmc.ActionIcon(
                                DashIconify(icon="feather:download"), 
                                color=color, 
                                variant=variant,
                                id="btn-download",
                                n_clicks=0,
                                mb=10,
                            ),
            )
    def btnConfig(
        variant="default",color="blue",style={}
    ):
        return html.Div(
                dmc.ActionIcon(
                                DashIconify(icon="feather:settings"), 
                                color=color, 
                                variant=variant,
                                id="btn-config",
                                n_clicks=0,
                                mb=10,
                                style = style
                            ),
            )
    def button(
        text="",variant="filled",color="indigo",ids=None
    ):
        return html.Div(
                [
                    dmc.Button(text,variant=variant,color=color,id=ids),
                ]
            )
    
    def actionIcon(
        variant="default",
        color="blue",
        id='btn-icon',
        style={'position': 'absolute','top': '4px','right': '4px','z-index': '99'},
        icono='maximize'
    ):
        return html.Div(
                dmc.ActionIcon(
                                DashIconify(icon=f"feather:{icono}"), 
                                color=color, 
                                variant=variant,
                                id=id,
                                n_clicks=0,
                                mb=10,
                                style=style
                            ),
            )
    
class Entry():
    
    def checkbox(
        ids=None,label=""
    ):
        return html.Div(
            [
                dmc.Checkbox(id=ids, label=label, mb=10)
            ]
        )
    
    def checkboxGroup(
        ids,texto,value=[],orientacion="horizontal",size="xs",requerido=False,offset="sm",space="xs",child=[]
    ):
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
        return [dmc.Checkbox(label=i, value=i) for i in list]
    
    def checkList(ids,texto,options=[],value=[],inline=False):
        return dbc.Checklist(  
                                        id=ids,
                                        options=options,
                                        value=value,
                                        inline=inline,
                                        input_checked_style={
                                            "backgroundColor": "rgb(34, 139, 230)",
                                            "borderColor": "rgb(34, 139, 230)",
                                        },     
                ),
        
    def datepickerRange(
        id='',
        #first=datetime.now().date(), 
        #last=datetime.now().date() + timedelta(days=5),
        label='',
        size='sm',
        disabled=False,
        
    ):
        return html.Div(
                        [
                            dmc.DateRangePicker(
                                id=id,
                                label=label,
                                #description="You can also provide a description",
                                locale='es',
                                size=size,
                                disabled=disabled,
                                #value=[first,last],
                                #tyle={"width": 330},
                            ), 
                        ]
                    )
    
    def datePickerRangeId(
        ids="date-range-picker",text='Fecha inicio y fin - Campaña',value=None,minimo=None,maximo=None
    ):
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
        
    def datePicker(
        id="",text='',value=None,minimo=None,maximo=None
    ):
        return html.Div([
            dmc.DatePicker(
                id = id,
                label = text,
                #description="You can also provide a description",
                minDate = minimo,
                maxDate = maximo,
                value = value,
                locale = "es",
                clearable = False
                
            ),
        ])
    def inputNumber():
        return html.Div(
            dmc.NumberInput(
                label="Number input with decimal steps",
                value=0.05,
                precision=2,
                min=-1,
                step=0.01,
                max=1,
                style={"width": 250},
            )
        )
        
    def inputNumPercent(
        ids='input-num',label="Number input",value=10,minimo=0,maximo=100
    ):
        return html.Div(
            dmc.NumberInput(
                id=ids,
                label=label,
                value=value,
                precision=1,
                min=minimo,
                step=1,
                max=maximo,
                #style={"width": 100},
                icon=DashIconify(icon="feather:percent"),
                #size="md",
            )
        )
        
    def radioGroup(
        id='',texto='',value=[],size="sm",space="xs",orientacion="horizontal",children=[]
    ):
        return  html.Div(
                    [
                        dmc.RadioGroup(
                            id=id,
                            children=children,
                            value=value,
                            label=texto,
                            size=size,
                            spacing=space,
                            mt=1,
                            orientation=orientacion,
                        ),
                        
                    ]
                )
    
    def radioChild(list):
        return [dmc.Radio(label=i, value=i) for i in list]
    
    def checkList(id='',inline=False):
        return html.Div([
            dbc.Checklist(  
                        id=id,
                        inline=inline,
                        input_checked_style={
                                        "backgroundColor": "rgb(34, 139, 230)",
                                        "borderColor": "rgb(34, 139, 230)",
                        },     
                        label_style={'font-size': '12px'} 
            ),
        ])
    
    def select(
        id='',texto='',place="Todos",value=None,data=[],clearable=True, searchable = False, size='md'
    ):
        return  html.Div(
            dmc.Select(
                id=id,
                #data=data,#["USDINR", "EURUSD", "USDTWD", "USDJPY"],
                data=data,
                label=texto,
                clearable=clearable,
                placeholder=place,
                style={'font-size': "90%"},
                value=value,
                size=size,
                searchable = searchable
                #searchable=True,
                #style={"width": 200},
                #icon=DashIconify(icon="radix-icons:magnifying-glass"),
                #rightSection=DashIconify(icon="radix-icons:chevron-down"),
            )
    )
        
    def multiSelect(
        id='w',texto='',place="",value=None,data=[],size='md'):
        return html.Div(
            dmc.MultiSelect(
                        #data=["React", "Angular", "Svelte", "Vue"],
                        id=id,
                        label=texto,
                        placeholder=place,
                        searchable=True,
                        nothingFound="Opción no encontrada",
                        value=value,
                        data=data,
                        style={'font-size': "80%"},
                        size=size, 
                    )
        )    
    
    def textInput(
        label="",id='',required=False,size="sm",error=False,value = None
    ):
        return html.Div([dmc.TextInput(label=label,id=id,required=required,size=size,error=error,value=value)]) 
    
    def numberInput(
        label="",id=None,value=0,precision=2,minimo=-10,step=0.01
    ):
        return  html.Div(
            [dmc.NumberInput(
                            label=label,
                            value=value,
                            precision=precision,
                            min=minimo,
                            step=step,
                            id=id)
            ]
        )
    
    def textAreaInput(
        label="",place="",autosize=True,minimorow=2,ids=None
    ):
        return html.Div(
            [dmc.Textarea(
                id=ids,
                label=label,
                placeholder=place,
                autosize=autosize,
                minRows=minimorow,
                ),
            ]
        )
    def chipGroup(id = '', content = []):
        return html.Div(
                [
                    dmc.Center(
                        dmc.ChipGroup(
                        children= content,
                        id=id,
                        #value=value,
                        multiple=True,
                    ),
                    )
                    

                ]
            )

    def slider(id = '', value = 11 , marks = [], label_tick = True, minimo = 0, maximo = 40, step = 0.5):
        return html.Div(
                [
                    dmc.Slider(
                        id = id,
                        value = value,
                        updatemode="drag",
                        marks = marks,
                        labelAlwaysOn= label_tick,
                        min= minimo, 
                        max= maximo,
                        step= step
                    ),
                    

                ]
            )
    
class Title():
    
    def title(text="",order=1,ids='id'):
        return html.Div([dmc.Title(text, order=order,id=ids)])
    

class Picking():
    def segmented(
        id='',value=None,data=[],
        full_width=True,color='rgb(34, 184, 207)',size='xs'
    ):
        return html.Div([
                dmc.SegmentedControl(
                                    id=id,
                                    value=value,
                                    data=data,
                                    fullWidth=full_width,
                                    color=color,
                                    size=size
                                ),
        ])
    