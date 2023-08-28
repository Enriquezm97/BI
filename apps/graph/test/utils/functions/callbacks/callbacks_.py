from dash import Input, Output,State,no_update,dcc,html
from apps.graph.test.constans import DIC_RECURSOS_AGRICOLA,COLORS_G10,DICT_TIPO_COSTO,DICT_CULTIVOS_COLOR
from apps.graph.test.utils.functions.functions_filters import *
from apps.graph.test.utils.functions.functions_data import *
from apps.graph.test.utils.components.components_main import DataDisplay,Button
from apps.graph.test.utils.figures import *
from apps.graph.test.utils.frame import Graph
from apps.graph.test.utils.tables import tableDag
from apps.graph.test.utils.blocks.block_card import cardDivider

import sys


##############################
def create_callback_offcanvas_filters(app, id_input_btn = "btn-filter"):
    @app.callback(
        Output("offcanvas-placement", "is_open"),
        Input(id_input_btn, "n_clicks"),
        State("offcanvas-placement", "is_open"),
    )
    def toggle_offcanvas_scrollable(n1, is_open):
        if n1:
            return not is_open
        return is_open
    

def create_callback_opened_modal(
    app,
    modal_id ='',
    children_out_id = '', 
    id_button = '', 
    height_modal = 500, 
    type_children = 'Figure'
): 
    @app.callback(
        Output(modal_id, "opened"),
        Output(modal_id, "children"),
        Input(id_button, "n_clicks"),
        State(children_out_id,'figure'),
        State(modal_id, "opened"),
        prevent_initial_call=True,
    )
    #if type_children == 'Figure':
    def toggle_modal(n_clicks,figure, opened):
        
            fig=go.Figure(figure)
            fig.update_layout(height = height_modal)
        
            if n_clicks:
                return True,dcc.Graph(figure=fig)
            else:
                return not opened
    