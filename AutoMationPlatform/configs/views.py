import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render #用于返回html页面 重定向
from django.db.models import Q, Count #组合查询
from rest_framework.views import APIView
from .models import Configures
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response #需要结合APIview使用
from .serializers import ConfigSerializer, ConfigUpdateSerializer
from projects.models import Projects
from interfaces.models import Interfaces
from django_filters.rest_framework import DjangoFilterBackend
from utils import handel_data

class ConfigView(GenericAPIView):
    queryset = Configures.objects.all()
    serializer_class = ConfigSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    ordering_fields = ['name']

    def get(self, request):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)

    def post(self, request):
        serializer_obj = self.serializer_class(data=request.data)
        try:
            serializer_obj.is_valid(raise_exception=True)
            interface_dict = serializer_obj.validated_data.pop('interface')
            serializer_obj.validated_data['interface_id'] = interface_dict['iid']   #结合interface
        except:
            data = serializer_obj.errors
            return Response(data, status=200)
        Configures.objects.create(**serializer_obj.validated_data)
        return Response({"code": 0, "message": 'success'}, status=200)

    def delete(self, request, pk):
        obj = Configures.objects.get(id=pk)
        obj.delete()
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)

    def put(self, request, pk):
        obj = Configures.objects.get(id=pk)
        if obj.name == (request.data)['name']:
            serializer_obj = ConfigUpdateSerializer(data=request.data)
        else:
            serializer_obj = ConfigSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        interface_dict = serializer_obj.validated_data.pop('interface')
        serializer_obj.validated_data['interface_id'] = interface_dict['iid']
        data = serializer_obj.validated_data
        obj.name = data.get('name') or obj.name
        obj.author = data.get('author') or obj.author
        obj.request = data.get('request') or obj.request
        obj.interface_id = data.get('interface_id') or obj.interface_id
        obj.save()
        return Response({"code": 0, "message": 'success'})


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
        data = {"data": []}
        for name in obj:
            data['data'].append(name)
        return Response(data)



class ConfigDetail(GenericAPIView):

    def post(self, request):
        name = (request.data)['name']
        if name == '':
            allData = Configures.objects.all()
            serializer_obj = ConfigSerializer(instance=allData, many=True)
            return Response({"code": 0, "results": serializer_obj.data})
        else:
            Data = Configures.objects.filter(name__icontains=name)
            serializer_obj = ConfigSerializer(instance=Data, many=True)
        return Response({"code": 0, "results": serializer_obj.data})



class deleteALL(GenericAPIView):

    def post(self, request):
        idLists = request.data['idlist']
        for id in idLists:
            Configures.objects.get(id=id).delete()
        allData = Configures.objects.all()
        serializer_obj = ConfigSerializer(instance=allData, many=True)
        return Response({"code": 0, "results": serializer_obj.data})


class getDetail(GenericAPIView):

    def get(self, request, pk):
        obj = Configures.objects.get(id=pk)
        config_request = json.loads(obj.request, encoding='utf-8')
        serializer_obj = ConfigSerializer(instance=obj)
        data = {}
        req = serializer_obj.data
        data['configure_name'] = req['name']
        data['author'] = req['author']
        pro_id = Projects.objects.filter(projectname=req['interface']['project']).values('id')[0]['id']
        int_id = Interfaces.objects.filter(name=req['interface']['name']).values('id')[0]['id']
        data['selected_project_id'] = pro_id
        data['selected_interface_id'] = int_id
        config_headers = config_request['config']['request']['headers']
        data['header'] = handel_data.handel_header_params(config_headers)
        config_globalVar = config_request['config']['variables']
        data['globalVar'] = handel_data.handle_globalVar_parameterized(config_globalVar)
        return Response(data, status=200)

