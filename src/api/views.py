from django.shortcuts import render, render_to_response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer, CustomerListSerializer, ProductListSerializer, \
    StockListSerializer, ShopListSerializer, OrderListSerializer
from django.contrib.auth.models import User
from .models import Customer, Product, Shop, Stock, Order


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerList(ListAPIView, CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer


class ProductList(ListAPIView, CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ShopList(ListAPIView, CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopListSerializer


class StockList(ListAPIView, CreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockListSerializer


class OrderList(ListAPIView, CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer






@api_view(['GET'])
def hello_world(request):
    res = User.objects.all()
    data = []

    for user in res:
        a = {
            'imie': user.username,
            'nowe id': user.id,
            'mail usera': user.email
        }
        data.append(a)

    return Response(data, status=201)