from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'profile_image', 'web_site', 'intro', 'phone_number']

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        email = user.pop('email')
        username = user.pop('username')

        super().update(instance, validated_data)

        #email 형식 검사
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
            instance.user.email = email
        instance.user.username = username
        instance.save()
        return instance
