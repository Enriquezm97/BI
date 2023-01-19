import dash_bootstrap_components as dbc
from dash import dcc, html

def offcanvas(componentes=[]):
    return html.Div(
        dbc.Offcanvas(children =componentes,
                      scrollable=True,
                      id="offcanvas-placement",
                      title="Filtros",
                      is_open=False,
                      backdrop=False,
                      style={"width":250}
                    )
    )