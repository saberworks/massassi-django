from django.urls import path

from . import views
from .models import News

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('old/', views.OldNewsView.as_view(), name='oldnews'),
    path('old/<int:year>/', views.YearView.as_view(), name='oldyear'),
    path('old/<int:year>/<int:month>/', views.MonthView.as_view(), name='oldmonth'),
]
