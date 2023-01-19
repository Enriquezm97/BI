


from django.shortcuts import redirect


class SuperUsuarioMixin(object):
    
    def dispatch(self,request,*args, **kwargs):
        if request.user.is_staff:
            return super(CLASS_NAME,self).dispath(request,*args,**kwargs)
        return redirect('index')