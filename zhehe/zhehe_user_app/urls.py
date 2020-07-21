from django.urls import re_path
from . import views

app_name = 'zhehe'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^home/', views.home, name='home'),
    re_path(r'^contact/', views.contact, name='contact'),
    re_path(r'^download/(?P<document>.+)/', views.download, name='download'),
    re_path(r'^edit/(?P<document>.+)/', views.edit, name='edit'),
    re_path(r'^delete/(?P<document>.+)/', views.delete, name='delete'),
    re_path(r'new/', views.new_doc, name='new_doc')
]