from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'home/disconnect/$',views.disconnect, name='disconnect'),
    url(r'home/connect/$',views.connect, name='connect'),
    url(r'home/findDeviceHtml/$', views.findDeviceHtml, name='findDeviceHtml'),
    url(r'^$', views.index, name='index'), #^$
]
