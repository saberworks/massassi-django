from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>', views.OurPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# TODO TODO TODO
# implement password change form...

# below provided by django
# TODO: link to and/or implement each
# path('login/', views.LoginView.as_view(), name='login'),
# path('logout/', views.LogoutView.as_view(), name='logout'),
#
# path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
# path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
#
