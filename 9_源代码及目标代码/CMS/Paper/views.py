from django.shortcuts import render
from rest_framework import viewsets, response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from Paper.models import *
from Paper.serializers import *
# Create your views here.

class PaperViewSet(viewsets.ModelViewSet):
	queryset = Paper.objects.all()
	serializer_class = PaperSerializer

	@action(methods=['GET'],detail=False)	
	def paper(self, request):
		'''
		with open('file_name.txt') as f:
        	c = f.read()
    	return HttpResponse(c)
		'''
		def file_iterator(file_name, chunk_size=512):
			with open(file_name) as f:
				while True:
					c = f.read(chunk_size)
					if c:
						yield c
					else:
						break
		try:
			rootpath = "C:/Apache2/paper/"
			url = request.path
			tmp = url.split("paper/")
			url+=tmp[2]
		except:
			return Response(a, status = status.HTTP_400_BAD_REQUEST)
		if url is not None:
			response = StreamingHttpResponse(file_iterator(url))
			response['Content-Type'] = 'application/octet-stream'
			response['Content-Disposition'] = 'attachment;filename="{0}"'.format(url)
			return response
		a = collections.OrderedDict({"errorInfo":"服务器出错，请稍后重试。"})
		return Response(a, status = status.HTTP_400_BAD_REQUEST)
		