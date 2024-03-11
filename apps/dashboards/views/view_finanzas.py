from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from ...users.models import Empresa,Usuario,Rubro
from ..content.finanzas import dashboard_bg,dashboard_balance_ap,dashboard_analisis_activo,dashboard_analisis_pasivo

class Balance_General(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
        code_empresa=Empresa.objects.filter(pk=user_filter).values_list('ruc_empresa',flat=True)[0]
        id_app =f'{code_empresa}-balance-general'
        dashboard=dashboard_bg(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        return render(request,'Finanzas/finanzas.html',context)
    
class Balance_AP(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
        code_empresa=Empresa.objects.filter(pk=user_filter).values_list('ruc_empresa',flat=True)[0]
        id_app =f'{code_empresa}-balance-ap'
        dashboard=dashboard_balance_ap(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        return render(request,'Finanzas/finanzas.html',context)
    

class Analisis_Activo(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
        code_empresa=Empresa.objects.filter(pk=user_filter).values_list('ruc_empresa',flat=True)[0]
        id_app =f'{code_empresa}-analisis-activo'
        dashboard=dashboard_analisis_activo(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        return render(request,'Finanzas/finanzas.html',context)
    
#Analisis_Pasivo
class Analisis_Pasivo(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
        code_empresa=Empresa.objects.filter(pk=user_filter).values_list('ruc_empresa',flat=True)[0]
        id_app =f'{code_empresa}-analisis-pasivo'
        dashboard=dashboard_analisis_pasivo(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        return render(request,'Finanzas/finanzas.html',context)