from .helpers import DefaultCommands
from .models import Product, Stock, ShopBucket, OrderProducts, Order
from .customer_serializers import UserBucketAddProductSerializer
from django.db import transaction



class CustomerProductListCommand(DefaultCommands):
    @classmethod
    def execute(cls, serializer):
        products = {}
        stocks = []
        for item in serializer.data:
            products[item['product_uuid']] = {
                'product_uuid': item['product_uuid'],
                'status': item['status'],
                'name': item['name'],
                'description': item['description'],
                'price': item['price'],
                'product_type': item['product_type'],
                'quantity': 0
            }
            stocks.append(str(item['product_uuid']))

            res = Stock.objects.filter(product_code__in=stocks)
            for item in res:
                products[str(item.product_code_id)]['quantity'] = item.quantity

        response = [value for key, value in products.items()]
        return response


class CustomerAddProductToBucketCommand(DefaultCommands):
    @classmethod
    def execute(cls, request, *args, **kwargs):
        stock = kwargs.get('stock')
        res = {}

        product = Product.objects.get(product_uuid=request.data['product'])

        res['customer'] = request.user.uuid
        res['quantity'] = request.data['quantity']
        res['product'] = product.product_uuid
        res['value'] = product.price

        # serializer_class = UserBucketAddProductSerializer(data=res)
        serializer = UserBucketAddProductSerializer(data=res)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            Stock.objects.filter(stock_uuid=stock.pk).update(quantity=stock.quantity - int(request.data['quantity']),
                                                             in_reservation=stock.in_reservation + int(
                                                                 request.data['quantity']))
            serializer.save()

        return res
