from django.urls import path

from . import views

app_name = 'holiday'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:year>/', views.YearView.as_view(), name='year'),
]
