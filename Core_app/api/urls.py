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
router.register('contratos-parcelas-vendedor-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosParcelasVendedorEmailStatusModelViewSet, basename='contratos-parcelas-vendedor-email-status')
router.register('contratos-parcelas-comprador-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosParcelasCompradorEmailStatusModelViewSet, basename='contratos-parcelas-comprador-email-status')
router.register('contratos-vendedor-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosVendedorEmailStatusViewSet, basename='contratos-vendedor-email-status')
router.register('contratos-comprador-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosCompradorEmailStatusViewSet, basename='contratos-comprador-email-status')
router.register('dashboard/seu-email-aqui', viewsets.DashBoardViewSet, basename='dashboard')
router.register('registro-usuario/email/password', viewsets.RegistroUsuarioViewSet, basename='registro-usuario')
router.register('resetar-senha/email/senha', viewsets.ResetarSenhaViewSet, basename='resetar-senha')
router.register('ContratosAllContratoParcelasAllViewSet', viewsets.ContratosAllContratoParcelasAllViewSet, basename='ContratosAllContratoParcelasAllModelViewSet')

urlpatterns = [
  path('custom-login/', viewsets.CustomLoginView.as_view(), name='custom-login'),
  path('execute_query_sql_function/', viewsets.execute_query_sql, name='execute_query_sql'),
  path('execute_query_sql_class/', viewsets.ExecuteQuerySqlViewSet.as_view({'post':'execute_query_sql'}), name='execute_query_sql'),
  path('contratos-vendedor-email/<str:email>/', viewsets.ContratosVendedorEmailViewSet.as_view({'get': 'list'}), name='contratos-vendedor-email'),
  path('contratos-comprador-email/<str:email>/', viewsets.ContratosCompradorEmailViewSet.as_view({'get': 'list'}), name='contratos-comprador-email'),
  path('contratos-email-status/<str:email>/<str:status>/', viewsets.ContratosEmailStatusViewSet.as_view({'get': 'list'}), name='contratos-email-status'),
  path('contratos-parcelas-vendedor-email-status/<str:email>/<str:status>/', viewsets.ContratosParcelasVendedorEmailStatusModelViewSet.as_view({'get': 'list'}), name='contratos-parcelas-vendedor-email-status'),
  path('contratos-parcelas-comprador-email-status/<str:email>/<str:status>/', viewsets.ContratosParcelasCompradorEmailStatusModelViewSet.as_view({'get': 'list'}), name='contratos-parcelas-comprador-email-status'),
  path('contratos-comprador-email-status/<str:email>/<str:status>/', viewsets.ContratosCompradorEmailStatusViewSet.as_view({'get': 'list'}), name='contratos-comprador-email-status'),
  path('contratos-vendedor-email-status/<str:email>/<str:status>/', viewsets.ContratosVendedorEmailStatusViewSet.as_view({'get': 'list'}), name='contratos-vendedor-email-status'),
  path('resetar-senha/<str:email>/<str:password>/', viewsets.ResetarSenhaViewSet.as_view({'get': 'list'}), name='resetar-senha'),
  path('dashboard/<str:email>/', viewsets.DashBoardViewSet.as_view({'get': 'list'}), name='dashboard'),
  path('registro-usuario/<str:email>/<str:password>/', viewsets.RegistroUsuarioViewSet.as_view({'get': 'list'}), name='registro-usuario'),
  #router.register('ContratosAllContratoParcelasAllModelViewSet', viewsets.ContratosAllContratoParcelasAllModelViewSet, basename='ContratosAllContratoParcelasAllModelViewSet')
  path('ContratosAllContratoParcelasAllViewSet/<str:contrato_id>/', viewsets.ContratosAllContratoParcelasAllViewSet.as_view({'get': 'retrieve'}), name='ContratosAllContratoParcelasAllModelViewSet'),
  #!Rotas para autenticação JWT
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
