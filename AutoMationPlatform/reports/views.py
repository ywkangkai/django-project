import json
import os
from utils import dowmload
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response  # 需要结合APIview使用
from .serializers import ReportsModelSerializer
from .models import Reports
# pip install django_filters
from django.http.response import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter  # 指定排序引擎


class ReportsView(GenericAPIView):

    queryset = Reports.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
    # 需要指定serializer_class，当前接口中需要使用到的序列化器类
    serializer_class = ReportsModelSerializer
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
        try:
            Reports.objects.create(**serializer_obj.validated_data)
            return Response({'code': 0, 'message': 'success'})
        except:
            return Response(serializer_obj.errors)

    def delete(self, request, pk):
        obj = Reports.objects.filter(id=pk).first()
        obj.delete()
        serializer_obj = ReportsModelSerializer(instance=self.get_queryset(), many=True)
        return Response({"code": 0, "results": serializer_obj.data})



class Reportdetail(GenericAPIView):

    def get(self, request, pk):
        obj = Reports.objects.get(id=pk)
        serializer_obj = ReportsModelSerializer(instance=obj)
        return Response(serializer_obj.data)

class DownLoad(GenericAPIView):

    def post(self, request, pk):
        obj = Reports.objects.get(id=pk)
        serializer_obj = ReportsModelSerializer(instance=obj)
        print(serializer_obj.data)
        report_name = serializer_obj.data['name']
        report_html = serializer_obj.data['html']
        report_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/download_report'
        file_path = report_dir+'/'+report_name+'.html'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_html)
        response = StreamingHttpResponse(dowmload.get_file_content(file_path))
        html_file_name = escape_uri_path(report_name + '.html')
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachement; filename*=UTF-8''{html_file_name}"
        return response

class deleteALL(GenericAPIView):

    def post(self, request):
        idLists = (request.data)['idlist']
        print(idLists)
        for id in idLists:
            Reports.objects.get(id=id).delete()
        allData = Reports.objects.all()
        serializer_obj = ReportsModelSerializer(instance=allData, many=True)
        return Response({"code": 0, "results": serializer_obj.data})


class openReport(GenericAPIView):

    def post(self, request):
        id = request.data['id']
        obj = Reports.objects.get(id=id)
        serializer_obj = ReportsModelSerializer(instance=obj)
        name = serializer_obj.data['name']
        html = serializer_obj.data['html']
        data = {
            'html': html
        }
        return Response(data, status=200)