from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from apps.graph.dash_apps import simpleexample


urlpatterns = [
    path('login',views.login_view, name='login'),
    path('logout',views.logout_view, name='logout'),
    path('profile/',views.update_profile, name='update_profile'),
    
    path('crear-user/',views.registo_user_view, name='crear_user'),
    path('modificar-user/<int:id>/',views.modificar_user_view, name='modificar_user'),
    
    path('crear-profile/',views.registo_profile_view, name='crear_profile'),
    path('lista-usuarios/',views.listar_usuario, name='lista_usuarios'),
    path('form-test/',views.form_test_view, name='form_test'),
]

  




