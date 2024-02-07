from django.db import models

class TipoDashboard(models.Model):
    name_type_dashboard = models.CharField(max_length=200, blank=True,null=False)
    description = models.CharField(max_length=300, blank=True,null=False)
    create_tipo_dashboard = models.DateTimeField(auto_now_add=True,null=True)
    modified_tipo_dashboard = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):

        return self.name_type_dashboard
class StoreProcedures(models.Model):
    tipo_dashboard = models.ForeignKey(TipoDashboard,on_delete=models.CASCADE,null=True)
    name_sp = models.CharField(max_length=500, blank=True,null=False)
    var_categ = models.CharField(max_length=2000, blank=False,null=False)
    var_numerico = models.CharField(max_length=2000, blank=False,null=False)
    create_sp = models.DateTimeField(auto_now_add=True,null=True)
    modified_sp = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):

        return self.name_sp

class PaletaColores(models.Model):
    name_paleta = models.CharField(max_length=100, blank=True,null=False)
    colors_list =  models.CharField(max_length=1000, blank=True,null=False)
    create_paleta_colors = models.DateTimeField(auto_now_add=True,null=True)
    modified_paleta_colors = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):

        return self.name_paleta
# CADA CONFIG SERA POR EMPRESA 
class ConfigDashboard(models.Model):
    name_config = models.CharField(max_length=100,blank=True,null=False)
    ticklabel_color = models.CharField(max_length=30,default='black')
    ticklabel_size = models.IntegerField(default = 12)
    showticklabels = models.BooleanField(default=True)
    plot_bgcolor = models.CharField(default = '#ffffff',max_length=30, blank=True,null=False)
    paper_bgcolor = models.CharField(default = '#ffffff',max_length=30, blank=True,null=False)
    create_config_dashboard = models.DateTimeField(auto_now_add=True,null=True)
    modified_config_dashboard = models.DateTimeField(auto_now=True,null=True)
    paleta_colores=models.ForeignKey(PaletaColores,on_delete=models.CASCADE,null=True)

    def __str__(self):

        return self.name_config

class TipoGrafico(models.Model):
    name_tipo_grafico = models.CharField(max_length=200, blank=True,null=False)
    create_tipo_grafico = models.DateTimeField(auto_now_add=True,null=True)
    modified_tipo_grafico = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.name_tipo_grafico


class ConfigGrafico(models.Model):
    tipo_dashboard = models.ForeignKey(TipoDashboard,on_delete=models.CASCADE,null=True)
    name_grafico = models.CharField(max_length=200, blank=True,null=False)
    tipo_grafico = models.ForeignKey(TipoGrafico,on_delete=models.CASCADE,null=True)
    var_categorica = models.CharField(max_length=200, choices=[])
    var_numerico = models.CharField(max_length=200, choices=[],null=True)
    create_grafico = models.DateTimeField(auto_now_add=True,null=True)
    modified_grafico= models.DateTimeField(auto_now=True,null=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define las opciones del campo choices utilizando los valores de la columna 'opcion' de StoreProcedures
        self._meta.get_field('var_categorica').choices = [(obj.var_categ, obj.var_categ) for obj in StoreProcedures.objects.all()]
        self._meta.get_field('var_numerico').choices = [(obj.var_numerico, obj.var_numerico) for obj in StoreProcedures.objects.all()]
    
    def __str__(self):
        return self.name_grafico
    