import json
import os
import yaml
import os
from datetime import datetime
from httprunner.api import HttpRunner
from rest_framework.response import Response
from debugtalks.models import DebugTalks
from configs.models import Configures
from testcases.models import Testcases
from reports.models import Reports
from httprunner.report import render_html_report

def create_report(runner, report_dir, report_name=None):
    """
    创建测试报告
    :param runner:
    :param report_name:
    :return:
    """
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime

    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        # 对时间戳进行处理
        try:
            time_stamp = int(item['time']['start_at'])
            item['time']['start_at'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

        try:
            for record in item['records']:
                # 对时间戳进行处理
                try:
                    time_stamp = int(record['meta_data']['request']['start_timestamp'])
                    record['meta_data']['request']['start_timestamp'] = \
                        datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    pass

                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    summary = json.dumps(runner.summary, ensure_ascii=False)
    #print(summary)
    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')


    try:
        with open(report_dir, encoding='utf-8') as stream:
            reports = stream.read()
    except:
        raise RuntimeError('文件读取失败')


    test_report = {
        'name': report_name,
        'result': runner.summary['success'],
        'success': runner.summary['stat']['testcases']['success'],
        'failed': runner.summary['stat']['testcases']['fail'],
        'count': runner.summary['stat']['testcases']['total'],
        'html': reports,
        'summary': summary
    }
    #print(test_report)
    report_obj = Reports.objects.create(**test_report)

    return report_obj.id



def generate_testcase_file(instance, env, testcase_dir_path):
    testcase_list = []
    config = {
        'config': {
            'name': instance['name'],
            'base_url': env.base_url if env else '',
            'request': {},
        }
    }
    testcase_list.append(config)

    instance_request = json.loads(instance['request'])

    # 获取include信息
    include = json.loads(instance['include'])
    # 获取request字段
    # request = instance_request['test']['request']
    request = instance_request
    # 获取用例所属接口名称
    interface_name = instance['interface']['name']
    # 获取用例所属项目名称
    project_name = instance['interface']['project']

    testcase_run_path = testcase_dir_path + '/' + project_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')

    if not os.path.exists(testcase_run_path):
        os.makedirs(testcase_run_path)
        # 生成debugtalk.py文件，放到项目根目录下
        debugtalk_obj = DebugTalks.objects.filter(project__projectname=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj else ''
        with open(os.path.join(testcase_run_path, 'debugtalk.py'), 'w', encoding='utf-8') as f:
            f.write(debugtalk)

    testcase_dir_path = testcase_run_path + '/' + interface_name
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # {"config":1,"testcases":[1,2,3]}
    # if 'config' in include:
    #     config_id = include['config']
    #     config_obj = Configures.objects.filter(id=config_id).first()
    #
    #     if config_obj:
    #         config_request = json.loads(config_obj.request, encoding='utf-8')
    #         print('3333333333333333')
    #         print(config_request)
    #         print(type(config_request))
    #         request = config_request['config']['request']
    #         #config_request['config']['request']['base_url'] = env.base_url if env else ''
    #         testcase_list[0]['config']['request'] = request
    #         print(testcase_list)
    #         with open('kk.yaml', 'w', encoding='utf-8') as f:
    #             yaml.dump(testcase_list, f, allow_unicode=True)


    # 处理前置用例
    if 'testcases' in include:
        for testcase_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                continue
            testcase_list.append(testcase_request)

    # 把当前需要执行的用例追加到testcase_list最后
    testcase_list.append(request)


    with open(os.path.join(testcase_dir_path, instance['name'] + '.yaml'), 'w', encoding='utf-8') as f:
        yaml.dump(testcase_list, f, allow_unicode=True)

    result = run_testcase(instance, testcase_run_path)

    return result


def generate_interface_file(instance, env, testcase_dir_path, file_time):
    testcase_list = []
    config = {
        'config': {
            'name': instance['name'],
            'base_url': env.base_url if env else '',
            'request': {},
        }
    }
    testcase_list.append(config)

    instance_request = json.loads(instance['request'])

    # 获取include信息
    include = json.loads(instance['include'])
    # 获取request字段
    # request = instance_request['test']['request']
    request = instance_request
    # 获取用例所属接口名称
    interface_name = instance['interface']['name']
    # 获取用例所属项目名称
    project_name = instance['interface']['project']

    testcase_run_path = testcase_dir_path + '/' + project_name + '_' + file_time

    if not os.path.exists(testcase_run_path):
        os.makedirs(testcase_run_path)
        # 生成debugtalk.py文件，放到项目根目录下
        debugtalk_obj = DebugTalks.objects.filter(project__projectname=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj else ''
        with open(os.path.join(testcase_run_path, 'debugtalk.py'), 'w', encoding='utf-8') as f:
            f.write(debugtalk)

    testcase_dir_path = testcase_run_path + '/' + interface_name
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    if 'testcases' in include:
        for testcase_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                continue
            testcase_list.append(testcase_request)

    # 把当前需要执行的用例追加到testcase_list最后
    testcase_list.append(request)

    full_path = os.path.join(testcase_dir_path, interface_name + '.yaml')

    with open(full_path, 'a', encoding='utf-8') as f:
        yaml.dump(testcase_list, f, allow_unicode=True)

    return full_path



def generate_project_file(instance, env, testcase_dir_path, file_time):


    instance_request = json.loads(instance['request'])

    # 获取include信息
    include = json.loads(instance['include'])
    # 获取request字段
    # request = instance_request['test']['request']
    request = instance_request
    # 获取用例所属接口名称
    interface_name = instance['interface']['name']
    # 获取用例所属项目名称
    project_name = instance['interface']['project']

    testcase_list = []
    config = {
        'config': {
            'name': project_name,
            'base_url': env.base_url if env else '',
            'request': {},
        }
    }
    testcase_list.append(config)

    testcase_run_path = testcase_dir_path + '/' + project_name + '_' + file_time

    if not os.path.exists(testcase_run_path):
        os.makedirs(testcase_run_path)
        # 生成debugtalk.py文件，放到项目根目录下
        debugtalk_obj = DebugTalks.objects.filter(project__projectname=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj else ''
        with open(os.path.join(testcase_run_path, 'debugtalk.py'), 'w', encoding='utf-8') as f:
            f.write(debugtalk)

    testcase_dir_path = testcase_run_path + '/' + project_name
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    if 'testcases' in include:
        for testcase_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                continue
            testcase_list.append(testcase_request)

    # 把当前需要执行的用例追加到testcase_list最后
    testcase_list.append(request)

    run_path = os.path.join(testcase_dir_path, project_name + '.yaml')

    with open(run_path, 'a', encoding='utf-8') as f:
        yaml.dump(testcase_list, f, allow_unicode=True)

    return testcase_run_path


def run_testcase(instance, testcase_dir_path):
    # 1、运行用例
    report_paths = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/testing_report'
    report_name = instance['name'] + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_dir = report_paths + '/' + report_name + '.html'
    runner = HttpRunner(report_dir=report_paths, report_file=f'{report_name}.html')
    try:

        runner.run(testcase_dir_path)
    except Exception as e:
        res = {'ret': False, 'message': '用例执行失败'}
        return Response(res, status=400)

    # 2、创建报告
    report_id = create_report(runner, report_dir, instance['name'])

    # 3、用例运行成功之后，需要把生成的报告id返回
    data = {
        'id': report_id
    }
    return Response(data, status=201)


def run_interface(instance, testcase_dir_path):
    # 1、运行用例
    report_paths = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/testing_report'
    report_name = instance + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_dir = report_paths + '/' + report_name + '.html'
    runner = HttpRunner(report_dir=report_paths, report_file=f'{report_name}.html')
    try:

        runner.run(testcase_dir_path)
    except Exception as e:
        res = {'ret': False, 'message': '用例执行失败'}
        return Response(res, status=400)

    # 2、创建报告
    report_id = create_report(runner, report_dir, instance)

    # 3、用例运行成功之后，需要把生成的报告id返回
    data = {
        'id': report_id
    }
    return Response(data, status=201)


