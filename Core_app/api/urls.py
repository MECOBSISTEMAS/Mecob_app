from django.urls import path
from rest_framework import routers

from . import viewsets
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router = routers.DefaultRouter()

#Com o atalho ctrl + clique em 'PessoasModelViewSet'
#O endpoint /pessoas irá listas todas as pessoas de 10 em 10 por página
router.register('pessoas', viewsets.PessoasModelViewSet, basename='pessoas')

#Com o atalho ctrl + clique em 'ContratoParcelasModelViewSet'
#O endpoint /contrato_parcelas retorna todos os contratos das parcelas de 10 em 10 por página
router.register('contrato_parcelas', viewsets.ContratoParcelasModelViewSet, basename='contrato_parcelas')

#O endpoint /contratos retorna todos os contratos de 10 em 10 por página
router.register('contratos', viewsets.ContratosModelViewSet, basename='contratos')

#O endpoint /eventos retorna todos os eventos de 10 em 10 por página
router.register('eventos', viewsets.EventosModelViewSet, basename='eventos')

#O endpoint /contratos-vendedor irá retornar todos os contratos da pessoa como vendedora
router.register('contratos-vendedor', viewsets.ContratosVendedorViewSet, basename='contratos-vendedor')

#O endpoint /contratos-vendedor-email/seu-email-aqui irá retornar todos os contratos de uma pessoa como vendedora passando seu email como parametro
router.register(r'contratos-vendedor-email/seu-email-aqui', viewsets.ContratosVendedorEmailViewSet, basename='contratos-vendedor-email')

#O endpoint /contratos-comprador irá retornar todos os contratos de uma pessoa como compradora
router.register('contratos-comprador', viewsets.ContratosCompradorViewSet, basename='contratos-comprador')

#O endpoint /contratos-comprador-email/seu-email-aqui  irá retornar todos os contratos de uma pessoa como compradora passando seu email como parametro
router.register('contratos-comprador-email/seu-email-aqui', viewsets.ContratosCompradorEmailViewSet, basename='contratos-comprador-email')

#O endpoint /consulta-juridico irá retornar todos os contratos da pessoa como vendedora em que o contrato está com o status acao_judicial
router.register('consulta-juridico', viewsets.ConsultaJuridicoViewSet, basename='consulta-juridico')

#O endpoint /recuperacao-credito retorna todos os contratos da pessoa como vendedora em que o contrato está com o status pendente
router.register('recuperacao-credito', viewsets.RecuperacaoCreditoViewSet, basename='recuperacao-credito')

#O endpoint /contratos-email-status/seu-email-aqui ira retornar todos os contratos da pessoa como vendedora e suas parcelas passando seu e-mail parametro
router.register('contratos-email-status/seu-email-aqui', viewsets.ContratosEmailStatusViewSet, basename='contratos-email-status')

#O endpoint /contratos-parcelas-vendedor-email-status/seu-email-aqui/status-do-contrato
router.register('contratos-parcelas-vendedor-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosParcelasVendedorEmailStatusModelViewSet, basename='contratos-parcelas-vendedor-email-status')

#O endpoint /contratos-parcelas-comprador-email-status/seu-email-aqui/status-do-contrato
router.register('contratos-parcelas-comprador-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosParcelasCompradorEmailStatusModelViewSet, basename='contratos-parcelas-comprador-email-status')

#O endpoint /contratos-vendedor-email-status/seu-email-aqui/status-do-contrato
router.register('contratos-vendedor-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosVendedorEmailStatusViewSet, basename='contratos-vendedor-email-status')

#O endpoint /contratos-comprador-email-status/seu-email-aqui/status-do-contrato
router.register('contratos-comprador-email-status/seu-email-aqui/status-do-contrato', viewsets.ContratosCompradorEmailStatusViewSet, basename='contratos-comprador-email-status')

#O endpoint /dashboard/seu-email-aqui
router.register('dashboard/seu-email-aqui', viewsets.DashBoardViewSet, basename='dashboard')

#O endpoint /registro-usuario/email/password
router.register('registro-usuario/email/password', viewsets.RegistroUsuarioViewSet, basename='registro-usuario')

#O endpoint /resetar-senha/email/senha
router.register('resetar-senha/email/senha', viewsets.ResetarSenhaViewSet, basename='resetar-senha')

#O endpoint /ContratosAllContratoParcelasAllViewSet
router.register('ContratosAllContratoParcelasAllViewSet', viewsets.ContratosAllContratoParcelasAllViewSet, basename='ContratosAllContratoParcelasAllModelViewSet')

#O endpoint /contratos-vendedor-email-quantidade/seu-email-aqui/quantidade/status
router.register('contratos-vendedor-email-quantidade/seu-email-aqui/quantidade/status', viewsets.ContratosVendedorEmailQuantidadeViewSet, basename='contratos-vendedor-email-quantidade')

#O endpoint /contratos-comprador-email-quantidade/seu-email-aqui/quantidade/status
router.register('contratos-comprador-email-quantidade/seu-email-aqui/quantidade/status', viewsets.ContratosCompradorEmailQuantidadeViewSet, basename='contratos-comprador-email-quantidade')
urlpatterns = [
  path('custom-login/', viewsets.CustomLoginView.as_view(), name='custom-login'),
  path('execute_query_sql_function/', viewsets.execute_query_sql, name='execute_query_sql'),
  path('execute_query_sql_class/', viewsets.ExecuteQuerySqlViewSet.as_view({'post':'execute_query_sql'}), name='execute_query_sql'),
  path('contratos-vendedor-email/<str:email>/', viewsets.ContratosVendedorEmailViewSet.as_view({'get': 'list'}), name='contratos-vendedor-email'),
  path('contratos-vendedor-email-quantidade/<str:email>/<int:quantidade>/<str:status>/', viewsets.ContratosVendedorEmailQuantidadeViewSet.as_view({'get': 'list'}), name='contratos-vendedor-email-quantidade'),
  path('contratos-comprador-email-quantidade/<str:email>/<int:quantidade>/<str:status>/', viewsets.ContratosCompradorEmailQuantidadeViewSet.as_view({'get':'list'}), name='contratos-comprador-email-quantidade'),
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
