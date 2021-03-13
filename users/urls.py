from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]

# below provided by django
# TODO: link to and/or implement each
# path('login/', views.LoginView.as_view(), name='login'),
# path('logout/', views.LogoutView.as_view(), name='logout'),
#
# path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
# path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
#
# path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
# path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
# path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
# path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
