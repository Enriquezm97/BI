from dash.dependencies import Output, Input, State

def drawerAction(app):
    @app.callback(
    Output("drawer", "opened"),
    Input("drawer-transition-button", "n_clicks"),
    prevent_initial_call=True,
    )
    def drawer_demo(n_clicks):
        return True

def offcanvasAction(app):
    @app.callback(
        Output("offcanvas-placement", "is_open"),
        Input("btn-filter", "n_clicks"),
        State("offcanvas-placement", "is_open"),
    )
    def toggle_offcanvas_scrollable(n1, is_open):
        if n1:
            return not is_open
        return is_open