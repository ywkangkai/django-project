import json
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.shortcuts import render  # 用于返回html页面 重定向
from django.db.models import Q, Count  # 组合查询
from rest_framework.views import APIView
from projects.models import Projects
from interfaces.models import Interfaces
from testcases.models import Testcases
from testsuites.models import Testsuits
from configs.models import Configures
from envs.models import Envs
from debugtalks.models import DebugTalks
from reports.models import Reports



class SummaryAPIView(APIView):

    def get(self, request):
        user = request.user
        user_info = {
            'username': user.username,
            'role': '管理员' if user.is_superuser else '普通用户',
        }

        projects_count = Projects.objects.count()
        interfaces_count = Interfaces.objects.count()
        testcases_count = Testcases.objects.count()
        testsuits_count = Testsuits.objects.count()
        configures_count = Configures.objects.count()
        envs_count = Envs.objects.count()
        debug_talks_count = DebugTalks.objects.count()
        reports_count = Reports.objects.count()

        statistics = {
            'projects_count': projects_count,
            'interfaces_count': interfaces_count,
            'testcases_count': testcases_count,
            'testsuits_count': testsuits_count,
            'configures_count': configures_count,
            'envs_count': envs_count,
            'debug_talks_count': debug_talks_count,
            'reports_count': reports_count,
            # 'success_rate': success_rate,
            # 'fail_rate': fail_rate,
        }

        return Response(data={
            'user': user_info,
            'statistics': statistics
        })