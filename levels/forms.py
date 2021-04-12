from django import forms
from django.forms import ModelForm

from .models import LevelComment, LevelRating

class CommentForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = LevelComment
        fields = ['comment']

class RatingForm(ModelForm):
    required_css_class = 'required'
    possible_choices = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.possible_choices = list(map(lambda i: (i, i), range(1, 11)))
        self.possible_choices.insert(0, ('', ''))

        self.fields['rating'] = forms.ChoiceField(choices=self.possible_choices)

    class Meta:
        model = LevelRating
        fields = ['rating']

class SearchForm(forms.Form):
    required_css_class = 'required'

    terms = forms.CharField(
        label="Search For",
        strip=True,
        help_text="enter keywords to search for",
        required=True,
    )
