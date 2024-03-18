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
    
    path('modificar-empresa',views.modificar_empresa_view, name = 'modificar_empresa'),
    
    path('crear-profile/',views.registo_profile_view, name='crear_profile'),
    path('lista-usuarios/',views.listar_usuario, name='lista_usuarios'),
    path('form-test/',views.form_test_view, name='form_test'),
    
    path('login2',views.login_2, name='login2'),
     
     ##admin
    path('new-user',views.regSuperUsuario_user, name='new_user'),
    path('all-users',views.administrarUsuario, name='all_usuarios'),
    path('new-empresa',views.regSuperUsuario_empresa, name='new_empresa'),
    path('all-empresa',views.administrarEmpresa, name='all_empresas'),
    path('update-empresa/<int:id>/',views.modSuperUsuario_empresa, name='update_empresa_admin'),
     
]   

  




