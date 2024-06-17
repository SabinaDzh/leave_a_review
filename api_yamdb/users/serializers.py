from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Пользователь"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'},
            'email': {'max_length': 254},
            'username': {'max_length': 150},
        }
