import re

from django.core.exceptions import ValidationError


def username_validator(value):
    if value == 'me':
        raise ValidationError('Нельзя указать "me" в поле username!')

    wrong_symbols = re.sub(r'^[\w.@+-]+\Z', '', value, count=0, flags=0)

    if wrong_symbols:
        raise ValidationError(
            'В поле username присутствуют запрещенные символы:',
            f'"{wrong_symbols}"')
