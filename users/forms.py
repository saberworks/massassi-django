from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User


class OurUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.save()
        return user

class OurLoginForm(AuthenticationForm):
    required_css_class = 'required'

class OurPasswordResetForm(PasswordResetForm):
    required_css_class = 'required'
