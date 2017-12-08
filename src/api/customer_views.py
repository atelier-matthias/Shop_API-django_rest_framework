from django.shortcuts import redirect
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.authentication import authenticate
from django.contrib.auth import login, logout
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, \
    GenericAPIView, UpdateAPIView, RetrieveUpdateAPIView
from .customer_serializers import UserDetailsSerializer, ProductListSerializer, \
    StockListSerializer, ShopListSerializer, OrderListSerializer, UserLoginSerializer, UserRegisterSerializer, \
    UserUpdateDetailsSerializer, UserUpdatePasswordSerializer, UserBucketDetailsSerializer, UserBucketAddProductSerializer
from django.contrib.auth.models import User
from .models import Product, Shop, Order, CustomerProfile, ShopBucket


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


class ProfileDetails(RetrieveAPIView):
    queryset = CustomerProfile.objects.filter()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.kwargs.update({'pk': self.request.user.uuid})
        user = self.get_object()
        serializer = self.get_serializer(user).data
        return Response(serializer)


class ProfileUpdate(UpdateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = UserUpdateDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'pk'

    def put(self, request, *args, **kwargs):
        self.kwargs.update({'pk': self.request.user.uuid})
        return self.update(request, *args, **kwargs)


class ProfileUpdatePassword(UpdateAPIView):
    queryset = CustomerProfile.objects.filter()
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'pk'

    def put(self, request, *args, **kwargs):
        self.kwargs.update({'pk': self.request.user.uuid})
        return self.update(request, *args, **kwargs)


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ShopList(ListAPIView, CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopListSerializer


class BucketDetails(RetrieveAPIView):
    queryset = ShopBucket.objects.all()
    serializer_class = UserBucketDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.kwargs.update({'pk': self.request.user.uuid})
        user = self.get_object()
        serializer = self.get_serializer(user).data
        return Response(serializer)


class BucketAddProduct(CreateAPIView):
    queryset = ShopBucket.objects.all()
    serializer_class = UserBucketAddProductSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        prod = dict()

        product = Product.objects.get(product_uuid=request.POST['product'])
        prod = request.data
        prod['customer'] = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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