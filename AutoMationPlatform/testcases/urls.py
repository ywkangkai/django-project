from django.urls import path, re_path

from testcases import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('add/', views.TestcaseView.as_view()),
    path('list/', views.TestcaseView.as_view()),
    path('update/', views.TestcaseView.as_view()),
    path('delete/<int:pk>/', views.TestcaseView.as_view()),
    path('detail/', views.testcaseDetail.as_view()),
    path('deleteall/', views.deleteALL.as_view()),
    path('project/name/', views.ProjectName.as_view()),
    path('interface/name/', views.InterfaceName.as_view()),
    path('configure/name/', views.configuresName.as_view()),
    path('name/', views.testcaseName.as_view()),
    path('get/detail/<int:pk>/', views.get_detail_testcase.as_view()),
    path('get/env/', views.EnvView.as_view()),
    path('run/', views.Run.as_view()),

]
