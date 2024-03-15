from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from apps.users.models import Empresa,Usuario,Rubro,Rol
from apps.dashboards.models import ConfigDashboard
from django.contrib.auth.models import User
from ..dashboards.crum import get_values_empresa
from .crum import *
import base64
#from .form import RegistroUser,RegistroProfile
# Create your views here.
def update_profile(request):
     return render(request,'users/update_profile.html')

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user:
                login(request, user)
                return redirect('home')#('/cuentas_por_pagar/')
        else:
                return render(request,'users/login.html',{'error':'Invalid username and password'})
        
    return render (request,'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def registo_user_view(request):
    empresa_ = get_empresas()
    rol_ = Rol.objects.all()
    lista_rol = [(fila.id, fila.name_rol) for fila in rol_]
    lista_empresa = [(fila.id, fila.name_empresa) for fila in empresa_]
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        celular = request.POST.get('celular')
        correo = request.POST.get('email')
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        empresa = request.POST.get('empresa')
        rol = request.POST.get('rol')
        picture =  request.FILES.get('picture')
        #picture = request.POST.get('picture')
        print(nombres,apellidos,celular,correo,username,password,empresa,rol,picture)
        # Crear el usuario
        if User.objects.filter(username=username).exists():
            return render(request, 'users/form_create_user.html', {'error': 'El nombre de usuario ya está en uso'})
        user = User.objects.create_user(username=username, email=correo, password=password)
        profile = Usuario(
                    username= username,
                    email = correo,
                    first_name = nombres,
                    last_name = apellidos,
                    phone = celular,
                    #picture = picture.read(),
                    datos_picture = base64.b64encode(picture.read()).decode('utf-8') ,
                    is_active = True,
                    user = user,
                    empresa = Empresa.objects.get(id=int(empresa)),
                    rol = Rol.objects.get(id=int(rol)),        
        )
        profile.save()
        return redirect('lista_usuarios')
    context = {'empresas':lista_empresa,'roles':lista_rol}
    return render(request, 'users/form_create_user.html', context)

def modificar_user_view(request,id):
    rol_ = Rol.objects.all()
    lista_rol = [(fila.id, fila.name_rol) for fila in rol_]
    
    reg_Usuario= Usuario.objects.get(id=id)
    
    user = User.objects.get(pk=reg_Usuario.user_id)
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        celular = request.POST.get('celular')
        correo = request.POST.get('email')
        rol = request.POST.get('rol')
        picture =  request.FILES.get('picture')
        is_active =  request.POST.get('is_active')
        print(is_active)
        
        user.email = correo
        user.is_active = True if is_active == 'on' else False
        user.save()

        reg_Usuario.first_name = nombres
        reg_Usuario.last_name = apellidos
        reg_Usuario.email =  correo
        reg_Usuario.phone = celular
        reg_Usuario.is_active = True if is_active == 'on' else False
        reg_Usuario.datos_picture = base64.b64encode(picture.read()).decode('utf-8')
        reg_Usuario.rol = Rol.objects.get(id=int(rol))
        reg_Usuario.save()
        return redirect('lista_usuarios')
    return render(request, 'users/form_modificar_user.html', context={'roles':lista_rol,'usuario':reg_Usuario,'user_id':id})










def registo_profile_view(request):
    
    empresa_ = get_empresas()
    rol_ = Rol.objects.all()
    lista_rol = [(fila.id, fila.name_rol) for fila in rol_]
    lista_empresa = [(fila.id, fila.name_empresa) for fila in empresa_]


    return render(request, 'users/form_create_profile.html',context={'roles':lista_rol,'empresas':lista_empresa})#, {'form': form}

def form_test_view(request):
    return render(request, 'users/test_form.html')


def listar_usuario(request):
    #usuarios = Empresa.objects.filter(id=get_empresa_id())[0]#.values_list('user_id',flat=True)#[0]
    usuarios = Usuario.objects.filter(empresa_id = get_empresa_id())
    return render(request, 'users/lista_usuarios.html',context={'users': usuarios})




def login_2(request):
    
    #if request.method == 'POST':

    #    username = request.POST.get('username')
    #    password = request.POST.get('password')

    #    user = authenticate(request,username=username,password=password)
    #    if user:
    #            login(request, user)
    #            return redirect('home')#('/cuentas_por_pagar/')
    #    else:
    #            return render(request,'users/login.html',{'error':'Invalid username and password'})
    if request.method == 'POST':
        usuario_nombre = request.POST.get('username')
        print(usuario_nombre)
        #usuario = User.objects.get(username=usuario_nombre)
        empresa_name = Usuario.objects.filter(username=usuario_nombre).values_list('empresa_id',flat=True)[0]
        #Empresa.objects.filter(id = id_empresa)
        empresas = Empresa.objects.filter(id=empresa_name)
        print(empresas)
        return render(request, 'users/login2.html', {'empresas': empresas})
    else:
        return render(request, 'users/login2.html', {'empresas': []})    
    #return render (request,'users/login2.html')
    
    
def modificar_empresa_view(request):
    rubro = Rubro.objects.all()
    config_dashboard = ConfigDashboard.objects.all()
    lista_rubro = [(fila.id, fila.name_rubro) for fila in rubro]
    lista_config = [(fila.id, fila.name_config) for fila in config_dashboard]
    print(get_values_empresa())
    empresa,id_rubro,id_config =get_values_empresa()
    if request.method == 'POST':
        get_nombre = request.POST.get('nombre')
        get_codigo = request.POST.get('codigo')
        get_celular = request.POST.get('celular')
        get_ruc = request.POST.get('ruc')
        get_rubro = request.POST.get('rubro')
        get_config = request.POST.get('config')
        get_picture = request.FILES.get('picture')
        
        empresa.name_empresa = get_nombre
        empresa.codigo_empresa = get_codigo
        empresa.phone_number_empresa = get_celular
        empresa.ruc_empresa = get_ruc
        empresa.rubro_empresa = Rubro.objects.get(id=int(get_rubro))
        empresa.config_dashboard = ConfigDashboard.objects.get(id=int(get_config))
        empresa.marca_empresa = base64.b64encode(get_picture.read()).decode('utf-8') if get_picture != None else empresa.marca_empresa
        empresa.save()
        return redirect('home')
    return render(request, 'users/form_modificar_empresa.html', {'empresa': empresa,'rubros':lista_rubro,'configs':lista_config}) 