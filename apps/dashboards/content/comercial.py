from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS,DASH_CSS_FILE
from ..build.layout.error.dashboard_error import ERROR
from ..build.api.get_connect import connect_api
from ..build.layout.layout_comercial import *
from ..build.utils.transform.t_comercial import *


def dashboard_inf_ventas(codigo = '',empresa_rubro = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    app.layout =  informe_comercial(rubro_empresa = empresa_rubro)
    
    return app

def dashboard_seguimiento_comercial(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    app.layout =  seguimiento_comercial(filtros={})
    
    return app

def dashboard_ventas_clientes(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    try:
        app.layout =  ventas_clientes(filtros={}, dataframe = None)
    except:
        app.layout = ERROR
    
    return app


def dashboard_ventas_productos(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    try:
        app.layout =  ventas_productos(filtros={}, dataframe = None)
    except:
        app.layout = ERROR
    
    return app

def dashboard_ventas_cultivos(codigo = ''):
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css(DASH_CSS_FILE)
    try:
        app.layout =  ventas_cultivos(filtros={}, dataframe = None)
    except:
        app.layout = ERROR
    
    return app

