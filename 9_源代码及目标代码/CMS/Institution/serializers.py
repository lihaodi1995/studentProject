from rest_framework import serializers
from .models import Institution,Employee

class InstitutionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Institution
		fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = '__all__'