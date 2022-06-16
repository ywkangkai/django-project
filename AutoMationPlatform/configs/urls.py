from django.urls import path, re_path

from configs import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('save/', views.ConfigView.as_view()),
    path('detail/', views.ConfigDetail.as_view()),
    path('list/', views.ConfigView.as_view()),
    path('delete/<int:pk>/', views.ConfigView.as_view()),
    path('update/<int:pk>/', views.ConfigView.as_view()),
    path('project/name/', views.ProjectName.as_view()),
    path('interface/name/', views.InterfaceName.as_view()),
    path('deleteall/', views.deleteALL.as_view()),
    path('detail/<int:pk>/', views.getDetail.as_view()),
]
