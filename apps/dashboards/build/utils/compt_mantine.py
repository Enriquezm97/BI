import dash_mantine_components as dmc

def Contenedor_dmc(id = 'mantine-provider',theme_style = {}, content = []):
    return dmc.MantineProvider(
            id = id,
            withGlobalStyles=True,
            theme= theme_style,
            inherit = True,
            children = content
    )

def titulo(texto = "", id = 'title', color = "#4e3a8e", align = 'justify', order = 2, class_js = None):
    return dmc.Title(
            children = texto,
            id = id,
            color=color,
            align = align,
            order = order,
            className = class_js
    ),
def cardHeader(titulo = '', color_card = ''):
    return dmc.Card(children=[
        dmc.Grid(children=[
            dmc.Col(titulo,span=12)
        ], gutter="xs")
    ],
        withBorder=True,
        shadow="sm",
        radius="md",         
        style={"position": "static",'background-color':color_card},
        p=5
    )

def Col(content = [],size = 12):
    return dmc.Col(children = content, xs=12,sm =12,md = size,lg = size, xl = size)



   
"""
id='overview-container',
                    justify="center",
                    className='animate__animated animate__fadeIn animate__slow',
                    gutter='xs'
"""