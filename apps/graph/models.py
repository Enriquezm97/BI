from django.db import models
from apps.users.models import Usuario as User
# Create your models here.
RATIOS = (
    ('Liquidez','Liquidez'),
    ('Rentabilidad', 'Rentabilidad'),
    ('Solvencia','Solvencia'),
)

class TipoIndicador(models.Model):
    
    
    name_tipo_indicador = models.CharField(max_length=100, blank=True,null=True)
    create_tipo_indicador = models.DateTimeField(auto_now_add=True,null=True)
    modified_tipo_indicador = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):

        return self.name_tipo_indicador

class Indicador(models.Model): 
    name =models.CharField(max_length=150)
    formula=models.CharField(max_length=150)
    rango_desde_1=models.FloatField(null=True)
    rango_hasta_1=models.FloatField(null=True)
    rango_color_1=models.CharField(max_length=7,null=True)
    rango_desde_2=models.FloatField(null=True)
    rango_hasta_2=models.FloatField(null=True)
    rango_color_2=models.CharField(max_length=7,null=True)
    rango_desde_3=models.FloatField(null=True)
    rango_hasta_3=models.FloatField(null=True)
    rango_color_3=models.CharField(max_length=7,null=True)
    ejex=models.CharField(max_length=50,null=True)
    ejey=models.CharField(max_length=50,null=True)
    valor_minimo=models.FloatField(null=True)
    valor_maximo=models.FloatField(null=True)
    dataframe=models.CharField(max_length=150,null=True)

    
    indicador_tipo=models.ForeignKey(TipoIndicador,on_delete=models.CASCADE,null=True)

    indicador_favorito=models.BooleanField(default=False)
    indicador_comentario=models.CharField(max_length=500,null=True)
    tipo_graph=models.CharField(max_length=50,null=True)
    usuario=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    create = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):

        return self.name

