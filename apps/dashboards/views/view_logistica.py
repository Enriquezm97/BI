from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from ...users.models import Empresa,Usuario,Rubro
from ..content.logistica import dashboard_stocks,dashboard_gestion_stock
from django.http import HttpResponse
import asyncio
from ..build.api.connector import APIConnector


class Stocks_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-stock'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        name_empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)[0]
        dashboard=dashboard_stocks(codigo = id_app, empresa = name_empresa)
        context = {'dashboard':dashboard, 'code':id_app}
        
        return render(request,'Logistica/logistica.html',context)
    
    
import asyncio
class Gestion_Stock(LoginRequiredMixin,View):
    
    
    login_url = reverse_lazy('login')
    #async def render_to_response(self, template_name, context):
        # Función para renderizar una plantilla y devolver una respuesta asíncrona
    #    template = self.get_template(template_name)
    #    html = await template.render_async(context)
    #    return HttpResponse(html)
    #async 
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True)[0]
        code_empresa=Empresa.objects.filter(pk=user_filter).values_list('ruc_empresa',flat=True)[0]
        id_app =f'{code_empresa}-gestion-stock'
        dashboard= dashboard_gestion_stock(codigo = id_app)#await 
        context = {'dashboard':dashboard, 'code':id_app}
        #await 
        return render(request,'Logistica/gestion_stock.html',context)#self.render_to_response('Logistica/gestion_stock.html',context)#,context
    
    