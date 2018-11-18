from django.shortcuts import render
from rest_framework import viewsets, response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from Admin.models import *
from Admin.serializers import *
from Institution.models import Institution
# Create your views here.

class AdminViewSet(viewsets.ModelViewSet):
	queryset = Admin.objects.all()
	serializer_class = AdminSerializer

	@action(methods = ['POST'],detail = False)
	def checkinstitution(self,request):
		id=request.data.get("institution_id")
		status=request.data.get("status")
		thisinstitution=Institution.objects.get(id=id)
		thisinstitution.status=status

	def retrive(self,request,pk=None):
		thisinstitution=Institution.objects.get(id=pk)
		template = loader.get_template('conference.html')
		context = {
		    'institution': thisinstitution,
		}
		return HttpResponse(template.render(context, request))
		#NEED MODIFY
