from django.contrib.auth import get_user_model
from rest_framework.relations import SlugRelatedField
from rest_framework import serializers

from users.models import ROLES


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Пользователь"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }
