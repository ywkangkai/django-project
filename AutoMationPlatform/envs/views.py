import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render #用于返回html页面 重定向
from django.db.models import Q, Count #组合查询
from rest_framework.views import APIView
from django.views import View
from rest_framework.generics import GenericAPIView
from .models import Envs
from rest_framework.response import Response #需要结合APIview使用
from .serializers import EnvSerializer, EidtEnvSerializerWithNoName, EidtEnvSerializer
from django_filters.rest_framework import DjangoFilterBackend  #pip install django_filters
from rest_framework.filters import OrderingFilter #指定排序引擎

class EnvsView(GenericAPIView):
    queryset = Envs.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
    serializer_class = EnvSerializer  # 需要指定serializer_class，当前接口中需要使用到的序列化器类
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
        serializer_obj = self.serializer_class(data=request.data)
        try:
            serializer_obj.is_valid(raise_exception=True)
        except:
            return  Response(serializer_obj.errors, status=200)
        Envs.objects.create(**serializer_obj.validated_data)
        return Response({'code':0, 'message':'success'}, status=200)

    def put(self, request, pk):
        obj = Envs.objects.get(id=pk)
        if obj.name == (request.data)['name']:
            serializer_obj = EidtEnvSerializerWithNoName(data=request.data)
        else:
            serializer_obj = EidtEnvSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        data = serializer_obj.validated_data
        obj.name = data.get('name') or obj.name
        obj.desc = data.get('desc') or obj.desc
        obj.base_url = data.get('base_url') or obj.base_url
        obj.save()

        serializer_data = EnvSerializer(instance=self.get_queryset(), many=True)
        return Response({"code": 0, "results": serializer_data.data})

    def delete(self, request, pk):
        obj = Envs.objects.get(id=pk)
        obj.delete()
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)




class EnvDetail(GenericAPIView):
    queryset = Envs.objects.all()

    def post(self, request):
        name = (request.data)['name']
        if name == '':
            allData = Envs.objects.all()
            serializer_obj = EnvSerializer(instance=allData, many=True)
            return Response({"code": 0, "results": serializer_obj.data})
        else:
            Data = Envs.objects.filter(name__icontains=name)
            serializer_obj = EnvSerializer(instance=Data, many=True)
        return Response({"code": 0, "results": serializer_obj.data})





# class putProject(View):
#
#     def put(self, request, pk):
#         qs = Projects.objects.all()
#         obj = Projects.objects.get(id=pk)
#         data = request.body
#         data = json.loads(data)
#         if data['projectname'] == '':
#             return Response({'code': 1, "msg":'参数有误'})
#         obj.projectname = data.get('projectname') or obj.projectname
#         obj.leader = data.get('leader') or obj.leader
#         obj.test = data.get('test') or obj.test
#         obj.appname = data.get('appname') or obj.appname
#         obj.save()
#         serializer_obj = ProjectsSerializer(instance=qs, many=True)
#         return JsonResponse({"code": 0, "results": serializer_obj.data})



class deleteALL(GenericAPIView):

    def post(self, request):
        idLists = (request.data)['idlist']
        print(idLists)
        print(type(idLists[0]))
        for id in idLists:
            Envs.objects.get(id=id).delete()
        allData = Envs.objects.all()
        serializer_obj = EnvSerializer(instance=allData, many=True)
        return JsonResponse({"code": 0, "results": serializer_obj.data})
