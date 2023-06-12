from rest_framework import serializers
from ..existing_models import (
  Pessoas, 
  ContratoParcelas, 
  Contratos,
  Eventos,
)

class PessoasModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoas
        fields = '__all__'
  
  
class ContratoParcelasModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoParcelas
        fields = ['id','dt_vencimento', 'dt_credito', 'vl_parcela']
        #fields = '__all__'
  
class ContratosModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contratos
        fields = ['id','descricao', 'dt_contrato', 'vl_contrato','nu_parcelas', 'status', 'suspenso', 'vendedor', 'comprador', 'eventos']
        #fields = '__all__'

class EventosModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = ['nome']
        #fields = '__all__'