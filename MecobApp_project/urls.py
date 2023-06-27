from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #acesso a pagina de administração
    path('admin/', admin.site.urls),
    #acesso a pagina de api de autenticação do django-rest-framework
    path('api-auth/', include('rest_framework.urls')),
    #acesso aos apps instanciados pelo django
    path('', include('Core_app.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)