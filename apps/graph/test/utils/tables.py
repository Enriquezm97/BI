import dash_ag_grid as dag
import pandas as pd
from dash import dash_table

def tableDag(
            id = '',
            columnDefs = [],
            dataframe = pd.DataFrame(),
            defaultColDef = {"resizable": True, "sortable": True, "filter": True, "minWidth":100},
            theme = "ag-theme-balham",
            rules_col = [],
            dashGridOptions = {"domLayout": "autoHeight"},
            rowClassRules ={},
            column_size = "responsiveSizeToFit",
            style = {'font-size':15} 
):
    return dag.AgGrid(
                id=id,
                columnDefs=columnDefs,
                rowData=dataframe.to_dict("records"),
                columnSize = column_size,
                defaultColDef=defaultColDef,
                className = theme,
                rowClassRules=rowClassRules,
                style=style,
                dashGridOptions=dashGridOptions,
                #columnDefs=columnDefs,
            ), 
