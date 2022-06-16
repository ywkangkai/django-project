from django.urls import path, re_path

from interfaces import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('add/', views.InterfacetView.as_view()),
    path('list/', views.InterfacetView.as_view()),
    path('edit/<int:pk>/', views.InterfacetView.as_view()),
    path('delete/<int:pk>/', views.InterfacetView.as_view()),
    path('detail/', views.interfaceDetail.as_view()),
    path('deleteall/', views.deleteALL.as_view()),
    path('project/name', views.ProjectName.as_view()),
    path('env/', views.EnvView.as_view()),
    path('run/', views.Run.as_view()),
]
