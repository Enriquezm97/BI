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
from apps.graph.build.containers.index import index,row_index
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from apps.graph.build.containers.Finanzas.finanzas import dashEstadoSituacion,dashEstadoGananciasPerdidas,dashCostosGenerales ,dashER,dashEstadoSituacion2

from django.core.cache import cache
from ..test.utils.crum import * 
#####new structure
from apps.graph.test.layouts.produccion import ejecucionCampania,costosCampania,resumenCampania,rtesind_sin_estado
from apps.graph.test.layouts.comercial import informeComercial,ventaSegmented,ventasClientes,ventasProductos,ventasCultivos,ventasComparativo
from apps.graph.test.layouts.finanzas import estadoResultados,estadoGP,crear_ratio_finanzas
from apps.graph.mixins import AdministradoMixin,AnalistaMixin,AsistenteMixin
from apps.graph.test.layouts.comercial import input_dict_general,input_ventas_x,input_ventas_samplast
from apps.graph.test.layouts.inicio import inicio_dash

from apps.graph.test.Connection.apis import connection_api
from apps.graph.test.utils.functions.functions_transform import *
import asyncio 
from django.http.response import HttpResponse

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

def home(request):
    #owo=request.user.id
    dashboard=HomeScraper()
    context={'dashboard':dashboard}
    return render(request, 'home.html',context)

def liveUpdate(request):
    dashboard=HomeScraper()
    context={'dashboard':dashboard}
    return render(request, 'live_update.html',context)
"""
class TestView(LoginRequiredMixin,View):
    models=Usuario
    template_name='test.html'
    login_url = reverse_lazy('login')#'/user/login/'
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #username=list(Usuario.objects.filter(user_id=id_user).values_list('username',flat=True))
        empresa=(Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True))
        #empresa_name=(Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True))
        rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)
       
        #dashboard=tailwindcss()
        print(rubro[0])
        dashboard=index(rubro=rubro[0])
        #if cache.get(dashboard):
        
        
        context = {'dashboard':dashboard}
       
        return render(request,'test.html',context)
        
"""
from asgiref.sync import sync_to_async
#print(get_rubro_empresa())

async def view_test(request):#
    id_user = get_current_user()
    print('owo')
    print(id_user)
    #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #print(get_rubro_empresa())
       #dashboard =  await index(rubro='Comercial' )#get_rubro_empresa()
    return render(request,'test.html',{'dashboard':await index('Comercial')})
    
import asyncio     
from django.utils.decorators import classonlymethod  
from django.contrib.auth import get_user_model
#result = await asyncio.gather(do_a_network_call("some_input")) 

#@method_decorator(cache_page(60 * 15), name='dispatch')
class TestView(LoginRequiredMixin,View):
    models=Usuario
    template_name='test.html'
    login_url = reverse_lazy('login')
    
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-inicio'
        
        return render(request,'test.html',{'dashboard':  inicio_dash(codigo = id_app),'code':id_app})#kwargs={'rubro': rubro_empresa}
        

class Test2View(View):
    
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)

        dashboard = rtesind_sin_estado()#resumenCampania()
        kwargs['dash_app_id']=id_user
        kwargs['codigo']=id_user
        kwargs['empresa']=empresa
        context = {'dashboard':dashboard,'id':{"target_id": {"value": id_user}} }
        #name_empresa
        return render(request,'test2.html',context)


##AGRICOLA
class PlanSiembraView(LoginRequiredMixin,AdministradoMixin,View):
    login_url = reverse_lazy('login')

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        id_app =f'{id_user}-vagricola'
        #dashboard=plandeSiembra(empresa[0])
        dashboard=ejecucionCampania(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        
        return render(request,'dashboards/Agricola/plansiembra.html',context)

class CostosCampañaView(LoginRequiredMixin,AdministradoMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        id_app =f'{id_user}-vcostos'
        dashboard=costosCampania(codigo=id_app)
        context = {'dashboard':dashboard,'code':id_app}
        return render(request,'dashboards/Agricola/costos_campaña.html',context)

class VariablesAgricolasView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        
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

class CargasdePersonalView(LoginRequiredMixin,AnalistaMixin,View):
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
        dashboard=estadoResultados()#estadodeResultadosFinanzas(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Otros/estado_resultados.html',context)

class EstadodeSituacionView(LoginRequiredMixin,AnalistaMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
       
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        dashboard=estadodeSituacionFinanzas(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Otros/estado_situacion.html',context)

class GastosOperativosView(LoginRequiredMixin,AnalistaMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
       
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        
        dashboard=gastosOperativosFinanzas(empresa[0])
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Otros/gastos_operativos.html',context)





class InformedeVentas1View(LoginRequiredMixin,AsistenteMixin,View):
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
        rubro=Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        id_app =f'{id_user}-informe-comercial'
        
        
        
        dashboard=informeComercial(codigo = id_app,rubro_empresa=rubro)#informeVentas(empresa_name[0],rubro[0],staff_filter[0])
        
        context = {'dashboard':dashboard, 'code': id_app}
        return render(request,'dashboards/Comercial/informe_ventas_1.html',context)




class VentasExportacionView(LoginRequiredMixin,AsistenteMixin,View):
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

class Ventas1View(LoginRequiredMixin,AsistenteMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=ventas1(empresa[0],staff_filter[0])
        

        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/ventas1.html',context)

class Ventas2View(LoginRequiredMixin,AsistenteMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=ventas2(empresa[0],staff_filter[0])
        
        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/ventas2.html',context)
    


class VentasCore(LoginRequiredMixin,AsistenteMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)[0]
        id_app =f'{id_user}-segmented-comercial'
        
        if empresa =='SAMPLAST':
            entrada_filt = input_ventas_samplast
        else:
            entrada_filt = input_dict_general
        dashboard=ventaSegmented(filtros=entrada_filt,codigo = id_app)
        #

        context = {'dashboard':dashboard,'code':id_app}
        return render(request,'dashboards/Comercial/comercial_segmented.html',context)

class VentasTipo(LoginRequiredMixin,AsistenteMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=tipoVenta(empresa[0],staff_filter[0])
        

        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/tipoVenta.html',context)
    
class VentasComparativo(LoginRequiredMixin,AsistenteMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        staff_filter=list(Usuario.objects.filter(user_id=id_user).values_list('is_staff',flat=True))
        dashboard=ventasComparativo(empresa[0],staff_filter[0])
        

        context = {'dashboard':dashboard}
        return render(request,'dashboards/Comercial/ventasComparativo.html',context)







class ContenedoresExportView1(LoginRequiredMixin,AdministradoMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=contenedoresExportados1('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Comercial/contenedores_exportados_1.html',context)
class ContenedoresExportView2(LoginRequiredMixin,AdministradoMixin,View):
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
    
class EstadoSituacionView(LoginRequiredMixin,AnalistaMixin,View):
    #login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=dashEstadoSituacion()#contenedoresExportados2('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Finanzas/estado_situacion.html',context)


class EstadoGananciasPerdidasView(LoginRequiredMixin,AnalistaMixin,View):
    #login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        id_app =f'{id_user}-estado_perdidas_ganancias'
        #'estado_perdidas_ganancias'
        dashboard=estadoGP(codigo=id_app)
        context = {'dashboard':dashboard, 'code': id_app}
       
        return render(request,'dashboards/Finanzas/estado_gp.html',context)
    
class FinanzasCostosGenerales(LoginRequiredMixin,AnalistaMixin,View):
    #login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=dashCostosGenerales()#contenedoresExportados2('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Finanzas/costos_generales.html',context)

class FinanzasEstadoResultados(LoginRequiredMixin,AnalistaMixin,View):
    #login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        id_app =f'{id_user}-estado_resultados_finanzas'
        #'estado_resultados_finanzas'
        dashboard=estadoResultados(codigo = id_app)#contenedoresExportados2('ARONA',True)
        context = {'dashboard':dashboard, 'code': id_app}
       
        return render(request,'dashboards/Finanzas/finanzas_estado_resultados.html',context)




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
    

#################################VISTAS
class dashC(LoginRequiredMixin,AsistenteMixin,View):
    
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
         
        #dashboard=dashComercialCliente()
        #dashboard=dashComercialClienteCultivo()
        #dashboard=dashComercialProductoCultivo()
        dashboard=dashComercialCultivo()

        kwargs['codigo']=id_user
        kwargs['empresa']=empresa
        context = {'dashboard':dashboard,'empresa':empresa[0]}
        #name_empresa
        return render(request,'dashboards/Comercial/dashcultivo.html',context)

class dashCC(LoginRequiredMixin,AsistenteMixin,View):
    
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        id_app =f'{id_user}-clientes-comercial' 
        dashboard=ventasClientes(codigo=id_app)#'clientes-comercial'
        

        kwargs['codigo']=id_user
        kwargs['empresa']=empresa
        context = {'dashboard':dashboard,'empresa':empresa[0],'code':id_app}
        #name_empresa
        return render(request,'dashboards/Comercial/comercial_cliente.html',context)

class dashCCC(LoginRequiredMixin,AsistenteMixin,View):
    
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
         
        #dashboard=dashComercialCliente()
        dashboard=dashComercialClienteCultivo()
        
        kwargs['codigo']=id_user
        kwargs['empresa']=empresa
        context = {'dashboard':dashboard,'empresa':empresa[0]}
        #name_empresa
        return render(request,'dashboards/Comercial/comercial_cliente_cultivo.html',context)

class dashCP(LoginRequiredMixin,AsistenteMixin,View):
    
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        id_app =f'{id_user}-productos-comercial' 
        #dashboard=dashComercialCliente()
        #dashboard=dashComercialClienteCultivo()
        dashboard=ventasProductos(codigo = id_app)#'productos-comercial'
        #dashboard=dashComercialProductoCultivo()
        #dashboard=dashComercialCultivo()
        
        kwargs['codigo']=id_user
        kwargs['empresa']=empresa
        context = {'dashboard':dashboard,'empresa':empresa[0],'code': id_app}
        #name_empresa
        return render(request,'dashboards/Comercial/comercial_producto.html',context)

class dashCPC(LoginRequiredMixin,AsistenteMixin,View):
    
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
         
        #dashboard=dashComercialCliente()
        #dashboard=dashComercialClienteCultivo()
        #dashboard=dashComercialProducto()
        dashboard=dashComercialProductoCultivo()

        kwargs['codigo']=id_user
        kwargs['empresa']=empresa
        context = {'dashboard':dashboard,'empresa':empresa[0]}
        #name_empresa
        return render(request,'dashboards/Comercial/comercial_producto_cultivo.html',context)

class dashCCultivo(LoginRequiredMixin,AsistenteMixin,View):
    
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        id_app =f'{id_user}-cultivos-comercial'
        #dashboard=dashComercialCliente()
        #dashboard=dashComercialClienteCultivo()
        #dashboard=dashComercialProducto()
        #dashboard=dashComercialProductoCultivo()
        dashboard=ventasCultivos(codigo = id_app)
        
        kwargs['codigo']=id_user
        kwargs['empresa']=empresa
        context = {'dashboard':dashboard,'empresa':empresa[0],'code':id_app}
        #name_empresa
        return render(request,'dashboards/Comercial/comercial_cultivo.html',context)

class dashCComparativo(LoginRequiredMixin,AsistenteMixin,View):
    
    def get(self,request,*args, **kwargs):
        #dashboard=tailwindcss()
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        id_app =f'{id_user}-comercial_comparativo'
        #dashboard=dashComercialCliente()
        #dashboard=dashComercialClienteCultivo()
        #dashboard=dashComercialProductoCultivo()
        #dashboard=dashComercialCultivo()
        dashboard=ventasComparativo(codigo = id_app)

        kwargs['codigo']=id_user
        kwargs['empresa']=empresa
        context = {'dashboard':dashboard,'empresa':empresa[0],'code':id_app}
        #name_empresa
        return render(request,'dashboards/Comercial/comercial_comparativo.html',context)
    
class EstadoSituacion2View(LoginRequiredMixin,AnalistaMixin,View):
    #login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        #user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        #empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        #dashboard=ventas2(empresa[0])
        dashboard=dashEstadoSituacion2()#contenedoresExportados2('ARONA',True)
        context = {'dashboard':dashboard}
       
        return render(request,'dashboards/Finanzas/estado_situacion2.html',context)
    
    
    



"""
import asyncio     
from django.utils.decorators import classonlymethod  
from django.contrib.auth import get_user_model
#result = await asyncio.gather(do_a_network_call("some_input")) 
class TestView(LoginRequiredMixin,View):
    models=Usuario
    template_name='test.html'
    login_url = reverse_lazy('login')
    view_is_async = True
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view
    async def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        user_filter= list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=  (Empresa.objects.filter(pk=user_filter[0]).values_list('rubro_empresa_id',flat=True))
        rubro=  Rubro.objects.filter(pk=empresa[0]).values_list('name_rubro',flat=True)[0]
        return render(request,'test.html',{'dashboard': await index(rubro = rubro)})

"""