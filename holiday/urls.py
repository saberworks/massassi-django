from django.urls import path

from . import views

app_name = 'holiday'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('random/', views.RandomUrlView.as_view(), name='random'),
    path('<int:year>/', views.YearView.as_view(), name='year'),
]
