from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from apps.users.models import Empresa,Usuario,Rubro,Rol
from django.contrib.auth.models import User
from .crum import *
from .form import RegistroUser,RegistroProfile
# Create your views here.
def update_profile(request):
     return render(request,'users/update_profile.html')

def login_view(request):
    #empresas=list(Empresa.objects.all())
    
    #context={'empresas':empresas}
    if request.method == 'POST':
        
        #print('*' * 10)
        #username = request.POST['username']
        #password = request.POST['password']
        username = request.POST.get('username')
        password = request.POST.get('password')
        #empresa=request.POST.get('empresa')
        #user_filter=list(Usuario.objects.filter(username=username).values_list('empresa_id',flat=True))
        #enterprise=list(Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True))
        #print(enterprise)
        #print(empresa)
        #if empresa in enterprise:

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
    if request.method == 'POST':
        form = RegistroUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Puedes redirigir a donde desees después de registrar un nuevo usuario
    else:
        form = RegistroUser()

    return render(request, 'users/form_create_user.html', {'form': form})


def registo_profile_view(request):
    print(User.objects.filter(id=get_user_id()))
    empresa_ = get_empresas()
    rol_ = Rol.objects.all()
    lista_rol = [(fila.id, fila.name_rol) for fila in rol_]
    lista_empresa = [(fila.id, fila.name_empresa) for fila in empresa_]
    #if request.method == 'POST':
        #form = RegistroProfile(request.POST)
        #if form.is_valid():
        #    form.save()
        #    return redirect('login')  # Puedes redirigir a donde desees después de registrar un nuevo usuario
    #else:
        #form = RegistroProfile()

    return render(request, 'users/form_create_profile.html',context={'roles':lista_rol,'empresas':lista_empresa})#, {'form': form}

def form_test_view(request):
    return render(request, 'users/test_form.html')
