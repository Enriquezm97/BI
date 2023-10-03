from crum import get_current_user
from apps.users.models import Empresa,Usuario,Mantenedor
from django.contrib.auth.models import User
from apps.graph.models import Indicador

def get_empresa():
    print(get_current_user())
    id_user= User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]
    id_empresa = Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
    empresa = Empresa.objects.filter(pk=id_empresa).values_list('name_empresa',flat=True)[0]
    return empresa


def get_nombre_user():
    print(get_current_user())
    id_user= User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]
    
    return Usuario.objects.filter(user=id_user).values_list('username',flat=True)[0]



def get_indicadores_name():
    id_user= User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]
    id_empresa = Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
    usuarios_list = list(Usuario.objects.filter(empresa_id=id_empresa).values_list('id',flat=True))
    #names_indicador_empresa = 
    return list(Indicador.objects.filter(usuario_id__in=usuarios_list).values_list('name',flat=True))

def get_data_conection():
    print(get_current_user())
    id_user= User.objects.filter(username=get_current_user()).values_list('id',flat=True)[0]
    id_empresa = Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
    api_publica = Mantenedor.objects.filter(empresa_id=id_empresa).values_list('api_publica',flat=True)[0]
    token = Mantenedor.objects.filter(empresa_id=id_empresa).values_list('token',flat=True)[0]
    return api_publica,token
