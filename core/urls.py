from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from apps.graph.views.views import Error404View,Error505View
from apps.graph.test.utils.crum import *
#app_name = "users_app"
from datetime import datetime
#{str(datetime.now()).strip().replace(" ","").replace(":","").replace("-","").replace(".","")}/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_plotly_dash.urls')),#django_plotly_dash/
    path('',include('apps.graph.urls')),
    path('user/',include('apps.users.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = Error404View.as_view()

handler500 = Error505View.as_error_view()     