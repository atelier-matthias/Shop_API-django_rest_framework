import uuid
from django.db import models
from model_utils.models import StatusModel, SoftDeletableModel
from model_utils import Choices
from django.utils.timezone import now

class Customer(SoftDeletableModel):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    phone_nr = models.IntegerField()
    email = models.EmailField(max_length=40)

    def __str__(self):
        return self.email


class Product(StatusModel, SoftDeletableModel):
    RTV = 'rtv'
    MEDIA = 'media'
    PRODUCT_TYPE = (
        (RTV, 'rtv'),
        (MEDIA, 'media')
    )

    STATUS = Choices('new', 'promotions', 'sales')
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False, default='NoName')
    description = models.TextField(max_length=1000, default="no description")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE, default=RTV)

    def __str__(self):
        return self.name


class Shop(StatusModel, SoftDeletableModel):
    STATUS = Choices('open', 'closed')
    shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default=None)


class Stock(models.Model):
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    shop_num = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None)
    quantity = models.SmallIntegerField


class Order(StatusModel):
    CASH = 'cash'
    PAYU = 'payu'
    CARD = 'card'
    PAYMENT_TYPE = (
        (CASH, 'cash'),
        (PAYU, 'payu'),
        (CARD, 'card')
    )
    STATUS = Choices('new', 'to_pay', 'payed', 'error', 'returned')
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.ForeignKey(Customer)
    product_id = models.ForeignKey(Product)
    shop_id = models.ForeignKey(Shop)
    created = models.DateTimeField(default=now)
    paid = models.DateTimeField(blank=True, null=True)
    sum = models.DecimalField(max_digits=8, decimal_places=2)
    payment = models.CharField(max_length=20, choices=PAYMENT_TYPE, default=CASH)





