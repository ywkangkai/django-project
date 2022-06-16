import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render  # 用于返回html页面 重定向
from django.db.models import Q, Count  # 组合查询
from rest_framework.views import APIView
from django.views import View
from projects.models import Projects
from rest_framework.generics import GenericAPIView
from .models import Testsuits
from interfaces.models import Interfaces
from rest_framework.response import Response  # 需要结合APIview使用
from .serializers import TestsuitesSerializer, EditTestsuiteSerializer, EditTestsuitWithNoNameSerializer, TestsuitesDetailSerializer
# pip install django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter  # 指定排序引擎


class TestsuiteView(GenericAPIView):
    queryset = Testsuits.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
    # 需要指定serializer_class，当前接口中需要使用到的序列化器类
    serializer_class = TestsuitesSerializer
    filter_backends = [DjangoFilterBackend]  # DRF框架中的过滤引擎，有它才能对下面字段进行过滤
    filterset_fields = ['name']  # 可根据这些字段进行过滤，任意添加模型类中的字段
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

    def post(self, request):
        data = request.data
        serializer_obj = self.serializer_class(data=data)
        serializer_obj.is_valid(raise_exception=True)
        project = serializer_obj.validated_data.pop('project_id')
        serializer_obj.validated_data['project'] = project
        try:
            Testsuits.objects.create(**serializer_obj.validated_data)
            #serializer_obj.validated_data.pop('project') #project是个对象在反序列化时即json.loads会报错所以要踢出
            return Response({"code": 1, "message": "success"}, status=200)
        except:
            return Response({"code": 1, "message": "faild"}, status=200)

    def put(self, request, pk):

        obj = Testsuits.objects.get(id=pk)
        if obj.name == (request.data)['name']:
            serializer_obj = EditTestsuitWithNoNameSerializer(data=request.data)
        else:
            serializer_obj = EditTestsuiteSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        data = serializer_obj.validated_data
        project = data.pop('project_id')
        data['project'] = project
        obj.name = data.get('name') or obj.name
        obj.include = data.get('include') or obj.include
        obj.project = data.get('project') or obj.project
        obj.save()
        return Response({"code": 0, "message": '修改成功'})

    def delete(self, request, pk):
        obj = Testsuits.objects.get(id=pk)
        obj.delete()
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)




class InterfaceName(APIView):

    def post(self, request):
        id = request.data['id']
        obj = Interfaces.objects.filter(project_id=id).values('name', 'id')
        data = {"data": []}
        for name in obj:
            data['data'].append(name)
        return Response(data)



class testsuiteDetail(GenericAPIView):
    queryset = Testsuits.objects.all()

    def post(self, request):
        name = (request.data)['name']
        if name == '':
            allData = Testsuits.objects.all()
            serializer_obj = TestsuitesSerializer(instance=allData, many=True)
            return Response({"code": 0, "results": serializer_obj.data})
        else:
            Data = Testsuits.objects.filter(name__icontains=name)
            serializer_obj = TestsuitesSerializer(instance=Data, many=True)
        return Response({"code": 0, "results": serializer_obj.data})


class ProjectName(APIView):

    def get(self, request):
        obj = Projects.objects.all().values('projectname', 'id')
        data = {"data": []}
        for name in obj:
            data['data'].append(name)
        return Response(data)


class get_detail_testsuite(APIView):

    def get(self, request, pk):
        obj = Testsuits.objects.get(id=pk)
        serializer_obj = TestsuitesDetailSerializer(instance=obj)
        name = serializer_obj.data['name']
        project_id = serializer_obj.data['project_id']
        includes = json.loads(serializer_obj.data['include'])
        include = eval(includes['include'])
        include_list = []
        for id in include:
            obj = Interfaces.objects.filter(id=id).values('id', 'name')
            if len(obj) != 0:
                include_list.append(obj[0])
        uninclude = eval(includes['uninclude'])
        uninclude_list = []
        for id in uninclude:
            obj = Interfaces.objects.filter(id=id).values('id', 'name')
            if len(obj) != 0:
                uninclude_list.append(obj[0])
        data = {
            'name': name,
            'project_id': project_id,
            'include': include_list,
            'uninclude': uninclude_list
        }
        print(data)
        return Response(data)



class deleteALL(GenericAPIView):

    def post(self, request):
        idLists = (request.data)['idlist']
        for id in idLists:
            Testsuits.objects.get(id=id).delete()
        allData = Testsuits.objects.all()
        serializer_obj = TestsuitesSerializer(instance=allData, many=True)
        return JsonResponse({"code": 0, "results": serializer_obj.data})
