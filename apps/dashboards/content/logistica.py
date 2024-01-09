from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from ..build.layout.error.dashboard_error import ERROR
from ..build.api.get_connect import connect_api
from ..build.layout.layout_logistica import logistica_build
from ..build.utils.transform.t_logistica import *

def dashboard_stocks(codigo = '',empresa = ''):#filtros = ['select-anio','select-grupo','select-rango']
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout =  logistica_build() 
    try:
        if empresa == 'SAMPLAST':
            dff  = connect_api(sp_name = 'nsp_stocks_bi_samplast')
        else :
            dff  = connect_api(sp_name = 'nsp_stocks')
        stocks_df = clean_stocks(df = dff)
        print(stocks_df)
        #app.layout =  logistica_build()   
    except:
        app.layout = ERROR
    #app.layout =  logistica_build() 
    #dff  = connect_api(sp_name = 'nsp_stocks_bi_samplast')
    #stocks_df = clean_stocks(df = dff)
    #print(stocks_df)
    return app