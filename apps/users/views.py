from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from apps.users.models import Empresa,Usuario,Rubro,Rol
from apps.dashboards.models import ConfigDashboard
from django.contrib.auth.models import User
from ..dashboards.crum import get_values_empresa
from .utils import status_cliente
from crum import get_current_user
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
    usuariox =User.objects.get(username = get_current_user())
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
        
        
        user.email = correo
        user.is_active = True if is_active == 'on' else False
        user.save()

        reg_Usuario.first_name = nombres
        reg_Usuario.last_name = apellidos
        reg_Usuario.email =  correo
        reg_Usuario.phone = celular
        reg_Usuario.is_active = True if is_active == 'on' else False
        reg_Usuario.datos_picture = base64.b64encode(picture.read()).decode('utf-8')if picture != None else reg_Usuario.datos_picture
        reg_Usuario.rol = Rol.objects.get(id=int(rol))
        reg_Usuario.save()
        
        if usuariox.is_staff == True and usuariox.is_superuser == True and usuariox.is_active == True:
            return redirect('all_usuarios')
        else:
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





############################### VIEW SUPER USUARIO

def regSuperUsuario_user(request):
    usuariox =User.objects.get(username = get_current_user())
    if usuariox.is_staff == True and usuariox.is_superuser == True and usuariox.is_active == True:
        empresa = Empresa.objects.all()
        rol = Rol.objects.all()
        lista_empresas = [(fila.id, fila.name_empresa) for fila in empresa]
        lista_roles = [(fila.id, fila.name_rol) for fila in rol]
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
            
            if User.objects.filter(username=username).exists():
                return render(request, 'users/admin/form_usuarios_create.html', {'empresas':lista_empresas,'roles':lista_roles,'error': 'El nombre de usuario ya está en uso'})
            user = User.objects.create_user(username=username, email=correo, password=password)
            profile = Usuario(
                    username= username,
                    email = correo,
                    first_name = nombres,
                    last_name = apellidos,
                    phone = celular,
                    #picture = picture.read(),
                    datos_picture = base64.b64encode(picture.read()).decode('utf-8') if picture !=None else '',
                    is_active = True,
                    user = user,
                    empresa = Empresa.objects.get(id=int(empresa)),
                    rol = Rol.objects.get(id=int(rol)),        
            )
            profile.save()
            return redirect('all_usuarios')
        return render(request, 'users/admin/form_usuarios_create.html',{'empresas':lista_empresas,'roles':lista_roles})
    else:
        return render(request, 'users/admin/error.html')

    
def administrarUsuario(request):
    usuariox =User.objects.get(username = get_current_user())
    if usuariox.is_staff == True and usuariox.is_superuser == True and usuariox.is_active == True:
        usuarios = Usuario.objects.all()
        return render(request, 'users/admin/tabla_usuarios.html',{'users':usuarios})#,{'empresas':lista_empresas,'roles':lista_roles}
    else:
        return render(request, 'users/admin/error.html')
    

def regSuperUsuario_empresa(request):
    usuariox =User.objects.get(username = get_current_user())
    empresa_valid = Empresa.objects.all()
    lista_empresa_valid = [fila.name_empresa for fila in empresa_valid]
    if usuariox.is_staff == True and usuariox.is_superuser == True and usuariox.is_active == True:
        rubro = Rubro.objects.all()
        config_dashboard = ConfigDashboard.objects.all()
        lista_rubro = [(fila.id, fila.name_rubro) for fila in rubro]
        lista_config = [(fila.id, fila.name_config) for fila in config_dashboard]
        #empresa = Empresa.objects.all()
        if request.method == 'POST':
            #empresa
            get_nombre = request.POST.get('nombre')
            get_codigo = request.POST.get('codigo')
            get_celular = request.POST.get('celular')
            get_ruc = request.POST.get('ruc')
            get_rubro = request.POST.get('rubro')
            get_config = request.POST.get('config')
            get_picture = request.FILES.get('picture')
            #mantenedor
            get_ippublica=request.POST.get('ip_publica')
            get_iplocal = request.POST.get('ip_local')
            get_server = request.POST.get('server_bd')
            get_puerto = request.POST.get('puerto_bd')
            get_user = request.POST.get('user_bd')
            get_pass = request.POST.get('pass_bd')
            get_name = request.POST.get('name_bd')
            get_token = request.POST.get('token_bd')
            if get_nombre in lista_empresa_valid:
                return render(request, 'users/admin/form_empresas_create.html', {'rubros':lista_rubro,'configs':lista_config,'error': 'El nombre de empresa ya está en uso'})
            empresa = Empresa(
                name_empresa = get_nombre,
                codigo_empresa = get_codigo,
                phone_number_empresa = get_celular,
                ruc_empresa = get_ruc,
                rubro_empresa = Rubro.objects.get(id=int(get_rubro)),
                config_dashboard = ConfigDashboard.objects.get(id=int(get_config)),
                marca_empresa = base64.b64encode(get_picture.read()).decode('utf-8') if get_picture != None else '',
                #mantenedor
                api_publica = get_ippublica,
                api_local = get_iplocal,
                servidor_bd = get_server,
                puerto_bd = get_puerto,
                usuario_bd = get_user,
                password_bd = get_pass,
                name_bd = get_name,
                token = get_token
            )
            empresa.save()
            
            return redirect('all_empresas')
        return render(request, 'users/admin/form_empresas_create.html', {'rubros':lista_rubro,'configs':lista_config})
    else:
        return render(request, 'users/admin/error.html')
    

def administrarEmpresa(request):
    usuariox =User.objects.get(username = get_current_user())
    if usuariox.is_staff == True and usuariox.is_superuser == True and usuariox.is_active == True:
        empresas = Empresa.objects.all()
        lista_ip = [status_cliente(fila.api_publica) for fila in empresas]
        empresas_ = zip(empresas,lista_ip)
        return render(request, 'users/admin/tabla_empresas.html',{'empresas':empresas_})
    else:
        return render(request, 'users/admin/error.html')
    

def modSuperUsuario_empresa(request,id):
    usuariox =User.objects.get(username = get_current_user())
    update_empresa= Empresa.objects.get(id=id)
    empresa_valid = Empresa.objects.all()
    lista_empresa_valid = [fila.name_empresa for fila in empresa_valid]
    if usuariox.is_staff == True and usuariox.is_superuser == True and usuariox.is_active == True:
        rubro = Rubro.objects.all()
        config_dashboard = ConfigDashboard.objects.all()
        lista_rubro = [(fila.id, fila.name_rubro) for fila in rubro]
        lista_config = [(fila.id, fila.name_config) for fila in config_dashboard]
        #empresa = Empresa.objects.all()
        if request.method == 'POST':
            #empresa
            get_nombre = request.POST.get('nombre')
            get_codigo = request.POST.get('codigo')
            get_celular = request.POST.get('celular')
            get_ruc = request.POST.get('ruc')
            get_rubro = request.POST.get('rubro')
            get_config = request.POST.get('config')
            get_picture = request.FILES.get('picture')
            #mantenedor
            get_ippublica=request.POST.get('ip_publica')
            get_iplocal = request.POST.get('ip_local')
            get_server = request.POST.get('server_bd')
            get_puerto = request.POST.get('puerto_bd')
            get_user = request.POST.get('user_bd')
            get_pass = request.POST.get('pass_bd')
            get_name = request.POST.get('name_bd')
            get_token = request.POST.get('token_bd')
            
            #if get_nombre in lista_empresa_valid:
            #    return render(request, 'users/admin/form_empresas_update.html', {'rubros':lista_rubro,'configs':lista_config,'empresa_id':id,'empresa':update_empresa,'error': 'El nombre de empresa ya está en uso'})
            
            update_empresa.name_empresa = get_nombre
            #update_empresa.codigo_empresa = get_codigo
            update_empresa.phone_number_empresa = get_celular
            #update_empresa.ruc_empresa = get_ruc
            update_empresa.rubro_empresa = Rubro.objects.get(id=int(get_rubro))
            update_empresa.config_dashboard = ConfigDashboard.objects.get(id=int(get_config))
            update_empresa.marca_empresa = base64.b64encode(get_picture.read()).decode('utf-8') if get_picture != None else update_empresa.marca_empresa
            #mantenedor
            update_empresa.api_publica = get_ippublica
            update_empresa.api_local = get_iplocal
            update_empresa.servidor_bd = get_server
            update_empresa.puerto_bd = get_puerto
            update_empresa.usuario_bd = get_user
            update_empresa.password_bd = get_pass
            update_empresa.name_bd = get_name
            update_empresa.token = get_token
            update_empresa.save()
            
            return redirect('all_empresas')
        return render(request, 'users/admin/form_empresas_update.html', {'rubros':lista_rubro,'configs':lista_config,'empresa_id':id,'empresa':update_empresa})
    else:
        return render(request, 'users/admin/error.html')