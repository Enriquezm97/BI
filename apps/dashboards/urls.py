from django.urls import path, include, re_path
from .views.view_comercial import *
from .views.view_finanzas import *
from .views.view_logistica import *
from .views.view_produccion import *
from .views.view_test import *

urlpatterns = [
    #comercial
    path('ventas-informe',Informe_ventas.as_view(),name='informe_ventas'),
    path('seguimiento-comercial',Seguimiento_comercial.as_view(),name='seguimiento_comercial'),
    path('ventas-clientes',Ventas_clientes.as_view(),name='ventas_clientes'),
    path('ventas-productos',Ventas_productos.as_view(),name='ventas_productos'),
    path('ventas-cultivos',Ventas_cultivos.as_view(),name='ventas_cultivos'),
    #logistica
    path('stocks',Stocks_View.as_view(),name='stocks'),
    path('gestion-stock',test_View.as_view(),name='gestion_stock'),
    #produccion
    path('ejecucion-campania',Ejecucion_campania.as_view(),name='ejecucion_campania'),
]