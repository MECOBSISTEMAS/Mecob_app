from rest_framework import viewsets, pagination
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from django.core import paginator
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