from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from accounts_profile.models import AccountProfile
from accounts_profile.serializers import AccountProfileSerializer


class AccountProfileViewSet(ModelViewSet):

    queryset = AccountProfile.objects.all()
    serializer_class = AccountProfileSerializer
