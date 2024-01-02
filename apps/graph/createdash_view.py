from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView,UpdateView,DeleteView,View,TemplateView,DetailView
from django.urls import reverse_lazy
from plotly.offline import plot
import plotly.graph_objects as go
from apps.graph.form import *
from apps.graph.build.containers.Otros.Otros import *
from apps.graph.build.containers.Created.created import *
from apps.graph.build.containers.Formularios.form_crear_indicador import *
from django.contrib.auth.models import User
from apps.users.models import Empresa,Usuario
from apps.graph.models import Indicador
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.graph.mixins import AdministradoMixin,AnalistaMixin
from apps.graph.test.layouts.finanzas import crear_ratio_finanzas,editar_ratio_finanzas,eliminar_ratio_finanzas

class FormIndicadorView(LoginRequiredMixin,AnalistaMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        id_app =f'{id_user}-create_ratio'#'create_ratio'
        dashboard=crear_ratio_finanzas(codigo = id_app,empresa = empresa[0],usuario = id_user)
        context = {'dashboard':dashboard,'code':id_app}
        return render(request,'dash_created/Indicadores/form_indicador.html',context)

#@login_required
#def IndicadorAllView(request):
    #current_user= requets.user
#    indicadores=Indicador.objects.all()
#    context={'indicadores':indicadores}
    
#    return render(request,'dash_created/Indicadores/mostrar_all.html',context)
class IndicadorAllView(LoginRequiredMixin,AnalistaMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    
    def get(self,request,*args, **kwargs):
        
        user_filter=list(Usuario.objects.filter(user_id=self.request.user.id).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        indicadores=Indicador.objects.filter(dataframe=empresa[0])
        
        context={'indicadores':indicadores}
        return render(request,'dash_created/Indicadores/mostrar_all.html',context)

class IndicadorShowView(LoginRequiredMixin,AnalistaMixin,DetailView):

    models=Indicador
    template_name= 'dash_created/Indicadores/mostrar_indicador.html'
    pk_url_kwarg='pk'
    login_url = reverse_lazy('login')#'/user/login/'
    #if pk == None:
    #    template_name= 'dash_created/Indicadores/mostrar_indicador.html'
    #elif pk !=None:
    #    template_name= 'dash_created/Indicadores/mostrar_all.html'
    def get(self,request, *args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        pk=kwargs['pk']
        print(pk)
        print(empresa[0])
        name=list(Indicador.objects.filter(id=pk).values_list('name',flat=True))
        formula=list(Indicador.objects.filter(id=pk).values_list('formula',flat=True))
        rango_desde_1=list(Indicador.objects.filter(id=pk).values_list('rango_desde_1',flat=True))
        rango_hasta_1=list(Indicador.objects.filter(id=pk).values_list('rango_hasta_1',flat=True))
        rango_color_1=list(Indicador.objects.filter(id=pk).values_list('rango_color_1',flat=True))
        rango_desde_2=list(Indicador.objects.filter(id=pk).values_list('rango_desde_2',flat=True))
        rango_hasta_2=list(Indicador.objects.filter(id=pk).values_list('rango_hasta_2',flat=True))
        rango_color_2=list(Indicador.objects.filter(id=pk).values_list('rango_color_2',flat=True))
        rango_desde_3=list(Indicador.objects.filter(id=pk).values_list('rango_desde_3',flat=True))
        rango_hasta_3=list(Indicador.objects.filter(id=pk).values_list('rango_hasta_3',flat=True))
        rango_color_3=list(Indicador.objects.filter(id=pk).values_list('rango_color_3',flat=True))
        comentario=list(Indicador.objects.filter(id=pk).values_list('indicador_comentario',flat=True))
       
        parametros=name+formula+rango_desde_1+rango_hasta_1+rango_color_1+rango_desde_2+rango_hasta_2+rango_color_2+rango_desde_3+rango_hasta_3+rango_color_3+comentario
        #graph=Draw_Ind(parametros[1],parametros[0],parametros[2],parametros[3],parametros[4],parametros[5]) 
        dashboard=IndicadorDash(parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5],parametros[6],parametros[7],parametros[8],parametros[9],parametros[10],parametros[11],empresa[0])
        
        context={'name':parametros[0],'dashboard':dashboard}#,''graph':graph,
        return render(request,'dash_created/Indicadores/mostrar_indicador.html',context)
    

class IndicadorEditarView(LoginRequiredMixin,AnalistaMixin,DetailView):

    models=Indicador
    template_name= 'dash_created/Indicadores/editar_indicador.html'
    pk_url_kwarg='pk'
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request, *args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        pk=kwargs['pk']
        tipo=list(Indicador.objects.filter(id=pk).values_list('indicador_tipo',flat=True))
        name=list(Indicador.objects.filter(id=pk).values_list('name',flat=True))
        formula=list(Indicador.objects.filter(id=pk).values_list('formula',flat=True))
        rango_desde_1=list(Indicador.objects.filter(id=pk).values_list('rango_desde_1',flat=True))
        rango_hasta_1=list(Indicador.objects.filter(id=pk).values_list('rango_hasta_1',flat=True))
        rango_color_1=list(Indicador.objects.filter(id=pk).values_list('rango_color_1',flat=True))
        rango_desde_2=list(Indicador.objects.filter(id=pk).values_list('rango_desde_2',flat=True))
        rango_hasta_2=list(Indicador.objects.filter(id=pk).values_list('rango_hasta_2',flat=True))
        rango_color_2=list(Indicador.objects.filter(id=pk).values_list('rango_color_2',flat=True))
        rango_desde_3=list(Indicador.objects.filter(id=pk).values_list('rango_desde_3',flat=True))
        rango_hasta_3=list(Indicador.objects.filter(id=pk).values_list('rango_hasta_3',flat=True))
        rango_color_3=list(Indicador.objects.filter(id=pk).values_list('rango_color_3',flat=True))
        comentario=list(Indicador.objects.filter(id=pk).values_list('indicador_comentario',flat=True))
       
        parametros=tipo + name+formula+rango_desde_1+rango_hasta_1+rango_color_1+rango_desde_2+rango_hasta_2+rango_color_2+rango_desde_3+rango_hasta_3+rango_color_3+comentario
        #graph=Draw_Ind(parametros[1],parametros[0],parametros[2],parametros[3],parametros[4],parametros[5]) 
        dashboard=editar_ratio_finanzas(parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5],parametros[6],parametros[7],parametros[8],parametros[9],parametros[10],parametros[11],parametros[12],pk)
        
        context={'dashboard':dashboard}#,''graph':graph,
        return render(request,'dash_created/Indicadores/editar_indicador.html',context) 
    
class IndicadorEliminarView(LoginRequiredMixin,AnalistaMixin,DetailView):

    models=Indicador
    template_name= 'dash_created/Indicadores/eliminar_indicador.html'
    pk_url_kwarg='pk'
    login_url = reverse_lazy('login')#'/user/login/'

    def get(self,request, *args, **kwargs):
        id_user=self.request.user.id
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)
        pk=kwargs['pk']
        tipo=list(Indicador.objects.filter(id=pk).values_list('indicador_tipo',flat=True))[0]
        name=list(Indicador.objects.filter(id=pk).values_list('name',flat=True))[0]
        formula=list(Indicador.objects.filter(id=pk).values_list('formula',flat=True))[0]
    
        dashboard=eliminar_ratio_finanzas(tipo,name,formula,pk)
        
        context={'dashboard':dashboard}#,''graph':graph,
        return render(request,'dash_created/Indicadores/eliminar_indicador.html',context) 
    
    
    

@login_required
def IndicadorShowView2(request,pk):
    #current_user = request.user.id
    #Usuario.objects.filter(user_id=).values_list('empresa_id',flat=True)
    if pk==None:
        template='dash_created/Indicadores/mostrar_all.html'
    else:
        template= 'dash_created/Indicadores/mostrar_indicador.html'
        name=list(Indicador.objects.filter(id=pk).values_list('name',flat=True))
        formula=list(Indicador.objects.filter(id=pk).values_list('formula',flat=True))
        rango_desde_1=list(Indicador.objects.filter(id=pk).values_list('rango_desde_1',flat=True))
        rango_hasta_1=list(Indicador.objects.filter(id=pk).values_list('rango_hasta_1',flat=True))
        rango_color_1=list(Indicador.objects.filter(id=pk).values_list('rango_color_1',flat=True))
        rango_desde_2=list(Indicador.objects.filter(id=pk).values_list('rango_desde_2',flat=True))
        rango_hasta_2=list(Indicador.objects.filter(id=pk).values_list('rango_hasta_2',flat=True))
        rango_color_2=list(Indicador.objects.filter(id=pk).values_list('rango_color_2',flat=True))
        rango_desde_3=list(Indicador.objects.filter(id=pk).values_list('rango_desde_3',flat=True))
        rango_hasta_3=list(Indicador.objects.filter(id=pk).values_list('rango_hasta_3',flat=True))
        rango_color_3=list(Indicador.objects.filter(id=pk).values_list('rango_color_3',flat=True))
        comentario=list(Indicador.objects.filter(id=pk).values_list('indicador_comentario',flat=True))
        parametros=name+formula+rango_desde_1+rango_hasta_1+rango_color_1+rango_desde_2+rango_hasta_2+rango_color_2+rango_desde_3+rango_hasta_3+rango_color_3+comentario
        #graph=Draw_Ind(parametros[1],parametros[0],parametros[2],parametros[3],parametros[4],parametros[5]) 
        dashboard=IndicadorDash(parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5],parametros[6],parametros[7],parametros[8],parametros[9],parametros[10],parametros[11],'Nisira')
    
    context={'name':parametros[0],'dashboard':dashboard}#,''graph':graph,
    return render(request,template,context)

class IndicadorCreateView(CreateView):
   model = Indicador
   form_class = IndicadorForm
   template_name = 'dash_created/Indicadores/form.html'
   success_url = reverse_lazy('indicador_all')
  

   
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['title'] = 'Crear Indicador'
       #context['graph']=show_graph_indicador()
       context['OptionsPartidas']=lista_partidas
       #form = IndicadorForm(self.request.POST)#self.request.POST
       #if form.is_valid():
       # indi = form.save(commit=False)
       # indi.usuario_id = self.request.user.id
       # indi.save()
       #indicator = Indicador(usuario_id=self.request.user)  
       #form = IndicadorForm(self.request.POST, instance=indicator)
       #if form.is_valid():
       #     indicator.save()
       return context
    
def IndicadorRentabilidadAllView(request):
    indicadores=Indicador.objects.filter(indicador_tipo='Rentabilidad')
    context={'indicadores':indicadores}
    return render(request,'core/Finanzas/Indicadores/Rentabilidad/lista_rentabilidad.html',context)

def IndicadorRentabilidadShowView(request,pk):
    if pk==None:
        template='core/Finanzas/Indicadores/Rentabilidad/lista_rentabilidad.html'
    else:
        
        name=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('name',flat=True))
        formula=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('formula',flat=True))
        rango_desde_1=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('rango_desde_1',flat=True))
        rango_hasta_1=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('rango_hasta_1',flat=True))
        rango_color_1=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('rago_color_1',flat=True))
        rango_desde_2=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('rango_desde_2',flat=True))
        rango_hasta_2=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('rango_hasta_2',flat=True))
        rango_color_2=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('rago_color_2',flat=True))
        rango_desde_3=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('rango_desde_3',flat=True))
        rango_hasta_3=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('rango_hasta_3',flat=True))
        rango_color_3=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('rago_color_3',flat=True))
        comentario=list(Indicador.objects.filter(id=pk,indicador_tipo='Rentabilidad').values_list('indicador_comentario',flat=True))
        parametros=name+formula+rango_desde_1+rango_hasta_1+rango_color_1+rango_desde_2+rango_hasta_2+rango_color_2+rango_desde_3+rango_hasta_3+rango_color_3+comentario
        #graph=Draw_Ind(parametros[1],parametros[0],parametros[2],parametros[3],parametros[4],parametros[5]) 
        dashboard=prueba(parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5],parametros[6],parametros[7],parametros[8],parametros[9],parametros[10],parametros[11])


        context={'name':parametros[0],'dashboard':dashboard}
        template='core/Finanzas/Indicadores/Rentabilidad/indicador_rentabilidad.html'
    return render(request,template,context)

##############################################
def IndicadorSolvenciaAllView(request):
    indicadores=Indicador.objects.filter(indicador_tipo='Solvencia')
    context={'indicadores':indicadores}
    
    return render(request,'core/Finanzas/Indicadores/Solvencia/lista_solvencia.html',context)

def IndicadorSolvenciaShowView(request,pk):
    if pk==None:
        template='core/Finanzas/Indicadores/Solvencia/lista_solvencia.html'
    else:
        name=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('name',flat=True))
        formula=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('formula',flat=True))
        rango_desde_1=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('rango_desde_1',flat=True))
        rango_hasta_1=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('rango_hasta_1',flat=True))
        rango_color_1=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('rago_color_1',flat=True))
        rango_desde_2=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('rango_desde_2',flat=True))
        rango_hasta_2=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('rango_hasta_2',flat=True))
        rango_color_2=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('rago_color_2',flat=True))
        rango_desde_3=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('rango_desde_3',flat=True))
        rango_hasta_3=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('rango_hasta_3',flat=True))
        rango_color_3=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('rago_color_3',flat=True))
        comentario=list(Indicador.objects.filter(id=pk,indicador_tipo='Solvencia').values_list('indicador_comentario',flat=True))
        parametros=name+formula+rango_desde_1+rango_hasta_1+rango_color_1+rango_desde_2+rango_hasta_2+rango_color_2+rango_desde_3+rango_hasta_3+rango_color_3+comentario
        #graph=Draw_Ind(parametros[1],parametros[0],parametros[2],parametros[3],parametros[4],parametros[5]) 
        dashboard=prueba(parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5],parametros[6],parametros[7],parametros[8],parametros[9],parametros[10],parametros[11])
        context={'name':parametros[0],'dashboard':dashboard}
        template='core/Finanzas/Indicadores/Solvencia/indicador_solvencia.html'
    return render(request,template,context)

##################################



def IndicadorLiquidezAllView(request):
    indicadores=Indicador.objects.filter(indicador_tipo='Liquidez')
    context={'indicadores':indicadores}
    
    return render(request,'core/Finanzas/Indicadores/Liquidez/lista_liquidez.html',context)

def IndicadorLiquidezShowView(request,pk):
    if pk==None:
        template='core/Finanzas/Indicadores/Liquidez/lista_liquidez.html'
    else:
        
        name=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('name',flat=True))
        formula=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('formula',flat=True))
        rango_desde_1=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('rango_desde_1',flat=True))
        rango_hasta_1=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('rango_hasta_1',flat=True))
        rango_color_1=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('rago_color_1',flat=True))
        rango_desde_2=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('rango_desde_2',flat=True))
        rango_hasta_2=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('rango_hasta_2',flat=True))
        rango_color_2=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('rago_color_2',flat=True))
        rango_desde_3=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('rango_desde_3',flat=True))
        rango_hasta_3=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('rango_hasta_3',flat=True))
        rango_color_3=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('rago_color_3',flat=True))
        comentario=list(Indicador.objects.filter(id=pk,indicador_tipo='Liquidez').values_list('indicador_comentario',flat=True))
        parametros=name+formula+rango_desde_1+rango_hasta_1+rango_color_1+rango_desde_2+rango_hasta_2+rango_color_2+rango_desde_3+rango_hasta_3+rango_color_3+comentario
        #graph=Draw_Ind(parametros[1],parametros[0],parametros[2],parametros[3],parametros[4],parametros[5]) 
        dashboard=prueba(parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5],parametros[6],parametros[7],parametros[8],parametros[9],parametros[10],parametros[11])

        context={'name':parametros[0],'dashboard':dashboard}
        template='core/Finanzas/Indicadores/Liquidez/indicador_liquidez.html'
    
    
    return render(request,template,context)

