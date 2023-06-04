from rest_framework import viewsets
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
    queryset = Pessoas.objects.all()[0:100]
 
class PessoasViewSets(viewsets.ViewSet):
    def list(self, request):
        queryset = Pessoas.objects.all()[0:100]
        queryset_serialized = PessoasModelSerializer(queryset, many=True)
        return Response(queryset_serialized.data)
    
    def retrieve(self, request, pk):
        queryset = Pessoas.objects.get(pk=pk)
        queryset_serialized = PessoasModelSerializer(queryset)
        return Response(queryset_serialized.data)

class ContratosVendedorViewSets(viewsets.ViewSet):
    def list(self, request):
        contratos = Contratos.objects.filter(
            vendedor=Pessoas.objects.get(email=request.user.username)
        )
        queryset_serialized = {
            'contratos': ContratosModelSerializer(contratos, many=True).data
        }
        return Response(queryset_serialized)
    
    def retrieve(self, request, pk):
        queryset = Contratos.objects.get(pk=pk)
        queryset_serialized = ContratosModelSerializer(queryset)
        return Response(queryset_serialized.data)

class ContratoParcelasModelViewSet(viewsets.ModelViewSet):
    serializer_class = ContratoParcelasModelSerializer
    queryset = ContratoParcelas.objects.all()
 
class ContratosModelViewSet(viewsets.ModelViewSet):
    serializer_class = ContratosModelSerializer
    queryset = Contratos.objects.all()
 
class EventosModelViewSet(viewsets.ModelViewSet):	
    serializer_class = EventosModelSerializer
    queryset = Eventos.objects.all()