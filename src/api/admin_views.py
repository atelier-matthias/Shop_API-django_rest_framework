from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from .serializers import UserSerializer, ProductListSerializer, \
    StockListSerializer, ShopListSerializer, OrderListSerializer
from .admin_serializers import AdminCustomerUpdateSerializer, AdminShopBucketSerializer, AdminOrdersSerializers
from .models import Product, Shop, Stock, Order, CustomerProfile, ShopBucket, OrderProducts
from .paginationController import StandardPagination
from django.db import transaction



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
        bucket = ShopBucket.objects.filter(customer_uuid=request.user.uuid)
        if not bucket:
            return Response("bucket is empty", status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            with transaction.atomic():
                for item in bucket:
                    o = OrderProducts(order_uuid=serializer.instance,
                                      quantity=item.quantity,
                                      product_uuid=item.product_uuid,
                                      value=item.value)
                    o.save()
                ShopBucket.objects.filter(customer_uuid=request.user.uuid).delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AdminOrderDetails(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = AdminOrdersSerializers
    permission_classes = [IsAdminUser, ]
    lookup_url_kwarg = 'order_uuid'


class AdminShopBucketList(ListAPIView, CreateAPIView):
    queryset = ShopBucket.objects.all()
    serializer_class = AdminShopBucketSerializer
    permission_classes = [IsAdminUser, ]


class AdminShopBucketDetails(RetrieveUpdateDestroyAPIView):
    queryset = ShopBucket.objects.all()
    serializer_class = AdminShopBucketSerializer
    permission_classes = [IsAdminUser, ]
    lookup_url_kwarg = 'bucket_uuid'
