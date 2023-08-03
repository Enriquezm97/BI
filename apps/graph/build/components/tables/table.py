from dash import dash_table
from dash import dash_table,html
import dash_ag_grid as dag

def tableAgGrid(dataframe,col='',row_blue=''):
     name_first_col=dataframe.columns[0]
     
     return html.Div([
            dag.AgGrid(
                                    #id="datatable-result",
        #[{"field": i} for i in table_df.columns]
                                    columnDefs=[{"field": dataframe.columns[0],"type": "leftAligned","maxWidth": 200}]+[{"field": i,"type": "leftAligned","maxWidth": 110} for i in dataframe.columns[-2:]],
                                    rowData=dataframe.to_dict("records"),
                                    #dashGridOptions={"rowSelection": "multiple"},
                                    #columnSize="sizeToFit",
                                    defaultColDef={"resizable": True},
                                    #style={'overflow': "auto"},#'max-height': f'{300}px',
                                    className="ag-theme-balham headers2",
                                    #"['Flavia Mccloskey', 'Lilly Boaz'].includes(params.data.employee)"
                                    #'filter_query': '{ACTIVO CORRIENTE} contains "Total"'
                                    #"params.data.sickDays > 5 && params.data.sickDays <= 7"
                                    rowClassRules={"bg-primary fw-bold": f"params.data.ACTIVO CORRIENTE == '{row_blue}'"},#{col}
                                    columnSize="sizeToFit",
                                    dashGridOptions={"domLayout": "autoHeight"},
                                    #dashGridOptions={"alignedGrids": ["bottom-grid"]},
                                    suppressDragLeaveHidesColumns=False,
                                    style={'height': '100%'},
                                ),
     ])


def table_dash(dataframe):
       return dash_table.DataTable(
        data=dataframe.to_dict('records'),
        columns=[
            {'name': i, 'id': i}
            if i != 'Date' else
            {'name': 'Date', 'id': 'Date', 'type': 'datetime'}
            for i in dataframe.columns
        ],
        style_table={'overflowY': 'auto'},
        fixed_rows={'headers': True},
        style_as_list_view=True,
        style_cell={'padding': '12px',
                                 'font-family': 'sans-serif',
                                  'font-size': '14px',
                                  'text_align': 'left',

                                  'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'maxWidth': 0
                                  #'minWidth': 30, 'maxWidth': 70, #'width': 95
                                },
        style_cell_conditional=[
            {'if': {'column_id': 'ACTIVO CORRIENTE'},
            'width': '45%'},
            {'if': {'column_id': 'PASIVO CORRIENTE'},
            'width': '45%'},
            {'if': {'column_id': 'PASIVO NO CORRIENTE'},
            'width': '45%'},
            {'if': {'column_id': 'ACTIVO NO CORRIENTE'},
            'width': '45%'},
            {'if': {'column_id': 'PATRIMONIO'},
            'width': '45%'},
        ],
        style_header={
                        #'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'text_align': 'left',
                        'font-size': '14px',    
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'
                    },
         tooltip_data=[
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in dataframe.to_dict('records')
        ],
        tooltip_duration=None,
        
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{ACTIVO CORRIENTE} contains "Total"'
            },
        
            'backgroundColor': '#0074D9',
            'color': 'white',
            'fontWeight': 'bold',
        },
        {
            
            'if': {
                'filter_query': '{PASIVO CORRIENTE} contains "Total"'
            },
            
            'backgroundColor': '#0074D9',
            'color': 'white',
            'fontWeight': 'bold',
        },
        {
            
            
            'if': {
                'filter_query': '{ACTIVO NO CORRIENTE} contains "Total"'
            },
            
            'backgroundColor': '#0074D9',
            'color': 'white',
            'fontWeight': 'bold',
        },
        {
            
            
            'if': {
                'filter_query': '{PASIVO NO CORRIENTE} contains "Total"'
            },
            
            'backgroundColor': '#0074D9',
            'color': 'white',
            'fontWeight': 'bold',
        },
        {
            
            
            'if': {
                'filter_query': '{PATRIMONIO} contains "Total"'
            },
            'backgroundColor': '#0074D9',
            'color': 'white',
            'fontWeight': 'bold',
        },

    ]
        
    )



def table_dash_gp(dataframe):
       return dash_table.DataTable(
        data=dataframe.to_dict('records'),
        columns=[
            {'name': i, 'id': i}
            if i != 'Date' else
            {'name': 'Date', 'id': 'Date', 'type': 'datetime'}
            for i in dataframe.columns
        ],
        style_table={'height': '1300px'},#'overflowY': 'auto',
        fixed_rows={'headers': True},
        style_as_list_view=True,
        style_cell={'padding': '10px',
                                 'font-family': 'sans-serif',
                                  'font-size': '13px',
                                  'text_align': 'right',

                                  'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'maxWidth': 0
                                  #'minWidth': 30, 'maxWidth': 70, #'width': 95
                                },
        style_cell_conditional=[
            {'if': {'column_id': 'grupo_funcion'},
            'width': '15%'},
            
        ],
        style_header={
                        #'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'text_align': 'center',
                        'font-size': '12px',    
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'
                    },
         tooltip_data=[
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in dataframe.to_dict('records')
        ],
        tooltip_duration=None,
        
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{grupo_funcion} contains "UTILIDAD"'
            },
        
            'backgroundColor': '#0074D9',
            'color': 'white',
            'fontWeight': 'bold',
        },
        {
            
            'if': {
                'filter_query': '{grupo_funcion} contains "EBIT"'
            },
            
            'backgroundColor': '#0074D9',
            'color': 'white',
            'fontWeight': 'bold',
        },
        {
            
            
            'if': {
                'filter_query': '{grupo_funcion} contains "EBT"'
            },
            
            'backgroundColor': '#0074D9',
            'color': 'white',
            'fontWeight': 'bold',
        },
        

    ]
        
    )