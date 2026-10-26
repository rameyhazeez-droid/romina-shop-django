

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_home, name="blogHome"),
    path('blog_home/', views.blog_home, name='blogHome'),
    path('blog_detail/', views.blog_detail, name='blogDetail'),

]