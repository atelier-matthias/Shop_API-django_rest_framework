from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Shop, Stock, Order, CustomerProfile
from django.contrib.auth.hashers import make_password


class UserLoginSerialization(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['username', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserDetails(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'

    def create(self, validated_data):
        user = super(CustomerSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



