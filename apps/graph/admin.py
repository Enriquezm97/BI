
from django.contrib import admin

from .models import Indicador
from .models import TipoIndicador
# Register your models here.
admin.site.register(Indicador)
admin.site.register(TipoIndicador)
