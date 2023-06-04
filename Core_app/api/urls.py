from django.urls import path
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register('pessoas', viewsets.PessoasModelViewSet, basename='pessoas')
router.register('pessoas-viewset', viewsets.PessoasViewSets, basename='pessoas-viewset')
router.register('contrato_parcelas', viewsets.ContratoParcelasModelViewSet, basename='contrato_parcelas')
router.register('contratos', viewsets.ContratosModelViewSet, basename='contratos')
router.register('eventos', viewsets.EventosModelViewSet, basename='eventos')
router.register('contratos-vendedor', viewsets.ContratosVendedorViewSets, basename='contratos-vendedor')
urlpatterns = [
] + router.urls
