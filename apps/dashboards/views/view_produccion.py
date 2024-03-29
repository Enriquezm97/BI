from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from ...users.models import Empresa,Usuario,Rubro
from ..content.produccion import *

class Ejecucion_campania(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-informe-ventas'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True)
        rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        dashboard=dashboard_ejecucion_campania(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        
        return render(request,'Produccion/produccion.html',context)