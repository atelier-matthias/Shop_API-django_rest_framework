from django.conf.urls import url
from . import customer_views, admin_views

app_name = 'api'

UUID_RE = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"


admin_routes = [
    url(r'^admin/customers/$', admin_views.AdminUserList.as_view()),
    url(r'^admin/customers/(?P<user_uuid>%s)/$' % UUID_RE, admin_views.AdminUserDetails.as_view()),
    url(r'^admin/products/$', admin_views.AdminProductList.as_view()),
    url(r'^admin/shops/$', admin_views.AdminShopList.as_view()),
    url(r'^admin/stocks/$', admin_views.AdminStockList.as_view()),
    url(r'^admin/stocks/(?P<stock_uuid>%s)/$' %UUID_RE, admin_views.AdminStockDetails.as_view()),

    url(r'^admin/orders/$', admin_views.AdminOrderList.as_view()),
    url(r'^admin/orders/(?P<order_uuid>%s)/$' % UUID_RE, admin_views.AdminOrderDetails.as_view()),
    url(r'^admin/orders/(?P<order_uuid>%s)/set_paid$' % UUID_RE, admin_views.AdminOrderSetPaid.as_view()),

    url(r'^admin/buckets/$', admin_views.AdminShopBucketList.as_view()),
    url(r'^admin/buckets/(?P<bucket_uuid>%s)/$' % UUID_RE, admin_views.AdminShopBucketDetails.as_view()),

]

customer_routes = [
    url(r'^login/$', customer_views.UserLogin.as_view()),
    url(r'^logout/$', customer_views.UserLogout.as_view()),
    url(r'^register/$', customer_views.RegisterUser.as_view()),
    url(r'^profile/$', customer_views.ProfileDetails.as_view()),
    url(r'^profile/(?P<customer_uuid>%s)/$' % UUID_RE, customer_views.ProfileUpdate.as_view()),
    url(r'^profile/(?P<customer_uuid>%s)/setpassword$' % UUID_RE, customer_views.ProfileUpdatePassword.as_view()),

    url(r'^products/$', customer_views.ProductList.as_view()),
    url(r'^shops/$', customer_views.ShopList.as_view()),
    # url(r'^stocks/$', customer_views.StockList.as_view()),
    url(r'^orders/$', customer_views.OrderList.as_view()),
]

misc_routes = [
    url(r'^hello/$', customer_views.hello_world, name='hello_world'),
]

urlpatterns = admin_routes + customer_routes + misc_routes