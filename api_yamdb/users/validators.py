from django.core.exceptions import ValidationError


def username_me_validator(value):
    if value == 'me':
        raise ValidationError('Нельзя указать "me" в поле username!')