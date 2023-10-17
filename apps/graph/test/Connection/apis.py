import pandas as pd
from apps.graph.test.utils.crum import get_data_connection
from apps.graph.test.Connection.read_api import getApi


def connection_api(sp_name = 'nsp_rpt_ventas_detallado'):
    ip, token_ =get_data_connection()
    dataframe = pd.DataFrame(getApi(api=f'http://{ip}:3005/api/consulta/{sp_name}',token = token_))
    return dataframe