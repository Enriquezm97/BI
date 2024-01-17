import asyncio     
from django.utils.decorators import classonlymethod  
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from apps.users.models import Empresa,Usuario,Rubro
from ...graph.test.layouts.logistica import *

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


@method_decorator(cache_page(60 * 15), name='dispatch')
class Logistica_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        id_app =f'{id_user}-alm_stock'

        context = {'dashboard': logistica_dash(codido = id_app),'code':id_app}
        return render(request,'logistica/logistica_dash.html',context)

#@method_decorator(cache_page(60 * 15), name='dispatch')
class Alm_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        #'initial_arguments':{"dash_app_id": {"value": id_user}}
        #name_app = f'id_user-{alm_stock}'
        id_app =f'{id_user}-alm_stock'
        context = {'dashboard':  alm_stock_dash(codido= id_app), 'code': id_app}
        return render(request,'logistica/logistica_alm.html',context)
    
    
  