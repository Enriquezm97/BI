from crum import get_current_user
from apps.users.models import Empresa,Usuario
from django.contrib.auth.models import User

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
#Producto.objects.filter(disponible=True) 