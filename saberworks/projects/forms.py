from django.forms import ModelForm

from saberworks.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['games', 'tags', 'name', 'description', 'accent_color', 'image', 'user']

class ProjectEditForm(ModelForm):
    class Meta:
        model = Project
        fields = ['games', 'tags', 'name', 'description', 'accent_color', 'image']

class ProjectSetImageForm(ModelForm):
    class Meta:
        model = Project
        fields = ['image']
