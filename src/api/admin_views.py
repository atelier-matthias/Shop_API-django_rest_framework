from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer, ProductListSerializer, AdminCustomerUpdateSerializer, \
    StockListSerializer, ShopListSerializer, OrderListSerializer
from .models import Product, Shop, Stock, Order, CustomerProfile
from .paginationController import StandardPagination


class AdminUserList(ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]
    pagination_class = StandardPagination


class AdminUserDetails(RetrieveUpdateDestroyAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = AdminCustomerUpdateSerializer
    permission_classes = [IsAdminUser, ]
    lookup_url_kwarg = 'userUuidStr'


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


class AdminOrderList(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAdminUser, ]



