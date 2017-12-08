from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from .serializers import UserSerializer, ProductListSerializer, \
    StockListSerializer, ShopListSerializer, OrderListSerializer
from .admin_serializers import AdminCustomerUpdateSerializer, AdminShopBucketSerializer, AdminOrdersSerializers, \
    AdminShopSerializer, AdminOrderProductSerializer, AdminOrderStatusSetPaidSerialize
from .models import Product, Shop, Stock, Order, CustomerProfile, ShopBucket, OrderProducts
from .paginationController import StandardPagination
from django.db import transaction
from .error_codes import ErrorCodes
from datetime import datetime


class AdminUserList(ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]
    pagination_class = StandardPagination


class AdminUserDetails(RetrieveUpdateDestroyAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = AdminCustomerUpdateSerializer
    permission_classes = [IsAdminUser, ]
    lookup_url_kwarg = 'user_uuid'


class AdminProductList(ListAPIView, CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminUser,]


class AdminShopList(ListAPIView, CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopListSerializer
    permission_classes = [IsAdminUser, ]


class AdminStockList(ListAPIView, CreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockListSerializer
    permission_classes = [IsAdminUser, ]


class AdminOrderList(ListAPIView, CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAdminUser, ]

    def create(self, request, *args, **kwargs):
        bucket = ShopBucket.objects.filter(customer=request.user.uuid)
        if not bucket:
            return Response("bucket is empty", status=status.HTTP_404_NOT_FOUND)
        else:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                for item in bucket:
                    o = OrderProducts(order=serializer.instance,
                                      quantity=item.quantity,
                                      product=item.product,
                                      value=item.value)
                    o.save()
                ShopBucket.objects.filter(customer=request.user.uuid).delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AdminOrderDetails(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = AdminOrdersSerializers
    permission_classes = [IsAdminUser, ]
    lookup_url_kwarg = 'order_uuid'

    def get(self, request, *args, **kwargs):
        res = dict()

        order = self.get_object()
        serializer = self.get_serializer(order).data

        res['status'] = order.status
        res['uuid'] = order.order_uuid
        res['date_paid'] = order.date_paid
        res['customer'] = {
            'email': order.customer.email,
            'first_name': order.customer.first_name,
            'uuid': order.customer.pk
        }
        res['sum'] = serializer['sum']
        res['shop'] = {
            'name': order.shop.name,
            'status': order.shop.status,
            'shop_uuid': order.shop.pk
        }

        self.serializer_class = AdminOrderProductSerializer
        orderProducts = OrderProducts.objects.select_related('order')
        res['products'] = [self.get_serializer(o).data for o in orderProducts]

        return Response(res, 200)


class AdminOrderSetPaid(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = AdminOrderStatusSetPaidSerialize
    permission_classes = [IsAdminUser, ]
    lookup_url_kwarg = 'order_uuid'

    def put(self, request, *args, **kwargs):
        update = dict()

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        update['status'] = Order.PAID
        update['date_paid'] = request.data['date_paid'] if request.data['date_paid'] else datetime.now()
        serializer = self.get_serializer(instance, data=update, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class AdminShopBucketList(ListAPIView, CreateAPIView):
    queryset = ShopBucket.objects.all()
    serializer_class = AdminShopBucketSerializer
    permission_classes = [IsAdminUser, ]


class AdminShopBucketDetails(RetrieveUpdateDestroyAPIView):
    queryset = ShopBucket.objects.all()
    serializer_class = AdminShopBucketSerializer
    permission_classes = [IsAdminUser, ]
    lookup_url_kwarg = 'bucket_uuid'
