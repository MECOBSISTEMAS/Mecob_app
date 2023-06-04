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
		fields = '__all__'
  
class ContratosModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contratos
		fields = '__all__'

class EventosModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Eventos
		fields = '__all__'