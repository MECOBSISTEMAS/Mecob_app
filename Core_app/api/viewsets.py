from rest_framework import viewsets, pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from rest_framework.decorators import api_view, action
from dj_rest_auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core import paginator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db import connection
import locale

from datetime import datetime, date, timedelta
from django.db import models
from .serializers import (
    PessoasModelSerializer,
    ContratoParcelasModelSerializer,
    ContratosModelSerializer,
    EventosModelSerializer,
    ContratosAllModelSerializer,
    ContratoParcelasAllModelSerializer,
)

from ..existing_models import (
    Pessoas,
    ContratoParcelas,
    Contratos,
    Eventos,
)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#* retorne mensagem SIM caso o usuario esteja autenticado e NÂO caso dê qualquer falha
class CustomLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()
        if original_response.status_code == 200:
            original_response.data['is_authenticated'] = True
        else:
            original_response.data['is_authenticated'] = False
        #retorne o username que foi usado para logar
        original_response.data['username'] = self.request.data['username']
        try:
            original_response.data['nome'] = PessoasModelSerializer(Pessoas.objects.get(email=self.request.data['username'])).data['nome']
        except Pessoas.DoesNotExist:
            original_response.data['nome'] = 'Nenhuma pessoa encontrada com esse email'
        except Exception as e:
            original_response.data['nome'] = e
        return original_response

@api_view(['POST'])
def execute_query_sql(request):
    try:
        body = request.data.get('body', {})
        sql = body.get('sql', '')

        with connection.cursor() as cursor:
            cursor.execute(sql)
            queryset = cursor.fetchall()
            return Response(queryset)
    except Exception as e:
        return Response({'error': str(e)})

class ContratosAllContratoParcelasAllViewSet(viewsets.ViewSet):
    """ essa função tem por objetivo retornar todos os contratos e suas respectivas parcelas serializadas"""
    def list(self, request):
        message:str = "Passe o id do contrato na url"
        return Response(message)

    """ essa função tem por objetivo retornar o contrato com base no id e retornar todos os campos do contrato e suas respectivas parcelas serializadas"""
    def retrieve(self, request, contrato_id):
        contrato_queryset = Contratos.objects.get(id=contrato_id)
        contrato_serialized = ContratosAllModelSerializer(contrato_queryset, many=False).data
        parcelas_queryset = ContratoParcelas.objects.filter(
            contratos=contrato_id)
        contrato_serialized['parcelas'] = ContratoParcelasAllModelSerializer(parcelas_queryset, many=True).data
        return Response(contrato_serialized)
class ExecuteQuerySqlViewSet(viewsets.ViewSet):
    @action(methods=['post'], detail=False)
    def execute_query_sql(self, request):
        try:
            body = request.data
            sql = body.get('sql', '')

            with connection.cursor() as cursor:
                cursor.execute(sql)
                queryset = cursor.fetchall()
                return Response(queryset)
        except Exception as e:
            return Response({'error': str(e)})

class ResetarSenhaViewSet(viewsets.ViewSet):
    """ essa função tem por objetivo resetar a senha do usuario,
     passando o argumento email e senha na url  """
    def list(self, request, email, password):
        try:
            user = User.objects.get(username=email)
            user.set_password(password)
            user.save()
            return Response({'success': 'Senha resetada com sucesso'})
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'})
        except Exception as e:
            return Response({'error': e})
    def retrive(self, request):
        return Response({'error': 'Método não permitido, forneça o email da pessoa e o password no endpoint'})



class PessoasModelViewSet(viewsets.ModelViewSet):
    #como mudar de pagina
    serializer_class = PessoasModelSerializer
    queryset = Pessoas.objects.all()
    pagination_class = pagination.PageNumberPagination


#aplique a autenticação obrigatoria aqui

class ContratosVendedorViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    contratos: Contratos.objects.none()
    def list(self, request):
        self.contratos = Contratos.objects.filter(
            vendedor=Pessoas.objects.get(email=request.user.username),
            status='confirmado'
        )
        queryset_serialized = {
            'contratos': ContratosModelSerializer(self.contratos, many=True).data
        }
        return Response(queryset_serialized)

    def retrieve(self, request, pk):
        queryset = self.contratos.get(pk=pk)
        queryset_serialized = ContratosModelSerializer(queryset)
        return Response(queryset_serialized.data)
    

class ContratosVendedorEmailQuantidadeViewSet(viewsets.ViewSet):
    """ esse endpoint ira servir todos os contratos da pessoa assim que passar o email e assim tambem a quantidade
     de contratos que ele ira solicatar pela url utilizar a paginação """
    def list(self, request, email:str, quantidade:int, status:str):
        contratos_queryset = Contratos.objects.filter(
            vendedor=Pessoas.objects.get(email=email),
            status=status
        ).order_by('-dt_contrato')[:quantidade]
        contratos_serialized = ContratosModelSerializer(contratos_queryset, many=True).data
        for contrato in contratos_serialized:
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            contrato['vendedor'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['vendedor'])).data
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.count()
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.filter(id=contrato['eventos']).first(), many=False).data
            for parcela in contrato['parcelas']:
                parcela['dt_vencimento'] = datetime.strptime(parcela['dt_vencimento'], '%Y-%m-%d').strftime('%d/%m/%Y')
                parcela['id'] = parcela['nu_parcela']
        return Response({"results":contratos_serialized})
    

class ContratosCompradorEmailQuantidadeViewSet(viewsets.ViewSet):
    def list(self, request, email:str, quantidade:int, status:str):
        contratos_queryset = Contratos.objects.filter(
            comprador=Pessoas.objects.get(email=email),
            status=status
        ).order_by('-dt_contrato')[:quantidade]
        contratos_serialized = ContratosModelSerializer(contratos_queryset, many=True).data
        for contrato in contratos_serialized:
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            contrato['vendedor'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['vendedor'])).data
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.count()
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.filter(id=contrato['eventos']).first(), many=False).data
            for parcela in contrato['parcelas']:
                parcela['dt_vencimento'] = datetime.strptime(parcela['dt_vencimento'], '%Y-%m-%d').strftime('%d/%m/%Y')
                parcela['id'] = parcela['nu_parcela']
        return Response({"results":contratos_serialized})
    
class ContratosVendedorEmailViewSet(viewsets.ViewSet):
    contratos = Contratos.objects.none()

    def list(self, request, email):
        contratos_queryset = Contratos.objects.filter(
            vendedor=Pessoas.objects.get(email=email),
            status='confirmado'
        ).order_by('-dt_contrato')
        
        contratos_serialized = ContratosModelSerializer(contratos_queryset, many=True).data

        for contrato in contratos_serialized:
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data 
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.filter(id=contrato['eventos']), many=True).data

        queryset_serialized = {
            'contratos': contratos_serialized
        }
        return Response(queryset_serialized)

class ContratosCompradorEmailViewSet(viewsets.ViewSet):
    def list(self, request, email):
        contratos_queryset = Contratos.objects.filter(
            comprador=Pessoas.objects.get(email=email),
            status='confirmado'
        )
        contratos_serialized = ContratosModelSerializer(contratos_queryset, many=True).data
        
        
        for contrato in contratos_serialized:
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.filter(id=contrato['eventos']), many=True).data
            
        queryset_serialized = {
            'contratos': contratos_serialized
        }
            
        return Response(queryset_serialized)
    
class ContratosCompradorViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    contratos: Contratos.objects.none()
    def list(self, request):
        self.contratos = Contratos.objects.filter(
            comprador=Pessoas.objects.get(email=request.user.username),
            status='confirmado'
        )
        queryset_serialized = {
            'contratos': ContratosModelSerializer(self.contratos, many=True).data
        }
        return Response(queryset_serialized)
    
    def retrive(self, request, pk):
        queryset = self.contratos.get(pk=pk)
        queryset_serialized = ContratosModelSerializer(queryset)
        return Response(queryset_serialized.data)
    
class ContratosEmailStatusViewSet(viewsets.ViewSet):
    def list(self, request, email:str, status:str):
        queryset_contratos = Contratos.objects.filter(
            vendedor=Pessoas.objects.get(email=email),
               status=status
        )
        queryset_contratos_serialized = ContratosModelSerializer(queryset_contratos, many=True).data
        for contrato in queryset_contratos_serialized:
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.filter(vl_pagto=0).count()
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
                
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.get(id=contrato['eventos']), many=False).data
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data 
            
        return Response(queryset_contratos_serialized)
    
class ContratosParcelasVendedorEmailStatusModelViewSet(viewsets.ModelViewSet):
    queryset = Contratos.objects.all().order_by('-id').exclude(status='excluido')
    serializer_class = ContratosModelSerializer
    pagination_class = PageNumberPagination
    filterset_fields = ['vendedor', 'status']  # Campos para filtragem
    
    def get_queryset(self):
        email = self.kwargs.get('email')
        status = self.kwargs.get('status')
        
        queryset = super().get_queryset().filter(
            vendedor=Pessoas.objects.get(email=email),
            status=status
        ).order_by('-dt_contrato')
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        queryset_contratos_serialized = response.data['results']
        
        for contrato in queryset_contratos_serialized:
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            #faça com que o campo dt_vencimento seja exposta da seguinte forma: dd/mm/yyyyy
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.count()
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            contrato['vendedor'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['vendedor'])).data
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
                
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.get(id=contrato['eventos']), many=False).data
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data 
            for parcela in contrato['parcelas']:
                parcela['dt_vencimento'] = datetime.strptime(parcela['dt_vencimento'], '%Y-%m-%d').strftime('%d/%m/%Y')
                parcela['id'] = parcela['nu_parcela']
            
        response.data['results'] = queryset_contratos_serialized
        return response
        
class ContratosParcelasCompradorEmailStatusModelViewSet(viewsets.ModelViewSet):
    queryset = Contratos.objects.all().order_by('-id').exclude(status='excluido')
    serializer_class = ContratosModelSerializer
    pagination_class = PageNumberPagination
    filterset_fields = ['comprador', 'status']  # Campos para filtragem
    
    def get_queryset(self):
        email = self.kwargs.get('email')
        status = self.kwargs.get('status')
        
        queryset = super().get_queryset().filter(
            comprador=Pessoas.objects.get(email=email),
            status=status
        ).order_by('-dt_contrato')
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        queryset_contratos_serialized = response.data['results']
        
        for contrato in queryset_contratos_serialized:
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.count()
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            contrato['vendedor'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['vendedor'])).data
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_pagto__isnull=True).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
                
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.get(id=contrato['eventos']), many=False).data
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data 
            for parcela in contrato['parcelas']:
                parcela['dt_vencimento'] = datetime.strptime(parcela['dt_vencimento'], '%Y-%m-%d').strftime('%d/%m/%Y')
                parcela['id'] = parcela['nu_parcela']
            
        response.data['results'] = queryset_contratos_serialized
        return response

class ContratosVendedorEmailStatusViewSet(viewsets.ViewSet):
    def list(self, request, email:str, status:str):
        queryset_contratos = Contratos.objects.filter(
            vendedor=Pessoas.objects.get(email=email),
               status=status
        ).order_by('-id').exclude(status='excluido')
        queryset_contratos_serialized = ContratosModelSerializer(queryset_contratos, many=True).data
        for contrato in queryset_contratos_serialized:
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.count()
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            """ if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'A vencer' """
            if parcelas_queryset.filter(Q(dt_vencimento__lt=datetime.now().date()) & (Q(dt_pagto__isnull=True))).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(Q(dt_vencimento__gte=datetime.now().date()) & Q(dt_pagto__isnull=True)).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
                
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.get(id=contrato['eventos']), many=False).data
            #contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data 
            
        return Response(queryset_contratos_serialized)
    
class ContratosCompradorEmailStatusViewSet(viewsets.ViewSet):
    def list(self, request, email:str, status:str):
        queryset_contratos = Contratos.objects.filter(
            comprador=Pessoas.objects.get(email=email),
               status=status
        ).order_by('-id').exclude(status='excluido')
        queryset_contratos_serialized = ContratosModelSerializer(queryset_contratos, many=True).data
        for contrato in queryset_contratos_serialized:
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.count()
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            """ if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'Em atraso' """
            """ para saber se o contrato esta em atraso precisa seguir os seguintes criterios:
              """
            if parcelas_queryset.filter(Q(dt_vencimento__lt=datetime.now().date()) & (Q(dt_pagto__isnull=True))).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(Q(dt_vencimento__gte=datetime.now().date()) & Q(dt_pagto__isnull=True)).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
                
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.get(id=contrato['eventos']), many=False).data
            #contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data 
            
        return Response(queryset_contratos_serialized)

    
class DashBoardViewSet(viewsets.ViewSet):
    def list(self, request, email):
        #! Quantidade de todos os contratos da pessoa
        try:
            pessoa = Pessoas.objects.get(email=email)
        except Pessoas.DoesNotExist:
            return Response({'error': 'Pessoa não encontrada'})
        contratos_vendedor_queryset = Contratos.objects.filter(
            vendedor=pessoa,
        ).exclude(status='excluido')
        
        contratos_comprador_queryset = Contratos.objects.filter(
            comprador=pessoa
        ).exclude(status='excluido')
        
        queryset = {
            "cliente": pessoa.nome,
            "id": pessoa.id,
            "quantidade_de_contratos": contratos_vendedor_queryset.count() or 0,
            "total_dos_contratos": contratos_vendedor_queryset.aggregate(models.Sum('vl_contrato'))['vl_contrato__sum'] or 0,
            "vendas_confirmadas": {
                "quantidade" :contratos_vendedor_queryset.filter(status='confirmado').count() or 0,
                "total": contratos_vendedor_queryset.filter(status='confirmado').aggregate(models.Sum('vl_contrato'))['vl_contrato__sum'] or 0,
            },
            "vendas_em_acao_judicial": {
                "quantidade": contratos_vendedor_queryset.filter(status='acao_judicial').count() or 0,
                "total": contratos_vendedor_queryset.filter(status='acao_judicial').aggregate(models.Sum('vl_contrato'))['vl_contrato__sum'] or 0,
            },
            "recuperacao_de_credito": {
                "quantidade": contratos_vendedor_queryset.filter(status='pendente').count() or 0,
                "total": contratos_vendedor_queryset.filter(status='pendente').aggregate(models.Sum('vl_contrato'))['vl_contrato__sum'] or 0,
            },
            "compras_confirmadas": {
                "quantidade": contratos_comprador_queryset.filter(status='confirmado').count() or 0,
                "total": contratos_comprador_queryset.filter(status='confirmado').aggregate(models.Sum('vl_contrato'))['vl_contrato__sum'] or 0,
            },
        }

        queryset["total_dos_contratos_em_real"] = locale.currency(queryset['total_dos_contratos'], grouping=True, symbol=None)
        queryset["vendas_confirmadas"]["total_em_real"] = locale.currency(queryset['vendas_confirmadas']['total'], grouping=True, symbol=None)
        queryset["vendas_em_acao_judicial"]["total_em_real"] = locale.currency(queryset['vendas_em_acao_judicial']['total'], grouping=True, symbol=None)
        queryset["recuperacao_de_credito"]["total_em_real"] = locale.currency(queryset['recuperacao_de_credito']['total'], grouping=True, symbol=None)
        queryset["compras_confirmadas"]["total_em_real"] = locale.currency(queryset['compras_confirmadas']['total'], grouping=True, symbol=None)
        
        queryset['total_vendas_credito_confirmadas_judicial'] = queryset['vendas_confirmadas']['total'] + queryset['vendas_em_acao_judicial']['total'] + queryset['recuperacao_de_credito']['total']
        queryset['quantidade_total_vendas_credito_confirmadas_judiciais'] = queryset['vendas_confirmadas']['quantidade'] + queryset['vendas_em_acao_judicial']['quantidade'] + queryset['recuperacao_de_credito']['quantidade']
        #formatando em real
        queryset["total_vendas_credito_confirmadas_judicial_em_real"] = locale.currency(queryset['total_vendas_credito_confirmadas_judicial'], grouping=True, symbol=None)

        return Response(queryset)

class RegistroUsuarioViewSet(viewsets.ViewSet):
    def list(self, request, email, password):
        try:
            pessoa = Pessoas.objects.get(email=email)
            if User.objects.filter(username=email).exists():
                return Response({'error': 'Usuário já existe'})
            else:
                User.objects.create_user(username=email, password=password).save()
                return Response({'success': 'Usuário criado com sucesso'})
        except Pessoas.DoesNotExist:
            return Response({'error': 'Não há nenuma pessoa com o email no banco de dados'})
        except Exception as e:
            return Response({'error': e})
    def retrive(self, request):
        return Response({'error': 'Método não permitido, forneça o email da pessoa no endpoint'})
            

class ConsultaJuridicoViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    contratos: Contratos.objects.none()
    def list(self, request):
        self.contratos = Contratos.objects.filter(
            vendedor=Pessoas.objects.get(email=request.user.username),
            status='acao_judicial'
        )
        queryset_serialized = {
            'contratos': ContratosModelSerializer(self.contratos, many=True).data
        }
        return Response(queryset_serialized)
    def retrive(self, request, pk):
        queryset = self.contratos.get(pk=pk)
        queryset_serialized = ContratosModelSerializer(queryset)
        return Response(queryset_serialized.data)
    
class RecuperacaoCreditoViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    contratos: Contratos.objects.none()
    def list(self, request):
        self.contratos = Contratos.objects.filter(
            vendedor=Pessoas.objects.get(email=request.user.username),
            status='pendente'
        )
        queryset_serialized = {
            'contratos': ContratosModelSerializer(self.contratos, many=True).data
        }
        return Response(queryset_serialized)
    def retrive(self, request, pk):
        queryset = self.contratos.get(pk=pk)
        queryset_serialized = ContratosModelSerializer(queryset)
        return Response(queryset_serialized.data)

class ContratoParcelasModelViewSet(viewsets.ModelViewSet):
    serializer_class = ContratoParcelasModelSerializer
    queryset = ContratoParcelas.objects.all()
    pagination_class = pagination.PageNumberPagination
 
class ContratosModelViewSet(viewsets.ModelViewSet):
    serializer_class = ContratosModelSerializer
    queryset = Contratos.objects.all()
    pagination_class = pagination.PageNumberPagination
 
class EventosModelViewSet(viewsets.ModelViewSet):	
    serializer_class = EventosModelSerializer
    queryset = Eventos.objects.all()
    pagination_class = pagination.PageNumberPagination