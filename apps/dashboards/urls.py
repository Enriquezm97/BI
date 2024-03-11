from django.urls import path, include, re_path
from .views.view_comercial import *
from .views.view_finanzas import *
from .views.view_logistica import *
from .views.view_produccion import *
from .views.view_test import *
from .views.view_formularios import *

urlpatterns = [
    #comercial
    path('ventas-informe',Informe_ventas.as_view(),name='informe_ventas'),
    path('seguimiento-comercial',Seguimiento_comercial.as_view(),name='seguimiento_comercial'),
    path('ventas-clientes',Ventas_clientes.as_view(),name='ventas_clientes'),
    path('ventas-productos',Ventas_productos.as_view(),name='ventas_productos'),
    path('ventas-cultivos',Ventas_cultivos.as_view(),name='ventas_cultivos'),
    path('ventas',Ventas_Agro_exp.as_view(),name='ventas_'),
    #logistica
    path('stocks',Stocks_View.as_view(),name='stocks'),
    path('gestion-stock-test',test_View.as_view(),name='gestion_stock_test'),
    path('gestion-stock',Gestion_Stock.as_view(),name='gestion_stock'),
    #produccion
    path('ejecucion-campania',Ejecucion_campania.as_view(),name='ejecucion_campania'),
    #testing 
    path('resize',resize_View.as_view(),name='resize'),
    
    path('modficar-config-dashboard',update_config_dashboards,name='update_config_dashboard'),
    
    #finanzas
    path('balance-general',Balance_General.as_view(),name='balence_general'),
    path('balance-ap',Balance_AP.as_view(),name='balence_ap'),
    path('analisis-activo',Analisis_Activo.as_view(), name = 'analisis_activo'),
    path('analisis-pasivo',Analisis_Pasivo.as_view(), name = 'analisis_pasivo')
]