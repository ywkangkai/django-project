import json
import re
import time
import paramiko
from harbor.models import Harbor
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from .models import Repository
from gitstatus.models import GitStatus
from rest_framework.response import Response  # 需要结合APIview使用
from .serializers import RepositoryModelSerializer, RepositoryEditSerializer,GitStatusModelSerializer
# pip install django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter  # 指定排序引擎





class RepositorytView(GenericAPIView):
    queryset = Repository.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
    # 需要指定serializer_class，当前接口中需要使用到的序列化器类
    serializer_class = RepositoryModelSerializer
    filter_backends = [DjangoFilterBackend]  # DRF框架中的过滤引擎，有它才能对下面字段进行过滤
    filterset_fields = ['name']  # 可根据这些字段进行过滤，任意添加模型类中的字段
    ordering_fields = ['name', 'id']

    def get(self, request):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            for i in serializer_obj.data:
                if i['send'] == True:
                    i['send'] = '是'
                else:
                    i['send'] = '否'
                obj = GitStatus.objects.get(respository_id=i['id'])
                status_obj = GitStatusModelSerializer(instance=obj)
                status_obj = status_obj.data
                i['status'] = status_obj
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)

    def post(self, request):
        data = request.data
        serializer_obj = self.serializer_class(data=data)
        serializer_obj.is_valid(raise_exception=True)
        try:
            obj = Repository.objects.create(**serializer_obj.validated_data)
            form_data = {
                'respository_id': obj.id
            }
            GitStatus.objects.create(**form_data)
            return Response({"code": 0, "message": "success"}, status=200)
        except:
            return Response({"code": 1, "message": "faild"}, status=400)

    def put(self, request):
        id = request.data['id']
        obj = Repository.objects.get(id=id)
        if obj.name == request.data['name']:
            serializer_obj = RepositoryEditSerializer(data=request.data)
        else:
            serializer_obj = RepositoryModelSerializer(data=request.data)
        try:
            serializer_obj.is_valid(raise_exception=True)
        except:
            return Response(serializer_obj.errors)
        data = serializer_obj.validated_data
        obj.name = data.get('name') or obj.name
        obj.git = data.get('git') or obj.git
        obj.server = data.get('server') or obj.server
        obj.type = data.get('type') or obj.type
        obj.address = data.get('address') or obj.address
        obj.send = data.get('send') or obj.send
        obj.build = data.get('build') or obj.build
        obj.save()
        data = {
            'code': 0,
            'message': 'success'
        }
        return Response(data, status=200)

    def delete(self, request, pk):
        obj = Repository.objects.get(id=pk)
        obj.delete()
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.serializer_class(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.serializer_class(instance=qs, many=True)
        return Response(serializer_obj.data, status=200)


class getDeatil(GenericAPIView):

    def post(self, request):
        id = request.data['id']
        obj = Repository.objects.get(id=id)
        serializer_obj = RepositoryModelSerializer(instance=obj)
        return Response(serializer_obj.data)


class deleteALL(GenericAPIView):

    def post(self, request):
        idLists = (request.data)['idlist']
        for id in idLists:
            Repository.objects.get(id=id).delete()
        allData = Repository.objects.all()
        serializer_obj = RepositoryModelSerializer(instance=allData, many=True)
        return JsonResponse({"code": 0, "results": serializer_obj.data})


class searchRepository(GenericAPIView):
    queryset = Repository.objects.all()

    def post(self, request):
        name = request.data['name']
        if name == '':
            allData = Repository.objects.all()
            serializer_obj = RepositoryModelSerializer(instance=allData, many=True)
            return Response({"code": 0, "results": serializer_obj.data})
        else:
            Data = Repository.objects.filter(projectname__icontains=name)
            serializer_obj = RepositoryModelSerializer(instance=Data, many=True)
        return Response({"code": 0, "results": serializer_obj.data})

#第一步拉取代码到服务器
class Git(GenericAPIView):

    def post(self, request):
        id = request.data['id']
        obj = Repository.objects.get(id=id)
        server_address = obj.server
        git = obj.git
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server_address, 22, username='root', password='ywkangkai@1314', timeout=4)
            try:
                stdin, stdout, stderr = client.exec_command(f'cd /data/; mkdir myproject; cd myproject; git clone {git}', get_pty=True)
                result = stdout.read().decode()
                print(result)
                time.sleep(5)

                filename = re.findall('mkdir: cannot create directory ‘(.+?)’: File exists', result)
                if 'mkdir: cannot create directory ‘myproject’: File exists' in result:
                    data = {
                        'code': 0,
                        "message": f'文件夹{filename[0]}已存在'
                    }
                    form = {
                        'git': '已完成',
                        'git_status1': 'error',
                        'git_description': f'文件夹{filename[0]}已存在'
                    }
                    client.exec_command('cd /data; rm -rf myproject')
                    GitStatus.objects.filter(respository=obj).update(**form)
                    return Response(data)

                elif 'already exists and is not an empty directory' in result:
                    data = {
                        'code': 0,
                        "message": '代码拉去失败，请检查文件夹是否为空，或者已存在'
                    }
                    form = {
                        'git': '已完成',
                        'git_status1': 'error',
                        'git_description': '代码拉去失败，请检查文件夹是否为空，或者已存在'
                    }
                    client.exec_command('cd /data; rm -rf myproject')
                    GitStatus.objects.filter(respository=obj).update(**form)
                    return Response(data)

                elif 'Cloning into' in result:
                    data = {
                        'code': 0,
                        "message": '项目拉取完成'
                    }
                    form = {
                        'git': '已完成',
                        'git_status1': 'success',
                        'git_description': '项目拉取完成'
                    }
                    GitStatus.objects.filter(respository=obj).update(**form)
                    return Response(data)
                else:
                    data = {
                        'code': 1,
                        'message': '项目拉取失败'
                    }
                    form = {
                        'git': '已完成',
                        'git_status1': 'error',
                        'git_description': '项目拉取失败'
                    }
                    client.exec_command('cd /data; rm -rf myproject')
                    GitStatus.objects.filter(respository=obj).update(**form)
                    return Response(data)
            except:
                data = {
                    'code': 1,
                    'message': '项目拉取失败'
                }
                form = {
                    'git': '已完成',
                    'git_status1': 'error',
                    'git_description': '项目拉取失败'
                }
                client.exec_command('cd /data; rm -rf myproject')
                GitStatus.objects.filter(respository=obj).update(**form)
                return Response(data)

        except:
            data = {
                'code': 1,
                'message': '服务器链接失败'
            }
            form = {
                'git': '已完成',
                'git_status1': 'error',
                'git_description': '服务器链接失败'
            }
            client.exec_command('cd /data; rm -rf myproject')
            GitStatus.objects.filter(respository=obj).update(**form)
            return Response(data)
        finally:
            client.close()


class Compile(GenericAPIView):

    def post(self, request):
        global images
        command = ''
        id = request.data['id']
        obj = Repository.objects.get(id=id)
        server_address = obj.server
        build = obj.build
        build = json.loads(build)
        setup = build['setup']
        setup = setup.split('\n')
        for i in setup:
            if '#编写shell，一条命令占一行，以分号结尾' not in i:
                command = command + i
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server_address, 22, username='root', password='ywkangkai@1314', timeout=4)
            try:
                stdin, stdout, stderr = client.exec_command(command, get_pty=True)
                content = stdout.read().decode()
                print(content)
                if 'Successfully' in content:
                    images = re.findall('Successfully tagged (.*)?', content)
                    data = {
                        'code': 0,
                        "message": '镜像构建成功'
                    }
                    form = {
                        'build_before': '已完成',
                        'build_before_status2': 'success',
                        'build_before_description': '镜像构建成功'
                    }
                    # stdin, stdout, stderr = client.exec_command("docker images |awk 'NR==2' |awk '{print $1}'", get_pty=True)
                    # name = stdout.read().decode().strip()
                    # stdin, stdout, stderr = client.exec_command("docker images |awk 'NR==2' |awk '{print $2}'", get_pty=True)
                    # tag = stdout.read().decode().strip()
                    harbor_data = {
                        'name': images[0].replace("\r", ""),
                        'repository_id': id
                    }
                    Harbor.objects.create(**harbor_data)
                    GitStatus.objects.filter(respository=obj).update(**form)
                    return Response(data)
                elif 'unable to prepare context:' in content:
                    data = {
                        'code': 0,
                        "message": '缺少dockerfile文件'
                    }
                    form = {
                        'build_before': '已完成',
                        'build_before_status2': 'error',
                        'build_before_description': '缺少dockerfile文件'
                    }
                    client.exec_command('cd /data; rm -rf myproject')
                    GitStatus.objects.filter(respository=obj).update(**form)
                    return Response(data)
            except:
                data = {
                    'code': 1,
                    'message': '镜像构建失败'
                }
                form = {
                    'build_before': '已完成',
                    'build_before_status2': 'error',
                    'build_before_description': '镜像构建失败'
                }
                GitStatus.objects.filter(respository=obj).update(**form)
                return Response(data)

        except:
            data = {
                'code': 1,
                'message': '服务器链接失败'
            }
            form = {
                'build_before': '已完成',
                'build_before_status2': 'error',
                'build_before_description': '服务器链接失败'
            }
            GitStatus.objects.filter(respository=obj).update(**form)
            return Response(data)
        finally:
            client.close()


class buildAftet(GenericAPIView):
    def post(self, request):
        command = ''
        id = request.data['id']
        obj = Repository.objects.get(id=id)
        server_address = obj.server
        build = obj.build
        build = json.loads(build)
        setup = build['teardown']
        setup = setup.split('\n')
        for i in setup:
            if '#编写shell，一条命令占一行，以分号结尾' not in i:
                command = command + i
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server_address, 22, username='root', password='ywkangkai@1314', timeout=4)
            try:
                stdin, stdout, stderr = client.exec_command(command, get_pty=True)
                content = stdout.read().decode()
                print(content)
                data = {
                    'code': 0,
                    'message': '构建后步骤执行成功'
                }
                form = {
                    'build_after': '已完成',
                    'build_after_status4': 'success',
                    'build_after_description': '构建后步骤执行成功'
                }
                GitStatus.objects.filter(respository=obj).update(**form)
                return Response(data)
            except:
                data = {
                    'code': 1,
                    'message': '构建后步骤执行失败'
                }
                form = {
                    'build_after': '已完成',
                    'build_after_status4': 'error',
                    'build_after_description': '构建后步骤执行失败'
                }
                GitStatus.objects.filter(respository=obj).update(**form)
                return Response(data)
        except:
            data = {
                'code': 1,
                'message': '服务器链接失败'
            }
            form = {
                'build_after': '已完成',
                'build_after_status4': 'error',
                'build_after_description': '服务器链接失败'
            }
            GitStatus.objects.filter(respository=obj).update(**form)
            return Response(data)





class add(GenericAPIView):

    # def post(self, request):
    #     data = request.data
    #     obj = Repository.objects.get(id=19)
    #     GitStatus.objects.filter(respository=obj).update(**data)
    #     return Response({'code': 1})

    def get(self, request):
        obj = GitStatus.objects.get(respository_id=19)
        print(obj.git)
        return Response({'code': 1})