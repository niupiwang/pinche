from django.conf.urls import url

from niupih import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^order_list/$', views.order_list, name='order_list'),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^user_detail/(\d+)/$', views.user_detail, name='user_detail'),
    url(r'^update_user/(\d+)/$', views.update_user, name='update_user'),
    url(r'^admin_add', views.admin_add, name='admin_add'),
    url(r'^admin_detail/$', views.admin_detail, name='admin_detail'),
    url(r'^bus_list/$', views.bus_list, name='bus_list'),
    url(r'^car_list/$', views.car_list, name='car_list'),

]