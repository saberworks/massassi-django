from django.urls import path

from . import views

app_name = 'levels'

urlpatterns = [
    path('', views.CategoryIndexView.as_view(), name='index'),
    path('<slug>/', views.CategoryDetailView.as_view(), name='category'),
]
