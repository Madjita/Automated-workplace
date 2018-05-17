from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'connect/$',views.connect, name='connect'),
    url(r'disconnect/$',views.disconnect, name='disconnect')
]
