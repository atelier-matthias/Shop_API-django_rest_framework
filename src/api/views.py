from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.authentication import authenticate
from django.contrib.auth import login
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, \
    GenericAPIView
from .serializers import UserSerializer, ProductListSerializer, \
    StockListSerializer, ShopListSerializer, OrderListSerializer, CustomerSerializer, UserLoginSerialization
from django.contrib.auth.models import User
from .models import Product, Shop, Stock, Order, CustomerProfile


class UserLogin(GenericAPIView):
    serializer_class = UserLoginSerialization

    def post(self, request, *args, **kwargs):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

        return Response("success", status=200)



class UserList(ListAPIView, CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerList(ListAPIView, CreateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerSerializer


class ProductList(ListAPIView, CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]


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