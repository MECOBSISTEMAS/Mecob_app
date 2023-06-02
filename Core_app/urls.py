from django.urls import path, include
from .api import urls

urlpatterns = [
    #path('', views.index, name='index'),
    path('', include(urls))
]
