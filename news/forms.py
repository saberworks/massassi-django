from django import forms


class NewsSearchForm(forms.Form):
    required_css_class = 'required'

    terms = forms.CharField(
        label="Search For",
        strip=True,
        help_text="enter keywords to search for",
        required=True,
    )
