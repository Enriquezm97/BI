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
    path('', views.TestView.as_view(), name='home'),
    
    path('live',views.TestView,name='test'),
    path('test/<int:codigo>/<slug:empresa>',views.Test2View.as_view(),name='test2'),
    
    path('plan-siembra',login_required(views.PlanSiembraView.as_view()),name='plan_siembra'),
    path('costos-campaña',login_required(views.CostosCampañaView.as_view()),name='costos_campaña'),
    path('variables-agricolas',login_required(views.VariablesAgricolasView.as_view()),name='variables_agricolas'),
    path('hectareas-sembradas',login_required(views.HectareasSembradasView.as_view()),name='hectareas_sembradas'),
    path('costos-cultivo',login_required(views.CostosCultivoView.as_view()),name='costos_cultivo'),
    
    path('cargas-personal/',login_required(views.CargasdePersonalView.as_view()),name='cargas_personal'),
    #path(r'cargas-personal/(?P<pk>[\w-]+)/$',login_required(views.CargasdePersonalView),name='cargas_personal'),
    
    path('estado-de-resultados',login_required(views.EstadodeResultadosView.as_view()),name='estado_resultados'),
    path('estado-de-situacion',login_required(views.EstadodeSituacionView.as_view()),name='estado_situacion'),
    path('gastos-operativos',login_required(views.GastosOperativosView.as_view()),name='gastos_operativos'),

    path('informe-ventas', login_required(views.InformedeVentas1View.as_view()),name='informe_ventas'),
    path('ventas-exportacion',login_required(views.VentasExportacionView.as_view()),name='ventas_exportacion'),
    path('ventas-1',login_required(views.Ventas1View.as_view()),name='ventas_1'),
    path('ventas-2',login_required(views.Ventas2View.as_view()),name='ventas_2'),

    path('ctrl-contenedores-1',login_required(views.ContenedoresExportView1.as_view()),name='ctrl_contenedores_1'),
    path('ctrl-contenedores-2',login_required(views.ContenedoresExportView2.as_view()),name='ctrl_contenedores_2'),


    #path('Create_Graph',createdash_view.create_graph,name='create_graph'),
    path('indicadores/',createdash_view.IndicadorAllView.as_view(),name='indicador_all'),
    re_path(r'^indicadores/(?P<pk>[\w-]+)/$',createdash_view.IndicadorShowView.as_view(),name='indicador'),#createdash_view.IndicadorShowView
    path('create-indicador/',createdash_view.FormIndicadorView.as_view(),name='create_indicador'),
    path('form-indicador',createdash_view.FormIndicadorView.as_view(),name='form')
]
