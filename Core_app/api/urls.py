from django.urls import path
from rest_framework import routers

from . import viewsets
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router = routers.DefaultRouter()
router.register('pessoas', viewsets.PessoasModelViewSet, basename='pessoas')
router.register('contrato_parcelas', viewsets.ContratoParcelasModelViewSet, basename='contrato_parcelas')
router.register('contratos', viewsets.ContratosModelViewSet, basename='contratos')
router.register('eventos', viewsets.EventosModelViewSet, basename='eventos')
router.register('contratos-vendedor', viewsets.ContratosVendedorViewSet, basename='contratos-vendedor')
router.register(r'contratos-vendedor-email/seu-email-aqui', viewsets.ContratosVendedorEmailViewSet, basename='contratos-vendedor-email')
router.register('contratos-comprador', viewsets.ContratosCompradorViewSet, basename='contratos-comprador')
router.register('contratos-comprador-email/seu-email-aqui', viewsets.ContratosCompradorEmailViewSet, basename='contratos-comprador-email')
router.register('consulta-juridico', viewsets.ConsultaJuridicoViewSet, basename='consulta-juridico')
router.register('recuperacao-credito', viewsets.RecuperacaoCreditoViewSet, basename='recuperacao-credito')
router.register('contratos-email-status/seu-email-aqui', viewsets.ContratosEmailStatusViewSet, basename='contratos-email-status')
router.register('contratos-vendedor-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosVendedorEmailStatusModelViewSet, basename='contratos-vendedor-email-status')
router.register('contratos-comprador-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosCompradorEmailStatusModelViewSet, basename='contratos-comprador-email-status')
urlpatterns = [
  path('contratos-vendedor-email/<str:email>/', viewsets.ContratosVendedorEmailViewSet.as_view({'get': 'list'}), name='contratos-vendedor-email'),
  path('contratos-comprador-email/<str:email>/', viewsets.ContratosCompradorEmailViewSet.as_view({'get': 'list'}), name='contratos-comprador-email'),
  path('contratos-email-status/<str:email>/<str:status>/', viewsets.ContratosEmailStatusViewSet.as_view({'get': 'list'}), name='contratos-email-status'),
  path('contratos-vendedor-email-status/<str:email>/<str:status>/', viewsets.ContratosVendedorEmailStatusModelViewSet.as_view({'get': 'list'}), name='contratos-vendedor-email-status'),
  path('contratos-comprador-email-status/<str:email>/<str:status>/', viewsets.ContratosCompradorEmailStatusModelViewSet.as_view({'get': 'list'}), name='contratos-comprador-email-status'),
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
