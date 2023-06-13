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
router.register('contratos-email-status-model/seu-email-aqui', viewsets.ContratosEmailStatusModelViewSet, basename='contratos-email-status-model')
urlpatterns = [
  path('contratos-vendedor-email/<str:email>/', viewsets.ContratosVendedorEmailViewSet.as_view({'get': 'list'}), name='contratos-vendedor-email'),
  path('contratos-comprador-email/<str:email>/', viewsets.ContratosCompradorEmailViewSet.as_view({'get': 'list'}), name='contratos-comprador-email'),
  path('contratos-email-status/<str:email>/<str:status>/', viewsets.ContratosEmailStatusViewSet.as_view({'get': 'list'}), name='contratos-email-status'),
  path('contratos-email-status-model/<str:email>/<str:status>/', viewsets.ContratosEmailStatusModelViewSet.as_view({'get': 'list'}), name='contratos-email-status-model'),
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
