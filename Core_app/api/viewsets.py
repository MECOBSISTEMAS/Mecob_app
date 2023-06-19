from rest_framework import viewsets, pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from dj_rest_auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core import paginator
from datetime import datetime, date, timedelta
from django.db import models
from .serializers import (
    PessoasModelSerializer,
    ContratoParcelasModelSerializer,
    ContratosModelSerializer,
    EventosModelSerializer,
)

from ..existing_models import (
    Pessoas,
    ContratoParcelas,
    Contratos,
    Eventos,
)


#* retorne mensagem SIM caso o usuario esteja autenticado e NÂO caso dê qualquer falha
class CustomLoginView(LoginView):
    def get_response(self):
        orginal_response = super().get_response()
        if orginal_response.status_code == 200:
            orginal_response.data['is_authenticated'] = True
        else:
            orginal_response.data['is_authenticated'] = False
        #retorne o username que foi usado para logar
        orginal_response.data['username'] = self.request.data['username']
        return orginal_response

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
    
class ContratosVendedorEmailViewSet(viewsets.ViewSet):
    contratos = Contratos.objects.none()

    def list(self, request, email):
        contratos_queryset = Contratos.objects.filter(
            vendedor=Pessoas.objects.get(email=email),
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
        print(queryset_contratos.count())
        for contrato in queryset_contratos_serialized:
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.filter(vl_pagto=0).count()
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
                
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.get(id=contrato['eventos']), many=False).data
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data 
            
        return Response(queryset_contratos_serialized)
    
class ContratosParcelasVendedorEmailStatusModelViewSet(viewsets.ModelViewSet):
    queryset = Contratos.objects.all()
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
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.count()
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            contrato['vendedor'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['vendedor'])).data
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
                
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.get(id=contrato['eventos']), many=False).data
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data 
            
        response.data['results'] = queryset_contratos_serialized
        return response
        
class ContratosParcelasCompradorEmailStatusModelViewSet(viewsets.ModelViewSet):
    queryset = Contratos.objects.all()
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
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'A vencer'
            else:
                contrato['status_contrato'] = 'Liquidado'
                
            contrato['parcelas_pagas_e_em_falta'] = f'{parcelas_pagas}/{parcelas_em_falta}'
            contrato['eventos'] = EventosModelSerializer(Eventos.objects.get(id=contrato['eventos']), many=False).data
            contrato['parcelas'] = ContratoParcelasModelSerializer(parcelas_queryset, many=True).data 
            
        response.data['results'] = queryset_contratos_serialized
        return response

class ContratosVendedorEmailStatusViewSet(viewsets.ViewSet):
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
            parcelas_em_falta = parcelas_queryset.count()
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
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
        )
        queryset_contratos_serialized = ContratosModelSerializer(queryset_contratos, many=True).data
        for contrato in queryset_contratos_serialized:
            parcelas_queryset = ContratoParcelas.objects.filter(
                contratos=contrato['id'])
            parcelas_pagas = parcelas_queryset.filter(vl_pagto__gt=0).count()
            parcelas_em_falta = parcelas_queryset.count()
            contrato['comprador'] = PessoasModelSerializer(Pessoas.objects.get(id=contrato['comprador'])).data
            if parcelas_queryset.filter(dt_vencimento__lt=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
                contrato['status_contrato'] = 'Em atraso'
            elif parcelas_queryset.filter(dt_vencimento__gte=datetime.now().date(), dt_credito__isnull=True, vl_pagto=0).exists():
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
        )
        
        contratos_comprador_queryset = Contratos.objects.filter(
            comprador=pessoa
        )
        
        queryset = {
            "quantidade_de_contratos": contratos_vendedor_queryset.count(),
            "total_dos_contratos": contratos_vendedor_queryset.aggregate(models.Sum('vl_contrato'))['vl_contrato__sum'],
            "vendas_confirmadas": {
                "quantidade" :contratos_vendedor_queryset.filter(status='confirmado').count(),
                "total": contratos_vendedor_queryset.filter(status='confirmado').aggregate(models.Sum('vl_contrato'))['vl_contrato__sum'],
            },
            "vendas_em_acao_judicial": {
                "quantidade": contratos_vendedor_queryset.filter(status='acao_judicial').count(),
                "total": contratos_vendedor_queryset.filter(status='acao_judicial').aggregate(models.Sum('vl_contrato'))['vl_contrato__sum'],
            },
            "recuperacao_de_credito": {
                "quantidade": contratos_vendedor_queryset.filter(status='pendente').count(),
                "total": contratos_vendedor_queryset.filter(status='pendente').aggregate(models.Sum('vl_contrato'))['vl_contrato__sum']
                },
            "compras_confirmadas": {
                "quantidade": contratos_comprador_queryset.filter(status='confirmado').count(),
                "total": contratos_comprador_queryset.filter(status='confirmado').aggregate(models.Sum('vl_contrato'))['vl_contrato__sum']
            }
            
        }
        
        queryset['total_vendas_credito_confirmadas_judicial'] = queryset['vendas_confirmadas']['total'] + queryset['vendas_em_acao_judicial']['total'] + queryset['recuperacao_de_credito']['total'] + queryset['compras_confirmadas']['total']
        queryset['quantidade_total_vendas_credito_confirmadas_judiciais'] = queryset['vendas_confirmadas']['quantidade'] + queryset['vendas_em_acao_judicial']['quantidade'] + queryset['recuperacao_de_credito']['quantidade'] + queryset['compras_confirmadas']['quantidade']
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