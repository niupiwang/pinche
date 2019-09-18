from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^select/$', views.select, name='select'),
    url(r'^buy/$', views.buy, name='buy'),
url(r'^pay/$', views.pay, name='pay'),
url(r'^payment/$', views.payment, name='payment'),
url(r'^news/$', views.news, name='news'),



    # 常用联系人
url(r'^relation/$', views.relation, name='relation'),
    url(r'^userinfo/$', views.userinfo, name='userinfo'),
    url(r'^last/$', views.UserView.as_view(), name='last'),
    url(r'^userinfo/$', views.userinfo,name='userinfo'),
    url(r'^last/$',views.UserView.as_view(),name='last'),

    # 登录登出注册
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^yzm/$',views.yzm,name='yzm'),
]