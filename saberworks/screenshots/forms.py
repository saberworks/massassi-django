from django.forms import ModelForm

from saberworks.models import Screenshot

class AddScreenshotForm(ModelForm):
    class Meta:
        model = Screenshot
        fields = ['image', 'project', 'user']
