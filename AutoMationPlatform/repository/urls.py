from django.urls import path, re_path

from repository import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('add/', views.RepositorytView.as_view()),
    path('list/', views.RepositorytView.as_view()),
    path('update/', views.RepositorytView.as_view()),
    path('delete/<int:pk>/', views.RepositorytView.as_view()),
    path('detail/', views.getDeatil.as_view()),
    path('deleteall/', views.deleteALL.as_view()),
    # path('project/name', views.ProjectName.as_view()),
    path('search/', views.searchRepository.as_view()),
    path('git/', views.Git.as_view()),
    path('compile/', views.Compile.as_view()),
    path('tianjia/', views.add.as_view()),
    path('after/', views.buildAftet.as_view()),

]
