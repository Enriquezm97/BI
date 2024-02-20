from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from apps.users.models import Empresa,Usuario,Rubro,Rol
from django.contrib.auth.models import User
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
    
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        celular = request.POST.get('celular')
        correo = request.POST.get('email')
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        rol = request.POST.get('rol')
        picture =  request.FILES.get('picture')
        is_active =  request.FILES.get('is_active')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'users/form_modificar_user.html', {'error': 'El nombre de usuario ya está en uso'})
        
        user = User.objects.create_user(username=username, email=correo, password=password, is_active = True if is_active == 'on' else False)
        profile = Usuario(
                    username= username,
                    email = correo,
                    first_name = nombres,
                    last_name = apellidos,
                    phone = celular,
                    #picture = picture.read(),
                    datos_picture = base64.b64encode(picture.read()).decode('utf-8') ,
                    is_active = True if is_active == 'on' else False,
                    user = user,
                    rol = Rol.objects.get(id=int(rol)),        
        )
    return render(request, 'users/form_modificar_user.html', context={'roles':lista_rol,'usuario':reg_Usuario})










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
