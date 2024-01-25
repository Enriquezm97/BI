from dash import Input, Output,State,no_update,dcc,html
import pandas as pd
import plotly.graph_objects as go


def opened_modal(
    app,
    id = '',
    height_modal = 500, 
    type_children = 'Figure'
): 
    
    modal_id = f'modal_{id}'
    id_button = f'maxi_{id}'
    @app.callback(
        [Output(modal_id, "opened"),
         Output(modal_id, "children")],
        [Input(id_button, "n_clicks")],
        [State(id,'figure'),
        State(modal_id, "opened")],
        prevent_initial_call=True,
    )
    #if type_children == 'Figure':
    def toggle_modal(n_clicks,figure, opened):
        
            fig=go.Figure(figure)
            fig.update_traces(hoverlabel=dict(font_size=30,bgcolor="white"),)
            fig.update_layout(height = height_modal,
                              
                              title_font_size = 30)
            
            fig.update_xaxes(
                             tickfont=dict(size=20),
                             color='black',
                             showticklabels = True,
                             title_font_family="sans-serif",
                             title_font_size = 30,
                             automargin=True
                            )
            fig.update_yaxes(
                             tickfont=dict(size=20),
                             color='black',
                             showticklabels = True,
                             title_font_family="sans-serif",
                             title_font_size = 30,
                             automargin=True
                            )  
            fig.update_layout(
                legend=dict(
                    
                    title_font_family="sans-serif",
                    font=dict(
                        family="sans-serif",
                        size=25,
                        color="black"
                    ),
                    
                )
            )
            try:
                fig.update_traces(hoverinfo='label+percent+value', textfont_size = 20,marker=dict(line=dict(color='#000000', width=1)))
            except:
                pass
        
            if n_clicks:
                return True,dcc.Graph(figure=fig)
            else:
                return not opened
            
def offcanvas_filters(app, id_input_btn = "btn-filter"):
    @app.callback(
        Output("offcanvas-placement", "is_open"),
        Input(id_input_btn, "n_clicks"),
        State("offcanvas-placement", "is_open"),
    )
    def toggle_offcanvas_scrollable(n1, is_open):
        if n1:
            return not is_open
        return is_open

def download_data(
    app,input_id_data="data-values",input_id_btn="btn-download",output="download", name_file="comercial.xlsx"
):
    @app.callback(
            Output(output, "data"),
            
            Input(input_id_btn, "n_clicks"),
            State(input_id_data,"data"),
            prevent_initial_call=True,
            
            )
    def update_download(n_clicks_download,data):
        if n_clicks_download:
            df = pd.DataFrame(data)
            return dcc.send_data_frame(df.to_excel, name_file, sheet_name="Sheet_name_1",index =False)
