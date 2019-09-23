from django.conf.urls import url
from django.views.static import serve

import niupih
from niupi import settings
from niupih import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^order_list/$', views.order_list, name='order_list'),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^user_detail/(\d+)/$', views.user_detail, name='user_detail'),
    url(r'^user_update/(\d+)/$', views.user_update, name='user_update'),  # 不修改用户信息
    url(r'^admin_add', views.admin_add, name='admin_add'),
    url(r'^admin_list', views.admin_list, name='admin_list'),
    url(r'^admin_update/(\d+)/$', views.admin_update, name='admin_update'),
    url(r'^admin_detail/(\d+)/$', views.admin_detail, name='admin_detail'),
    url(r'^bus_list/$', views.bus_list, name='bus_list'),
    url(r'^bus_detail/(\d+)/$', views.bus_detail, name='bus_detail'),
    url(r'^bus_add/$', views.bus_add, name='bus_add'),
    url(r'^bus_add2/$', views.bus_add2, name='bus_add2'),
    url(r'^bus_delete/$', views.bus_delete, name='bus_delete'),
    url(r'^bus_delete/(\d+)/$', views.bus_delete, name='bus_delete'),
    url(r'^bus_update/(\d+)/$', views.bus_update, name='bus_update'),
    url(r'^car_list/$', views.car_list, name='car_list'),
    url(r'^car_detail/(\d+)/$', views.car_detail, name='car_detail'),


]

handler404 = niupih.views.page_not_found
handler500 = niupih.views.server_error
# url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
# url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
