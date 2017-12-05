from django.conf.urls import url
from . import views

app_name = 'api'


urlpatterns = [
    url(r'^users/$', views.UserList.as_view(), name='user_list'),
    url(r'^users/(?P<pk>[0-9]+)$', views.UserDetails.as_view(), name='user_list'),

    url(r'^customers/$', views.CustomerList.as_view(), name='customer_list'),
    url(r'^products/$', views.ProductList.as_view(), name='customer_list'),
    url(r'^shops/$', views.ShopList.as_view(), name='shop_list'),
    url(r'^stocks/$', views.StockList.as_view(), name='stock_list'),
    url(r'^orders/$', views.OrderList.as_view(), name='order_list'),





    #misc
    url(r'^hello/$', views.hello_world, name='hello_world'),
]