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


class AdminOrderProductSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        res = dict()
        res = {
            'value': instance.value,
            'quantity': instance.quantity,
            'product': instance.product_uuid.name
        }
        return res


class AdminOrdersSerializers(serializers.ModelSerializer):
    order_orderproducts = AdminOrderProductSerializer(many=True, read_only=True)
    shop_uuid = AdminShopSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('status', 'order_uuid', 'customer_uuid', 'shop_uuid', 'sum', 'order_orderproducts')
