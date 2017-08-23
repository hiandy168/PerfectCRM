from django.conf.urls import url
from crm import views

urlpatterns = [
    url(r'^$', views.index, name='sales_index'),
]