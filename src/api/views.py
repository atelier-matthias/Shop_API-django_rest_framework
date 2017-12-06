from django.shortcuts import redirect
from rest_framework.reverse import reverse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.authentication import authenticate
from django.contrib.auth import login, logout
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, \
    GenericAPIView, UpdateAPIView, RetrieveUpdateAPIView
from .serializers import UserSerializer, ProductListSerializer, \
    StockListSerializer, ShopListSerializer, OrderListSerializer, UserLoginSerializer, UserRegisterSerializer
from django.contrib.auth.models import User
from .models import Product, Shop, Stock, Order, CustomerProfile


class UserLogin(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

        return Response("success", status=200)


class UserLogout(APIView):
    def get(self, request):
        logout(request)
        return Response("user Logout", status=200)


class RegisterUser(CreateAPIView):
    serializer_class = UserRegisterSerializer


class ProfileDetails(ListAPIView, UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        return redirect('api:user_detail', userUuidStr=str(request.user.uuid))


class ProfileUpdate(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'userUuidStr'

    def get_queryset(self):
        return CustomerProfile.objects.filter(uuid=self.request.user.uuid)


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ShopList(ListAPIView, CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopListSerializer


class StockList(ListAPIView, CreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockListSerializer
    permission_classes = [IsAuthenticated, ]


class OrderList(ListAPIView, CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated, ]






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