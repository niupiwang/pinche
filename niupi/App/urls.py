from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^select/$', views.select, name='select'),
    url(r'^buy/$', views.buy, name='buy'),
url(r'^pay/$', views.pay, name='pay'),
url(r'^payment/$', views.payment, name='payment'),
url(r'^news/$', views.news, name='news'),

url(r'^pay_ali/$', views.pay_ali, name='pay_ali'),
url(r'^all/$', views.all, name='all'),
url(r'^pay_list/$', views.pay_list, name='pay_list'),
url(r'^send_new/$', views.send_new, name='send_new'),

url(r'^add_payment/$', views.add_payment, name='add_payment'),


    # 常用联系人
url(r'^relation/$', views.relation, name='relation'),
    url(r'^userinfo/$', views.userinfo, name='userinfo'),
    url(r'^last/$', views.UserView.as_view(), name='last'),
    url(r'^userinfo/$', views.userinfo,name='userinfo'),
    url(r'^last/$',views.UserView.as_view(),name='last'),


    # 登录登出注册找回密码
    url(r'^login/$',views.user_login,name='login'),
    url(r'^logout/$',views.user_logout,name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^yzm/$',views.yzm,name='yzm'),
    url(r'^sms/$',views.sms,name='sms'),
    url(r'^findpassword/$',views.findpassword,name='findpassword'),
]