from django.conf.urls import url
from . import views
from .views import hello_world

app_name = 'api'


urlpatterns = [
    url(r'^users/$', views.UserList.as_view(), name='user_list'),
    url(r'^users/(?P<pk>[0-9]+)$', views.UserDetails.as_view(), name='user_list'),





    #misc
    url(r'^hello/$', hello_world, name='hello_world'),
]