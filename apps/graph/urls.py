from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import createdash_view
from apps.graph.dash_apps import simpleexample
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',views.TestView.as_view(), name='home'),#template_name='app_name/template_name.html'),
    
    path('live',views.TestView,name='test'),
    path('test',views.Test2View.as_view(),name='test2'),    
    path('comercial-cliente',views.dashCC.as_view(),name='com-cliente'),  
    path('comercial-cliente-cultivo',views.dashCCC.as_view(),name='com-cliente-cultivo'), 
    path('comercial-producto',views.dashCP.as_view(),name='com-producto'),    
    path('comercial-producto-cultivo',views.dashCPC.as_view(),name='com-producto-cultivo'), 
    path('comercial-cultivo',views.dashCCultivo.as_view(),name='com-cultivo'), 
    path('comercial-comparativo',views.dashCComparativo.as_view(),name='com-comparativo'),


    path('<str:username>/ejecucion-campaña',views.PlanSiembraView.as_view(),name='plan_siembra'),
    path('<str:username>/costos-campaña',views.CostosCampañaView.as_view(),name='costos_campaña'),
    path('<str:username>/variables-agricolas',views.VariablesAgricolasView.as_view(),name='variables_agricolas'),
    path('<str:username>/hectareas-sembradas',views.HectareasSembradasView.as_view(),name='hectareas_sembradas'),
    path('<str:username>/costos-cultivo',views.CostosCultivoView.as_view(),name='costos_cultivo'),
    
    path('<str:username>/cargas-personal/',views.CargasdePersonalView.as_view(),name='cargas_personal'),
    #path(r'cargas-personal/(?P<pk>[\w-]+)/$',login_required(views.CargasdePersonalView),name='cargas_personal'),
    
    #path('<str:username>/estado-de-resultados',views.EstadodeResultadosView.as_view(),name='estado_resultados'),
    path('<str:username>/estado-de-situacion',views.EstadodeSituacionView.as_view(),name='estado_situacion'),
    path('<str:username>/gastos-operativos',views.GastosOperativosView.as_view(),name='gastos_operativos'),

    path('<str:username>/informe-ventas', views.InformedeVentas1View.as_view(),name='informe_ventas'),
    path('<str:username>/ventas-exportacion',views.VentasExportacionView.as_view(),name='ventas_exportacion'),
    path('<str:username>/ventas-1',views.Ventas1View.as_view(),name='ventas_1'),
    path('<str:username>/ventas-2',views.VentasTipo.as_view(),name='ventas_2'),
    path('<str:username>/ventas-core',views.VentasCore.as_view(),name='vencore'),
    path('<str:username>/ventas-tipo',views.VentasTipo.as_view(),name='ventipo'),
    path('<str:username>/ventas-comparativo',views.VentasComparativo.as_view(),name='vencomparativo'),


    path('<str:username>/ctrl-contenedores-1',views.ContenedoresExportView1.as_view(),name='ctrl_contenedores_1'),
    path('<str:username>/ctrl-contenedores-2',views.ContenedoresExportView2.as_view(),name='ctrl_contenedores_2'),


    #path('Create_Graph',createdash_view.create_graph,name='create_graph'),
    path('<str:username>/indicadores/',createdash_view.IndicadorAllView.as_view(),name='indicador_all'),
    path('<str:username>/indicadores/<int:pk>/',createdash_view.IndicadorShowView.as_view(),name='indicador'),#createdash_view.IndicadorShowView
    path('<str:username>/create-indicador/',createdash_view.FormIndicadorView.as_view(),name='create_indicador'),
    path('<str:username>/form-indicador',createdash_view.FormIndicadorView.as_view(),name='form'),

    path('<str:username>/estado-situacion',views.EstadoSituacionView.as_view(),name='estado_situacion2'),
    path('<str:username>/estado-gp',views.EstadoGananciasPerdidasView.as_view(),name='estado_gp'),
    path('<str:username>/costos-generales',views.FinanzasCostosGenerales.as_view(),name='costos_generales'),
    path('<str:username>/estado-resultados',views.FinanzasEstadoResultados.as_view(),name='estado_r'),
]
