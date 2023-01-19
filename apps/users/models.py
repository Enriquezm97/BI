
#from django.contrib.auth.models import User
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


#def user_profile_directory_path(instance, filename):
#    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#    profile_pic_name = 'users/{0}/profile.jpg'.format(instance.account)
#    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

#    if os.path.exists(full_path):
#    	os.remove(full_path)

# Create your models here.
class Empresa(models.Model):
    
    #user_empresa =  models.OneToOneField(User,on_delete=models.CASCADE)
    name_empresa = models.CharField(max_length=15, blank=True,null=True)
    phone_number_empresa = models.CharField(max_length=20, blank=True,null=True)
    picture_empresa = models.ImageField(upload_to='media',blank=True,null=True)
    codigo_empresa= models.CharField(max_length=15, blank=True,null=True)
    create_empresa = models.DateTimeField(auto_now_add=True,null=True)
    modified_empresa = models.DateTimeField(auto_now=True,null=True)

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

    picture = models.ImageField(upload_to='media',blank=True,null=True)
    #username =  models.OneToOneField(User,on_delete=models.CASCADE)
    #name = models.CharField(max_length=15, blank=True,null=True)
    phone = models.CharField(max_length=20, blank=True,null=True)
    #picture = models.ImageField(upload_to='media',blank=True,null=True)
    empresa=models.ForeignKey(Empresa,on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True,null=True)
    modified = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):

        return self.username


