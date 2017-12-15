from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from .customer_serializers import UserDetailsSerializer, ProductListSerializer, \
    ShopListSerializer, OrderListSerializer
from .admin_serializers import AdminCustomerUpdateSerializer, AdminShopBucketSerializer, AdminOrdersSerializers, \
    AdminOrderProductSerializer, AdminOrderStatusSetPaidSerialize, AdminStockListSerializer, AdminStockUpdateSerializer
from .models import Product, Shop, Stock, Order, CustomerProfile, ShopBucket, OrderProducts
from .controller_pagination import StandardPagination
from django.db import transaction
from datetime import datetime
from django_filters import rest_framework as filters
from .error_codes import HTTP409Response, ErrorCodes


class AdminUserList(ListAPIView):
    queryset = CustomerProfile.objects.filter()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAdminUser,]
    pagination_class = StandardPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('username', 'email')


class AdminUserDetails(RetrieveUpdateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = AdminCustomerUpdateSerializer
    permission_classes = [IsAdminUser, ]
    lookup_url_kwarg = 'user_uuid'


class AdminProductList(ListAPIView, CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminUser,]
    pagination_class = StandardPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('name', 'product_type')


class AdminShopList(ListAPIView, CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopListSerializer
    permission_classes = [IsAdminUser, ]


class AdminStockList(ListAPIView, CreateAPIView):
    serializer_class = AdminStockListSerializer
    permission_classes = [IsAdminUser, ]

    #GET filters
    def get_queryset(self):
        filters = {}
        if 'product_code' in self.request.GET:
            filters['product_code__name__contains'] = self.request.GET['product_code']
        # if 'shop_num' in self.request.GET:
        #     filters['shop_num__name__contains'] = self.request.GET['shop_num']

        return Stock.objects.filter(**filters)

    def post(self, request, *args, **kwargs):
        if Stock.objects.filter(product_code=request.POST['product_code']):
            return HTTP409Response(ErrorCodes.STOCK_ALREADY_CREATED)

        return super(AdminStockList, self).post(request, *args, **kwargs)


class AdminStockDetails(RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = AdminStockListSerializer
    permission_classes = [IsAdminUser, ]
    lookup_url_kwarg = 'stock_uuid'

    def put(self, request, *args, **kwargs):
        self.serializer_class = AdminStockUpdateSerializer
        return super(AdminStockDetails, self).put(request, *args, **kwargs)


class AdminOrderList(ListAPIView, CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = AdminOrdersSerializers
    permission_classes = [IsAdminUser, ]

    def create(self, request, *args, **kwargs):
        bucket = ShopBucket.objects.filter(customer=request.user.uuid)
        if not bucket:
            return HTTP409Response(ErrorCodes.BUCKET_IS_EMPTY)
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
