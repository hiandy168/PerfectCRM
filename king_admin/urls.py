from django.conf.urls import url
from king_admin import views

urlpatterns = [
    url(r'^$', views.index, name='table_index'),
    url(r'^/(\w+)/(\w+)/$', views.display_table_objs, name='table_objs'),
    ]