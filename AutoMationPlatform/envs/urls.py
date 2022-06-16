from django.urls import path, re_path

from envs import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('add/', views.EnvsView.as_view()),
    path('list/', views.EnvsView.as_view()),
    path('detail/', views.EnvDetail.as_view()),
    path('edit/<int:pk>/', views.EnvsView.as_view()),
    path('delete/<int:pk>/', views.EnvsView.as_view()),
    path('deleteall/', views.deleteALL.as_view()),

]
