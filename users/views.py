import django
import logging

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordChangeDoneView, PasswordResetCompleteView
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

    redirect_to = request.GET.get('next')

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

                if redirect_to:
                    return redirect(redirect_to)
                else:
                    return redirect('users:profile')

    return render(request, 'users/login.html', {'form': form, 'redirect_to': redirect_to})


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


###
## Password change (logged-in user)
#

@method_decorator(login_required, name='dispatch')
class OurPasswordChangeView(PasswordChangeView):
    form_class = OurPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'


@method_decorator(login_required, name='dispatch')
class OurPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'


###
## Password reset ("forgot password")
#

# Show reset form that asks for email address
class OurPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    form_class = OurPasswordResetForm
    success_url = reverse_lazy('users:password_reset_sent')
    template_name = 'users/password_reset.html'


# Show confirmation that email with reset instructions was sent
class OurPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_sent.html'

# Once user clicks emailed reset link, this view shows the set-password form
class OurPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_complete')
    template_name = 'users/password_reset_confirm.html'

# Finally, after user set a new password, show a confirmation page
class OurPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
