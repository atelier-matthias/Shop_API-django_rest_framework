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
        res = {}

        product = Product.objects.get(product_uuid=request.data['product'])

        res['customer'] = request.user.uuid
        res['quantity'] = request.data['quantity']
        res['product'] = product.product_uuid
        res['value'] = product.price

        serializer = UserBucketAddProductSerializer(data=res)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            stock = Stock.objects.get(product_code=request.data['product'])
            stock.quantity = stock.quantity - int(request.data['quantity'])
            stock.in_reservation = stock.in_reservation + int(request.data['quantity'])
            stock.save()

            serializer.save()

        return res


class CustomerBucketProductUpdateCommand(DefaultCommands):
    @classmethod
    def execute(cls, *args, **kwargs):
        res = kwargs.get('obj')
        new_quantity = kwargs.get('new_quantity')

        with transaction.atomic():
            stock = Stock.objects.get(product_code=res.product_id)
            stock.quantity = stock.quantity + res.quantity - new_quantity
            stock.in_reservation = stock.in_reservation - res.quantity + new_quantity
            stock.save()


class CustomerBucketProductRemoveCommand(DefaultCommands):
    @classmethod
    def execute(cls, **kwargs):
        obj = kwargs.get('obj')

        with transaction.atomic():
            stock = Stock.objects.get(product_code=obj.product_id)
            stock.in_reservation = stock.in_reservation - obj.quantity
            stock.quantity = stock.quantity + obj.quantity
            stock.save()
        pass