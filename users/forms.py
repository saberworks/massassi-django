from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class OurUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, **kwargs):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.save()
        return user

class OurLoginForm(AuthenticationForm):
    required_css_class = 'required'

class OurPasswordResetForm(PasswordResetForm):
    required_css_class = 'required'

class OurPasswordChangeForm(PasswordChangeForm):
    required_css_class = 'required'

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        # They're all fakking required, stupid stock forms suck
        for field in self.fields:
            self.fields[field].required = True
