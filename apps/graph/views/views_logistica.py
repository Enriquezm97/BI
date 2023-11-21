import asyncio     
from django.utils.decorators import classonlymethod  
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from apps.users.models import Empresa,Usuario,Rubro
from ...graph.test.layouts.logistica import *

class Logistica_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    view_is_async = True
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view
    async def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=(Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True))
        #rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        context = {'dashboard':await logistica_dash()}
        return render(request,'logistica/logistica_dash.html',context)

class Alm_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    view_is_async = True
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view
    async def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id

        context = {'dashboard': await alm_stock_dash()}
        return render(request,'logistica/logistica_alm.html',context)
    
  