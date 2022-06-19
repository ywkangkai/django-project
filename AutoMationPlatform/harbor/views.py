import json
from rest_framework.generics import GenericAPIView
from .models import Harbor
from projects.models import Projects
from rest_framework.response import Response #需要结合APIview使用
from .serializers import HarborSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter #指定排序引擎

class HarborView(GenericAPIView):
    queryset = Harbor.objects.all()
    serializer_class = HarborSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    ordering_fields = ['name', 'id']

    def post(self, request):
        id = request.data['id']
        harbors = Harbor.objects.filter(repository_id=id)
        serializer_obj = HarborSerializer(instance=harbors, many=True)
        return Response(serializer_obj.data)














