from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView,UpdateView,DeleteView,View,TemplateView
from django.urls import reverse_lazy
from plotly.offline import plot
import plotly.graph_objects as go
from apps.graph.build.containers.Otros.Otros import *
from core.services import *
import pandas as pd
from apps.graph.build.containers.test import prueba, prueba2, tailwindcss
from apps.graph.build.containers.Agricola.Agricola import *
from apps.graph.build.containers.Comercial.comercial import *

from apps.graph.form import *
from apps.graph.build.containers.Otros.Otros import *
from apps.graph.build.containers.Created.created import *
from apps.graph.build.containers.Scraper.scraper import *

from apps.graph.models import Indicador
from apps.users.models import Empresa,Usuario
from apps.graph.build.containers.test import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    #owo=request.user.id
    dashboard=HomeScraper()
    context={'dashboard':dashboard}
    return render(request, 'home.html',context)

def liveUpdate(request):
    dashboard=live_update()
    context={'dashboard':dashboard}
    return render(request, 'live_update.html',context)

class TestView(LoginRequiredMixin,View):
    models=Usuario
    template_name='test.html'
    login_url = reverse_lazy('login')#'/user/login/'
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        dashboard=index()
        
        context = {'dashboard':dashboard}
        return render(request,'test.html',context)

class Test2View(View):
    
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        dashboard=prueba2()
        print(empresa)
        print(type(empresa))
        print(empresa[0])
        kwargs['codigo']=id_user
        kwargs['empresa']=empresa
        context = {'dashboard':dashboard,'empresa':empresa[0]}
        #name_empresa
        return render(request,'test2.html',context)


##AGRICOLA
class PlanSiembraView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        dashboard=plandeSiembra(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Agricola/plansiembra.html',context)

class CostosCampañaView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        dashboard=costosAgricola(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Agricola/costos_campaña.html',context)

class VariablesAgricolasView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        dashboard=variablesAgricolas(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Agricola/variables_agricolas.html',context)

class HectareasSembradasView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        dashboard=hectareaSembrada(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Agricola/hectareas_sembradas.html',context)

class CostosCultivoView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')

    def get(self,request,*args, **kwargs):
        
        #dashboard=hectareaSembrada('68.168.108.184')
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        dashboard=costosCultivo(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Agricola/costos_cultivo.html',context)

class CargasdePersonalView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
      
        id_user=self.request.user.id
       
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        dashboard=cargasdePersonalFinanzas(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Otros/cargas_personal.html',context)

class EstadodeResultadosView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=hectareaSembrada('68.168.108.184')
        dashboard=estadodeResultadosFinanzas(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Otros/estado_resultados.html',context)

class EstadodeSituacionView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
       
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        dashboard=estadodeSituacionFinanzas(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Otros/estado_situacion.html',context)

class GastosOperativosView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
       
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        
        dashboard=gastosOperativosFinanzas(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Otros/gastos_operativos.html',context)





class InformedeVentas1View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
       
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        
        dashboard=informeVentas(empresa[0],staff_filter[0])
        
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/informe_ventas_1.html',context)


class VentasExportacionView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=ventasExportacion(empresa[0],staff_filter[0])
        
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/ventas_exportacion.html',context)

class Ventas1View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=ventas1(empresa[0],staff_filter[0])
        

        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/ventas1.html',context)

class Ventas2View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=ventas2(empresa[0],staff_filter[0])
        
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/ventas2.html',context)

class ContenedoresExportView1(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=contenedoresExportados1('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Comercial/contenedores_exportados_1.html',context)
class ContenedoresExportView2(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=contenedoresExportados2('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Comercial/contenedores_exportados_2.html',context)
################CREAR INDICADORES




class Error404View(TemplateView):
    template_name = "paginas/error_404.html"


class Error505View(TemplateView):
    template_name = "paginas/error_500.html"

    @classmethod
    def as_error_view(cls):

        v = cls.as_view()
        def view(request):
            r = v(request)
            r.render()
            return r
        return view