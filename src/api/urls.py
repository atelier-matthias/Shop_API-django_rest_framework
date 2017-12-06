from django.conf.urls import url
from . import views, admin_views

app_name = 'api'

UUID_RE = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"


admin_routes = [
    url(r'^admin/customers/$', admin_views.AdminUserList.as_view(), name='admin_user_list'),
    url(r'^admin/customers/(?P<userUuidStr>%s)/$' % UUID_RE, admin_views.AdminUserDetails.as_view(), name='admin_user_detail'),
    url(r'^admin/products/$', admin_views.AdminProductList.as_view(), name='admin_product_list'),
    url(r'^admin/shops/$', admin_views.AdminShopList.as_view(), name='admin_shop_list'),
    url(r'^admin/stocks/$', admin_views.AdminStockList.as_view(), name='admin_stock_list'),
    url(r'^admin/orders/$', admin_views.AdminOrderList.as_view(), name='admin_order_list'),
]



customer_routes = [
    url(r'^login/$', views.UserLogin.as_view(), name='login'),
    url(r'^logout/$', views.UserLogout.as_view(), name='logout'),
    url(r'^register/$', views.RegisterUser.as_view(), name='register'),
    url(r'^profile/$', views.ProfileDetails.as_view(), name='user_list'),
    url(r'^profile/(?P<userUuidStr>%s)/$' % UUID_RE, views.ProfileUpdate.as_view(), name='user_detail'),

    url(r'^products/$', views.ProductList.as_view(), name='product_list'),
    url(r'^shops/$', views.ShopList.as_view(), name='shop_list'),
    url(r'^stocks/$', views.StockList.as_view(), name='stock_list'),
    url(r'^orders/$', views.OrderList.as_view(), name='order_list'),
]

misc_routes = [
    url(r'^hello/$', views.hello_world, name='hello_world'),
]


urlpatterns = admin_routes + customer_routes