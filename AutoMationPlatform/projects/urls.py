from django.urls import path, re_path

from projects import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('add/', views.ProjectView.as_view()),
    path('list/', views.ProjectView.as_view()),
    path('detail/', views.ProjectDetail.as_view()),
    path('edit/<int:pk>/', views.ProjectView.as_view()),
    path('delete/<int:pk>/', views.ProjectView.as_view()),
    path('deleteall/', views.deleteALL.as_view()),
    path('get/env/', views.EnvView.as_view()),
    path('run/', views.Run.as_view()),

]
