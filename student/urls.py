from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^$', views.index, name='stu_index'),
    ]