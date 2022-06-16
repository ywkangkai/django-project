from django.urls import path, re_path

from testsuites import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('add/', views.TestsuiteView.as_view()),
    path('list/', views.TestsuiteView.as_view()),
    path('update/<int:pk>/', views.TestsuiteView.as_view()),
    path('edit/<int:pk>/', views.TestsuiteView.as_view()),
    path('delete/<int:pk>/', views.TestsuiteView.as_view()),
    path('detail/', views.testsuiteDetail.as_view()),
    path('deleteall/', views.deleteALL.as_view()),
    path('project/name/', views.ProjectName.as_view()),
    path('interface/name/', views.InterfaceName.as_view()),
    path('detail/<int:pk>/', views.get_detail_testsuite.as_view()),








]
