import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify

def btnFilter(variant="default",color="blue"):
    return html.Div(
            dmc.ActionIcon(
                            DashIconify(icon="feather:filter"), 
                            color=color, 
                            variant=variant,
                            id="btn-filter",
                            n_clicks=0,
                            mb=10,
                        ),
        )

def btnCollapse(variant="default",color="blue"):
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

def btnDownload(variant="default",color="blue"):
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