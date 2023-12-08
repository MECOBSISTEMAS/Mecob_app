from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView

urlpatterns = [
    #acesso a pagina de administração
    path('admin/', admin.site.urls),
    #acesso a pagina de api de autenticação do django-rest-framework
    path('api-auth/', include('rest_framework.urls')), #rota de autenticação utilizando a configuração nativa do framework
    #acesso aos apps instanciados pelo django
    path('', include('Core_app.urls')), 
    path('dj-rest-auth/', include('dj_rest_auth.urls')), #rota de autenticação utilizando a biblioteca dj-rest-auth
    #path('rest-auth/', include('rest_auth.urls')),
    #path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('rest-auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)