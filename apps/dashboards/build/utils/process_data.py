import pandas as pd

class ProcessNsp_rpt_ventas_detallado:
    def __init__(self,dataframe):
        self.dataframe = dataframe
    
    def productos_top(self,moneda = "",top = 20):
        dff = self.dataframe.groupby(
            ['Producto','Grupo Producto','Subgrupo Producto']
        )[[moneda]].sum().sort_values(moneda,ascending=True).tail(top).reset_index()
        return dff