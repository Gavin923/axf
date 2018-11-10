from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^market/(\d+)/(\d+)/$', views.market, name='market'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^mine/$', views.mine, name='mine'),
    url(r'^registe/$', views.registe, name='registe'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^checkaccount/$', views.checkaccount, name='checkaccount'),
    url(r'^addcart/$', views.addcart, name='addcart'),
    url(r'^subcart/$', views.subcart, name='subcart'),
    url(r'^changecartstatus/$', views.changecartstatus, name='changecartstatus'),
    url(r'^changecartselect/$', views.changecartselect, name='changecartselect'),
    url(r'^total/$', views.total, name='total'),
    url(r'^generateorder/$', views.generateorder, name='generateorder'),
    url(r'^orderinfo/(\d+)/$', views.orderinfo, name='orderinfo'),
    url(r'^notifyurl/$', views.notifyurl, name='notifyurl'),
    url(r'^returnurl/$', views.returnurl, name='returnurl'),
    url(r'^pay/$', views.pay, name='pay'),
]