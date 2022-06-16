from django.urls import path, re_path

from debugtalks import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('list/', views.DebugtalkView.as_view()),
    path('detail/', views.DebugTalkDetail.as_view()),
    path('code/<int:pk>/', views.DebugTalkEdit.as_view()),
    path('update/', views.DebugtalkView.as_view()),
]
