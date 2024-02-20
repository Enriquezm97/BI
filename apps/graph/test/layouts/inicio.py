import pandas as pd
from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from ..utils.crum import get_empresa
from ..Connection.apis import connection_api, conecction_data_tc
from ..utils.functions.functions_transform import clean_inventarios,clean_stock_alm
from apps.graph.test.utils.functions.functions_transform import *
from ..build.build_inicio import * 
from django.views.decorators.cache import cache_page
from apps.dashboards.build.layout.error.dashboard_error import ERROR
df =pd.read_parquet("data_inicio.parquet", engine="pyarrow")

def inicio_dash(codigo = ''):
    
    app = DjangoDash(name = codigo,external_stylesheets = EXTERNAL_STYLESHEETS, external_scripts = EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    
    #try:
    #if get_empresa()== 'SAMPLAST':                
    #    dff  = connection_api(sp_name = 'nsp_stocks_bi_samplast')
    #else:
    #    dff  = connection_api(sp_name = 'nsp_stocks')
        
    #dffff = connection_api(sp_name='nsp_rpt_ventas_detallado')
    #ventas_df = etl_comercial(dffff)    
        
    #logistica_df = clean_inventarios(df = dff) 
        
    app.layout = inicio_build(dataframe_tc = df  )#conecction_data_tc()
    #except:
    #    app.layout = ERROR
    
    return app