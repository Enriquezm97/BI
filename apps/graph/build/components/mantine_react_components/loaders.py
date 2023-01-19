import time
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback
from dash_iconify import DashIconify

def loadingOverlay(component,type="bars",colors="#01414b",size="xl"):
    return html.Div(dmc.LoadingOverlay(component,
                        loaderProps={"variant": type, "color": colors, "size": size},
                        loader=dmc.Image(
                            src="https://i.imgur.com/KIj15up.gif", alt="", caption="", width=70,height=70#
                            ),
    ))