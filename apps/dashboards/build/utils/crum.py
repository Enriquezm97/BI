from crum import get_current_user
from apps.users.models import Empresa,Usuario,Mantenedor,Rubro
from django.contrib.auth.models import User


def get_data_connect():
    id_user= User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]
    id_empresa = Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
    empresa = Empresa.objects.get(id = id_empresa)
    
    #api_publica = Mantenedor.objects.filter(empresa_id=id_empresa).values_list('api_publica',flat=True)[0]
    #token = Mantenedor.objects.filter(empresa_id=id_empresa).values_list('token',flat=True)[0]
    return empresa.api_publica,empresa.token

