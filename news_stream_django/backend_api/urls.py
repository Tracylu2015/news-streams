from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trending', views.trending, name='trending'),
    path('tags/<str:tag>', views.tags, name='tags')
]
