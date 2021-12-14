import re

from django.core import validators
from django.utils.deconstruct import deconstructible

# Old massassi had very few restrictions on usernames.  In addition, it didn't
# properly trim the beginning and end of input so some usernames have spaces in
# front and at the end.  Those users were imported into the django users table
# but with more restrictive regex, they weren't allowed to log in and I couldn't
# even change them in the admin.
#
# This validator now allows pretty much anything as username but now does
# enforce the blank space rule.  Yes, I'm aware that this means people can
# have silly usernames like '!' or "*&&*^^&%" and I'm ok with that.  They
# already do in the original massassi database.

@deconstructible
class OurUnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^(?! ).*(?<! )$'
    message = (
        'Enter a valid username. It may not start or end with whitespace.'
    )
    flags = 0
