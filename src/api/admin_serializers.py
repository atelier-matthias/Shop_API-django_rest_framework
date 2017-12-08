from rest_framework import serializers
from .models import Product, Shop, Stock, Order, CustomerProfile, ShopBucket, OrderProducts



class AdminCustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        user = super(AdminCustomerUpdateSerializer, self).update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AdminShopBucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopBucket
        fields = '__all__'


class AdminShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', 'status', 'shop_uuid')


class AdminOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ('product', 'quantity', 'value')


class AdminOrdersSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('status', 'order_uuid', 'customer', 'shop', 'sum', 'date_paid')


class AdminOrderStatusSetPaidSerialize(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('date_paid', 'status')