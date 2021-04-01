from django.forms import ModelForm

from .models import LevelComment

class CommentForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = LevelComment
        fields = ['comment']
