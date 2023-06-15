import dash_bootstrap_components as dbc
from dash import dcc, html
def modalMaximize(content=[]):
            return html.Div(
                [
                    dbc.ModalHeader(close_button=True),
                        #dbc.ModalTitle("Pantalla Completa"), close_button=True
                    #),
                    dbc.ModalBody(
                        [   
                            
                            content
                            #html.Div(dcc.Graph(figure=fig))
                        ]
                    ),
                ],
            )