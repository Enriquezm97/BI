from apps.users.models import Empresa,Usuario,Mantenedor,Rubro
from django.contrib.auth.models import User
from crum import get_current_user

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




    