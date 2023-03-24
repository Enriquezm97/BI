import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify



def cardIndex(title,link,graph,shadou,descripcion="Descripción"):
    return html.Div(
        dmc.Card(
                                children=[
                                    dmc.CardSection(
                                        dmc.Group(
                                            children=[
                                                html.A(title,href=link)
                                            #    dmc.Anchor(
                                            #    title,
                                            #    href=link,
                                            #)
                                               
                                                
                                            ],
                                            position="apart",
                                        ),
                                        withBorder=True,
                                        inheritPadding=True,
                                        py="xs",
                                    ),
                                    
                                    dmc.CardSection(
                                        children=[graph],
                                        #dmc.Image(
                                        #    src=image,
                                        #    mt="sm",
                                        #    height=300
                                        #),
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
                                radius="md",
                                #style={"width": 350},
                            )
    )