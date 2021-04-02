from django.urls import path

from . import views

app_name = 'levels'

urlpatterns = [
    path('', views.CategoryIndexView.as_view(), name='index'),
    path('<path>/', views.CategoryDetailView.as_view(), name='category'),
    path('files/<pk>.shtml', views.LevelDetailView.as_view(), name='level'),
    path('download/<pk>/', views.LevelDownloadView.as_view(), name='level_download'),
    path('comment/<int:level_id>/', views.CommentView.as_view(), name='comment'),
    path('rate/<int:level_id>/', views.RateView.as_view(), name='rate'),
    path('report_comment/<int:comment_id>/', views.ReportCommentView.as_view(), name='report_comment'),
]
