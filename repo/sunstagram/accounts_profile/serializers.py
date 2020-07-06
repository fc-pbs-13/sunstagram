from rest_framework import serializers
from .models import AccountProfile


class AccountProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='account.email')
    username = serializers.CharField(source='account.username')
    name = serializers.CharField(source='account.username')

    class Meta:
        model = AccountProfile
        fields = ['id', 'email', 'username', 'name', 'profileImage', 'webSite', 'intro', 'phoneNumber']
