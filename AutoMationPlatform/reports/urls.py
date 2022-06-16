from django.urls import path, re_path

from reports import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('add/', views.ReportsView.as_view()),
    path('list/', views.ReportsView.as_view()),
    path('download/<int:pk>/', views.DownLoad.as_view()),
    path('delete/<int:pk>/', views.ReportsView.as_view()),
    path('view/<int:pk>/', views.Reportdetail.as_view()),
    path('deleteall/', views.deleteALL.as_view()),
    path('open/', views.openReport.as_view()),



]
