from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('news_archive.html', views.OldNewsView.as_view(), name='oldnews'),
    path('news_search.html', views.SearchView.as_view(), name='oldsearch'),
    path('news_archive_<int:year>.html', views.YearView.as_view(), name='oldyear'),
    path('news_archive_<int:year>-<int:month>.html', views.MonthView.as_view(), name='oldmonth'),
]
