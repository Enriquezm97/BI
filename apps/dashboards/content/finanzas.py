from django_plotly_dash import DjangoDash
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS,DASH_CSS_FILE
from ..build.layout.error.dashboard_error import ERROR
from ..build.layout.layout_finanzas import *
from ..build.utils.transform.t_finanzas import *
from ..build.utils.crum import get_data_connect
from ..build.api.connector import  APIConnector
from ..build.components.figure_comp import *
from ..build.utils.figure import *
from ..build.utils.global_callback import * 

def dashboard_bg(codigo = ''):
    ip, token_ =get_data_connect()
    api = APIConnector(ip, token_)
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    finanzas_df = clean_bg(api.send_get_dataframe(endpoint="nsp_etl_situacion_financiera",params=None))
    app.layout =  balance_general(formato=finanzas_df['formato'].unique())
    
    
    @app.callback(
        [   
            Output('select-anio','data'),
            Output('select-mes','data'),
            Output('select-trismestre','data'),
            Output("data-values","data"),
            Output("notifications-update-data","children")
        ],
        [   
            Input('select-formato','value'),
            Input('select-anio','value'),
            Input('select-mes','value'),
            Input('select-trismestre','value'),
            #Input('select-moneda','value'),
        ],
    )
    def update_data_bg(*args):
        formato = args[0]
        year = args[1]
        month = args[2]
        trim = args[3]
        print(args)
        dff = finanzas_df[finanzas_df['formato']==formato]
        if validar_all_none(variables = (year,month,trim)) == True:
            df = dff.copy()
        else:
            df = dff.query(dataframe_filtro(values=(year,month,trim),columns_df=['Año','Mes_num','Trimestre']))
        
        return [
            [{'label': i, 'value': i} for i in sorted(df['Año'].unique())],
            [{'label': i, 'value': i} for i in sorted(df['Mes_num'].unique())],
            [{'label': i, 'value': i} for i in sorted(df['Trimestre'].unique())],
            df.to_dict('series'),  
            DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update')
        ]
    
    @app.callback(
        [   
            Output("fondo-maniobra-graph","figure"),
            Output("activo-group3-graph","figure"),
            Output("pasivo-group3-graph","figure"),
            #table-dag
            #Output("table-dag","rowData"),
            #Output("table-dag","columnDefs"),

        ],
        [   
            Input('select-moneda','value'),
            Input("data-values","data"),
        ],
    )
    def update_graph(moneda,data):
        df = pd.DataFrame(data)
        col_moneda = 'saldomof' if moneda == 'soles' else 'saldomex'
        
        #bg_df.groupby(['titulo1','titulo3'])[['saldomex']].sum().reset_index()
        activo_df = df[df['titulo1']=='ACTIVO']
        activo_p3_df = activo_df.groupby(['titulo1','titulo3'])[[col_moneda]].sum().sort_values(col_moneda).reset_index()
        pasivo_df = df[df['titulo1']=='PASIVO']
        pasivo_p3_df = pasivo_df.groupby(['titulo1','titulo3'])[[col_moneda]].sum().sort_values(col_moneda).reset_index()
        
        act_pas_corr_df = df[df['titulo2'].isin(['ACTIVO CORRIENTE','PASIVO CORRIENTE'])]
        corr_pivot_df = pd.pivot_table(act_pas_corr_df,index=['periodo','Año', 'Mes', 'Mes_num', 'Mes_', 'Trimestre'],values='saldomex',columns='titulo2',aggfunc='sum').reset_index()
        corr_pivot_df['Fondo de Maniobra'] = corr_pivot_df['ACTIVO CORRIENTE'] - corr_pivot_df['PASIVO CORRIENTE']
        fondo_mani_df = corr_pivot_df.groupby(['Mes_num','Mes_'])[['Fondo de Maniobra']].sum().sort_values('Mes_num',ascending = True).reset_index()
        
        table_df = df.groupby(['Año', 'Mes', 'Mes_num', 'Mes_','titulo1','titulo2', 'titulo3'])[[col_moneda]].sum().reset_index()
        pivot_test_df = pd.pivot_table(table_df,index=['titulo1','titulo2', 'titulo3'],values=col_moneda,columns=['Año','Mes_num'],aggfunc='sum').fillna(0).reset_index()
        return [
            bar_ver(df = fondo_mani_df, height = 300, x = 'Mes_',y='Fondo de Maniobra',name_x='Mes',name_y='Fondo de Maniobra',title = '',color = '#4374E6'),
            bar_hor(df = activo_p3_df, height = 300, x= col_moneda, y = 'titulo3', name_x=moneda, name_y='Activo',title = '',color = '#4543E6'),
            bar_hor(df = pasivo_p3_df, height = 300, x= col_moneda, y = 'titulo3', name_x=moneda, name_y='Pasivo',title = '',color = '#7EC2EB'),
            #pivot_test_df.to_dict("records"),
            #fields_columns(columns = table_df.columns),

        ]
        #patrimonio = df[df['titulo1']=='PATRIMONIO']
        #patrimonio.groupby(['titulo1','titulo3'])[[col_moneda]].sum().reset_index()
    opened_modal(app, id="fondo-maniobra-graph",height_modal=900)
    opened_modal(app, id="activo-group3-graph",height_modal=900)
    opened_modal(app, id="pasivo-group3-graph",height_modal=900)
    return app


def dashboard_balance_ap(codigo = ''):
    ip, token_ =get_data_connect()
    api = APIConnector(ip, token_)
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    finanzas_df = clean_bg(api.send_get_dataframe(endpoint="nsp_etl_situacion_financiera",params=None))
    app.layout =  balance_activo_pasivo(formato=finanzas_df['formato'].unique())
    
    @app.callback(
        [   
            Output('select-anio','data'),
            Output('select-mes','data'),
            Output('select-trismestre','data'),
            Output("data-values","data"),
            Output("notifications-update-data","children")
        ],
        [   
            Input('select-formato','value'),
            Input('select-anio','value'),
            Input('select-mes','value'),
            Input('select-trismestre','value'),
            #Input('select-moneda','value'),
        ],
    )
    def update_data_bg(*args):
        formato = args[0]
        year = args[1]
        month = args[2]
        trim = args[3]
        print(args)
        dff = finanzas_df[finanzas_df['formato']==formato]
        if validar_all_none(variables = (year,month,trim)) == True:
            df = dff.copy()
        else:
            df = dff.query(dataframe_filtro(values=(year,month,trim),columns_df=['Año','Mes_num','Trimestre']))
        
        return [
            [{'label': i, 'value': i} for i in sorted(df['Año'].unique())],
            [{'label': i, 'value': i} for i in sorted(df['Mes_num'].unique())],
            [{'label': i, 'value': i} for i in sorted(df['Trimestre'].unique())],
            df.to_dict('series'),  
            DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update')
        ]
    @app.callback(
        [   
            Output("ap-pie-graph","figure"),
            Output("avsp-line-graph","figure"),
            Output("comp-activo-graph","figure"),
            Output("comp-pasivo-graph","figure"),

        ],
        [   
            Input('select-moneda','value'),
            Input("data-values","data"),
        ],
    )
    def update_graph(moneda,data):
        df = pd.DataFrame(data)
        col_moneda = 'saldomof' if moneda == 'soles' else 'saldomex'
        colors_ = px.colors.qualitative.Bold+px.colors.qualitative.Set3
        
        ap_dff = df[df['titulo1'].isin(['ACTIVO','PASIVO'])]
        
        ap_df = ap_dff.groupby(['titulo1'])[[col_moneda]].sum().reset_index()
        ap_df[col_moneda] = ap_df[col_moneda].abs()
        
        line_df = ap_dff.groupby(['Año','Mes_num','Mes_','titulo1'])[[col_moneda]].sum().reset_index()
        line_df[col_moneda] = line_df[col_moneda].abs()
        line_pivot_dff = pd.pivot_table(line_df,index=['Año','Mes_num', 'Mes_'],values=col_moneda,columns='titulo1',aggfunc='sum').reset_index()
        line_pivot_dff['Year-Month'] = line_pivot_dff['Año'] +'-'+ line_pivot_dff['Mes_']
        
        activo_df = df[df['titulo1']=='ACTIVO']
        activo3_df = activo_df.groupby(['Año','Mes_num','Mes_','titulo3'])[[col_moneda]].sum().reset_index()
        activo3_df['Year-Month'] = activo3_df['Año'] +'-'+ activo3_df['Mes_']
        fig_activo = px.bar(activo3_df, y=activo3_df[col_moneda], x=activo3_df['Year-Month'],color = 'titulo3',template ='plotly_white',color_discrete_sequence =colors_,custom_data=['titulo3'] )
        fig_activo.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',height = 320)
        fig_activo.update_layout(barmode='relative',legend_title_text = 'Activo')
        fig_activo.update_traces(cliponaxis=False)
        fig_activo.update_xaxes(tickfont=dict(size=11),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 11,automargin=True) 
        fig_activo.update_yaxes(tickfont=dict(size=11),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 11,automargin=True)
        fig_activo.update_layout(
            margin = dict( l = 20, r = 40, b = 50, t = 20),
            xaxis_title = '<b>'+'Mes'+'</b>',
            yaxis_title = '<b>'+''+'</b>',
            legend=dict(font=dict(size=11,color="black"))
        )                                                                           #'%{customdata}%'
        fig_activo.update_traces(hovertemplate='<br><b>%{x}</b><br><b>%{customdata[0]}</b><br><b>%{y:,.2f}</b>',hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'))
        
        
        pasivo_df = df[df['titulo1']=='PASIVO']
        pasivo3_df = pasivo_df.groupby(['Año','Mes_num','Mes_','titulo3'])[[col_moneda]].sum().reset_index()
        pasivo3_df['Year-Month'] = pasivo3_df['Año'] +'-'+ pasivo3_df['Mes_']
        fig_pasivo = px.bar(pasivo3_df, y=pasivo3_df[col_moneda], x=pasivo3_df['Year-Month'],color = 'titulo3',template ='plotly_white',color_discrete_sequence =colors_,custom_data=['titulo3'])
        fig_pasivo.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',height = 320)
        fig_pasivo.update_layout(barmode='relative',legend_title_text = 'Pasivo')
        fig_pasivo.update_traces(cliponaxis=False)
        fig_pasivo.update_xaxes(tickfont=dict(size=11),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 11,automargin=True) 
        fig_pasivo.update_yaxes(tickfont=dict(size=11),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 11,automargin=True)
        fig_pasivo.update_layout(
            margin = dict( l = 20, r = 40, b = 50, t = 20,),
            xaxis_title = '<b>'+'Mes'+'</b>',
            yaxis_title = '<b>'+''+'</b>',
            legend=dict(font=dict(size=11,color="black"))
        )
        fig_pasivo.update_traces(hovertemplate='<br><b>%{x}</b><br><b>%{customdata[0]}</b><br><b>%{y:,.2f}</b>', hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'))
        
        return [pie_(
                    df = ap_df, 
                    label_col = 'titulo1', 
                    value_col = col_moneda, 
                    title = '',
                    height=300,
                    showlegend = True,
                    #color_list=['#ccaa14','#7a9c9f'],
                    dict_color={'ACTIVO':'#7a9c9f','PASIVO':'#ccaa14'},
                    hole = .6,
                    textinfo = 'percent+value',
                    textposition='outside'
                ),
                
                figure_n_traces(df = line_pivot_dff, height = 300 , trace = ['ACTIVO','PASIVO'],colors = ['#7a9c9f','#ccaa14'],ejex=['Year-Month'],hover_unified=True),
                fig_activo,
                fig_pasivo,
                
        ]
    opened_modal(app, id="ap-pie-graph",height_modal=900)
    opened_modal(app, id="avsp-line-graph",height_modal=600)
    opened_modal(app, id="comp-activo-graph",height_modal=900)
    opened_modal(app, id="comp-pasivo-graph",height_modal=900)
    return app 

def dashboard_analisis_activo(codigo = ''):
   #bg_analisis_activo
    ip, token_ =get_data_connect()
    api = APIConnector(ip, token_)
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    finanzas_df = clean_bg(api.send_get_dataframe(endpoint="nsp_etl_situacion_financiera",params=None))
    app.layout =  bg_analisis_activo(formato=finanzas_df['formato'].unique(),years=sorted(finanzas_df['Año'].unique()))#finanzas_df['formato'].unique()
    @app.callback(
        [   
            Output('select-mes','data'),
            Output('select-trismestre','data'),
            Output("data-values","data"),
            Output("notifications-update-data","children")
        ],
        [   
            Input('select-formato','value'),
            Input('select-anio','value'),
            Input('select-mes','value'),
            Input('select-trismestre','value'),
            #Input('select-moneda','value'),
        ],
    )
    def update_data_bg(*args):
        formato = args[0]
        year = args[1]
        month = args[2]
        trim = args[3]
        print(args)
        dff = finanzas_df[finanzas_df['formato']==formato]
        if validar_all_none(variables = (year,month,trim)) == True:
            df = dff.copy()
        else:
            df = dff.query(dataframe_filtro(values=(year,month,trim),columns_df=['Año','Mes_num','Trimestre']))
        
        return [
            [{'label': i, 'value': i} for i in sorted(df['Mes_num'].unique())],
            [{'label': i, 'value': i} for i in sorted(df['Trimestre'].unique())],
            df.to_dict('series'),  
            DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update')
        ]
    @app.callback(
        [   
            Output("activo-graph","figure"),
            Output("actvant-graph","figure"),
            Output("corr-ncorr-graph","figure"),
            Output("cuentas-act-graph","figure"),

        ],
        [   
            Input('select-moneda','value'),
            Input("data-values","data"),
        ],
    )
    def update_graph(moneda,data):
        df = pd.DataFrame(data)
        col_moneda = 'saldomof' if moneda == 'soles' else 'saldomex'
        colors_ = px.colors.qualitative.Bold+px.colors.qualitative.Set3
        
        activo_dff = df[df['titulo1'].isin(['ACTIVO'])]
        ap_df = activo_dff.groupby(['titulo2'])[[col_moneda]].sum().reset_index()
        
        year_act_df = activo_dff.groupby(['Año','Mes_num','Mes_'])[[col_moneda]].sum().reset_index()
        year_df = pd.pivot_table(year_act_df,index=['Mes_num', 'Mes_'],values=col_moneda,columns='Año',aggfunc='sum').reset_index()
        #ap_df[col_moneda] = ap_df[col_moneda].abs()
        
        act2_df = activo_dff.groupby(['Año','Mes_num','Mes_','titulo2'])[[col_moneda]].sum().reset_index()
        act2_pv_df = pd.pivot_table(act2_df,index=['Año','Mes_num', 'Mes_'],values=col_moneda,columns='titulo2',aggfunc='sum').reset_index()
        act2_pv_df['Year-Month'] = act2_pv_df['Año'] +'-'+ act2_pv_df['Mes_']
        
        act4_df = activo_dff.groupby(['titulo4'])[[col_moneda]].sum().sort_values(col_moneda).reset_index()
        
        return [pie_(
                    df = ap_df, 
                    label_col = 'titulo2', 
                    value_col = col_moneda, 
                    title = '',
                    height=300,
                    showlegend = True,
                    #color_list=['#ccaa14','#7a9c9f'],
                    dict_color={'ACTIVO CORRIENTE':'#2B4CEA','ACTIVO NO CORRIENTE':'#974EE6'},
                    hole = .6,
                    textinfo = 'percent+value',
                    textposition='outside'
                ),
                figure_n_traces(df = year_df, height = 300 , trace = sorted(year_act_df['Año'].unique()),colors = colors_,ejex=['Mes_']),
                figure_n_traces(df = act2_pv_df, height = 300 , trace = act2_df['titulo2'].unique(),colors = colors_,ejex=['Year-Month']),
                bar_ver(df = act4_df, height = 300 , x = 'titulo4',y = col_moneda,name_x = 'Nivel 4',name_y = 'Saldos',color = '#3aa99b', title = '',showticklabels_x = False,botton_size = None)
                #figure_two_traces(df = line_pivot_dff, height = 300 , trace = ['ACTIVO','PASIVO'],colors = ['#7a9c9f','#ccaa14']),
                #fig_activo,
                #fig_pasivo,
                ]
    opened_modal(app, id="activo-graph",height_modal=900)
    opened_modal(app, id="actvant-graph",height_modal=900)
    opened_modal(app, id="corr-ncorr-graph",height_modal=900)
    opened_modal(app, id="cuentas-act-graph",height_modal=900)
    
    return app

def dashboard_analisis_pasivo(codigo = ''):
   #bg_analisis_activo
    ip, token_ =get_data_connect()
    api = APIConnector(ip, token_)
    app = DjangoDash(name = codigo,external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/css/dashstyles.css" })
    finanzas_df = clean_bg(api.send_get_dataframe(endpoint="nsp_etl_situacion_financiera",params=None))
    cuenta_filt_df = finanzas_df['idcuenta'].str[:3]
    list_cuenta = cuenta_filt_df.unique()
    app.layout =  bg_analisis_pasivo(
        formato=finanzas_df['formato'].unique(),
        years=sorted(finanzas_df['Año'].unique()),
        data_cuenta=sorted(list_cuenta),
        value_cuenta=list_cuenta[0]
    )
    @app.callback(
        [   
            Output('select-mes','data'),
            Output('select-trismestre','data'),

            Output("data-values","data"),
            Output("notifications-update-data","children")
        ],
        [   
            Input('select-formato','value'),
            Input('select-anio','value'),
            Input('select-mes','value'),
            Input('select-trismestre','value'),
            #Input('select-moneda','value'),
        ],
    )
    def update_data_bg(*args):
        formato = args[0]
        year = args[1]
        month = args[2]
        trim = args[3]
        print(args)
        dff = finanzas_df[finanzas_df['formato']==formato]
        if validar_all_none(variables = (year,month,trim)) == True:
            df = dff.copy()
        else:
            df = dff.query(dataframe_filtro(values=(year,month,trim),columns_df=['Año','Mes_num','Trimestre']))
        
        cuenta_df = df['idcuenta'].str[:3]
        cuenta_value = cuenta_df.unique()
        
        return [
            [{'label': i, 'value': i} for i in sorted(df['Mes_num'].unique())],
            [{'label': i, 'value': i} for i in sorted(df['Trimestre'].unique())],
            df.to_dict('series'),  
            DataDisplay.notification(text=f'Se cargaron {len(df)} filas',title='Update')
        ]
    @app.callback(
        [   
            Output("pasivo-graph","figure"),
            Output("pasvant-graph","figure"),
            Output("corr-ncorr-graph","figure"),
            Output("cuentas-pas-graph","figure"),

        ],
        [   
            Input('select-moneda','value'),
            Input('select-cuenta','value'),
            Input("data-values","data"),
        ],
    )
    def update_graph(moneda,idcuenta,data):
        df = pd.DataFrame(data)
        
        col_moneda = 'saldomof' if moneda == 'soles' else 'saldomex'
        colors_ = px.colors.qualitative.Bold+px.colors.qualitative.Set3
        
        pasivo_dff = df[df['titulo1'].isin(['PASIVO'])]
        ap_df = pasivo_dff.groupby(['titulo2'])[[col_moneda]].sum().reset_index()
        ap_df[col_moneda] = ap_df[col_moneda].abs()
        
        year_act_df = pasivo_dff.groupby(['Año','Mes_num','Mes_'])[[col_moneda]].sum().reset_index()
        year_df = pd.pivot_table(year_act_df,index=['Mes_num', 'Mes_'],values=col_moneda,columns='Año',aggfunc='sum').reset_index()
        #ap_df[col_moneda] = ap_df[col_moneda].abs()
        
        pas2_df = pasivo_dff.groupby(['Año','Mes_num','Mes_','titulo2'])[[col_moneda]].sum().reset_index()
        pas2_pv_df = pd.pivot_table(pas2_df,index=['Año','Mes_num', 'Mes_'],values=col_moneda,columns='titulo2',aggfunc='sum').reset_index()
        pas2_pv_df['Year-Month'] = pas2_pv_df['Año'] +'-'+ pas2_pv_df['Mes_']
        
        pas4_df = pasivo_dff[pasivo_dff['idcuenta'].str.contains(idcuenta)]
        pas4_df = pas4_df.groupby(['titulo4'])[[col_moneda]].sum().sort_values(col_moneda).reset_index()
        
        return [pie_(
                    df = ap_df, 
                    label_col = 'titulo2', 
                    value_col = col_moneda, 
                    title = '',
                    height=300,
                    showlegend = True,
                    #color_list=['#ccaa14','#7a9c9f'],
                    dict_color={'PASIVO CORRIENTE':'#2B4CEA','PASIVO NO CORRIENTE':'#974EE6'},
                    hole = .6,
                    textinfo = 'percent+value',
                    textposition='outside'
                ),
                figure_n_traces(df = year_df, height = 300 , trace = sorted(year_act_df['Año'].unique()),colors = colors_,ejex=['Mes_']),
                figure_n_traces(df = pas2_pv_df, height = 300 , trace = pas2_df['titulo2'].unique(),colors = colors_,ejex=['Year-Month']),
                bar_ver(df = pas4_df, height = 300 , x = 'titulo4',y = col_moneda,name_x = 'Nivel 4',name_y = 'Saldos',color = '#3aa99b', title = '',showticklabels_x = False,botton_size = 50)
                #figure_two_traces(df = line_pivot_dff, height = 300 , trace = ['ACTIVO','PASIVO'],colors = ['#7a9c9f','#ccaa14']),
                #fig_activo,
                #fig_pasivo,
                ]
    opened_modal(app, id="pasivo-graph",height_modal=900)
    opened_modal(app, id="pasvant-graph",height_modal=900)
    opened_modal(app, id="corr-ncorr-graph",height_modal=900)
    opened_modal(app, id="cuentas-pas-graph",height_modal=900)
    return app