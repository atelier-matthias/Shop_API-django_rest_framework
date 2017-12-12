from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.authentication import authenticate
from django.contrib.auth import login, logout
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, \
    GenericAPIView, UpdateAPIView, RetrieveUpdateAPIView
from .customer_serializers import UserDetailsSerializer, ProductListSerializer, \
    ShopListSerializer, OrderListSerializer, UserLoginSerializer, UserRegisterSerializer, \
    UserUpdateDetailsSerializer, UserUpdatePasswordSerializer, UserBucketDetailsSerializer, \
    UserBucketAddProductSerializer, UserBucketProductQuantityUpdateSerializer ,OrderDetailsSerializer, \
    OrderProductsSerializer
from .controller_pagination import StandardPagination

from .models import Product, Shop, Order, CustomerProfile, ShopBucket, OrderProducts, Stock
from .error_codes import HTTP500Response, HTTP404Response, HTTP409Response, ErrorCodes


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
        else:
            return HTTP404Response(ErrorCodes.USER_OR_PASSWORD_NOT_MATCH)


class UserLogout(APIView):
    def get(self, request):
        logout(request)
        return Response("user Logout", status=200)


class RegisterUser(CreateAPIView):
    queryset = CustomerProfile.objects.filter()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        if CustomerProfile.objects.filter(email=request.POST['email']):
            return HTTP409Response(ErrorCodes.EMAIL_ALREADY_REGISTERED)

        return super(RegisterUser, self).post(request, *args, **kwargs)


class ProfileDetails(ListAPIView):
    # queryset = CustomerProfile.objects.filter()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    # lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return CustomerProfile.objects.filter(uuid=self.request.user.uuid)

    # def get(self, request, *args, **kwargs):
    #     self.kwargs.update({'pk': self.request.user.uuid})
    #     user = self.get_object()
    #     serializer = self.get_serializer(user).data
    #     return Response(serializer)


class ProfileUpdate(UpdateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = UserUpdateDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'customer_uuid'

    def put(self, request, *args, **kwargs):
        if CustomerProfile.objects.filter(email=request.POST['email']):
            return HTTP409Response(ErrorCodes.EMAIL_ALREADY_REGISTERED)

        return super(ProfileUpdate, self).put(request, *args, **kwargs)


class ProfileUpdatePassword(UpdateAPIView):
    queryset = CustomerProfile.objects.filter()
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'customer_uuid'

    # PUT body fields ('username', 'old_password', 'password')
    def put(self, request, *args, **kwargs):
        data = request.data

        username = data.get('username', None)
        password = data.get('old_password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            return super(ProfileUpdatePassword, self).put(request, *args, **kwargs)

        return HTTP404Response(ErrorCodes.USER_OR_PASSWORD_NOT_MATCH)


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = StandardPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('name', 'product_type')

    def get(self, request, *args, **kwargs):
        response = {}
        stocks = []
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for item in serializer.data:
                response[item['product_uuid']] = {
                    'status': item['status'],
                    'name': item['name'],
                    'description': item['description'],
                    'price': item['price'],
                    'product_type': item['product_type'],
                    'quantity': 0
                }
                stocks.append(str(item['product_uuid']))

            res = Stock.objects.filter(product_code__in=stocks)
            for item in res:
                response[str(item.product_code_id)]['quantity'] = item.quantity

            return self.get_paginated_response(response)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class ShopList(ListAPIView, CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopListSerializer


class BucketsProductsList(ListAPIView, CreateAPIView):
    serializer_class = UserBucketDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = StandardPagination

    def get_queryset(self):
        return ShopBucket.objects.filter(customer=self.request.user)

    def post(self, request, *args, **kwargs):
        if ShopBucket.objects.filter(customer=self.request.user, product=self.request.data['product']):
            return HTTP409Response(ErrorCodes.PRODUCT_ALREADY_IN_BUCKET)

        stock = Stock.objects.filter(product_code=request.POST['product']).first()
        if stock is None or stock.quantity is 0:
            return HTTP409Response(ErrorCodes.PRODUCT_NOT_AVALIABLE)

        else:
            req = {}

            product = Product.objects.get(product_uuid=self.request.data['product'])


            req['customer'] = self.request.user.uuid
            req['quantity'] = self.request.data['quantity']
            req['product'] = product.product_uuid
            req['value'] = product.price
            self.serializer_class = UserBucketAddProductSerializer
            serializer = self.get_serializer(data=req)
            serializer.is_valid(raise_exception=True)

            with transaction.atomic():
                Stock.objects.filter(stock_uuid=stock.pk).update(quantity=stock.quantity-1,
                                                                   in_reservation=stock.in_reservation+1)
                self.perform_create(serializer)

            headers = self.get_success_headers(req)

            return Response(req, status=status.HTTP_201_CREATED, headers=headers)


class BucketProductUpdate(RetrieveUpdateDestroyAPIView):
    queryset = ShopBucket.objects.filter()
    serializer_class = UserBucketProductQuantityUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'bucket_uuid'


class OrderList(ListAPIView, CreateAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def post(self, request, *args, **kwargs):
        bucket = ShopBucket.objects.filter(customer=self.request.user.uuid)
        if not bucket:
            return HTTP409Response(ErrorCodes.BUCKET_IS_EMPTY)
        else:
            total_value = 0
            for item in bucket:
                total_value += item.value * item.quantity

            order = {
                'status': Order.NEW,
                'customer': self.request.user.uuid,
                'data_created': datetime.now(),
                'payment': self.request.POST['payment'],
                'sum': total_value
            }
            serializer = self.get_serializer(data=order)
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            with transaction.atomic():
                try:
                    self.perform_create(serializer)
                    for item in bucket:
                        o = OrderProducts(order=serializer.instance,
                                          quantity=item.quantity,
                                          product=item.product,
                                          value=item.value)
                        o.save()
                    ShopBucket.objects.filter(customer=self.request.user.uuid).delete()
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                except:
                    return HTTP500Response(ErrorCodes.ORDER_NOT_CREATED)


class OrderDetails(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'order_uuid'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        res = OrderProducts.objects.filter(order=instance)

        self.serializer_class = OrderProductsSerializer
        products = []
        for item in res:
            products.append(self.get_serializer(item).data)

        return Response([serializer.data, products])


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