import django
import logging

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .forms import OurUserCreationForm, OurLoginForm, OurPasswordResetForm, OurPasswordChangeForm

logger = logging.getLogger(__name__)


@login_required
def index(request):
    return render(request, 'users/profile.html', {'user': request.user})


def login(request):
    # logged-in user can't re-login
    if request.user.is_authenticated:
        return redirect('users:profile')

    form = OurLoginForm()

    if request.method == 'POST':
        form = OurLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is None:
                form.add_error(None, form.get_invalid_login_error())
                form.add_error(None, "Unable to log you in :(")
            else:
                form.confirm_login_allowed(user)
                django.contrib.auth.login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('users:profile')

    return render(request, 'users/login.html', {'form': form})


def logout(request):
    if request.user.is_authenticated:
        django.contrib.auth.logout(request)

    return redirect('home')


def register(request):
    # logged-in user can't re-register
    if request.user.is_authenticated:
        raise PermissionDenied("You're already registered.")

    form = OurUserCreationForm()

    if request.method == 'POST':
        form = OurUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            django.contrib.auth.login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:profile')

    return render(request, 'users/register.html', {'form': form})


def password_reset(request):
    if request.user.is_authenticated:
        messages.info(request, "Please use the change password form.")
        return redirect('users:profile')

    form = OurPasswordResetForm()

    if request.method == 'POST':
        form = OurPasswordResetForm(request.POST)

        if form.is_valid():
            result = form.save(request=request, email_template_name='users/password_reset_email.html')
            messages.success(request, 'If the address you entered has an associated account, password reset instructions have been sent.')
            return redirect('home')

    return render(request, 'users/password_reset.html', {'form': form})


def password_reset_confirm(request, **kwargs):
    form = SetPasswordForm()
    form.required_css_class = 'required'

    return render(request, 'users/password_reset_confirm.html', {'form': form})


@login_required
def password_change_done(request):
    messages.success(request, 'Password changed successfully.')
    return redirect('users:profile')


#
# Class-based views follow
#

class OurPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_complete')


@method_decorator(login_required, name='dispatch')
class OurPasswordChangeView(PasswordChangeView):
    form_class = OurPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
