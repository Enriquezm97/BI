import base64
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from ..dashboards.models import ConfigDashboard


RUBRO = (
    ('Comercial','Comercial'),
    ('Agricola', 'Agricola'),
    ('Agroindustrial','Agroindustrial'),
    ('Industrial','Industrial'),
)
class Rol(models.Model):
    
    
    name_rol= models.CharField(max_length=50, blank=True,null=True)
    create_rol = models.DateTimeField(auto_now_add=True,null=True)
    modified_rol = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):

        return self.name_rol
    
class Rubro(models.Model):
    
    
    name_rubro = models.CharField(max_length=50, blank=True,null=True)
    create_rubro = models.DateTimeField(auto_now_add=True,null=True)
    modified_rubro = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):

        return self.name_rubro



class Empresa(models.Model):
    
    #user_empresa =  models.OneToOneField(User,on_delete=models.CASCADE)
    name_empresa = models.CharField(max_length=100, blank=True,null=True)
    phone_number_empresa = models.CharField(max_length=20, blank=True,null=True)
    picture_empresa = models.BinaryField(null=True)
    codigo_empresa= models.CharField(max_length=15, blank=True,null=True)
    ruc_empresa = models.CharField(max_length=12, blank=True,null=True)
    rubro_empresa=models.ForeignKey(Rubro,on_delete=models.CASCADE)
    config_dashboard=models.ForeignKey(ConfigDashboard,on_delete=models.CASCADE,null=True)
    create_empresa = models.DateTimeField(auto_now_add=True,null=True)
    modified_empresa = models.DateTimeField(auto_now=True,null=True)
    marca_empresa = models.TextField(blank=True)
    #
    api_publica = models.CharField(max_length=255,null=True)
    api_local = models.CharField(max_length=255,null=True)
    servidor_bd = models.CharField(max_length=255,null=True)
    puerto_bd = models.CharField(max_length=255,default='1433',null=True)
    usuario_bd = models.CharField(max_length=255,null=True)
    password_bd = models.CharField(max_length=100,null=True)
    name_bd = models.CharField(max_length=255,null=True)
    token = models.CharField(max_length=255,null=True)
    def imagen_encoded(self):
        from base64 import b64encode
        if self.picture_empresa:
            return b64encode(self.picture_empresa).decode('utf8')
        return None
    
    def __str__(self):

        return self.name_empresa

class Usuario(models.Model):
    #account = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    #user=models.ForeignKey(User, on_delete=models.CASCADE,default="")
    user =  models.OneToOneField(User,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    verified = models.BooleanField(default=False)
    requested_verified = models.BooleanField(default=False)

    picture = models.BinaryField(null=True)
    datos_picture = models.TextField(blank=True)
    #username =  models.OneToOneField(User,on_delete=models.CASCADE)
    #name = models.CharField(max_length=15, blank=True,null=True)
    phone = models.CharField(max_length=20, blank=True,null=True)
    #picture = models.ImageField(upload_to='media',blank=True,null=True)
    empresa=models.ForeignKey(Empresa,on_delete=models.CASCADE)
    rol=models.ForeignKey(Rol,on_delete=models.CASCADE,null=True)
    create = models.DateTimeField(auto_now_add=True,null=True)
    modified = models.DateTimeField(auto_now=True,null=True)

    def imagen_encoded(self):
        from base64 import b64encode
        if self.picture:
            return b64encode(self.picture).decode('utf8')
        return None

    def __str__(self):

        return self.username#, self.empresa


#class PerfilUser(AbstractUser):
#    picture = models.ImageField(upload_to='media',blank=True,null=True)
#    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
#3    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=True)
    # Otros campos adicionales del usuario

#    def __str__(self):
#        return self.username

class Mantenedor(models.Model):
    
    empresa=models.ForeignKey(Empresa,on_delete=models.CASCADE)
    api_publica = models.CharField(max_length=255,null=True)
    api_local = models.CharField(max_length=255,null=True)
    servidor_bd = models.CharField(max_length=255,null=True)
    puerto_bd = models.CharField(max_length=255,default='1433',null=True)
    usuario_bd = models.CharField(max_length=255,null=True)
    password_bd = models.CharField(max_length=100,null=True)
    name_bd = models.CharField(max_length=255,null=True)
    token = models.CharField(max_length=255,null=True)
    create_mantenedor = models.DateTimeField(auto_now_add=True,null=True)
    modified_mantenedor = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):

        return self.servidor_bd
    
"""
LA TABLA USUARIO SE QUIERE ELIMNAR CREANDO UNA ABSTRACCION DEL MODEL USER 
ESTO AYUDARA A PODER CREAR USUARIOS SIN PROBLEMA PERO TENIENDO ENCUENTA QUE 
LA TABLA USER DEBE ESTAR RELACIONADA A UNA EMPRESA Y A UN ROL
"""

#class UsuarioPersonalizado(AbstractUser):
    # Añadir campos adicionales aquí
#    fecha_nacimiento = models.DateField(null=True, blank=True)
    #telefono = models.CharField(max_length=15, blank=True)
    #direccion = models.CharField(max_length=255, blank=True)

    # Agregar más c
