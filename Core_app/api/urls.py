from django.urls import path
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register('pessoas', viewsets.PessoasModelViewSet, basename='pessoas')
router.register('contrato_parcelas', viewsets.ContratoParcelasModelViewSet, basename='contrato_parcelas')
router.register('contratos', viewsets.ContratosModelViewSet, basename='contratos')
router.register('eventos', viewsets.EventosModelViewSet, basename='eventos')
router.register('contratos-vendedor', viewsets.ContratosVendedorViewSet, basename='contratos-vendedor')
router.register('contratos-comprador', viewsets.ContratosCompradorViewSet, basename='contratos-comprador')
router.register('consulta-juridico', viewsets.ConsultaJuridicoViewSet, basename='consulta-juridico')
router.register('recuperacao-credito', viewsets.RecuperacaoCreditoViewSet, basename='recuperacao-credito')
urlpatterns = [
] + router.urls
