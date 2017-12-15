from rest_framework import serializers
from .models import Product, Shop, Stock, Order, CustomerProfile, ShopBucket, OrderProducts


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['username', 'password']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ('username', 'password', 'first_name', 'email')

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ('uuid', 'username', 'first_name', 'last_name', 'email', 'phone', 'city')


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ('password','username')

    def update(self, instance, validated_data):
        user = super(UserUpdatePasswordSerializer, self).update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ('first_name', 'last_name', 'email', 'phone', 'city')


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_uuid', 'status', 'name', 'description', 'price', 'product_type')


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_uuid', 'status', 'date_created', 'date_paid', 'sum', 'payment')


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = '__all__'


class UserBucketDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopBucket
        fields = ('quantity', 'product', 'value', 'bucket_uuid')


class UserBucketAddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopBucket
        fields = ('quantity', 'product', 'value', 'customer')


class UserBucketProductQuantityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopBucket
        fields = ('quantity', )
