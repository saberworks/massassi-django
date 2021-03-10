from pprint import pprint

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import OurUserCreationForm


@login_required
def index(request):
    context = {'user': request.user}
    pprint(dir(context))
    return render(request, 'users/profile.html', context)

def register(request):
    # logged-in user can't re-register
    if request.user.is_authenticated:
        raise PermissionDenied("You're already registered.")

    if request.method == 'POST':
        form = OurUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            login(request, user)
            messages.success(request, 'Registration successful!.')
            return redirect('users:profile')
    else:
        form = OurUserCreationForm()

    return render(request, 'users/register.html', {'form': form})
