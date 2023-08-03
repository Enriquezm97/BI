import dash_ag_grid as dag
import pandas as pd
from dash import dash_table

def tableDag(
            id = '',
            columnDefs = [],
            dataframe = pd.DataFrame(),
            defaultColDef = {"resizable": True, "sortable": True, "filter": True, "minWidth":100},
            theme = "ag-theme-balham",
            rules_col = []
):
    return dag.AgGrid(
                id=id,
                columnDefs=columnDefs,
                rowData=dataframe.to_dict("records"),
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                className = theme,
                rowClassRules={"bg-primary fw-bold": f"[{rules_col[0]}].includes(params.data.{rules_col[1]})"},
                #columnDefs=columnDefs,
            ), 
