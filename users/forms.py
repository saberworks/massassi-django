from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OurUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.save()
        return user
