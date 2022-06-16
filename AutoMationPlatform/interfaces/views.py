import json
import os
import time
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render  # 用于返回html页面 重定向
from django.db.models import Q, Count  # 组合查询
from rest_framework.views import APIView
from django.views import View
from projects.models import Projects
from rest_framework.generics import GenericAPIView
from .models import Interfaces
from testcases.models import Testcases
from envs.models import Envs
from testcases.serializers import TestCaseSerializer
from utils import common
from datetime import datetime
from rest_framework.response import Response  # 需要结合APIview使用
from .serializers import InterfacesSerializer, EditInterfacesSerializer, EditInterfacesWithNoNameSerializer, EnvSerializer
# pip install django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter  # 指定排序引擎


class InterfacetView(GenericAPIView):
    queryset = Interfaces.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
    # 需要指定serializer_class，当前接口中需要使用到的序列化器类
    serializer_class = InterfacesSerializer
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
        try:
            serializer_obj.is_valid(raise_exception=True)
        except:
            dict = {"code": 1, "message": "failed", 'name': '接口已存在'}
            return Response(dict, status=200)
        project = serializer_obj.validated_data.pop('project_id')
        serializer_obj.validated_data['project'] = project
        try:
            Interfaces.objects.create(**serializer_obj.validated_data)
            #serializer_obj.validated_data.pop('project') #project是个对象在反序列化时即json.loads会报错所以要踢出
            return Response({"code": 1, "message": "success"}, status=200)
        except:
            return Response({"code": 1, "message": "faild"}, status=200)

    def put(self, request, pk):
        obj = Interfaces.objects.get(id=pk)
        if obj.name == (request.data)['name']:
            serializer_obj = EditInterfacesWithNoNameSerializer(data=request.data)
        else:
            serializer_obj = EditInterfacesSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        data = serializer_obj.validated_data
        obj.name = data.get('name') or obj.name
        obj.desc = data.get('desc') or obj.desc
        obj.tester = data.get('tester') or obj.tester
        obj.project = data.get('project') or obj.project
        obj.save()

        serializer_data = InterfacesSerializer(instance=self.get_queryset(), many=True)
        return Response({"code": 0, "results": serializer_data.data})

    def delete(self, request, pk):
        obj = Interfaces.objects.get(id=pk)
        obj.delete()
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)




class interfaceDetail(GenericAPIView):
    queryset = Interfaces.objects.all()

    def post(self, request):
        name = (request.data)['name']
        if name == '':
            allData = Interfaces.objects.all()
            serializer_obj = InterfacesSerializer(instance=allData, many=True)
            return Response({"code": 0, "results": serializer_obj.data})
        else:
            Data = Interfaces.objects.filter(name__icontains=name)
            serializer_obj = InterfacesSerializer(instance=Data, many=True)
        return Response({"code": 0, "results": serializer_obj.data})


class ProjectName(APIView):

    def get(self, request):
        obj = Projects.objects.all().values('projectname', 'id')
        data = {"data": []}
        for name in obj:
            data['data'].append(name)
        return Response(data)


class deleteALL(GenericAPIView):

    def post(self, request):
        idLists = (request.data)['idlist']
        for id in idLists:
            Interfaces.objects.get(id=id).delete()
        allData = Interfaces.objects.all()
        serializer_obj = InterfacesSerializer(instance=allData, many=True)
        return JsonResponse({"code": 0, "results": serializer_obj.data})

class EnvView(GenericAPIView):

    def get(self, request):
        queryset = Envs.objects.all()
        serializer_obj = EnvSerializer(instance=queryset, many=True)
        return Response(serializer_obj.data)


class Run(GenericAPIView):

    def post(self, request):
        data = request.data
        obj = Interfaces.objects.get(id=data['iid'])
        interface_name = obj.name
        env_id = data['env_id']
        testcase_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/httprunner'
        env = Envs.objects.filter(id=env_id).first()
        testcase_obj = Testcases.objects.filter(interface=obj)
        testcase_obj = TestCaseSerializer(instance=testcase_obj, many=True)
        testcase_obj = testcase_obj.data
        time.sleep(2)
        if len(testcase_obj) == 0:
            data = {
                'code': '1',
                'message': '当前接口不存在用例无法运行'
            }
            return Response(data, status=200)

        # 生成yaml用例文件并运行测试用例
        full_path = ''
        time.sleep(2)
        file_time = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')
        for instance in testcase_obj:
            full_path = common.generate_interface_file(instance, env, testcase_dir_path, file_time)

        # 运行用例（生成报告）
        result = common.run_interface(interface_name, full_path)

        return result


