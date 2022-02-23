from django.forms import ModelForm

from saberworks.models import File

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = [
            'project', 'name', 'version', 'description',
            'file', 'image', 'user'
        ]

class FileEditForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'version', 'description']

class FileSetImageForm(ModelForm):
    class Meta:
        model = File
        fields = ['image']

class FileSetFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']
