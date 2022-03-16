from django.forms import ModelForm

from saberworks.models import File

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = [
            'project', 'title', 'name', 'version', 'description',
            'file', 'image', 'user'
        ]

class FileEditForm(ModelForm):
    class Meta:
        model = File
        fields = ['title', 'version', 'description', 'image']

class FileSetImageForm(ModelForm):
    class Meta:
        model = File
        fields = ['image']

class FileSetFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']

class StageFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['project', 'title', 'version', 'description', 'user']
