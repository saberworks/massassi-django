from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),

    path('register/', views.register, name='register'),

    ###
    ## Password change (for logged-in users)
    #

    # Show password change form
    path('password_change/', views.OurPasswordChangeView.as_view(), name='password_change'),

    # Show password change confirmation page
    path('password_change_done/', views.OurPasswordChangeDoneView.as_view(), name='password_change_done'),

    ###
    ## Password RESET ("forgot password")
    #

    # Show the password reset email address form ("forgot password")
    path('password_reset/', views.OurPasswordResetView.as_view(), name='password_reset'),

    # Show confirmation page that password reset email was sent
    path('password_reset_sent/', views.OurPasswordResetDoneView.as_view(), name='password_reset_sent'),

    # Show the password reset form that asks for new password once the reset email link is clicked
    path('password_reset_confirm/<slug:uidb64>/<slug:token>', views.OurPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    # Show confirmation page that password was actually reset
    path('password_reset_complete/', views.OurPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

