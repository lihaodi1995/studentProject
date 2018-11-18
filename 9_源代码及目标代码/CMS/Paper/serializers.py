from rest_framework import serializers
from Paper.models import *

class PaperSerializer(serializers.ModelSerializer):
	class Meta:
		model = Paper
		fields = '__all__'