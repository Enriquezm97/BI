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

from apps.graph.models import Indicador,TipoIndicador
from apps.users.models import Empresa,Usuario,Rubro
#from apps.graph.build.containers.test import *
from apps.graph.build.containers.index import index
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from apps.graph.build.containers.Finanzas.finanzas import dashEstadoSituacion,dashEstadoGananciasPerdidas,dashCostosGenerales ,dashER

from django.core.cache import cache

def home(request):
    #owo=request.user.id
    dashboard=HomeScraper()
    context={'dashboard':dashboard}
    return render(request, 'home.html',context)

def liveUpdate(request):
    dashboard=HomeScraper()
    context={'dashboard':dashboard}
    return render(request, 'live_update.html',context)

class TestView(LoginRequiredMixin,View):
    models=Usuario
    template_name='test.html'
    login_url = reverse_lazy('login')#'/user/login/'
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        username=list(Usuario.objects.filter(user_id=id_user).values_list('username',flat=True))
        empresa=(Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True))
        empresa_name=(Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True))
        rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)
        
        #dashboard=tailwindcss()
        
        dashboard=index(empresa_name[0],rubro[0],username[0])
        #if cache.get(dashboard):

        
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
        #dashboard=costosAgricola(empresa[0])
        dashboard=dashCostosProduccionAgricola()
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Agricola/costos_campaña.html',context)

class VariablesAgricolasView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=variablesAgricolas(empresa[0])
        dashboard=comparativoRecursos(empresa[0])
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
    #model=Usuario
    #def get_object(self):
    #    return get_object_or_404(Usuario, username=self.kwargs['username'])
    #def get_success_url(self):
    #    return reverse_lazy('informe_ventas', kwargs={"pk": self.request.user.id})

    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
       
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=(Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True))
        empresa_name=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        
        rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        
        dashboard=informeVentas(empresa_name[0],rubro[0],staff_filter[0])
        
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/informe_ventas_1.html',context)


class VentasExportacionView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=(Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True))
        empresa_name=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        
        rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=ventasExportacion(empresa_name[0],rubro[0],staff_filter[0])
        
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
    


class VentasCore(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=dashVentasCore()#ventasProductos(empresa[0],staff_filter[0])
        

        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/ventasProductos.html',context)

class VentasTipo(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=tipoVenta(empresa[0],staff_filter[0])
        

        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/tipoVenta.html',context)
    
class VentasComparativo(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=ventasComparativo(empresa[0],staff_filter[0])
        

        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/ventasComparativo.html',context)







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
    
class EstadoSituacionView(LoginRequiredMixin,View):
    #login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=dashEstadoSituacion()#contenedoresExportados2('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Finanzas/estado_situacion.html',context)


class EstadoGananciasPerdidasView(LoginRequiredMixin,View):
    #login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=dashEstadoGananciasPerdidas()#contenedoresExportados2('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Finanzas/estado_gp.html',context)
    
class FinanzasCostosGenerales(LoginRequiredMixin,View):
    #login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=dashCostosGenerales()#contenedoresExportados2('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Finanzas/costos_generales.html',context)

class FinanzasEstadoResultados(LoginRequiredMixin,View):
    #login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=dashER()#contenedoresExportados2('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Finanzas/estado_resultados.html',context)




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