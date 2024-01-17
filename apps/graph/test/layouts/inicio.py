import pandas as pd
from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from ..utils.crum import get_empresa
from ..Connection.apis import connection_api, connection_api_almstock
from ..utils.functions.functions_transform import clean_inventarios,clean_stock_alm
from apps.graph.test.utils.functions.functions_transform import *
from ..build.build_inicio import * 
from django.views.decorators.cache import cache_page


def inicio_dash(codigo = ''):
    
    app = DjangoDash(name = codigo,external_stylesheets = EXTERNAL_STYLESHEETS, external_scripts = EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    #try:
    if get_empresa()== 'SAMPLAST':                
        dff  = connection_api(sp_name = 'nsp_stocks_bi_samplast')
    else:
        dff  = connection_api(sp_name = 'nsp_stocks')
        
    dffff = connection_api(sp_name='nsp_rpt_ventas_detallado')
    ventas_df = etl_comercial(dffff)    
        
    logistica_df = clean_inventarios(df = dff) 
        
    app.layout = inicio_build(dataframe = logistica_df,dataframe_ventas= ventas_df)
    
    return app