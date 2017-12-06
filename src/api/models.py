import uuid
from django.db import models
from model_utils.models import StatusModel, SoftDeletableModel
from model_utils import Choices
from django.utils.timezone import now
from django.contrib.auth.models import User, AbstractUser


class CustomerProfile(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')


class Product(StatusModel, SoftDeletableModel):
    RTV = 'rtv'
    MEDIA = 'media'
    PRODUCT_TYPE = (
        (RTV, 'rtv'),
        (MEDIA, 'media')
    )

    STATUS = Choices('new', 'promotions', 'sales')
    product_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False, default='NoName')
    description = models.TextField(max_length=1000, default="no description")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE, default=RTV)

    def __str__(self):
        return self.name


class Shop(StatusModel, SoftDeletableModel):
    STATUS = Choices('open', 'closed')
    shop_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default=None)


class Stock(models.Model):
    stock_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    order_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_uuid = models.ForeignKey(CustomerProfile)
    product_uuid = models.ForeignKey(Product)
    shop_uuid = models.ForeignKey(Shop)
    created = models.DateTimeField(default=now)
    paid = models.DateTimeField(blank=True, null=True)
    sum = models.DecimalField(max_digits=8, decimal_places=2)
    payment = models.CharField(max_length=20, choices=PAYMENT_TYPE, default=CASH)




