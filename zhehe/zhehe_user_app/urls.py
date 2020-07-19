from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^home/', views.home),
    re_path(r'^contact/', views.contact, name='contact'),
    re_path(r'^download/(?P<note>.+)/', views.download, name='download'),
    re_path(r'new/', views.new_doc, name='new_doc')
]