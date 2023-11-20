import logging
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm

from .models import HolidayLogo

logger = logging.getLogger(__name__)

class EnterForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = HolidayLogo
        fields = ['author', 'logo']

    def clean_logo(self):
        image = self.cleaned_data.get('logo', False)

        if image:
            if image.size > 1024000 * 2:
                raise ValidationError("Image file too large ( > 2MB )")

            width, height = get_image_dimensions(image)

            if height > 500:
                raise ValidationError("Image is too tall ( > 300px )")

            if width > 1000:
                raise ValidationError("Image is too wide ( > 1000px )")

            return image
        else:
            raise ValidationError("Couldn't read uploaded image")
