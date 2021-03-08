from django.urls import path

from . import views

app_name = 'sotd'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:sotd_id>/', views.sotd, name='sotd'),
]

