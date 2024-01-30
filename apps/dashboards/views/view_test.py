from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from ...users.models import Empresa,Usuario,Rubro
from ..content.test_dash import dashboard_test,dashboard_resize


class test_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-stock'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        name_empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)[0]
        dashboard=dashboard_test(codigo = id_app, empresa = name_empresa)
        context = {'dashboard':dashboard, 'code':id_app}
        
        return render(request,'any.html',context)
    

class resize_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-resize'
        
        dashboard=dashboard_resize(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        
        return render(request,'any.html',context)