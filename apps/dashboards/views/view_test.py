from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from ...users.models import Empresa,Usuario,Rubro
from ..content.test_dash import dashboard_test,dashboard_resize


class test_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        
        id_user=self.request.user.id
        id_app =f'{id_user}-stock'
        user_filter=list(Usuario.objects.filter(user_id=id_user).values_list('empresa_id',flat=True))
        name_empresa=Empresa.objects.filter(pk=user_filter[0]).values_list('name_empresa',flat=True)[0]
        dashboard=dashboard_test(codigo = id_app, empresa = name_empresa)
        context = {'dashboard':dashboard, 'code':id_app}
        
        return render(request,'any.html',context)
    
    
    
from concurrent.futures import ThreadPoolExecutor
import requests
from datetime import datetime,timedelta
dict_CONSUMOSALM = {
                'C_EMP':'001','C_SUC':'','C_ALM': '',
                'C_FECINI':str(datetime.now()- timedelta(days = 6 * 30))[:8].replace('-', "")+str('01')  ,
                'C_FECFIN':str(datetime.now())[:10].replace('-', ""),
                'C_VALOR':'1','C_GRUPO':'','C_SUBGRUPO':'','C_TEXTO':'','C_IDPRODUCTO':'','LOTEP':'','C_CONSUMIDOR':''
            }

dict_SALDOSALM = {
                    'EMPRESA':'001','SUCURSAL':'','ALMACEN': '','FECHA':str(datetime.now())[:10].replace('-', ""),
                    'IDGRUPO':'','SUBGRUPO':'','DESCRIPCION':'','IDPRODUCTO':'','LOTEP':'',
            }
class resize_View(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request,*args, **kwargs):
        def send_get_json(params=None,endpoint = None):
            headers = {"Authorization": "Bearer {}".format("0N10S10Z10O10M10X10E10C10Y1lpu0N10O10H10T10I1sgk0Q10D10N10D10O10Z1lpu0T10o10d10e10i10z10x10b1lpu0S10n10r10N1rtg0I10Q1njh0M10J10q10I1lpumkimkiertlpuertsdfasdasdlpuertnjhmkiloisdfrtgsdfnjhmkiqwsloiqwsert")}
            url = f"http://68.168.108.10:3005/api/consulta/{endpoint}"
            response = requests.get(url, headers=headers,params = params)
            return response.json()
        print(datetime.now())
        with ThreadPoolExecutor(max_workers=2) as executor:
            resultado1 = executor.submit(send_get_json, dict_CONSUMOSALM, "NSP_OBJREPORTES_CONSUMOSALM_DET_BI")
            resultado2 = executor.submit(send_get_json,dict_SALDOSALM,"NSP_OBJREPORTES_SALDOSALMACEN_BI")
        print(datetime.now())
        #print(resultado1,resultado2)
        
        id_user=self.request.user.id
        id_app =f'{id_user}-resize'
        
        dashboard=dashboard_resize(codigo = id_app)
        context = {'dashboard':dashboard, 'code':id_app}
        
        return render(request,'any.html',context)