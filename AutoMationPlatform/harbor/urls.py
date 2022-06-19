from django.urls import path

from harbor import views



'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('list/', views.HarborView.as_view()),


]
