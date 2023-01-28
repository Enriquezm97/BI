
from django.contrib import admin
#from users.models import Usuario,Empresa
from .models import Usuario,Empresa,Rubro
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(Rubro)








#from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from django.contrib.auth.models import User
# Register your models   here.

#admin.site.register(Usuario)
#admin.site.register(Empresa)
"""
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):


    
    list_display = ('pk','user','phone_number','picture')
    list_display_links=('pk','user')
    #list_editable=('phone_numer')
    search_fields = ('user__email','user__first_name','user__last_name')

    list_filter = ('create','modified','user__is_active','user__is_staff')

    fieldsets=(
        ('Usuario',{
            'fields':(
                ('user','picture','phone_number')
                #('user','picture','phone_number')
                ),

        }),
        
    )

class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'usuarios'


class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)
    list_display = (
        'username',
        
        'is_active',
        'is_staff'
    )
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):


    
    list_display = ('pk','name_empresa','phone_number_empresa','picture_empresa','codigo_empresa')
    list_display_links=('pk','name_empresa')
    #list_editable=('phone_numer')
    #search_fields = ('user__email','user__first_name','user__last_name')

    #list_filter = ('create','modified','user__is_active','user__is_staff')

    fieldsets=(
        ('Empresa',{
            'fields':(
                ('name_empresa','picture_empresa','codigo_empresa')
                #('user','picture','phone_number')
                ),

        }),
        
    )


"""
