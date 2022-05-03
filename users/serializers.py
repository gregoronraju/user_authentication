"""
# 
# File          : serializers.py
# Created       : 02/05/22 8:08 PM
# Author        : Ron Greego
# Version       : v1.0.0
# Description   :
#
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.utils import timezone
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # update last login time
        user.last_login = timezone.now()
        user.save()

        # Add custom claims
        token['username'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], )

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'middle_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            middle_name=validated_data['middle_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'middle_name', 'last_name', 'last_login']
