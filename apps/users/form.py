
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario, Empresa, Rol
from.crum import get_empresa_id

class RegistroUser(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RegistroProfile(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingresa tus nombres','class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingresa tus apellidos','class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu username','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' :'Email', 'class': 'form-control'}))
    user = forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
    is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'onoffswitch','id': 'myonoffswitch'}))
    verified = forms.BooleanField()
    picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'número telefonico','class':'form-control'}))
    empresa = forms.ModelChoiceField(
                                queryset=Empresa.objects.filter(id = 6),
                                widget=forms.Select(attrs={'class': 'form-control'})
            )
    rol = forms.ModelChoiceField(
                                queryset=Rol.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control'})
            )
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','user','is_staff','verified','picture','phone','empresa','rol']