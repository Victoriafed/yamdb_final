import re
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):

    year_re = re.compile(r'^[\d{4}$]')
    if not year_re.match(str(value)):
        raise ValidationError(f'{value} - не верный формат')

    year = int(value)
    if year > timezone.now().year:
        raise ValidationError(f'{value} - год не может быть больше текущего')
