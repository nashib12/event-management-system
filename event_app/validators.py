import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
    
def password_validate(password): 
    pattern = r"[!@#$%^&*(),.?\":{}|<>]"
    if not re.search(pattern, password):
        raise ValidationError(_("Password must contain at least one special character."))