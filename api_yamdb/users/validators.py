import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(f'Недопустимое имя - {value}')
    if re.search(r'^[\w.@+-]+\Z', value) is None:
        raise ValidationError(
            'Не допустимые символы',
            params={'value': value},
        )
