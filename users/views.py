from pprint import pprint

import django
import logging

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import OurUserCreationForm, OurLoginForm

logger = logging.getLogger(__name__)

@login_required
def index(request):
    context = {'user': request.user}
    pprint(dir(context))
    return render(request, 'users/profile.html', context)

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

    if request.method == 'POST':
        form = OurUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            django.contrib.auth.login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:profile')
    else:
        form = OurUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def password_reset(request):
    return HttpResponse("OK");
