from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'date_joined']
        extra_kwargs = {'password': {'write_only': True},
                        'date_joined': {'read_only': True}}


class PasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['id', 'password', 'new_password', 'new_password2']
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
            'new_password': {'write_only': True},
            'new_password2': {'write_only': True},
        }
