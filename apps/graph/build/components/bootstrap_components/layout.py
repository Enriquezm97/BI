import dash_bootstrap_components as dbc
def Column(content=[],size=12):
      return dbc.Col(content,width=size,className=f"col-xl-{size} col-md-{size} col-sm-12 col-12 mb-3")

