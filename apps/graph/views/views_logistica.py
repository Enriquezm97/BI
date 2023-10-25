from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from ...graph.test.layouts.logistica import *

class Logistica_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')#'/user/login/'
    def get(self,request,*args, **kwargs):
        #id_user=self.request.user.id
        
        context = {'dashboard':logistica_dash()}
        return render(request,'logistica/logistica_dash.html',context)