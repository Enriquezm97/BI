import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify



def cardIndex(title,link,image,shadou,descripcion="Descripción"):
    return html.Div(
        dmc.Card(
                                children=[
                                    dmc.CardSection(
                                        dmc.Group(
                                            children=[
                                                dmc.Anchor(
                                                        #"Gastos Operativos", href="/gastos-operativos", 
                                                        title,
                                                        href=link,
                                                        underline=False, 
                                                    ),
                                            ],
                                            position="apart",
                                        ),
                                        withBorder=True,
                                        inheritPadding=True,
                                        py="xs",
                                    ),
                                    
                                    dmc.CardSection(
                                        dmc.Image(
                                            src=image,
                                            mt="sm",
                                            height=300
                                        ),
                                    ),
                                    dmc.Text(
                                        children=[
                                            dmc.Text(
                                                [
                                                    
                                                    descripcion,
                                                ]
                                            ),
                                        ],
                                        mt="sm",
                                        color="dimmed",
                                        size="sm",
                                    ),

                                ],
                                withBorder=True,
                                shadow=shadou,
                                radius="lg",
                                #style={"width": 350},
                            )
    )