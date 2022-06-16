import json
import os
import time
from datetime import datetime
from utils import common
from AutoMationPlatform import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from utils import handel_data
from projects.models import Projects
from rest_framework.generics import GenericAPIView
from interfaces.models import Interfaces
from configs.models import Configures
from .models import Testcases
from rest_framework.response import Response  # 需要结合APIview使用
from .serializers import TestCaseSerializer, EnvSerializer
from envs.models import Envs
# pip install django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter  # 指定排序引擎


class TestcaseView(GenericAPIView):
    queryset = Testcases.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
    # 需要指定serializer_class，当前接口中需要使用到的序列化器类
    serializer_class = TestCaseSerializer
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
        iid = serializer_obj.validated_data.pop('interface').get('iid')
        serializer_obj.validated_data['interface_id'] = iid
        try:
            Testcases.objects.create(**serializer_obj.validated_data)
            return Response({"code": 1, "message": "success"}, status=200)
        except:
            return Response({serializer_obj.errors}, status=400)

    def put(self, request):
        id = request.data['id']
        data = request.data['datas']
        obj = Testcases.objects.get(id=id)
        serializer_obj = TestCaseSerializer(data=data)
        serializer_obj.is_valid(raise_exception=True)
        # interface_obj= serializer_obj.validated_data.pop('interface')
        # interface_id = interface_obj['iid']
        data = serializer_obj.validated_data
        obj.author = data.get('author') or obj.author
        obj.name = data.get('name') or obj.name
        obj.request = data.get('request') or obj.request
        obj.include = data.get('include') or obj.include
        obj.interface_id = data.get('interface_id') or obj.interface_id
        try:
            obj.save()
            return Response({"code": 0, "message":'success'})
        except:
            return Response(serializer_obj.errors)

    def delete(self, request, pk):
        obj = Testcases.objects.get(id=pk)
        obj.delete()
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)




class testcaseDetail(GenericAPIView):
    queryset = Interfaces.objects.all()

    def post(self, request):
        name = (request.data)['name']
        if name == '':
            allData = Testcases.objects.all()
            serializer_obj = TestCaseSerializer(instance=allData, many=True)
            return Response({"code": 0, "results": serializer_obj.data})
        else:
            Data = Testcases.objects.filter(name__icontains=name)
            serializer_obj = TestCaseSerializer(instance=Data, many=True)
        return Response({"code": 0, "results": serializer_obj.data})


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

class configuresName(APIView):

    def post(self, request):
        id = request.data['id']
        obj = Configures.objects.filter(interface_id=id).values('name', 'id')
        data = {"data": []}
        for name in obj:
            data['data'].append(name)
        return Response(data)

class testcaseName(APIView):

    def post(self, request):
        id = request.data['id']
        obj = Testcases.objects.filter(interface_id=id).values('name', 'id')
        data = {"data": []}
        for name in obj:
            data['data'].append(name)
        return Response(data)


class deleteALL(GenericAPIView):

    def post(self, request):
        idLists = (request.data)['idlist']
        for id in idLists:
            Testcases.objects.get(id=id).delete()
        allData = Testcases.objects.all()
        serializer_obj = TestCaseSerializer(instance=allData, many=True)
        return JsonResponse({"code": 0, "results": serializer_obj.data})

class get_detail_testcase(GenericAPIView):

    def get(self, request, pk):
        obj = Testcases.objects.get(id=pk)
        serializer_obj = TestCaseSerializer(instance=obj)
        data = {}
        data['author'] = serializer_obj['author'].value
        data['testcase_name'] = serializer_obj['name'].value
        projectname = serializer_obj['interface']['project'].value
        pid = Projects.objects.filter(projectname=projectname).values('id')[0]['id']
        data['selected_project_id'] = pid

        interfacename = serializer_obj['interface']['name'].value
        iid = Interfaces.objects.filter(name=interfacename).values('id')[0]['id']
        data['selected_interface_id'] = iid

        datas = json.loads(serializer_obj.data['include'])
        cid = datas['config']
        data['selected_configure_id'] = cid

        selected_testcase_ids = datas.get('testcases')
        selected_testcase_list = []
        for obj in selected_testcase_ids:
            selected = Testcases.objects.filter(id=obj).values('id', 'name')
            if len(selected) != 0:
                selected_testcase_list.append(selected[0])
        data['selected_testcase_id'] = selected_testcase_list

        unselected_testcase_ids = datas.get('untestcases')
        unselected_testcase_list = []
        for obj in unselected_testcase_ids:
            unselected = Testcases.objects.filter(id=obj).values('id', 'name')
            if len(unselected) != 0:
                unselected_testcase_list.append(unselected[0])
        data['unselected_testcase_id'] = unselected_testcase_list

        request_obj = json.loads(serializer_obj.data['request'])

        data['method'] = request_obj['test']['request']['method']
        data['url'] = request_obj['test']['request']['url']

        param = request_obj['test']['request'].get('param')
        data['param'] = handel_data.handel_header_params(param)

        header = request_obj['test']['request'].get('headers')
        data['header'] = handel_data.handel_header_params(header)

        from_data = request_obj['test']['request'].get('data')
        data['variable'] = handel_data.handle_from_data(from_data)

        jsonVariable = json.dumps(request_obj['test']['request'].get('json'), ensure_ascii=False)
        data['jsonVariable'] = jsonVariable

        extract = request_obj['test'].get('extract')
        data['extract'] = handel_data.handle_extract(extract)

        validate = request_obj['test'].get('validate')
        data['validate'] = handel_data.handle_validate(validate)

        globalVar = request_obj['test'].get('variables')
        data['globalVar'] = handel_data.handle_globalVar_parameterized(globalVar)

        parameterized = request_obj['test'].get('parameters')
        data['parameterized'] = handel_data.handle_globalVar_parameterized(parameterized)

        setupHooks = request_obj['test'].get('setup_hooks')
        data['setupHooks'] =handel_data.handle_setup_teardown(setupHooks)

        teardownHooks= request_obj['test'].get('teardown_hooks')
        data['teardownHooks'] = handel_data.handle_setup_teardown(teardownHooks)

        return Response(data)



class EnvView(GenericAPIView):

    def get(self, request):
        queryset = Envs.objects.all()
        serializer_obj = EnvSerializer(instance=queryset, many=True)
        return Response(serializer_obj.data)

class Run(GenericAPIView):

    def post(self, request):
        data = request.data
        obj = Testcases.objects.get(id=data['iid'])
        serializer_obj = TestCaseSerializer(instance=obj)
        instance = serializer_obj.data
        env_id = data['env_id']
        testcase_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/httprunner'
        #testcase_dir_path = path + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')
        #os.mkdir(testcase_dir_path)
        env = Envs.objects.filter(id=env_id).first()
        # 生成yaml用例文件并运行测试用例
        try:
            time.sleep(2)
            result = common.generate_testcase_file(instance, env, testcase_dir_path)
            return result
        except:
            return Response({'code': '1', 'message': '用例运行失败'}, status=400)
        # 运行用例（生成报告）
        #result = common.run_testcase(instance, testcase_dir_path)

