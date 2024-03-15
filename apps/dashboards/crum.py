from apps.users.models import Empresa,Usuario
from django.contrib.auth.models import User
from crum import get_current_user
from .models import ConfigDashboard

def get_empresa_id():
    id_user= User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]
    id_empresa = Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
    return id_empresa

def get_user_id():
    return User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]

def get_empresas():
    id_user= User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]
    id_empresa = Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
    return Empresa.objects.filter(id = id_empresa)

def get_config_dashboard():
    id_user= User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]
    id_empresa = Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
    id_config_dash = Empresa.objects.filter(id = id_empresa).values_list('config_dashboard_id',flat=True)[0]
    config_ = ConfigDashboard.objects.get(id = id_config_dash)
    id_paleta = ConfigDashboard.objects.filter(id = id_config_dash).values_list('paleta_colores_id',flat=True)[0]
    return config_,id_paleta#(id = id_config_dash)

def get_values_empresa():
    id_user= User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]
    id_empresa = Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
    empresa_obj = Empresa.objects.get(id = id_empresa)
    rubro_id = empresa_obj.rubro_empresa_id
    config_id = empresa_obj.config_dashboard_id
    return empresa_obj, rubro_id,config_id