from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from ...users.models import Empresa,Usuario,Rubro
from ..content.comercial import *

class Informe_ventas(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-informe-ventas'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True)
        rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        dashboard=dashboard_inf_ventas(codigo = id_app, empresa_rubro = rubro)
        context = {'dashboard':dashboard, 'code':id_app}
        
        return render(request,'Comercial/comercial.html',context)

class Seguimiento_comercial(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-seguimiento-comercial'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True)
        rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        dashboard = dashboard_seguimiento_comercial(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        
        return render(request,'Comercial/comercial.html',context)

class Ventas_clientes(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-ventas-clientes'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True)
        #rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        dashboard = dashboard_ventas_clientes(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        return render(request,'Comercial/comercial.html',context)

class Ventas_productos(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-ventas-productos'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True)
        #rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        dashboard = dashboard_ventas_productos(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        return render(request,'Comercial/comercial.html',context)

class Ventas_cultivos(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-ventas-cultivos'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True)
        #rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        dashboard = dashboard_ventas_cultivos(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        return render(request,'Comercial/comercial.html',context)
    
    
class Ventas_Agro_exp(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-ventas-exportacion'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True)
        #rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        dashboard = dashboard_ventas_agricola(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        return render(request,'Comercial/comercial.html',context)