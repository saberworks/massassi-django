from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('oldnews/', views.DetailView.as_view(), name='old'),
]
