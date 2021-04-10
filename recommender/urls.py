from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('like_post', views.like_post , name = "like_post"),
    path('unlike_post', views.unlike_post , name = "unlike_post")
]