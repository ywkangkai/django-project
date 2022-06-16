import json
import time
import os
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render #用于返回html页面 重定向
from django.db.models import Q, Count #组合查询
from utils import common
from rest_framework.views import APIView
from django.views import View
from datetime import datetime
from rest_framework.generics import GenericAPIView
from .models import Projects
from envs.models import Envs
from testcases.serializers import TestCaseSerializer
from envs.serializers import EnvSerializer
from testsuites.models import Testsuits
from interfaces.models import Interfaces
from testcases.models import Testcases
from rest_framework.response import Response #需要结合APIview使用
from .serializers import ProjectsSerializer
from django_filters.rest_framework import DjangoFilterBackend  #pip install django_filters
from rest_framework.filters import OrderingFilter #指定排序引擎
from debugtalks.models import DebugTalks

class ProjectView(GenericAPIView):
    queryset = Projects.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
    serializer_class = ProjectsSerializer  # 需要指定serializer_class，当前接口中需要使用到的序列化器类
    filter_backends = [DjangoFilterBackend]  # DRF框架中的过滤引擎，有它才能对下面字段进行过滤
    filterset_fields = ['projectname']  # 可根据这些字段进行过滤，任意添加模型类中的字段
    ordering_fields = ['projectname', 'leader', 'id']


    def get(self, request):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            response_list = serializer_obj.data
            data_list = []
            for item in response_list:
                project_id = item.get('id')
                interface_configure_qs = Interfaces.objects.values('id').annotate(configures=Count('configures')).filter(project_id=project_id)
                configures_count = 0
                for one_dict in interface_configure_qs:
                    configures_count += one_dict.get('configures')
                testsuites_count = Testsuits.objects.filter(project_id=project_id).count()

                interface_testcase_qs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).filter(project_id=project_id)
                testcases_count = 0
                for one_dict in interface_testcase_qs:
                    testcases_count += one_dict.get('testcases')

                item['configures'] = configures_count
                item['testsuits'] = testsuites_count
                item['testcases'] = testcases_count
                data_list.append(item)
            return self.get_paginated_response(data_list)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)

    def post(self, request):
        serializer_obj = self.serializer_class(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        obj = Projects.objects.create(**serializer_obj.validated_data)
        DebugTalks.objects.create(project=obj)
        return Response({'code': 0, 'message': 'success'}, status=200)

    def put(self, request, pk):
        obj = Projects.objects.get(id=pk)
        serializer_obj = self.serializer_class(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        data = serializer_obj.validated_data
        obj.projectname = data.get('projectname') or obj.projectname
        obj.leader = data.get('leader') or obj.leader
        obj.test = data.get('test') or obj.test
        obj.appname = data.get('appname') or obj.appname
        obj.save()

        serializer_data = ProjectsSerializer(instance=self.get_queryset(), many=True)
        return Response({"code": 0, "results": serializer_data.data})

    def delete(self, request, pk):
        obj = Projects.objects.get(id=pk)
        obj.delete()
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            response_list = serializer_obj.data
            data_list = []
            for item in response_list:
                project_id = item.get('id')
                interface_configure_qs = Interfaces.objects.values('id').annotate(
                    configures=Count('configures')).filter(project_id=project_id)
                configures_count = 0
                for one_dict in interface_configure_qs:
                    configures_count += one_dict.get('configures')
                testsuites_count = Testsuits.objects.filter(project_id=project_id).count()

                interface_testcase_qs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).filter(
                    project_id=project_id)
                testcases_count = 0
                for one_dict in interface_testcase_qs:
                    testcases_count += one_dict.get('testcases')

                item['configures'] = configures_count
                item['testsuits'] = testsuites_count
                item['testcases'] = testcases_count
                data_list.append(item)
            return self.get_paginated_response(data_list)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)





class ProjectDetail(GenericAPIView):
    queryset = Projects.objects.all()

    def post(self, request):
        projectname = (request.data)['projectname']
        if projectname == '':
            allData = Projects.objects.all()
            serializer_obj = ProjectsSerializer(instance=allData, many=True)
            return Response({"code": 0, "results": serializer_obj.data})
        else:
            Data = Projects.objects.filter(projectname__icontains=projectname)
            serializer_obj = ProjectsSerializer(instance=Data, many=True)
        return Response({"code": 0, "results": serializer_obj.data})





class putProject(View):

    def put(self, request, pk):
        qs = Projects.objects.all()
        obj = Projects.objects.get(id=pk)
        data = request.body
        data = json.loads(data)
        if data['projectname'] == '':
            return Response({'code': 1, "msg":'参数有误'})
        obj.projectname = data.get('projectname') or obj.projectname
        obj.leader = data.get('leader') or obj.leader
        obj.test = data.get('test') or obj.test
        obj.appname = data.get('appname') or obj.appname
        obj.save()
        serializer_obj = ProjectsSerializer(instance=qs, many=True)
        return JsonResponse({"code": 0, "results": serializer_obj.data})



class deleteALL(GenericAPIView):

    def post(self, request):
        idLists = (request.data)['idlist']
        for id in idLists:
            Projects.objects.get(id=id).delete()
        allData = Projects.objects.all()
        serializer_obj = ProjectsSerializer(instance=allData, many=True)
        return JsonResponse({"code": 0, "results": serializer_obj.data})


class EnvView(GenericAPIView):

    def get(self, request):
        queryset = Envs.objects.all()
        serializer_obj = EnvSerializer(instance=queryset, many=True)
        return Response(serializer_obj.data)

class Run(GenericAPIView):

    def post(self, request):
        pid = request.data['pid']
        env_id = request.data['env_id']
        env = Envs.objects.filter(id=env_id).first()
        project_obj = Projects.objects.get(id=pid)
        project_name = project_obj.projectname
        testcase_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/httprunner'
        interface_qs = Interfaces.objects.filter(project=project_obj)
        if len(interface_qs) == 0:
            time.sleep(2)
            data = {
                'code': 1,
                'message': '该项目下未添加接口无法执行'
            }
            return Response(data, status=200)

        run_testcase_list = []
        for interface in interface_qs:
            testcase_qs = Testcases.objects.filter(interface=interface)
            if len(testcase_qs) != 0:
                run_testcase_list.extend(testcase_qs)

        if len(run_testcase_list) == 0:
            time.sleep(2)
            data = {
                'code': 1,
                'message': '该项目下未添加测试用例无法执行'
            }
            return Response(data, status=200)
        file_time = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')

        run_testcase_path = ''
        for testcase_instance in run_testcase_list:
            serializer_instance = TestCaseSerializer(instance=testcase_instance)
            serializer_instance = serializer_instance.data
            run_testcase_path = common.generate_project_file(serializer_instance, env, testcase_dir_path, file_time)

        result = common.run_interface(project_name, run_testcase_path)
        return result

