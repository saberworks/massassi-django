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

class LevelSortForm(forms.Form):
    sortby = forms.ChoiceField(
        widget=forms.Select(attrs={"style": "width: 16ch"}),
        choices=(
            ("name", "Level Name"),
            ("author", "Author"),
            ("dl_count", "Downloads"),
            ("rating", "Rating"),
    ))

    num = forms.ChoiceField(
        widget=forms.Select(attrs={"style": "width: 8ch"}),
        choices=(
        ("25", "25"),
        ("50", "50"),
        ("100", "100"),
        ("9999", "all"),
    ))
