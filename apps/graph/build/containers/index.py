from dash import Dash, dcc, html, Input, Output,State,dash_table
from dash.dash_table.Format import Format, Group, Scheme, Symbol
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
from apps.graph.data.data import *
from apps.graph.build.components.mantine_react_components.cards import cardIndex
import json
from apps.graph.build.utils.dict_colors import *
from apps.graph.data.data import *
from apps.graph.build.components.draw.bar import *
from apps.graph.build.components.draw.pie import *
from apps.graph.build.components.draw.line import *
from apps.graph.build.utils.dict_colors import *
from apps.graph.data.transform_finanzas import balancePivot


def costos_agricolas(dff,cols,radio_costos,ejey,simbolo):
            dff_lote=dff.groupby(cols).sum().reset_index()
            try:
                dff_lote['AREA_CAMPAÑA']=dff_lote['AREA_CAMPAÑA'].astype('object')
                dff_lote.loc[:,'TOTAL']= dff_lote.sum(numeric_only=True, axis=1)
                dff_lote['AREA_CAMPAÑA']=dff_lote['AREA_CAMPAÑA'].astype('float64')
            except:
                pass
            
            if radio_costos == 'CT':
                
                dff_lote=dff_lote.sort_values('TOTAL',ascending=False)
                #x=dff_lote['NCONSUMIDOR']
                x=dff_lote[cols[0]]
                y=dff_lote['TOTAL']
                color=dff_lote['CULTIVO']
                owo=dff_lote['TOTAL'].max()
                if owo>999999:
                    dff_lote['TOTAL_y']=dff_lote['TOTAL']/1000000   
                    promedio=(dff_lote['TOTAL_y'].sum())/len(dff_lote[cols[0]].unique()) 
                    title=f'Costos {simbolo}. / {ejey} (Millón)'
                elif owo<999999:
                    dff_lote['TOTAL_y']=dff_lote['TOTAL']/1000
                    promedio=(dff_lote['TOTAL_y'].sum())/len(dff_lote[cols[0]].unique())    
                    title=f'Costos {simbolo}. / {ejey} (Mil)'
                elif owo <1000:
                    dff_lote['TOTAL_y']=dff_lote['TOTAL']/1
                    promedio=(dff_lote['TOTAL_y'].sum())/len(dff_lote[cols[0]].unique())      
                    title=f'Costos {simbolo} / {ejey}'
                dff_lote['PROMEDIO']=promedio
                ejetotal='TOTAL_y'
           
            #return BarGOV_SX(dff_lote['TOTAL_y'],x,title,color,None,'Lotes',simbolo,dff_lote['PROMEDIO'],dff_lote['AREA_CAMPAÑA'])

            elif radio_costos == 'CH':

                dff_lote['AH']=dff_lote['TOTAL']/dff_lote['AREA_CAMPAÑA']
                dff_lote=dff_lote.sort_values('AH',ascending=False)
                x=dff_lote[cols[0]]
                y=dff_lote['AH']
                color=dff_lote['CULTIVO']
                owo=dff_lote['AH'].max()
                if owo>999999:
                    dff_lote['AH_y']=dff_lote['AH']/1000000 
                    promedio=(dff_lote['AH_y'].sum())/len(dff_lote[cols[0]].unique())   
                    title=f'Costos {simbolo} / Ha x {ejey} (Millón)'
                elif owo<999999:
                    dff_lote['AH_y']=dff_lote['AH']/1000
                    promedio=(dff_lote['AH_y'].sum())/len(dff_lote[cols[0]].unique())  
                    title=f'Costos {simbolo} / Ha x {ejey} (Mil)'
                elif owo <1000:
                    dff_lote['AH_y']=dff_lote['AH']/1
                    promedio=(dff_lote['AH_y'].sum())/len(dff_lote[cols[0]].unique())  
                    title=f'Costos {simbolo} / Ha x {ejey}'
                dff_lote['PROMEDIO']=promedio
                ejetotal='AH_y' 
            #last_year=str(sorted(dff_lote['AÑO_CAMPAÑA'].unique())[-1])
            #titulo_core=f"{title}"+", ".join([last_year])#f"{title} "+", ".join([ultimo_year])
            return BarGOV_SX(dff_lote[ejetotal],x,title,color,None,ejey,simbolo)  

def container_index(empresa,tipo_empresa,username):
    if tipo_empresa == "Agricola" or tipo_empresa == "Agroindustrial":
        agro=dataAgricolaEmpresa(empresa)
        bc=dataBcEmpresa(empresa)
        comercial=dataVentasEmpresa(empresa)

        df_general=agro[0]
        df_costos=agro[2]
        ## PRIMER FIG AGRICOLA RECURSOS
        dff=df_general[df_general['AÑO_CULTIVO']==sorted(df_general['AÑO_CULTIVO'].unique())[-1]]
        df_graph=dff.groupby(['DSCVARIABLE','TIPO','week','AÑO_FECHA','SEMANA'])[['CANTIDAD']].sum().reset_index()
        df_graph=df_graph.sort_values(by=['week','AÑO_FECHA','SEMANA'],ascending=True)
        #print(df_graph)
        fig_recursos=line_agricola_card(df_graph,'week',"CANTIDAD",'DSCVARIABLE',330,'week','Cantidad','Recursos',orders=orderX('week',df_graph),title='Recursos Agricolas')
        ## SEGUNDA FIG AGRICOLA COSTOS
        print(df_costos)
        try:
            dff_costos= df_costos.pivot(index=('CODCULTIVO','VARIEDAD','CULTIVO','AREA_CAMPAÑA','IDCONSUMIDOR','NCONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA'),values=("SALDO_MEX"),columns=('TIPO'))#
            dff_costos=pd.DataFrame(dff_costos.to_records())
            dff_costos=dff_costos[dff_costos['AÑO_CAMPAÑA']==sorted(dff_costos['AÑO_CAMPAÑA'].unique())[-1]]
        except:
             
             dff_costos = pd.DataFrame(columns=['CODCULTIVO','VARIEDAD','CULTIVO','AREA_CAMPAÑA','IDCONSUMIDOR','NCONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA','SALDO_MEX','TIPO'],index=range(3))
             dff_costos=dff_costos.fillna(0)
        fig_costos=costos_agricolas(dff_costos,['CULTIVO'],'CT','Cultivo','$')

        ## COMERCIAL
        #df_informe_ventas=comercial
        df_informe_ventas=comercial[comercial['YEAR']==sorted(comercial['YEAR'].unique())[-1]]
        df_pais_pie=df_informe_ventas.groupby(['PAIS'])[['IMPORTEMEX']].sum().sort_values('IMPORTEMEX',ascending=True).reset_index()
        fig_comercial=paisFacturado(df_pais_pie,"none",'IMPORTEMEX','Ventas por País')

        ## FINANCIERO
        column='TRIM'
        group=['year','trimestre']
        x='trimestre'
        df_ratios=balancePivot('Trimestre','dolares',bc)
        df = pd.DataFrame()
        df['Agrupado']=df_ratios[column]
        df['valor']=df_ratios['ACTIVO    ']/df_ratios['PASIVO    ']
        promedio=df['valor'].sum()/len(df['Agrupado'].unique())
        df['promedio']=promedio
        fig_bc=figure__line(df['Agrupado'],df['valor'],df['promedio'],'TEST','Valor','Promedio',1,2,"#FF390E",2,3,"#FFF80E",3,4,"#15FF0E")


        container= html.Div(
                [
                    dbc.Row(
                    [
                        dbc.Col([
                            cardIndex('Recursos Agricolas',f'{username}/plan-ejecucion',dcc.Graph(figure=fig_recursos),"lg")
                            #dcc.Graph(figure=fig_recursos)
                        ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                        dbc.Col([
                            cardIndex('Costos Agricolas',f'{username}/costos-campaña',dcc.Graph(figure=fig_costos),"lg")
                           #dcc.Graph(figure=fig_costos)
                        ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                        
                    ],
                    
                ),
                    dbc.Row(
                        [
                        dbc.Col([
                            #dcc.Graph(figure=fig_comercial)
                            cardIndex('Informe de Ventas',f'{username}/informe-ventas',dcc.Graph(figure=fig_comercial),"lg")
                        ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                        dbc.Col([
                            cardIndex('Indicadores Financieros',f'{username}/indicadores',dcc.Graph(figure=fig_bc),"lg")
             
                        ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                        ],
                        
                    ),
                    ]
            )
                
    else:
            bc=dataBcEmpresa(empresa)
            comercial=dataVentasEmpresa(empresa)
             ## COMERCIAL
            #df_informe_ventas=comercial
            df_informe_ventas=comercial[comercial['YEAR']==sorted(comercial['YEAR'].unique())[-1]]
            df_pais_pie=df_informe_ventas.groupby(['PAIS'])[['IMPORTEMEX']].sum().sort_values('IMPORTEMEX',ascending=True).reset_index()
            fig_comercial=paisFacturado(df_pais_pie,"none",'IMPORTEMEX','Ventas por País')

            ## FINANCIERO
            column='TRIM'
            group=['year','trimestre']
            x='trimestre'
            df_ratios=balancePivot('Trimestre','dolares',bc)
            df = pd.DataFrame()
            df['Agrupado']=df_ratios[column]
            df['valor']=df_ratios['ACTIVO    ']/df_ratios['PASIVO    ']
            promedio=df['valor'].sum()/len(df['Agrupado'].unique())
            df['promedio']=promedio
            fig_bc=figure__line(df['Agrupado'],df['valor'],df['promedio'],'TEST','Valor','Promedio',1,2,"#FF390E",2,3,"#FFF80E",3,4,"#15FF0E")


            #fig_recursos=go.Figure([go.Bar(x=animals, y=[20, 14, 23])])
            container= html.Div([
                dbc.Row(
                        [
                        dbc.Col([
                            #dcc.Graph(figure=fig_comercial)
                            cardIndex('Informe de Ventas',f'{username}/informe-ventas',dcc.Graph(figure=fig_comercial),"lg")
                        ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                        dbc.Col([
                            cardIndex('Indicadores Financieros',f'{username}/indicadores',dcc.Graph(figure=fig_bc),"lg")
             
                        ],width=6,className="col-xl-6 col-md-6 col-sm-12 col-12 mb-3"),
                        ],
                        
                    ),
            ])
    return container
def orderX(x,df):
            if x == 'week':
                order={'week':sorted(df['week'].unique()),'DSCVARIABLE': sorted(df['DSCVARIABLE'].unique())}
            else: 
                order={}
            return order

def line_agricola_card(df,x,y,color,heig,x_title,y_title,title_legend,orders={},title='',):
    #tipo=df['TIPO'].unique()[0]
   
    ultimo_year=str(sorted(df['AÑO_FECHA'].unique())[-1])
    if x=='week':
        ejex='SEMANA'
    else:
        ejex='Fecha'
    #if tipo=='Riego':
    #    simbol=''
    fig=px.line(df, x=x, y=y, color=color,template='plotly_white',
                color_discrete_map=dict_recursos_agricola,
                category_orders=orders,
                title=f"{title} "+", ".join([ultimo_year]),#{titulo}+' '+{ultimo_year},
                hover_name=color,
                
                #hover_data={x:True,y:True},
                #hovertemplate ='<br><b>{ejex}</b>:%{x}'+
                #               '<br><b>Cantidad</b>: %{y}<br>'+
                #               '<br> %{color}',
                               )
    fig.update_layout(margin=dict(l=20,r=20,b=20,t=60,pad=0,autoexpand=True),#height=heig,
        xaxis_title=ejex,
        yaxis_title=y_title,
        legend_title_text=title_legend,
        
        )
    
    fig.update_traces(hovertemplate ='<br><b>Cantidad</b>: %{y:.1f} <br>')
    fig.update_xaxes(tickfont=dict(size=10))
    fig.update_yaxes(tickfont=dict(size=10))
    fig.update_layout(hovermode="x unified",hoverlabel=dict(font_size=12,font_family="sans-serif"))
    #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
    
    
        
    return fig

def index(empresa,tipo_empresa,username):
    """
    if tipo_empresa == "Agricola" or tipo_empresa == "Agroindustrial":
        agro=dataAgricolaEmpresa(empresa)
        bc=dataBcEmpresa(empresa)
        comercial=dataVentasEmpresa(empresa)

        df_general=agro[0]
        dff=df_general[df_general['AÑO_CULTIVO']==sorted(df_general['AÑO_CULTIVO'].unique())[-1]]
        df_graph=dff.groupby(['DSCVARIABLE','TIPO','week','AÑO_FECHA','SEMANA'])[['CANTIDAD']].sum().reset_index()
        df_graph=df_graph.sort_values(by=['week','AÑO_FECHA','SEMANA'],ascending=True)
        #print(df_graph)
        fig_recursos=line_agricola_card(df_graph,'week',"CANTIDAD",'DSCVARIABLE',330,'week','Kilogramos','Fertilizantes',orders=orderX('week',df_graph),title='Recursos Agricolas')

    else:
        bc=dataBcEmpresa(empresa)
        comercial=dataVentasEmpresa(empresa)
        animals=['giraffes', 'orangutans', 'monkeys']

        fig_recursos=go.Figure([go.Bar(x=animals, y=[20, 14, 23])])
    """ 

    
    app = DjangoDash('index', external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(
        [
            #container_index(tipo_empresa,fig_recursos)
            container_index(empresa,tipo_empresa,username)
            
        ]
    )

                
            