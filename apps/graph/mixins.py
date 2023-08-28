from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from apps.users.models import Empresa,Usuario,Rubro,Rol


class AdministradoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        id_user=self.request.user.id
        rol_id=list(Usuario.objects.filter(user_id=id_user).values_list('rol_id',flat=True))
        rol=Rol.objects.filter(pk=rol_id[0]).values_list('name_rol',flat=True)
        if rol[0] == 'Administrador':
        #if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')
    

class AnalistaMixin(object):
    def dispatch(self, request, *args, **kwargs):
        id_user=self.request.user.id
        rol_id=list(Usuario.objects.filter(user_id=id_user).values_list('rol_id',flat=True))
        rol=Rol.objects.filter(pk=rol_id[0]).values_list('name_rol',flat=True)
        if rol[0] == 'Administrador' or rol[0] == 'Analista':
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')

class AsistenteMixin(object):
    def dispatch(self, request, *args, **kwargs):
        id_user=self.request.user.id
        rol_id=list(Usuario.objects.filter(user_id=id_user).values_list('rol_id',flat=True))
        rol=Rol.objects.filter(pk=rol_id[0]).values_list('name_rol',flat=True)
        if rol[0] == 'Administrador' or rol[0] == 'Asistente':
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')
    
"""
class AdministradoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')
"""