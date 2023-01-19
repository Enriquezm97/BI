from django.forms import *
from requests import request

from apps.graph.models import Indicador

from django.contrib.auth.models import User

class IndicadorForm(ModelForm):

    #def __init__(self,*args, **kwargs):
    #    super().__init__(*args, **kwargs)
        

    class Meta:
        model= Indicador
        fields=['indicador_tipo','name','formula','rango_desde_1','rango_hasta_1','rango_color_1','rango_desde_2','rango_hasta_2','rango_color_2','rango_desde_3','rango_hasta_3','rango_color_3','indicador_favorito','indicador_comentario']#
        