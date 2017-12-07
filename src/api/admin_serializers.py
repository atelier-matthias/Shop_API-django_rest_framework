from rest_framework import serializers
from .models import Product, Shop, Stock, Order, CustomerProfile, ShopBucket, OrderProducts



class AdminCustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.set_password(instance.password)
        return instance


class AdminShopBucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopBucket
        fields = '__all__'


class AdminShopSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class AdminProductSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class AdminOrderProductSerializer(serializers.ModelSerializer):
    product = AdminProductSerializer(many=False, read_only=True)
    class Meta:
        model = OrderProducts
        fields = ('product', 'quantity', 'value')


class AdminOrdersSerializers(serializers.ModelSerializer):
    ordered_products = AdminOrderProductSerializer(many=True, read_only=True)
    shop = AdminShopSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('status', 'order_uuid', 'customer', 'shop', 'sum', 'ordered_products')
