from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserDetails(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


class Randomserializer(serializers.BaseSerializer):
    fields = ('data')

