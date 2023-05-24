import plotly.graph_objects as go
import plotly.express as px



def treemapEstadoSituacion(dataframe,list_path=['grupo1', 'grupo2', 'grupo3'],moneda='saldo_cargo_mof',titulo=''):
    if moneda == 'saldo_cargo_mof':
        #value_moneda='saldo_cargo_mof'
        hover='<b>%{label} </b> <br> Saldo(S/): %{value}<br>'
    elif moneda == 'saldo_cargo_mex':
        #value_moneda='saldo_cargo_mof'
        hover='<b>%{label} </b> <br> Saldo($): %{value}<br>'
    fig = px.treemap(dataframe, path=list_path, values=moneda,template='none',color_continuous_scale='RdBu')
    fig.update_traces(root_color="white")
    fig.update_layout( title=titulo,margin=dict(l=5, r=5, t=25, b=5))#,height=800
    fig.update_traces(hovertemplate =hover)
    return fig