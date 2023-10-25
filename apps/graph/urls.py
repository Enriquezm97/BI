from django.urls import path, include, re_path

import apps.graph.createdash_view as createdash_view
from .views.views_logistica import *
from .views.views import *

urlpatterns = [
    path('',TestView.as_view(), name='home'),#template_name='app_name/template_name.html'),
    
    path('live',TestView,name='test'),
    path('test',Test2View.as_view(),name='test2'),    
    path('<str:username>/comercial-cliente',dashCC.as_view(),name='com-cliente'),  
    path('comercial-cliente-cultivo',dashCCC.as_view(),name='com-cliente-cultivo'), 
    path('<str:username>/comercial-producto',dashCP.as_view(),name='com-producto'),    
    path('comercial-producto-cultivo',dashCPC.as_view(),name='com-producto-cultivo'), 
    path('<str:username>/comercial-cultivo',dashCCultivo.as_view(),name='com-cultivo'), 
    path('<str:username>/comercial-comparativo',dashCComparativo.as_view(),name='com-comparativo'),


    path('<str:username>/ejecucion-campaña',PlanSiembraView.as_view(),name='plan_siembra'),
    path('<str:username>/costos-campaña',CostosCampañaView.as_view(),name='costos_campaña'),
    path('<str:username>/variables-agricolas',VariablesAgricolasView.as_view(),name='variables_agricolas'),
    path('<str:username>/hectareas-sembradas',HectareasSembradasView.as_view(),name='hectareas_sembradas'),
    path('<str:username>/costos-cultivo',CostosCultivoView.as_view(),name='costos_cultivo'),
    
    path('<str:username>/cargas-personal/',CargasdePersonalView.as_view(),name='cargas_personal'),
    #path(r'cargas-personal/(?P<pk>[\w-]+)/$',login_required(views.CargasdePersonalView),name='cargas_personal'),
    
    #path('<str:username>/estado-de-resultados',views.EstadodeResultadosView.as_view(),name='estado_resultados'),
    path('<str:username>/estado-de-situacion',EstadodeSituacionView.as_view(),name='estado_situacion'),
    path('<str:username>/gastos-operativos',GastosOperativosView.as_view(),name='gastos_operativos'),

    path('<str:username>/informe-ventas', InformedeVentas1View.as_view(),name='informe_ventas'),
    path('<str:username>/ventas-exportacion',VentasExportacionView.as_view(),name='ventas_exportacion'),
    path('<str:username>/ventas-1',Ventas1View.as_view(),name='ventas_1'),
    path('<str:username>/ventas-2',VentasTipo.as_view(),name='ventas_2'),
    path('<str:username>/ventas-core',VentasCore.as_view(),name='vencore'),
    path('<str:username>/ventas-tipo',VentasTipo.as_view(),name='ventipo'),
    path('<str:username>/ventas-comparativo',VentasComparativo.as_view(),name='vencomparativo'),


    path('<str:username>/ctrl-contenedores-1',ContenedoresExportView1.as_view(),name='ctrl_contenedores_1'),
    path('<str:username>/ctrl-contenedores-2',ContenedoresExportView2.as_view(),name='ctrl_contenedores_2'),


    #path('Create_Graph',createdash_view.create_graph,name='create_graph'),
    path('<str:username>/indicadores/',createdash_view.IndicadorAllView.as_view(),name='indicador_all'),
    path('<str:username>/indicadores/<int:pk>/',createdash_view.IndicadorShowView.as_view(),name='indicador'),#createdash_view.IndicadorShowView
    path('<str:username>/create-indicador/',createdash_view.FormIndicadorView.as_view(),name='create_indicador'),
    path('<str:username>/modificar-indicador/<int:pk>/',createdash_view.IndicadorEditarView.as_view(),name='modificar_indicador'),
    path('<str:username>/eliminar-indicador/<int:pk>/',createdash_view.IndicadorEliminarView.as_view(),name='eliminar_indicador'),
    path('<str:username>/form-indicador',createdash_view.FormIndicadorView.as_view(),name='form'),

    path('<str:username>/estado-situacion',EstadoSituacionView.as_view(),name='estado_situacion2'),
    path('<str:username>/estado-situacion2',EstadoSituacion2View.as_view(),name='estado_situacion3'),
    path('<str:username>/estado-gp',EstadoGananciasPerdidasView.as_view(),name='estado_gp'),
    path('<str:username>/costos-generales',FinanzasCostosGenerales.as_view(),name='costos_generales'),
    path('<str:username>/estado-resultados',FinanzasEstadoResultados.as_view(),name='estado_r'),
    
    #logistica
    path('<str:username>/stocks',Logistica_View.as_view(),name='logistica_'),
]
