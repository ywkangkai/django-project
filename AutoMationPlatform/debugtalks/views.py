import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render #用于返回html页面 重定向
from django.db.models import Q, Count #组合查询
from rest_framework.views import APIView
from django.views import View
from rest_framework.generics import GenericAPIView
from .models import DebugTalks
from rest_framework.response import Response #需要结合APIview使用
from .serializers import DebugtalkSerializer
from projects.models import Projects
from interfaces.models import Interfaces
from django_filters.rest_framework import DjangoFilterBackend  #pip install django_filters
from rest_framework.filters import OrderingFilter #指定排序引擎
from debugtalks.models import DebugTalks

class DebugtalkView(GenericAPIView):
    queryset = DebugTalks.objects.all()
    serializer_class = DebugtalkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'project__projectname']
    ordering_fields = ['name', 'id']


    def get(self, request):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)

    def put(self, request):
        pk = request.data['id']
        obj = DebugTalks.objects.get(id=pk)
        serializer_obj = self.serializer_class(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        data = serializer_obj.validated_data
        obj.debugtalk = data.get('debugtalk') or obj.debugtalk
        obj.save()
        return Response({"code": 0, "message": 'success'})


class DebugTalkDetail(GenericAPIView):
    queryset = DebugTalks.objects.all()

    def post(self, request):
        name = (request.data)['name']
        if name == '':
            allData = DebugTalks.objects.all()
            serializer_obj = DebugtalkSerializer(instance=allData, many=True)
            return Response({"code": 0, "results": serializer_obj.data})
        else:
            # data = Projects.objects.filter(projectname__icontains=name)
            # print(data)
            # for i in data:

            #bubuglist = data.debugtalks
            Data = DebugTalks.objects.filter(project__projectname__icontains=name)
            print(Data)
            serializer_obj = DebugtalkSerializer(instance=Data, many=True)
        return Response({"code": 0, "results": serializer_obj.data})


class DebugTalkEdit(APIView):

    def get(self, request, pk):
        content = DebugTalks.objects.get(id=pk)
        serializer_obj = DebugtalkSerializer(instance=content)
        return Response(serializer_obj.data, status=200)


class ProjectName(APIView):

    def get(self, request):
        obj = Projects.objects.all().values('projectname', 'id')
        data = {"data": []}
        for name in obj:
            data['data'].append(name)
        return Response(data)

class InterfaceName(APIView):

    def post(self, request):
        id = request.data['id']
        obj = Interfaces.objects.filter(project_id=id).values('name', 'id')
        print(obj)
        data = {"data": []}
        for name in obj:
            data['data'].append(name)
        return Response(data)


