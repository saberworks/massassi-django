from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, \
    PasswordChangeDoneView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('password_change/', views.OurPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', views.password_change_done, name='password_change_done'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>', views.OurPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# TODO TODO TODO
# implement password change form...
# and email address form?

# below provided by django
# TODO: link to and/or implement each
# path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
# path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
#
