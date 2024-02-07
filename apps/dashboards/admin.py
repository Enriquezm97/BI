from django.contrib import admin
from .models import ConfigDashboard,PaletaColores,ConfigGrafico,TipoDashboard,TipoGrafico,StoreProcedures
# Register your models here.
admin.site.register(ConfigDashboard)
admin.site.register(PaletaColores)
admin.site.register(ConfigGrafico)
admin.site.register(TipoDashboard)
admin.site.register(TipoGrafico)
admin.site.register(StoreProcedures)