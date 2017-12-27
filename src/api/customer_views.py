from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import authenticate
from django.contrib.auth import login, logout
from django.conf import settings
from django_filters import rest_framework as filters
from django.middleware.csrf import get_token
from django.db import transaction
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, \
    GenericAPIView, UpdateAPIView
from .customer_serializers import UserDetailsSerializer, ProductListSerializer, \
    ShopListSerializer, OrderListSerializer, UserLoginSerializer, UserRegisterSerializer, \
    UserUpdateDetailsSerializer, UserUpdatePasswordSerializer, UserBucketDetailsSerializer, \
    UserBucketAddProductSerializer, UserBucketProductQuantityUpdateSerializer, \
    OrderDetailsSerializer, OrderProductsSerializer
from .controller_pagination import StandardPagination
from .models import Product, Shop, Order, CustomerProfile, ShopBucket, OrderProducts, Stock
from .error_codes import HTTP500Response, HTTP404Response, HTTP409Response, ErrorCodes, RETURN_OK
from .controller_payu import PayUGatewayCommands
from .helpers import DefaultCommands


class UserLogin(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            res = login(request, user)

            return Response({'status': 'OK', 'user': user.pk, 'CSRF_token': get_token(request)}, status=200)
        else:
            return HTTP404Response(ErrorCodes.USER_OR_PASSWORD_NOT_MATCH)


class UserLogout(APIView):
    def get(self, request):
        logout(request)
        return RETURN_OK('user logout')


class RegisterUser(CreateAPIView):
    queryset = CustomerProfile.objects.filter()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        if CustomerProfile.objects.filter(email=request.data['email']):
            return HTTP409Response(ErrorCodes.EMAIL_ALREADY_REGISTERED)

        return super(RegisterUser, self).post(request, *args, **kwargs)


class ProfileDetails(ListAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return CustomerProfile.objects.filter(uuid=self.request.user.uuid)


class ProfileUpdate(UpdateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = UserUpdateDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'customer_uuid'

    def put(self, request, *args, **kwargs):
        if CustomerProfile.objects.filter(email=request.data['email']):
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
    queryset = Product.objects.filter()
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

        stock = Stock.objects.filter(product_code=request.data['product']).first()
        if stock is None or stock.quantity is 0:
            return HTTP409Response(ErrorCodes.PRODUCT_NOT_AVALIABLE)

        if stock.quantity < int(request.data['quantity']):
            return HTTP409Response(ErrorCodes.NOT_ENOUGH_PRODUCTS_IN_MAGAZINES)

        else:
            res = {}

            product = Product.objects.get(product_uuid=self.request.data['product'])

            res['customer'] = self.request.user.uuid
            res['quantity'] = self.request.data['quantity']
            res['product'] = product.product_uuid
            res['value'] = product.price
            self.serializer_class = UserBucketAddProductSerializer
            serializer = self.get_serializer(data=res)
            serializer.is_valid(raise_exception=True)

            try:
                with transaction.atomic():
                    Stock.objects.filter(stock_uuid=stock.pk).update(quantity=stock.quantity-int(request.data['quantity']),
                                                                       in_reservation=stock.in_reservation+int(request.data['quantity']))
                    self.perform_create(serializer)

                headers = self.get_success_headers(res)
                return Response(res, status=status.HTTP_201_CREATED, headers=headers)
            except:
                return HTTP500Response(ErrorCodes.ADD_PRODUCT_TO_BUCKET_ERROR)


class BucketProductUpdate(RetrieveUpdateDestroyAPIView):
    queryset = ShopBucket.objects.filter()
    serializer_class = UserBucketProductQuantityUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'bucket_uuid'

    def put(self, request, *args, **kwargs):
        res = self.get_object()
        new_quantity = int(request.data['quantity'])

        if new_quantity == 0:
            return self.destroy(request, *args, **kwargs)

        if res.quantity == new_quantity:
            return super(BucketProductUpdate, self).put(request, *args, **kwargs)

        stock = Stock.objects.get(product_code=res.product_id)
        if res.quantity < new_quantity and stock.quantity < new_quantity - res.quantity:
            return HTTP409Response(ErrorCodes.NOT_ENOUGH_PRODUCTS_IN_MAGAZINES)

        else:
            with transaction.atomic():
                stock = Stock.objects.get(product_code=res.product_id)
                stock.quantity = stock.quantity + res.quantity - new_quantity
                stock.in_reservation = stock.in_reservation - res.quantity + new_quantity
                stock.save()

            return super(BucketProductUpdate, self).put(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        res = self.get_object()

        try:
            with transaction.atomic():
                stock = Stock.objects.get(product_code=res.product_id)
                stock.in_reservation = stock.in_reservation - res.quantity
                stock.quantity = stock.quantity + res.quantity
                stock.save()
            super(BucketProductUpdate, self).destroy(request, *args, **kwargs)
            return RETURN_OK("product removed")
        except:
            return HTTP500Response(ErrorCodes.BUCKET_PRODUCT_REMOVE_ERROR)


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
                'payment': self.request.data['payment'],
                'sum': total_value
            }
            serializer = self.get_serializer(data=order)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            with transaction.atomic():
                try:
                    for item in bucket:
                        s = Stock.objects.get(product_code=item.product_id)
                        s.in_reservation = s.in_reservation - item.quantity
                        o = OrderProducts(order=serializer.instance,
                                          quantity=item.quantity,
                                          product=item.product,
                                          value=item.value)
                        s.save()
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


class OrderSetCanceled(UpdateAPIView):
    queryset = Order.objects.filter()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'order_uuid'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        products = OrderProducts.objects.filter(order=instance)
        if instance.status == Order.ERROR or instance.status == Order.RETURNED:
            return HTTP409Response(ErrorCodes.WRONG_ORDER_STATUS)
        else:
            try:
                with transaction.atomic():
                    for item in products:
                        stock = Stock.objects.get(product_code=item.product_id)
                        stock.quantity = stock.quantity + item.quantity
                        stock.save()
                    order = Order.objects.get(order_uuid=instance.pk)
                    order.status = Order.RETURNED
                    order.save()
                return RETURN_OK('order returned')
            except:
                return HTTP500Response(ErrorCodes.ORDER_STATUS_UPDATE_ERROR)


class OrderPayUPayment(UpdateAPIView, DefaultCommands):
    queryset = Order.objects.filter()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'order_uuid'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        products = []
        orderProducts = OrderProducts.objects.filter(order=instance)

        for item in orderProducts:
            s = {
                'name': str(item.product.name),
                'unitPrice': int(item.value * 100),
                'quantity': item.quantity
            }
            products.append(s)

        order = {
                "notifyUrl": "https://your.eshop.com/notify",
                "orderUuid": str(instance.pk),
                "customerIp": str(get_client_ip(request)),
                "merchantPosId": str(settings.PAYU_MERCHANT_KEY),
                "description": "TEST_SHOP",
                "currencyCode": "PLN",
                "totalAmount": int(instance.sum * 100),
                "products": products
            }

        res = PayUGatewayCommands.create_order(orderBody=order)
        response = self.str2dict(res.history[0].text)
        with transaction.atomic():
            instance.payuID = response['orderId']
            instance.save()

        return RETURN_OK(response)


class OrderPayUStatus(RetrieveAPIView, DefaultCommands):
    queryset = Order.objects.filter()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'order_uuid'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        res = PayUGatewayCommands.get_order_status(instance.payuID)
        return Response(self.str2dict(res.text))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip