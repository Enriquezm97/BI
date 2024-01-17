from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS,DASH_CSS_FILE
from ..build.layout.error.dashboard_error import ERROR
from ..build.api.get_connect import connect_api
from ..build.layout.layout_produccion import *
from ..build.utils.transform.t_logistica import *

def dashboard_ejecucion_campania(codigo = ''):#filtros = ['select-anio','select-grupo','select-rango']
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    
    app.layout =  ejecucion_campania(dataframe = None)
    return app