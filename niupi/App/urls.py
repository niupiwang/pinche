from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^select/$', views.select, name='select'),
    url(r'^buy/$', views.buy, name='buy'),
    url(r'^userinfo/$', views.userinfo, name='userinfo'),
    url(r'^last/$', views.UserView.as_view(), name='last')
]

