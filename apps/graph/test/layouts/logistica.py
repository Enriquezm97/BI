import pandas as pd
from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from asgiref.sync import sync_to_async
#from ..utils.components.components_main import *
from ..utils.functions.callbacks.callbacks_logistica import *
from ..utils.functions.functions_transform import clean_inventarios,clean_stock_alm
from ..Connection.apis import connection_api, connection_api_almstock 
from ..utils.functions.callbacks.callbacks_ import *
from ..utils.crum import get_empresa
from ..build.build_error import ERROR
from ..build.build_logistica import logistica_build,alm_stock_build




def logistica_dash(codido = '',filtros = ['select-anio','select-grupo','select-rango']):

    app = DjangoDash(name=codido,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    try:
        if get_empresa()== 'SAMPLAST':
            dff  = connection_api(sp_name = 'nsp_stocks_bi_samplast')
        else:
            dff  = connection_api(sp_name = 'nsp_stocks')
        logistica_df = clean_inventarios(df = dff) 
        app.layout = logistica_build()
        filter_callback(app, filt = filtros, dataframe = logistica_df)
        graph_log(app)
        opened_modal(app, modal_id="modal-bar-stock-items",children_out_id="bar-stock-items", id_button="maximize-bar-stock-items",height_modal=900)
        opened_modal(app, modal_id="modal-bar-stock-familia",children_out_id="bar-stock-familia", id_button="maximize-bar-stock-familia",height_modal=900)
        opened_modal(app, modal_id="modal-bar-top-producto",children_out_id="bar-top-producto", id_button="maximize-bar-top-producto",height_modal=900)
        opened_modal(app, modal_id="modal-bar-stock-abc-ventas",children_out_id="bar-stock-abc-ventas", id_button="maximize-bar-stock-abc-ventas",height_modal=900)
        opened_modal(app, modal_id="modal-bar-stock-abc-valorizado",children_out_id="bar-stock-abc-valorizado", id_button="maximize-bar-stock-abc-valorizado",height_modal=900)
        opened_modal(app, modal_id="modal-pie-stock-antiguedad",children_out_id="pie-stock-antiguedad", id_button="maximize-pie-stock-antiguedad",height_modal=900)
        opened_modal(app, modal_id="modal-pie-items-antiguedad",children_out_id="pie-items-antiguedad", id_button="maximize-pie-items-antiguedad",height_modal=900)
    except:
        app.layout = ERROR
    return app


def alm_stock_dash(codido= '',filtros = ['select-almacen','select-tipo','select-grupo']):
    
        app = DjangoDash(name = codido,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)#,kwargs={'dash_app_id':{'value':123}}
        app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    #try:
        dff  = connection_api_almstock()#.apply_async()
        
        alm_dff = clean_stock_alm(df = dff)
        
        app.layout = alm_stock_build(df = alm_dff)
        filter_callback_alm(app, filt = filtros, dataframe = alm_dff)
        graph_alm(app)
        opened_modal(app, modal_id="modal-bar-importe-stock",children_out_id="bar-importe-stock", id_button="maximize-bar-importe-stock",height_modal=900)
        opened_modal(app, modal_id="modal-pie-estadoinv",children_out_id="pie-estadoinv", id_button="maximize-pie-estadoinv",height_modal=900)
        opened_modal(app, modal_id="modal-bar-respon",children_out_id="bar-respon", id_button="maximize-bar-respon",height_modal=900)
    #except:
    #    app.layout = ERROR 
        return app


