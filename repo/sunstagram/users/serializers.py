from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}, }
        read_only_fields = ('id', 'date_joined',)


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

    def validate(self, data):
        raw_password = data.get('new_password')
        raw_password2 = data.get('new_password2')
        if raw_password != raw_password2:
            raise serializers.ValidationError('Not matched password and password2')
        return raw_password

    def validate_password(self, value):
        user = User.objects.get(id=self.context.get('request').user.id)
        if user.password == value:
            return value
        else:
            raise serializers.ValidationError('incorrect password')
