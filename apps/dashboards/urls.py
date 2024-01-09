from django.urls import path, include, re_path
from .views.view_comercial import *
from .views.view_finanzas import *
from .views.view_logistica import *
from .views.view_produccion import *

urlpatterns = [
    path('stocks',Stocks_View.as_view(),name='stocks'),
]