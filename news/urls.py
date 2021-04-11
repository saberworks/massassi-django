from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('old/', views.OldNewsView.as_view(), name='oldnews'),
    path('old/search/', views.SearchView.as_view(), name='oldsearch'),
    path('old/<int:year>/', views.YearView.as_view(), name='oldyear'),
    path('old/<int:year>/<int:month>/', views.MonthView.as_view(), name='oldmonth'),
]
