from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from apps.users.models import Empresa,Usuario
from django.contrib.auth.models import User
# Create your views here.
def update_profile(request):
     return render(request,'users/update_profile.html')






def login_view(request):
    empresas=list(Empresa.objects.all())
    
    context={'empresas':empresas}
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
        
    return render (request,'users/login.html',context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')