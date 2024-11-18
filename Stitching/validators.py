import re
from django.core.exceptions import ValidationError

def validate_mobile_number(value):
    pattern = r'^((\+92)?(0092)?(92)?(0)?)(3)([0-9]{9})$'
    if not re.match(pattern, value):
        raise ValidationError('Enter a valid Pakistani mobile number.')