from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.authentication import authenticate
from django.contrib.auth import login, logout
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, \
    GenericAPIView
from .serializers import UserSerializer, ProductListSerializer, AdminCustomerUpdateSerializer, \
    StockListSerializer, ShopListSerializer, OrderListSerializer, UserLoginSerializer, UserRegisterSerializer
from django.contrib.auth.models import User
from .models import Product, Shop, Stock, Order, CustomerProfile


class AdminUserList(ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]


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